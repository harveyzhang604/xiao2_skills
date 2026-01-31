#!/usr/bin/env python3
"""
关键词评分模块 - V3 用户意图深挖版
"""

from config import THRESHOLDS, PAIN_TRIGGERS, INTENT_SIGNALS, WEIGHTS


# 用户意图类型定义
USER_INTENTS = {
    'calculate': {
        'keywords': ['calculator', 'calculate', 'calculation', 'compute', 'math'],
        'goal': '用户想计算某个数值',
        'clarity': '高'
    },
    'convert': {
        'keywords': ['converter', 'convert', 'conversion', 'transform', 'translate'],
        'goal': '用户想转换单位/格式/语言',
        'clarity': '高'
    },
    'generate': {
        'keywords': ['generator', 'generate', 'creator', 'maker', 'builder'],
        'goal': '用户想自动生成内容',
        'clarity': '高'
    },
    'check': {
        'keywords': ['checker', 'check', 'validate', 'verify', 'test'],
        'goal': '用户想验证/检查某事',
        'clarity': '高'
    },
    'compare': {
        'keywords': ['compare', 'comparison', 'vs', 'versus', 'alternative'],
        'goal': '用户想对比选项',
        'clarity': '高'
    },
    'find': {
        'keywords': ['finder', 'search', 'lookup', 'lookup', 'locate'],
        'goal': '用户想查找某物',
        'clarity': '中'
    },
    'plan': {
        'keywords': ['planner', 'plan', 'schedule', 'organizer'],
        'goal': '用户想规划/安排',
        'clarity': '中'
    },
    'track': {
        'keywords': ['tracker', 'track', 'monitor', 'measure'],
        'goal': '用户想追踪/监测',
        'clarity': '中'
    },
}


class KeywordScorer:
    """关键词评分器 - V3 增强版 + 深度搜索"""
    
    def __init__(self, trends_data, gpts_data, serp_data, deep_data=None):
        self.trends = trends_data or {}
        self.gpts = gpts_data or {}
        self.serp = serp_data or {}
        self.deep = deep_data or {}
        self.weights = WEIGHTS
    
    def score(self, keywords):
        """对关键词列表评分"""
        results = []
        
        for keyword in keywords:
            score = self._score_keyword(keyword)
            results.append(score)
        
        return results
    
    def _score_keyword(self, keyword):
        """对单个关键词评分 - V3 增强版 + 深度搜索"""
        trends = self.trends.get(keyword, {})
        gpts = self.gpts.get(keyword, {})
        serp = self.serp.get(keyword, {})
        deep = self.deep.get(keyword, {})
        
        # 1. Trend Score (GPTs 热度)
        trend_score = trends.get('trend_score', 50)
        
        # 2. Intent Score
        intent_score, signals = self._calc_intent_score(keyword)
        
        # 3. Competition Score
        competition_score = serp.get('competition_score', 60)
        
        # 4. Buildability Score
        buildability_score = self._calc_buildability(keyword)
        
        # 5. 深度搜索加成（基于真实社区需求）
        deep_bonus = self._calc_deep_bonus(deep)
        
        # 6. 综合评分
        final_score = (
            trend_score * self.weights['trend'] +
            intent_score * self.weights['intent'] +
            competition_score * self.weights['competition'] +
            buildability_score * self.weights['buildability'] +
            deep_bonus
        )
        
        # 降维打击加成 (+20 分)
        if serp.get('降维打击'):
            final_score = min(100, final_score + 20)
        
        # 用户意图分析
        user_intent_info = self._analyze_user_intent(keyword)
        
        return {
            'keyword': keyword,
            'final_score': round(final_score, 1),
            'trend_score': trend_score,
            'intent_score': intent_score,
            'competition_score': competition_score,
            'buildability_score': buildability_score,
            '降维打击': serp.get('降维打击', False),
            'competition': serp.get('competition', 'MEDIUM'),
            'ratio': gpts.get('ratio', 0),
            'avg_ratio': gpts.get('ratio', 0),  # 显示 GPTs 热度比
            'signals': ', '.join(signals) if signals else '普通',
            # 用户意图深挖字段
            'user_intent': user_intent_info['intent_types'],
            'user_goal': user_intent_info['goal'],
            'intent_clarity': user_intent_info['clarity'],
            # 深度搜索数据
            'demand_strength': deep.get('demand_strength', 'UNKNOWN'),
            'community_buzz': deep.get('community_buzz', 0),
            'is_pain_point': deep.get('is_pain_point', False),
            'is_tool_demand': deep.get('is_tool_demand', False),
            'is_comparison': deep.get('is_comparison', False),
        }
    
    def _calc_deep_bonus(self, deep):
        """计算深度搜索加成"""
        bonus = 0
        
        if not deep:
            return bonus
        
        # 高需求强度 (+15)
        if deep.get('demand_strength') == 'HIGH':
            bonus += 15
        elif deep.get('demand_strength') == 'MEDIUM':
            bonus += 8
        
        # 社区讨论热度 (+5)
        bonus += min(10, deep.get('community_buzz', 0) * 2)
        
        # 痛点需求 (+10)
        if deep.get('is_pain_point'):
            bonus += 10
        
        # 工具需求 (+5)
        if deep.get('is_tool_demand'):
            bonus += 5
        
        return bonus
    
    def _calc_intent_score(self, keyword):
        """计算需求意图强度 - 返回 (score, signals)"""
        score = 50  # 基础分
        keyword_lower = keyword.lower()
        signals = []
        
        # 强痛点词 (+40)
        for trigger in PAIN_TRIGGERS.get('strong', []):
            if trigger in keyword_lower:
                score += 40
                signals.append(f'痛点:{trigger}')
                break
        
        # 工具词 (+30)
        for tool in INTENT_SIGNALS.get('tool', []):
            if tool in keyword_lower:
                score += 30
                signals.append(f'工具:{tool}')
                break
        
        # 对比词 (+25)
        for compare in INTENT_SIGNALS.get('对比', []):
            if compare in keyword_lower:
                score += 25
                signals.append(f'对比:{compare}')
                break
        
        # B2B 词 (+25)
        for b2b in INTENT_SIGNALS.get('B2B', []):
            if b2b in keyword_lower:
                score += 25
                signals.append(f'B2B:{b2b}')
                break
        
        # 速度词 (+20)
        for speed in INTENT_SIGNALS.get('速度', []):
            if speed in keyword_lower:
                score += 20
                signals.append(f'速度:{speed}')
                break
        
        # 长尾词 (+15)
        word_count = len(keyword.split())
        if word_count >= 2:
            score += 15
            signals.append(f'长尾:{word_count}词')
        
        return min(100, score), signals
    
    def _calc_buildability(self, keyword):
        """计算可实现性"""
        keyword_lower = keyword.lower()
        
        # 工具词最容易实现
        for tool in ['calculator', 'generator', 'converter']:
            if tool in keyword_lower:
                return 100
        
        # 在线/免费工具
        for word in ['online', 'free', 'web']:
            if word in keyword_lower:
                return 85
        
        return 70
    
    def _analyze_user_intent(self, keyword):
        """用户意图深挖 - V3 核心功能
        
        分析用户真正想做什么：
        - calculate: 用户想计算某个数值
        - convert: 用户想转换单位/格式
        - generate: 用户想自动生成内容
        - check: 用户想验证/检查某事
        ...
        """
        keyword_lower = keyword.lower()
        matched_intents = []
        
        # 检测意图类型
        for intent_type, intent_info in USER_INTENTS.items():
            for kw in intent_info['keywords']:
                if kw in keyword_lower:
                    matched_intents.append(intent_type)
                    break
        
        # 去重
        matched_intents = list(set(matched_intents))
        
        # 生成 user_goal
        if len(matched_intents) == 0:
            return {
                'intent_types': 'general',
                'goal': '普通搜索需求',
                'clarity': '低'
            }
        elif len(matched_intents) == 1:
            intent = matched_intents[0]
            return {
                'intent_types': intent,
                'goal': USER_INTENTS[intent]['goal'],
                'clarity': USER_INTENTS[intent]['clarity']
            }
        else:
            # 复合需求
            intent_str = ', '.join(matched_intents)
            return {
                'intent_types': intent_str,
                'goal': f'复合需求：{" + ".join(matched_intents)}',
                'clarity': '高'  # 多个意图匹配，清晰度高
            }
    
    def get_final_results(self, scored_keywords):
        """生成最终决策结果 - V3 版"""
        results = []
        
        for kw in scored_keywords:
            score = kw.get('final_score', 0)
            
            # 决策
            if score >= THRESHOLDS['BUILD_NOW']:
                decision = '🔴 BUILD NOW'
            elif score >= THRESHOLDS['WATCH']:
                decision = '🟡 WATCH'
            else:
                decision = '❌ DROP'
            
            kw['decision'] = decision
            results.append(kw)
        
        # 按评分排序
        results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        return results
