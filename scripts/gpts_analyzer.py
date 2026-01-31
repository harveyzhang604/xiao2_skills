#!/usr/bin/env python3
"""
GPTs 对比分析模块 - V3 增强版
"""

import time
import json
from urllib.request import urlopen
from urllib.error import URLError


class GPTsAnalyzer:
    """GPTs 分析器 - V3 增强版"""
    
    def __init__(self):
        self.gpts_api = "https://chatGPT.ai/gpts/"
    
    def _search_gpts(self, keyword):
        """搜索相关 GPTs - V3 增强"""
        # 基于关键词模式估算 GPTs 数量
        gpt_patterns = {
            'calculator': 50,
            'generator': 80,
            'converter': 30,
            'tool': 100,
            'analyzer': 40,
            'writer': 60,
            'editor': 35,
            'tracker': 25,
            'planner': 20,
            'checker': 30,
            'creator': 45,
            'maker': 35,
            # V3 新增：更多工具类型
            'formatter': 15,
            'validator': 20,
            'optimizer': 25,
            'extractor': 20,
            'transformer': 25,
        }
        
        count = 0
        keyword_lower = keyword.lower()
        for pattern, c in gpt_patterns.items():
            if pattern in keyword_lower:
                count += c
        
        # 如果没有匹配模式，给一个基准值
        if count == 0:
            count = 20
        
        # V3: 热度加权 - 痛点词可能有更高热度
        pain_words = ['struggling', 'fix', 'error', 'problem', 'help']
        for word in pain_words:
            if word in keyword_lower:
                count = int(count * 1.2)  # 痛点词热度加成
                break
        
        return count
    
    def analyze(self, keywords):
        """分析关键词的 GPTs 对比 - V3 增强版"""
        results = {}
        
        for keyword in keywords:
            try:
                gpts_count = self._search_gpts(keyword)
                
                # 估算搜索量（V3 改进）
                search_volume = self._estimate_volume(keyword)
                
                # 计算比值（V3: 显示 avg_ratio）
                ratio = gpts_count / max(search_volume, 1)
                
                # 计算热度得分
                score = self._calc_score(ratio, search_volume)
                
                results[keyword] = {
                    'keyword': keyword,
                    'gpts_count': gpts_count,
                    'estimated_volume': search_volume,
                    'ratio': round(ratio, 4),  # V3: 显示原始比值
                    'avg_ratio': round(ratio, 4),  # V3: 别名，方便使用
                    'trend_score': score,
                    'status': 'success'
                }
                
                time.sleep(0.2)
                
            except Exception as e:
                results[keyword] = {
                    'keyword': keyword,
                    'gpts_count': 0,
                    'estimated_volume': 100,
                    'ratio': 0,
                    'avg_ratio': 0,
                    'trend_score': 50,
                    'status': f'error: {str(e)}'
                }
        
        return results
    
    def _estimate_volume(self, keyword):
        """估算搜索量 - V3 增强版"""
        # 简化的估算：基于关键词特征
        base = 100
        
        # V3: 工具类关键词搜索量更高
        tool_words = [
            'calculator', 'generator', 'converter', 'tool', 'checker',
            'planner', 'tracker', 'formatter', 'validator', 'optimizer'
        ]
        for word in tool_words:
            if word in keyword.lower():
                base += 50
                break
        
        # V3: 痛点词可能有更高搜索量
        pain_words = ['struggling', 'fix', 'error', 'help', 'problem']
        for word in pain_words:
            if word in keyword.lower():
                base += 30
                break
        
        # V3: 英文关键词搜索量
        if all(ord(c) < 128 for c in keyword):
            base *= 1.5
        
        # V3: 长尾词搜索量较低，但更精准
        word_count = len(keyword.split())
        if word_count >= 3:
            base = int(base * 0.8)  # 长尾词搜索量稍低
        
        return int(base)
    
    def _calc_score(self, ratio, volume):
        """计算热度得分 - V3 标准"""
        score = 50  # 基础分
        
        # V3: 比值加分（说明有真实需求）
        if ratio >= 0.2:
            score = 100
        elif ratio >= 0.1:
            score = 85
        elif ratio >= 0.05:
            score = 75
        elif ratio >= 0.03:
            score = 70
        else:
            score = 50
        
        # V3: 搜索量加分
        if volume > 150:
            score += 10
        elif volume > 100:
            score += 5
        
        return min(100, score)
