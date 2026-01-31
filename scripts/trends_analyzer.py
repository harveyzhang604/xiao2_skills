#!/usr/bin/env python3
"""
Google Trends 分析模块 V2
- 支持二级 Related Queries 深挖
"""

import time
from pytrends.request import TrendReq


class TrendsAnalyzer:
    """Google Trends 分析器 V2"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
    
    def analyze(self, keywords):
        """分析关键词趋势"""
        results = {}
        
        for keyword in keywords:
            try:
                # 构建 payload
                self.pytrends.build_payload(
                    kw_list=[keyword],
                    timeframe='today 3-m'
                )
                
                interest_over_time = self.pytrends.interest_over_time()
                related_queries = self.pytrends.related_queries()
                
                # 飙升查询
                rising = []
                if related_queries and keyword in related_queries:
                    rising_data = related_queries[keyword].get('rising', [])
                    if rising_data is not None:
                        rising = [q['query'] for q in rising_data.head(10).to_dict('records')]
                
                # 计算趋势得分
                score = 50  # 默认50分
                growth = 0
                if not interest_over_time.empty:
                    recent = interest_over_time[keyword].tail(7).mean()
                    older = interest_over_time[keyword].tail(30).mean() if len(interest_over_time) > 7 else recent
                    if older > 0:
                        growth = (recent - older) / older * 100
                        score = min(100, max(0, 50 + growth))
                
                results[keyword] = {
                    'keyword': keyword,
                    'trend_score': score,
                    'growth': growth,
                    'rising_queries': rising,
                    'level': '1st',  # 一级
                    'status': 'success'
                }
                
                # 🔥 二级深挖：对每个飙升词再查一次
                deep_rising = []
                for rq in rising[:5]:  # 只深挖前5个飙升词
                    try:
                        self.pytrends.build_payload(
                            kw_list=[rq],
                            timeframe='today 3-m'
                        )
                        sub_related = self.pytrends.related_queries()
                        
                        if rq in sub_related:
                            sub_rising = sub_related[rq].get('rising', [])
                            if sub_rising is not None:
                                for sq in sub_rising.head(5)['query']:
                                    if sq not in rising:  # 避免重复
                                        deep_rising.append({
                                            'query': sq,
                                            'parent': rq,
                                            'level': '2nd'
                                        })
                        
                        time.sleep(2)  # 避免限频
                    except:
                        pass
                
                if deep_rising:
                    results[keyword]['deep_rising'] = deep_rising
                    results[keyword]['level'] = '1st+2nd'
                
                time.sleep(1)
                
            except Exception as e:
                results[keyword] = {
                    'keyword': keyword,
                    'trend_score': 50,
                    'growth': 0,
                    'rising_queries': [],
                    'deep_rising': [],
                    'level': '1st',
                    'status': f'error: {str(e)}'
                }
        
        return results
    
    def get_all_rising(self, trends_data):
        """获取所有飙升词（一级 + 二级）"""
        all_rising = []
        
        for data in trends_data.values():
            # 一级飙升
            all_rising.extend(data.get('rising_queries', []))
            
            # 二级深挖
            for deep in data.get('deep_rising', []):
                all_rising.append(deep['query'])
        
        return list(set(all_rising))
