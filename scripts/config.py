#!/usr/bin/env python3
"""
配置参数 - V3 优化版
"""

# 评分阈值（V3: 65 分，更容易推荐）
THRESHOLDS = {
    "BUILD_NOW": 65,       # 立即做阈值
    "WATCH": 45,           # 观察阈值
    "MIN_GPTS_RATIO": 0.03,  # 最低 GPTs 比值
}

# SERP 弱竞争者（降维打击目标）
SERP_WEAK_COMPETITORS = [
    "reddit.com", "quora.com", "stackoverflow.com",
    "medium.com", "dev.to", "blogger.com", "wordpress.com"
]

# SERP 巨头（避开）
SERP_GIANTS = [
    "google.com", "microsoft.com", "adobe.com",
    "canva.com", "figma.com", "notion.so"
]

# 痛点触发词
PAIN_TRIGGERS = {
    "strong": [
        "struggling with", "how to fix", "error", "problem",
        "cannot", "doesn't work", "failed", "help",
        "urgent", "asap", "immediately"  # V3 新增：紧急需求
    ],
    "medium": [
        "best way", "how to create", "tutorial", "guide"
    ],
    "tool": [
        "calculator", "generator", "converter", "tool",
        "maker", "creator", "builder"
    ]
}

# 意图信号
INTENT_SIGNALS = {
    "tool": ["calculator", "generator", "converter", "tool", "maker", "checker"],
    "对比": ["vs", "alternative", "better than", "compare"],
    "B2B": ["bulk", "api", "export", "team", "business", "enterprise"],
    "速度": ["fast", "quick", "instant", "auto", "automatic", "easy"],
    "长尾": 2,  # 2个词以上
}

# 评分权重（V3 标准）
WEIGHTS = {
    "trend": 0.25,       # GPTs 热度
    "intent": 0.35,      # 需求强度（提高权重）
    "competition": 0.25, # 竞争度
    "buildability": 0.15, # 可实现性
}

# 输出目录
DATA_DIR = "data"

# 最大候选词数量（V3: 全部，不采样）
MAX_CANDIDATES = 500

# 降维打击加成分数
DIMENSION_ATTACK_BONUS = 20
