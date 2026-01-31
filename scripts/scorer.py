#!/usr/bin/env python3
"""
关键词评分器 V4 - 需求真伪识别 + 商业价值判断
================================================

核心功能：
1. 5问法验证需求真伪
2. 商业价值评分 (止痛药 vs 维生素)
3. 痛点深度评估
4. 竞争环境分析
5. pSEO 潜力评估
"""

from config import *
from typing import Dict, List, Tuple


class KeywordScorer:
    """关键词评分器 V4 - 需求验证版"""
    
    def __init__(self, trends_data: Dict = None, gpts_data: Dict = None, 
                 serp_data: Dict = None, deep_data: Dict = None):
        self.trends = trends_data or {}
        self.gpts = gpts_data or {}
        self.serp = serp_data or {}
        self.deep = deep_data or {}
        self.weights = WEIGHTS
    
    def score(self, keywords: List[str]) -> List[Dict]:
        """评分所有关键词"""
        results = []
        for keyword in keywords:
            score = self._score_keyword(keyword)
            results.append(score)
        return results
    
    def _score_keyword(self, keyword: str) -> Dict:
        """对单个关键词评分 - V4 完整版"""
        keyword_lower = keyword.lower()
        
        # 1. 需求真伪验证 (5问法)
        demand_validation = self._validate_demand(keyword_lower)
        
        # 2. 商业价值判断
        monetization = self._assess_monetization(keyword_lower)
        
        # 3. 痛点深度评分
        pain_score = self._calc_pain_score(keyword_lower)
        
        # 4. 竞争环境分析
        competition = self._analyze_competition(keyword_lower)
        
        # 5. 趋势评分
        trend = self._calc_trend(keyword_lower)
        
        # 6. 综合评分
        final_score = (
            demand_validation['score'] * self.weights['demand_validation'] +
            monetization['score'] * self.weights['monetization'] +
            pain_score['score'] * self.weights['pain_score'] +
            competition['score'] * self.weights['competition'] +
            trend['score'] * self.weights['trend']
        )
        
        # 7. 决策判断
        decision = self._make_decision(final_score, pain_score['score'], competition)
        
        # 8. pSEO 潜力评估
        pseo = self._assess_pseo_potential(keyword_lower)
        
        # 9. 变现建议
       变现建议 = self._suggest_monetization(monetization, pain_score)
        
        return {
            'keyword': keyword,
            'final_score': round(final_score, 1),
            
            # 需求验证
            'intent_type': demand_validation['intent_type'],  # transactional vs info
            'demand_valid': demand_validation['is_valid'],
            'demand_signals': demand_validation['signals'],
            
            # 商业价值
            'is_b2b': monetization['is_b2b'],
            'is_transactional': monetization['is_transactional'],
            'monetization_score': monetization['score'],
            
            # 痛点
            'pain_score': pain_score['score'],
            'pain_level': pain_score['level'],  # critical/medium/low
            'pain_keywords': pain_score['keywords'],
            
            # 竞争
            'competition_score': competition['score'],
            'competition_level': competition['level'],  # weak/low/medium/high
            'competitors': competition['competitors'],
            '降维打击': competition['is_weak'],
            
            # 趋势
            'trend_score': trend['score'],
            'is_rising': trend['is_rising'],
            
            # GPTS对比
            'gpts_ratio': self.gpts.get(keyword, {}).get('ratio', 0),
            
            # pSEO
            'pseo_score': pseo['score'],
            'pseo_potential': pseo['potential'],
            'pseo_patterns': pseo['patterns'],
            
            # 决策
            'decision': decision,
            
            # 变现建议
            '变现建议': 变现建议
        }
    
    def _validate_demand(self, keyword: str) -> Dict:
        """
        5问法验证需求真伪
        Q1: 是 Info 还是 Transactional 意图?
        Q2: 是否有工具/解决方案?
        Q3: 用户是否在抱怨?
        Q4: 是否有付费意愿?
        Q5: 竞争是否激烈?
        """
        signals = []
        is_transactional = False
        is_valid = False
        
        # Q1: Transactional 意图检测
        for signal in TRANSACTIONAL_SIGNALS['tool']:
            if signal in keyword:
                signals.append(f"工具信号: {signal}")
                is_transactional = True
        
        for signal in TRANSACTIONAL_SIGNALS['solve']:
            if signal in keyword:
                signals.append(f"解决信号: {signal}")
                is_transactional = True
        
        # Q2-Q4: 痛点检测 (有痛点 = 有需求)
        pain_count = 0
        for trigger in PAIN_TRIGGERS['critical']:
            if trigger in keyword:
                signals.append(f"痛点: {trigger}")
                pain_count += 3
        
        for trigger in PAIN_TRIGGERS['medium']:
            if trigger in keyword:
                signals.append(f"中痛点: {trigger}")
                pain_count += 2
        
        # Q3: 如果有痛苦信号，且是工具需求 = 强 Transactional
        if is_transactional and pain_count > 0:
            is_valid = True
            signals.append("✅ 强 Transactional 意图 + 痛点")
        elif is_transactional:
            is_valid = True
            signals.append("✅ Transactional 意图")
        elif pain_count > 3:
            is_valid = True
            signals.append("⚠️ 纯痛点表达，可能是 Info 意图")
        
        # Q5: 如果只是 Info 信号，降低权重
        info_count = 0
        for signal in INFO_SIGNALS:
            if signal in keyword:
                info_count += 1
                signals.append(f"INFO信号: {signal}")
        
        # 计算需求验证分数
        base_score = 50
        if is_transactional and is_valid:
            base_score += 30
        elif is_valid:
            base_score += 15
        base_score += pain_count
        base_score -= info_count * 5  # INFO信号降低分数
        
        return {
            'score': min(100, max(0, base_score)),
            'is_valid': is_valid,
            'intent_type': 'transactional' if is_transactional else 'info',
            'signals': signals[:5]  # 只保留前5个信号
        }
    
    def _assess_monetization(self, keyword: str) -> Dict:
        """商业价值判断 - 止痛药 vs 维生素"""
        score = 50  # 基础分
        signals = []
        is_b2b = False
        is_transactional = False
        
        # B2B 信号 = 高客单价
        for signal in TRANSACTIONAL_SIGNALS['b2b']:
            if signal in keyword:
                signals.append(f"B2B: {signal}")
                is_b2b = True
                score += 20
        
        # Transactional 信号 = 有付费可能
        for signal in TRANSACTIONAL_SIGNALS['tool']:
            if signal in keyword:
                signals.append(f"工具需求: {signal}")
                is_transactional = True
                score += 15
        
        # 解决类信号 = 止痛药
        for signal in TRANSACTIONAL_SIGNALS['solve']:
            if signal in keyword:
                signals.append(f"解决方案: {signal}")
                score += 10
        
        # 免费信号 = 低客单价但高流量
        if 'free' in keyword:
            signals.append("免费需求")
            score += 5  # 免费 = 低客单但高转化
        
        # online 信号 = 便捷需求
        if 'online' in keyword:
            signals.append("在线需求")
            score += 5
        
        return {
            'score': min(100, score),
            'is_b2b': is_b2b,
            'is_transactional': is_transactional,
            'signals': signals[:4]
        }
    
    def _calc_pain_score(self, keyword: str) -> Dict:
        """痛点深度评分 - 痛苦越深越容易收钱"""
        score = 50  # 基础分
        keywords = []
        level = 'low'
        
        # 强烈痛点
        for trigger in PAIN_TRIGGERS['critical']:
            if trigger in keyword:
                keywords.append(trigger)
                score += 20
                level = 'critical'
        
        # 中度痛点
        for trigger in PAIN_TRIGGERS['medium']:
            if trigger in keyword:
                keywords.append(trigger)
                score += 10
                if level != 'critical':
                    level = 'medium'
        
        # 修复类
        for trigger in PAIN_TRIGGERS['fix']:
            if trigger in keyword:
                keywords.append(trigger)
                score += 5
        
        return {
            'score': min(100, score),
            'level': level,
            'keywords': keywords[:3]
        }
    
    def _analyze_competition(self, keyword: str) -> Dict:
        """竞争环境分析"""
        score = 50  # 基础分
        competitors = []
        is_weak = False
        level = 'medium'
        
        # 检查是否已有 SERP 数据
        serp = self.serp.get(keyword, {})
        if serp:
            top_domains = serp.get('top_domains', [])
            competitors = top_domains
            
            # 巨头检测
            has_giant = any(g in d for d in top_domains for g in GIANTS)
            has_weak = any(w in d for d in top_domains for w in WEAK_COMPETITORS)
            
            if has_giant:
                score = 30
                level = 'high'
            elif has_weak:
                score = 90
                level = 'weak'
                is_weak = True
            else:
                score = 60
                level = 'medium'
        
        return {
            'score': score,
            'level': level,
            'competitors': competitors,
            'is_weak': is_weak
        }
    
    def _calc_trend(self, keyword: str) -> Dict:
        """趋势评分 - 看相对 GPTS 而不是绝对值"""
        # GPTS 对比
        gpts = self.gpts.get(keyword, {})
        ratio = gpts.get('ratio', 0)
        
        # 趋势数据
        trend = self.trends.get(keyword, {})
        is_rising = trend.get('is_rising', False)
        
        score = 50  # 基础分
        
        # GPTS 锚定
        if ratio >= GPTS_BENCHMARK['excellent_ratio']:
            score += 40
        elif ratio >= GPTS_BENCHMARK['great_ratio']:
            score += 30
        elif ratio >= GPTS_BENCHMARK['good_ratio']:
            score += 20
        elif ratio >= GPTS_BENCHMARK['base_ratio']:
            score += 10
        
        # 飙升加分
        if is_rising:
            score += 15
        
        return {
            'score': min(100, score),
            'is_rising': is_rising,
            'ratio': ratio
        }
    
    def _assess_pseo_potential(self, keyword: str) -> Dict:
        """pSEO 潜力评估 - 能否裂变出1000个页面"""
        score = 50
        patterns = []
        potential = 'low'
        
        # 检测 pSEO 模式
        for base, variants in PSEO_PATTERNS:
            if base in keyword:
                patterns.append(f"{base} + {variants}")
                score += 15
        
        # 长尾词潜力
        word_count = len(keyword.split())
        if 3 <= word_count <= 5:
            score += 15
            potential = 'medium'
        elif word_count >= 5:
            score += 25
            potential = 'high'
        
        # convert X to Y 模式 = 强 pSEO
        if ' to ' in keyword or ' from ' in keyword:
            score += 20
            patterns.append("X to Y 转换模式")
            potential = 'high'
        
        return {
            'score': min(100, score),
            'potential': potential,
            'patterns': patterns[:3]
        }
    
    def _suggest_monetization(self, monetization: Dict, pain_score: Dict) -> str:
        """变现建议"""
        if monetization['is_b2b']:
            return "B2B模式: API服务/企业订阅/团队版 (高客单价)"
        elif pain_score['level'] == 'critical':
            return "止痛药模式: 付费工具/一次性购买 (痛点深=易付费)"
        elif 'free' in monetization.get('signals', []):
            return "Freemium模式: 免费基础+高级付费 (高流量+中客单)"
        else:
            return "工具模式: 广告+增值服务 (稳健现金流)"
    
    def _make_decision(self, final_score: int, pain_score: int, competition: Dict) -> str:
        """最终决策"""
        # 基础决策
        if final_score >= THRESHOLDS['BUILD_NOW'] and pain_score >= THRESHOLDS['PAIN_SCORE_MIN']:
            decision = '🔴 BUILD NOW'
        elif final_score >= THRESHOLDS['WATCH']:
            decision = '🟡 WATCH'
        else:
            decision = '❌ DROP'
        
        # 降维打击加成
        if competition.get('is_weak') and pain_score >= 40:
            decision = '🔴 BUILD NOW 💎'
        
        return decision
    
    def get_final_results(self, scored_keywords: List[Dict]) -> List[Dict]:
        """生成最终决策结果"""
        results = []
        
        for kw in scored_keywords:
            kw['decision'] = self._make_decision(
                kw['final_score'],
                kw.get('pain_score', 0),
                {'is_weak': kw.get('降维打击', False)}
            )
            results.append(kw)
        
        # 按评分排序
        results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        return results
