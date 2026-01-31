#!/usr/bin/env python3
"""
Profit Hunter Ultimate V4 - 需求真伪识别 + 商业价值判断
=========================================================

核心理念：
1. 需求真伪识别 (5问法) - 区分 Info vs Transactional
2. 商业价值判断 - 止痛药 vs 维生素, B2B信号
3. 增长黑客策略 - pSEO潜力 + 截流建议
4. GPTS锚定基准 - 相对比率而非绝对值
5. 痛点=钱 - PAIN_TRIGGERS 专门盯着痛苦信号
"""

from datetime import datetime
from typing import Dict, List, Set, Tuple
import re

# ============ 配置区 ============

# ==================== 痛点信号词 (痛点 = 钱) ====================
PAIN_TRIGGERS = {
    # 强烈痛点 (得分高)
    "critical": [
        "struggling with", "how to fix", "error", "broken", "not working",
        "failed", "manual", "tedious", "time consuming", "slow", "cannot",
        "doesn't work", "help me", "problem with", "annoying", "frustrating",
        "wish there was", "why is there no", "tired of", "waste of time"
    ],
    # 中度痛点
    "medium": [
        "difficult", "hard to", "complicated", "confusing", "confused",
        "looking for", "need a tool", "searching for", "best way to"
    ],
    # 修复/解决类
    "fix": [
        "fix", "repair", "recover", "restore", "solve", "resolve", "heal"
    ]
}

# ==================== 商业意图信号 ====================
# Transactional 意图 (想解决问题/付费)
TRANSACTIONAL_SIGNALS = {
    "tool": [
        "tool", "app", "software", "generator", "converter", "calculator",
        "maker", "creator", "builder", "editor", "downloader", "online",
        "free", "without login", "no signup", "instant", "quick"
    ],
    "b2b": [  # B2B = 高客单价
        "bulk", "batch", "api", "export", "team", "enterprise", "multiple",
        "mass", "automation", "automatic", "workflow", "integration"
    ],
    "solve": [
        "solve", "remove", "delete", "clean", "optimize", "fix", "repair"
    ]
}

# Info 意图 (只是看看) - 权重降低
INFO_SIGNALS = [
    "what is", "how to", "guide", "tutorial", "learn", "understand",
    "examples", "tips", "best", "review", "comparison"
]

# ==================== 竞争分析 ====================
# 弱竞争者 (降维打击目标)
WEAK_COMPETITORS = [
    "reddit.com", "quora.com", "stackoverflow.com", "medium.com",
    "dev.to", "blogger.com", "wordpress.com", "github.com",
    "youtube.com", "wikipedia.org", "pinterest.com"
]

# 巨头 (避开)
GIANTS = [
    "google.com", "microsoft.com", "adobe.com", "canva.com", "figma.com",
    "notion.so", "airtable.com", "shopify.com", "amazon.com", "apple.com"
]

# ==================== GPTS 锚定基准 ====================
# GPTS 搜索量作为基准线
GPTS_BENCHMARK = {
    "base_ratio": 0.05,    # 5% = 入门门槛
    "good_ratio": 0.10,    # 10% = 好机会
    "great_ratio": 0.20,   # 20% = 绝佳机会
    "excellent_ratio": 0.50  # 50% = 极品
}

# ==================== 评分权重 ====================
WEIGHTS = {
    "demand_validation": 0.25,   # 需求真伪验证
    "monetization": 0.25,        # 商业价值
    "competition": 0.20,         # 竞争环境
    "pain_score": 0.20,          # 痛点深度
    "trend": 0.10                # 趋势
}

# ==================== 阈值 ====================
THRESHOLDS = {
    "BUILD_NOW": 70,   # 70分以上立即做
    "WATCH": 50,       # 50-70分观察
    "PAIN_SCORE_MIN": 40  # 痛点分数最低要求
}

# ==================== pSEO 潜力词根 ====================
PSEO_PATTERNS = [
    ("convert", ["to", "from", "into"]),
    ("generate", ["for", "with", "without"]),
    ("remove", ["from", "background", "watermark"]),
    ("extract", ["from", "audio", "text"]),
    ("download", ["from", "video", "audio"]),
    ("batch", ["process", "convert", "transform"]),
    ("free", ["online", "tool", "app"]),
    ("automatic", ["tool", "generator", "workflow"])
]

# ==================== 变现建议 ====================
MONETIZATION_TYPES = {
    "b2b": ["API服务", "企业订阅", "团队版", "导出收费"],
    "b2c": ["广告变现", "Freemium", "一次性购买", "联盟营销"],
    "saas": ["订阅制", "按量付费", "功能付费", "白标方案"]
}
