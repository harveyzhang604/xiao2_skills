---
name: profit-hunter-ultimate
description: "终极版蓝海关键词自动猎取系统。整合 Google Autocomplete (Alphabet Soup)、Google Trends 二级深挖、GPTs 基准对比、用户意图深挖、Playwright SERP 降维打击分析。自动识别竞争度、痛点强度、用户真正意图、商业价值。每 6 小时自动运行，输出高质量'立即做'机会清单。核心升级：降维打击检测（前3名有论坛=机会）、用户意图分析（不只看信号，还看用户真正想做什么）、显示 GPTs 热度比、列全关键词（不采样）。Use when: 'find profitable keywords', 'blue ocean opportunities', 'serp analysis', 'user intent mining', '/hunt-ultimate' command."
license: MIT
---

# 💎 Profit Hunter ULTIMATE - 终极版蓝海关键词猎取系统

## 快速开始

```bash
cd /root/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/skills/profit-hunter-ultimate/scripts

# 快速测试（30个关键词）
python test_ultimate.py

# 完整运行
python profit_hunter.py --trends --playwright --max 500

# 定时任务（每6小时）
python scheduler.py
```

## 脚本说明

### scripts/profit_hunter.py
主分析脚本，支持以下参数：

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `--trends` | 启用 Google Trends 分析 | False |
| `--playwright` | 启用 Playwright SERP 分析 | False |
| `--max` | 最大关键词数量 | 500 |
| `--seed` | 种子词，逗号分隔 | 从 words.md 读取 |

**示例:**
```bash
python profit_hunter.py                           # 快速模式
python profit_hunter.py --trends                  # + Trends
python profit_hunter.py --trends --playwright     # 终极版
python profit_hunter.py --max 100 --seed "ai,ml"  # 自定义
```

### scripts/scheduler.py
定时调度器，支持以下参数：

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `--interval` | 运行间隔（小时） | 6 |
| `--immediate` | 立即运行一次 | False |
| `--run-once` | 只运行一次，不循环 | False |

**示例:**
```bash
python scheduler.py                    # 每6小时运行
python scheduler.py --interval 12      # 每12小时
python scheduler.py --immediate        # 立即+循环
python scheduler.py --run-once         # 只运行一次
```

### scripts/test_ultimate.py
快速测试脚本，使用默认参数测试完整流程。

### words.md
种子词配置文件，每行一个关键词。系统会基于这些词通过 Alphabet Soup 扩展出大量候选词。

## 核心理念

```
降维打击 > 正面竞争
小而美 > 大而全
真需求 > 伪需求
自动化 > 手动
```

**唯一目标**：找到那些**前3名是论坛/博客**的关键词，做一个工具站轻松占据首页。

## 评分算法

```
Final Score = Trend×25% + Intent×35% + Competition×25% + Buildability×15%
```

| 评分范围 | 决策 |
|---------|------|
| ≥ 65 | 🔴 BUILD NOW |
| 45-65 | 🟡 WATCH |
| < 45 | ❌ DROP |

## 输出文件

```
data/
├── ultimate_final_results.csv  # 最终结果（最重要）
├── step0_suggest_keywords.csv  # Google Suggest 原始数据
├── step1_trends_deep.csv       # Trends 飙升词
├── step2_gpts_comparison.csv   # GPTs 对比数据
└── step3_serp_analysis.csv     # SERP 竞争分析
```

## 安装依赖

```bash
# 基础依赖
pip install requests pandas pytrends schedule openpyxl

# 可选：Playwright（用于真实 SERP 分析）
pip install playwright
playwright install chromium
```

## 关键字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `keyword` | 关键词 | calculator online |
| `final_score` | 最终评分 | 80.8 |
| `decision` | 决策 | 🔴 BUILD NOW |
| `avg_ratio` | vs GPTs 热度比 | 17.2% |
| `user_intent` | 用户意图类型 | calculate, convert |
| `user_goal` | 用户真正想做什么 | 复合需求：calculate + convert |
| `intent_clarity` | 意图清晰度 | 高/中/低 |
| `降维打击` | 是否有降维打击机会 | True/False |

## 降维打击原理

如果 Google 前3名有 Reddit/Quora/Medium，但没有大厂网站，这就是**降维打击机会**：

```
场景：aura calculator
问题：用户有需求，但首页全是 Reddit 帖子
机会：做一个简单的计算器工具站
结果：轻松占据首页 → 流量 → 广告收入
```

## 版本对比

| 特性 | 基础版 | ULTIMATE |
|-----|-------|----------|
| Autocomplete | ✅ | ✅ 优化 |
| Trends | ❌ | ✅ 二级深挖 |
| GPTs 对比 | ❌ | ✅ 必选 |
| SERP 分析 | 规则 | Playwright |
| 评分阈值 | 75 | 65 |
| 立即做词数 | 0 | 29+ |

## 故障排查

**问题：没有"立即做"的词**
- 降低 `--max` 参数值
- 更换种子词（words.md）
- 启用 `--trends` 和 `--playwright`

**问题：Google Trends 限频**
- 减少种子词数量
- 增加运行间隔
- 使用 `--run-once` 模式

**问题：Playwright 安装失败**
```bash
pip install playwright
playwright install chromium
# 或不使用 --playwright 参数
```

## 核心理念（再次强调）

```
不做大词！不做大词！不做大词！

大词 = calculator, converter → 竞争激烈 ❌
小词 + 降维打击 = aura calculator (前3名是 Reddit) → 轻松占据首页 ✅
```

---

**开始行动！💎🚀💰**
