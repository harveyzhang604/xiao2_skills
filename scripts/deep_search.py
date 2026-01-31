#!/usr/bin/env python3
"""
深度搜索分析模块 V3 - 真实需求挖掘
使用 Reddit API 直接搜索用户痛点和需求
"""

import asyncio
import aiohttp
import re
import requests
import logging
from typing import Dict, List
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class DeepSearchAnalyzer:
    """深度搜索分析器 V3 - Reddit API 真实搜索"""
    
    def __init__(self):
        # 痛点信号词
        self.pain_keywords = [
            "struggling with", "how to fix", "error", "problem",
            "cannot", "doesn't work", "failed", "help me",
            "annoying", "tedious", "time consuming", "frustrated",
            "wish there was", "looking for", "need a tool", 
            "how do i", "is there a", "best way to", "tired of",
            "waste of time", "manually", "repetitive", "boring",
            "broken", "not working", "difficult", "hard to"
        ]
        
        # 需求信号词
        self.demand_signals = {
            "calculator": "计算需求",
            "generator": "生成需求",
            "converter": "转换需求",
            "formatter": "格式化需求",
            "parser": "解析需求",
            "checker": "验证需求",
            "finder": "查找需求",
            "maker": "制作需求",
            "creator": "创建需求",
            "tool": "工具需求",
            "free": "免费需求",
            "online": "在线需求",
            "easy": "易用需求",
            "automatic": "自动化需求"
        }
    
    def search_reddit_api(self, keyword: str) -> Dict:
        """使用 Reddit API 搜索真实痛点讨论"""
        results = {
            "reddit_posts": [],
            "pain_points": [],
            "real_complaints": [],
            "total_mentions": 0,
            "validation_score": 0
        }
        
        try:
            # Reddit 公开搜索 API
            url = "https://www.reddit.com/search.json"
            params = {
                "q": keyword,
                "limit": 20,
                "sort": "relevance",
                "restrict_sr": False,
                "t": "year"
            }
            headers = {"User-Agent": "Mozilla/5.0"}
            
            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            posts = data.get("data", {}).get("children", [])
            results["total_mentions"] = len(posts)
            
            pain_count = 0
            for post in posts:
                post_data = post.get("data", {})
                title = post_data.get("title", "").lower()
                selftext = post_data.get("selftext", "").lower()
                combined = title + " " + selftext
                
                # 检测痛点
                for pain in self.pain_keywords:
                    if pain in combined:
                        pain_count += 1
                        results["pain_points"].append(pain)
                        
                        # 提取真实抱怨
                        if pain in title and len(title) < 200:
                            results["real_complaints"].append({
                                "text": post_data.get("title", ""),
                                "score": post_data.get("score", 0),
                                "comments": post_data.get("num_comments", 0),
                                "url": f"https://reddit.com{post_data.get('permalink', '')}"
                            })
                        break
            
            # 计算验证分数
            total_comments = sum(p["comments"] for p in results["real_complaints"])
            total_score = sum(p["score"] for p in results["real_complaints"])
            
            results["validation_score"] = min(100,
                pain_count * 10 + 
                total_comments / 10 + 
                total_score / 20
            )
            
            logger.info(f"   ✅ Reddit: {results['total_mentions']}条讨论, {pain_count}个痛点")
            
        except Exception as e:
            logger.debug(f"Reddit API error for '{keyword}': {e}")
        
        return results
    
    def analyze_google_serp(self, keyword: str) -> Dict:
        """分析 Google SERP 需求"""
        results = {
            "tool_results": 0,
            "forum_results": 0,
            "commercial_intent": 0,
            "related_queries": [],
            "is_question": False
        }
        
        try:
            url = f"https://www.google.com/search?q={quote_plus(keyword)}&num=10"
            headers = {"User-Agent": "Mozilla/5.0"}
            
            response = requests.get(url, headers=headers, timeout=15)
            html = response.text
            
            # 检测工具类结果
            tool_domains = ["calculator", "converter", "generator", "tool", "online"]
            for domain in tool_domains:
                results["tool_results"] += html.lower().count(domain)
            
            # 检测论坛结果
            forum_domains = ["reddit.com", "stackoverflow", "quora", "forum"]
            for domain in forum_domains:
                results["forum_results"] += html.lower().count(domain)
            
            # 提取相关查询
            related = re.findall(r'">([^<]+)</a>', html)
            results["related_queries"] = related[:5]
            
            # 检测是否问答型
            question_words = ["how", "what", "why", "where", "when"]
            if any(qw in keyword.lower() for qw in question_words):
                results["is_question"] = True
            
            # 计算商业意图
            results["commercial_intent"] = min(100,
                results["tool_results"] * 5 + 
                results["forum_results"] * 3
            )
            
        except Exception as e:
            logger.debug(f"Google SERP error for '{keyword}': {e}")
        
        return results
    
    def detect_user_intent(self, keyword: str) -> Dict:
        """深挖用户意图（用户真正想做什么）"""
        keyword_lower = keyword.lower()
        
        # 意图模式匹配
        intent_patterns = {
            "calculate": ["calculator", "calculate", "compute", "formula"],
            "convert": ["converter", "convert", "to", "from", "into"],
            "generate": ["generator", "generate", "create", "maker", "builder"],
            "check": ["checker", "check", "verify", "validate", "test"],
            "compare": ["vs", "versus", "compare", "difference", "alternative"],
            "download": ["download", "downloader", "get", "save"],
            "edit": ["editor", "edit", "modify", "change"],
            "analyze": ["analyzer", "analyze", "analytics", "report"],
            "track": ["tracker", "track", "monitor", "follow"],
            "search": ["finder", "search", "find", "lookup"]
        }
        
        detected = []
        for intent, patterns in intent_patterns.items():
            for p in patterns:
                if p in keyword_lower:
                    detected.append(intent)
                    break
        
        # 用户目标映射
        intent_goals = {
            "calculate": "用户想计算某个数值",
            "convert": "用户想转换单位/格式/语言",
            "generate": "用户想自动生成内容",
            "check": "用户想验证/检查某事",
            "compare": "用户想对比选项",
            "download": "用户想下载资源",
            "edit": "用户想编辑/修改内容",
            "analyze": "用户想分析数据",
            "track": "用户想追踪/监控",
            "search": "用户想查找信息"
        }
        
        if not detected:
            return {
                "intent": "general",
                "goal": "未知意图（可能是信息查询）",
                "clarity": "低"
            }
        elif len(detected) == 1:
            return {
                "intent": detected[0],
                "goal": intent_goals.get(detected[0], "执行具体操作"),
                "clarity": "高"
            }
        else:
            return {
                "intent": "+".join(detected),
                "goal": f"复合需求：{' + '.join(detected)}",
                "clarity": "中"
            }
    
    def analyze_keyword(self, keyword: str) -> Dict:
        """综合深度分析单个关键词"""
        logger.info(f"   🔍 深度分析: {keyword}")
        
        # Reddit API 搜索
        reddit = self.search_reddit_api(keyword)
        
        # Google SERP 分析
        google = self.analyze_google_serp(keyword)
        
        # 用户意图深挖
        intent = self.detect_user_intent(keyword)
        
        # 综合分析
        analysis = {
            "keyword": keyword,
            "reddit": reddit,
            "google": google,
            "intent": intent,
            "demand_strength": self._calc_demand_strength(reddit, google),
            "pain_point_score": reddit.get("validation_score", 0),
            "opportunity_score": self._calc_opportunity(reddit, google),
            "is_tool_demand": any(t in keyword.lower() for t in ["tool", "generator", "calculator", "converter"]),
            "is_pain_point": len(reddit.get("pain_points", [])) > 0,
            "is_comparison": "vs" in keyword.lower() or "alternative" in keyword.lower(),
            "is_question": google.get("is_question", False),
            "user_goal": intent.get("goal", ""),
            "user_intent": intent.get("intent", "")
        }
        
        return analysis
    
    def _calc_demand_strength(self, reddit: Dict, google: Dict) -> str:
        """计算需求强度"""
        score = 0
        
        if reddit.get("total_mentions", 0) > 5:
            score += 3
        elif reddit.get("total_mentions", 0) > 0:
            score += 1
        
        if reddit.get("validation_score", 0) >= 50:
            score += 3
        elif reddit.get("validation_score", 0) >= 20:
            score += 1
        
        if google.get("forum_results", 0) > 3:
            score += 2
        
        if google.get("is_question"):
            score += 1
        
        if score >= 6:
            return "HIGH"
        elif score >= 3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calc_opportunity(self, reddit: Dict, google: Dict) -> int:
        """计算机会分数"""
        score = 50
        
        if google.get("tool_results", 0) > 0:
            score += 10
        
        if google.get("forum_results", 0) > 2:
            score += 10
        
        if reddit.get("total_mentions", 0) > 3:
            score += 10
        
        if reddit.get("validation_score", 0) >= 50:
            score += 15
        
        return min(100, score)
    
    def analyze_batch(self, keywords: List[str]) -> Dict[str, Dict]:
        """批量深度分析"""
        results = {}
        
        logger.info(f"🎯 开始深度分析 {len(keywords)} 个关键词...")
        
        for i, keyword in enumerate(keywords, 1):
            try:
                analysis = self.analyze_keyword(keyword)
                results[keyword] = analysis
                
                demand = analysis["demand_strength"]
                pain = "⚠️" if analysis["is_pain_point"] else ""
                mentions = analysis["reddit"].get("total_mentions", 0)
                logger.info(f"   {i}/{len(keywords)} {keyword}: {demand} {pain} (讨论:{mentions})")
                
            except Exception as e:
                logger.error(f"分析失败 '{keyword}': {e}")
                results[keyword] = {"keyword": keyword, "error": str(e)}
        
        logger.info(f"✅ 完成 {len(results)} 个关键词深度分析")
        return results


# 便捷函数
def deep_search(keywords: List[str]) -> Dict[str, Dict]:
    """执行深度搜索"""
    analyzer = DeepSearchAnalyzer()
    return analyzer.analyze_batch(keywords)


if __name__ == "__main__":
    test_keywords = [
        "free image converter tool",
        "python json formatter online",
        "website seo checker free",
        "logo maker without watermark",
        "password generator strong"
    ]
    
    results = deep_search(test_keywords)
    
    for kw, data in results.items():
        print(f"\n{'='*60}")
        print(f"关键词: {kw}")
        print(f"需求强度: {data.get('demand_strength', 'N/A')}")
        print(f"痛点分数: {data.get('pain_point_score', 0)}")
        print(f"机会分数: {data.get('opportunity_score', 0)}")
        print(f"用户意图: {data.get('user_intent', '')}")
        print(f"用户目标: {data.get('user_goal', '')}")
