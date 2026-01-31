#!/usr/bin/env python3
"""
深度搜索分析器 V4 - 需求真伪验证 + 商业价值判断
====================================================

核心功能：
1. 5问法验证需求真伪
2. Reddit 痛点挖掘
3. 竞争域名分析
4. 真实搜索意图判断
"""

import asyncio
import aiohttp
import re
import requests
import logging
from typing import Dict, List
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class DeepSearchAnalyzerV4:
    """深度搜索分析器 V4 - 需求验证版"""
    
    def __init__(self):
        # 痛点信号词
        self.pain_keywords = PAIN_TRIGGERS['critical'] + PAIN_TRIGGERS['medium']
        
        # 需求信号词
        self.demand_signals = TRANSACTIONAL_SIGNALS
    
    def validate_demand_5_questions(self, keyword: str, 
                                     reddit_data: Dict = None,
                                     google_data: Dict = None) -> Dict:
        """
        5问法验证需求真伪
        
        Q1: 是 Info 还是 Transactional 意图?
        Q2: 是否有工具/解决方案?
        Q3: 用户是否在抱怨?
        Q4: 是否有付费意愿?
        Q5: 竞争是否激烈?
        """
        keyword_lower = keyword.lower()
        
        answers = {}
        score = 0
        
        # Q1: 意图类型
        is_transactional = False
        for signal in self.demand_signals['tool']:
            if signal in keyword_lower:
                is_transactional = True
                answers['Q1'] = f"Transactional (工具需求): {signal}"
                score += 20
                break
        
        if not is_transactional:
            for signal in INFO_SIGNALS:
                if signal in keyword_lower:
                    answers['Q1'] = f"Info (信息需求): {signal}"
                    score -= 10
                    break
            else:
                answers['Q1'] = "Mixed (混合)"
        
        # Q2: 解决方案检测
        has_solution = False
        for signal in ['tool', 'app', 'software', 'generator', 'online']:
            if signal in keyword_lower:
                has_solution = True
                answers['Q2'] = f"有明确解决方案信号: {signal}"
                score += 10
                break
        
        if not has_solution:
            answers['Q2'] = "无明确解决方案信号"
        
        # Q3: 痛点检测
        pain_count = 0
        found_pains = []
        for pain in self.pain_keywords:
            if pain in keyword_lower:
                found_pains.append(pain)
                pain_count += 1
        
        if pain_count > 0:
            answers['Q3'] = f"痛点发现: {', '.join(found_pains)}"
            score += pain_count * 15
        else:
            answers['Q3'] = "未发现明显痛点"
        
        # Q4: 付费意愿 (通过 Reddit 分析)
        if reddit_data:
            comments = reddit_data.get('total_mentions', 0)
            if comments > 5:
                answers['Q4'] = f"Reddit讨论活跃 ({comments}条), 可能存在付费需求"
                score += 15
            elif comments > 0:
                answers['Q4'] = f"少量Reddit讨论 ({comments}条)"
                score += 5
            else:
                answers['Q4'] = "Reddit无活跃讨论"
        else:
            answers['Q4'] = "无Reddit数据"
        
        # Q5: 竞争分析
        if google_data:
            competitors = google_data.get('competitors', [])
            has_giant = any(c in GIANTS for c in competitors)
            has_weak = any(c in WEAK_COMPETITORS for c in competitors)
            
            if has_giant:
                answers['Q5'] = f"巨头存在: {competitors[:2]}"
                score -= 20
            elif has_weak:
                answers['Q5'] = f"弱竞争 (机会): {competitors[:2]}"
                score += 25
            else:
                answers['Q5'] = f"中等竞争: {competitors[:2] if competitors else '未知'}"
        else:
            answers['Q5'] = "无竞争数据"
        
        # 最终验证结果
        is_valid = score >= 60 and (is_transactional or pain_count > 0)
        
        return {
            'is_valid': is_valid,
            'score': min(100, max(0, score)),
            'intent_type': 'transactional' if is_transactional else 'info',
            'questions': answers,
            'pain_count': pain_count,
            'found_pains': found_pains
        }
    
    def search_reddit_real(self, keyword: str) -> Dict:
        """真实搜索 Reddit 痛点讨论"""
        results = {
            'total_mentions': 0,
            'pain_posts': [],
            'sentiment': 'neutral',
            'solution_seeking': 0
        }
        
        try:
            url = f"https://www.reddit.com/search.json?q={quote_plus(keyword)}&limit=20&sort=relevance"
            headers = {"User-Agent": "Mozilla/5.0"}
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            posts = data.get("data", {}).get("children", [])
            results['total_mentions'] = len(posts)
            
            pain_posts = []
            solution_seeking = 0
            
            for post in posts:
                post_data = post.get("data", {})
                title = post_data.get("title", "").lower()
                selftext = post_data.get("selftext", "").lower()
                combined = title + " " + selftext
                
                # 痛点检测
                for pain in self.pain_keywords:
                    if pain in combined:
                        pain_posts.append({
                            'title': post_data.get("title", ""),
                            'score': post_data.get("score", 0),
                            'comments': post_data.get("num_comments", 0)
                        })
                        break
                
                # 解决方案寻求
                for signal in ['looking for', 'need a tool', 'is there a', 'wish there was']:
                    if signal in combined:
                        solution_seeking += 1
                        break
            
            results['pain_posts'] = pain_posts[:5]
            results['solution_seeking'] = solution_seeking
            
            # 情感分析
            if len(pain_posts) > 3:
                results['sentiment'] = 'negative'  # 大量痛点
            elif solution_seeking > 2:
                results['sentiment'] = 'seeking'  # 寻求解决方案
            
        except Exception as e:
            logger.debug(f"Reddit search error for '{keyword}': {e}")
        
        return results
    
    def analyze_google_serp(self, keyword: str) -> Dict:
        """分析 Google SERP 竞争环境"""
        results = {
            'competitors': [],
            'has_giant': False,
            'has_weak': False,
            'commercial_intent': 0
        }
        
        try:
            url = f"https://www.google.com/search?q={quote_plus(keyword)}&num=10"
            headers = {"User-Agent": "Mozilla/5.0"}
            
            response = requests.get(url, headers=headers, timeout=15)
            html = response.text
            
            # 提取域名
            domains = re.findall(r'https?://([^/]+)', html)
            unique_domains = []
            for d in domains:
                d = d.replace('www.', '')
                if d not in unique_domains and len(d) < 50:
                    unique_domains.append(d)
            
            results['competitors'] = unique_domains[:5]
            
            # 检测巨头
            for domain in unique_domains:
                if any(g in domain for g in GIANTS):
                    results['has_giant'] = True
                    break
            
            # 检测弱竞争者
            for domain in unique_domains:
                if any(w in domain for w in WEAK_COMPETITORS):
                    results['has_weak'] = True
                    break
            
            # 商业意图
            tool_count = sum(1 for d in unique_domains for t in ['tool', 'app', 'software'] if t in d)
            results['commercial_intent'] = min(100, tool_count * 20)
            
        except Exception as e:
            logger.debug(f"Google SERP error for '{keyword}': {e}")
        
        return results
    
    def analyze_keyword(self, keyword: str) -> Dict:
        """综合深度分析"""
        logger.info(f"   🔍 深度分析: {keyword}")
        
        # 获取数据
        reddit = self.search_reddit_real(keyword)
        google = self.analyze_google_serp(keyword)
        
        # 5问法验证
        validation = self.validate_demand_5_questions(keyword, reddit, google)
        
        # 商业价值判断
        monetization_score = self._calc_monetization(keyword)
        
        # 痛点分数
        pain_score = self._calc_pain(keyword, reddit)
        
        return {
            'keyword': keyword,
            'validation': validation,
            'reddit': reddit,
            'google': google,
            'monetization_score': monetization_score,
            'pain_score': pain_score,
            'demand_strength': self._calc_demand_strength(validation, reddit, google),
            'is_valid_transactional': validation['intent_type'] == 'transactional' and validation['is_valid'],
            'is_pain_point': validation['pain_count'] > 0
        }
    
    def _calc_monetization(self, keyword: str) -> Dict:
        """计算商业价值"""
        score = 50
        signals = []
        keyword_lower = keyword.lower()
        
        # B2B
        for signal in TRANSACTIONAL_SIGNALS['b2b']:
            if signal in keyword_lower:
                signals.append(f"B2B: {signal}")
                score += 20
                break
        
        # Transactional
        for signal in TRANSACTIONAL_SIGNALS['tool']:
            if signal in keyword_lower:
                signals.append(f"工具: {signal}")
                score += 15
                break
        
        # 免费
        if 'free' in keyword_lower:
            signals.append("免费")
            score += 5
        
        return {'score': min(100, score), 'signals': signals}
    
    def _calc_pain(self, keyword: str, reddit: Dict) -> Dict:
        """计算痛点分数"""
        score = 50
        keyword_lower = keyword.lower()
        keywords = []
        level = 'low'
        
        for pain in self.pain_keywords:
            if pain in keyword_lower:
                keywords.append(pain)
                score += 15
                level = 'critical' if 'struggling' in pain or 'fix' in pain else 'medium'
        
        if reddit.get('solution_seeking', 0) > 0:
            score += 10
            level = 'critical'
        
        return {'score': min(100, score), 'level': level, 'keywords': keywords[:3]}
    
    def _calc_demand_strength(self, validation: Dict, reddit: Dict, google: Dict) -> str:
        """计算需求强度"""
        score = validation['score']
        
        if reddit.get('total_mentions', 0) > 5:
            score += 20
        elif reddit.get('total_mentions', 0) > 0:
            score += 10
        
        if google.get('has_weak') and not google.get('has_giant'):
            score += 25
        
        if score >= 80:
            return 'HIGH'
        elif score >= 50:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def analyze_batch(self, keywords: List[str]) -> Dict[str, Dict]:
        """批量深度分析"""
        results = {}
        
        logger.info(f"🎯 开始深度分析 {len(keywords)} 个关键词...")
        
        for i, keyword in enumerate(keywords, 1):
            try:
                analysis = self.analyze_keyword(keyword)
                results[keyword] = analysis
                
                status = "✅" if analysis['is_valid_transactional'] else "⚠️"
                demand = analysis['demand_strength']
                logger.info(f"   {i}/{len(keywords)} {keyword}: {demand} {status}")
                
            except Exception as e:
                logger.error(f"分析失败 '{keyword}': {e}")
                results[keyword] = {"keyword": keyword, "error": str(e)}
        
        logger.info(f"✅ 完成 {len(results)} 个关键词深度分析")
        return results


# 便捷函数
def deep_search(keywords: List[str]) -> Dict[str, Dict]:
    """执行深度搜索"""
    analyzer = DeepSearchAnalyzerV4()
    return analyzer.analyze_batch(keywords)
