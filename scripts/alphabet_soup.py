#!/usr/bin/env python3
"""
Google Autocomplete 挖词模块 (Alphabet Soup)
"""

import time
import random
import requests
from urllib.parse import quote


class GoogleSuggestHarvester:
    """Google 自动补全挖词器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _get_suggestions(self, keyword):
        """获取单个关键词的建议"""
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={quote(keyword)}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data[1] if len(data) > 1 else []
        except Exception as e:
            pass
        
        return []
    
    def _get_related(self, keyword):
        """获取相关查询"""
        url = f"https://www.google.com/search?q={quote(keyword)}&hl=en"
        
        # 简化版：只返回主关键词
        return []
    
    def harvest(self, seed_words, max_per_word=20):
        """批量挖词"""
        all_suggestions = set()
        
        for word in seed_words:
            # 基础建议
            suggestions = self._get_suggestions(word)
            all_suggestions.update(suggestions[:max_per_word])
            
            # 字母汤变体
            for char in 'abcdefghijklmnopqrstuvwxyz':
                variant = f"{char} {word}"
                suggestions = self._get_suggestions(variant)
                all_suggestions.update(suggestions[:max_per_word // 2])
            
            # 随机延迟，避免限频
            time.sleep(random.uniform(0.5, 1.5))
        
        return all_suggestions


# 简化版实现
def simple_harvest(keywords, max_results=100):
    """简单版挖词（不依赖外部API）"""
    results = set()
    
    # 种子词 + 后缀组合
    suffixes = [
        " calculator", " generator", " converter", " tool",
        " online", " free", " for beginners", " template",
        " maker", " creator", " checker", " analyzer"
    ]
    
    for base in keywords:
        for suffix in suffixes:
            results.add((base + suffix).strip())
            if len(results) >= max_results:
                return results
    
    return results
