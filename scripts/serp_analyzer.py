#!/usr/bin/env python3
"""
SERP 竞争分析模块 - 降维打击检测 - V3 简化版
"""


class SERPAnalyzer:
    """SERP 竞争分析器 - V3 简化版"""
    
    def __init__(self):
        self.weak_competitors = [
            "reddit.com", "quora.com", "stackoverflow.com",
            "medium.com", "dev.to", "blogger.com", "wordpress.com",
            "github.com", "youtube.com", "wikipedia.org"
        ]
        
        self.giants = [
            "google.com", "microsoft.com", "adobe.com",
            "canva.com", "figma.com", "notion.so",
            "amazon.com", "apple.com", "facebook.com"
        ]
    
    def analyze(self, keywords):
        """分析 SERP 竞争度 - V3 简化版"""
        results = {}
        
        for keyword in keywords:
            try:
                # V3: 简化的竞争分析
                competition = self._analyze_competition(keyword)
                results[keyword] = {
                    'keyword': keyword,
                    'competition': competition['level'],
                    'competition_score': competition['score'],
                    'top_domains': competition['domains'],
                    'weak_competitors_found': competition['weak_found'],
                    '降维打击': competition['is_weak'],
                    'status': 'success'
                }
            except Exception as e:
                results[keyword] = {
                    'keyword': keyword,
                    'competition': 'UNKNOWN',
                    'competition_score': 60,
                    'top_domains': [],
                    'weak_competitors_found': False,
                    '降维打击': False,
                    'status': f'error: {str(e)}'
                }
        
        return results
    
    def _analyze_competition(self, keyword):
        """分析单个关键词的竞争度 - V3 规则"""
        keyword_lower = keyword.lower()
        
        # 工具词通常是 Medium/Blog/Reddit 排名较高
        tool_words = ['calculator', 'generator', 'converter', 'tool', 'checker']
        has_tool = any(word in keyword_lower for word in tool_words)
        
        # 痛点词可能竞争较小
        pain_words = ['struggling', 'fix', 'error', 'help', 'problem']
        has_pain = any(word in keyword_lower for word in pain_words)
        
        # 免费/在线工具
        free_words = ['free', 'online', 'web']
        is_free = any(word in keyword_lower for word in free_words)
        
        # V3: 降维打击判断
        if has_tool and (is_free or has_pain):
            # 工具词 + 免费/痛点 = 可能是降维打击机会
            return {
                'level': 'WEAK',
                'score': 90,
                'domains': ['medium.com', 'dev.to', 'reddit.com'],
                'weak_found': True,
                'is_weak': True  # V3: 工具词容易降维打击
            }
        elif has_tool:
            return {
                'level': 'LOW',
                'score': 80,
                'domains': ['medium.com', 'blogger.com'],
                'weak_found': True,
                'is_weak': True
            }
        elif is_free:
            return {
                'level': 'MEDIUM',
                'score': 60,
                'domains': ['blogger.com', 'wordpress.com'],
                'weak_found': False,
                'is_weak': False
            }
        else:
            return {
                'level': 'MEDIUM',
                'score': 60,
                'domains': [],
                'weak_found': False,
                'is_weak': False
            }
    
    def is_weak_competitor(self, domain):
        """检测是否是弱竞争者"""
        return any(wc in domain.lower() for wc in self.weak_competitors)
    
    def is_giant(self, domain):
        """检测是否是大厂"""
        return any(g in domain.lower() for g in self.giants)
