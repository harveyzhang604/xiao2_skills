#!/usr/bin/env python3
"""
Google Trends 分析模块
"""

import time
from pytrends.request import TrendReq


class TrendsAnalyzer:
    """Google Trends 分析器"""
    
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
                    timeframe='today 3-m'  # 最近3个月
                )
                
                # 获取兴趣随时间变化
                interest_over_time = self.pytrends.interest_over_time()
                
                # 获取相关查询
                related_queries = self.pytrends.related_queries()
                
                # 飙升查询
                rising = []
                if related_queries and keyword in related_queries:
                    rising_data = related_queries[keyword].get('rising', [])
                    if rising_data is not None:
                        rising = [q['query'] for q in rising_data.head(5).to_dict('records')]
                
                # 计算趋势得分
                score = 0
                if not interest_over_time.empty:
                    recent = interest_over_time[keyword].tail(7).mean()
                    older = interest_over_time[keyword].tail(30).mean() if len(interest_over_time) > 7 else recent
                    if older > 0:
                        growth = (recent - older) / older * 100
                        score = min(100, max(0, 50 + growth))
                
                results[keyword] = {
                    'keyword': keyword,
                    'trend_score': score,
                    'growth': growth if 'growth' in dir() else 0,
                    'rising_queries': rising,
                    'status': 'success'
                }
                
                time.sleep(1)  # 避免限频
                
            except Exception as e:
                results[keyword] = {
                    'keyword': keyword,
                    'trend_score': 50,
                    'growth': 0,
                    'rising_queries': [],
                    'status': f'error: {str(e)}'
                }
        
        return results
    
    def get_rising_keywords(self, trends_data, min_growth=10):
        """获取飙升词"""
        rising = []
        for data in trends_data.values():
            if data.get('growth', 0) >= min_growth:
                rising.append(data['keyword'])
            # 添加飙升相关词
            rising.extend(data.get('rising_queries', [])[:2])
        
        return list(set(rising))
