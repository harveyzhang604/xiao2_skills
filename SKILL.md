---
name: profit-hunter-ultimate
description: "终极版蓝海关键词猎取系统 V3。整合 Google Autocomplete + Google Trends 二级深挖 + GPTs 基准对比 + 用户意图深挖 + Playwright SERP 降维打击分析。自动识别竞争度、痛点强度、用户真正意图、商业价值。每 6 小时自动运行，输出高质量'立即做'机会清单。核心升级：用户意图分析（calculate/convert/generate/check）、显示 GPTs 热度比、全部关键词输出（不采样）。Use when: 'find profitable keywords', 'blue ocean opportunities', 'serp analysis', 'user intent mining', '/hunt-ultimate' command."
license: MIT
---

# 💎 Profit Hunter ULTIMATE V3 - 终极版蓝海关键词猎取系统

## 🎯 核心理念

```
降维打击 > 正面竞争
小而美 > 大而全
真需求 > 伪需求
自动化 > 手动
```

**唯一目标**：找到那些**前3名是论坛/博客**的关键词，做一个工具站轻松占据首页。

---

## 🚀 V3 核心升级

### 1. **用户意图深挖（⭐ 核心）**

```python
不只检测信号，还要分析用户真正想做什么：

- calculate: 用户想计算某个数值
- convert: 用户想转换单位/格式
- generate: 用户想自动生成内容
- check: 用户想验证/检查某事
- compare: 用户想对比选项
- ...
```

**输出字段：**
- `user_intent`: 意图类型（如 "calculate, convert"）
- `user_goal`: 用户真正想做什么（如 "复合需求：calculate + convert"）
- `intent_clarity`: 意图清晰度（高/中/低）

### 2. **GPTs 热度比显示（⭐ 重要）**

```
CSV 和终端都显示 avg_ratio：

例如：
- avg_ratio = 17.2% → 候选词达到 GPTs 的 17.2% 热度
- avg_ratio = 3.5%  → 刚好达到入围线
```

### 3. **全部关键词输出（⭐ 不采样）**

```
旧版：只采样 30 个
新版：全部种子词 + 全部挖掘结果（500+）

max_candidates = 500（默认）
```

### 4. **SERP 降维打击检测**

```python
if Google 前3名有 Reddit/Quora：
    → 🟢 WEAK (降维打击机会！)
    → Competition Score = 100 分
    → 🔴 BUILD NOW
```

### 5. **二级 Related Queries 深挖**

```
Step 1: 找飙升词（Rising Queries）
Step 2: 对每个飙升词，再找它的飙升词
        ↓
     发现隐藏更深的机会
```

---

## 📋 V3 完整工作流程

```
Step 0: Google Autocomplete 海量挖词（Alphabet Soup）
        ↓
Step 1: Google Trends 飙升词捕捉 + 二级深挖
        ↓
Step 2: GPTs 基准对比（热度验证）✅
        ↓
Step 3: SERP 竞争分析（Playwright 降维打击检测）
        ↓
Step 4: 需求意图评分（Pain Points Detection）
        ↓
Step 4.5: 用户意图深挖 ⭐（User Intent Mining）
        ↓
Step 5: 终极评分（优化算法）
        ↓
Step 6: 输出决策（BUILD/WATCH/DROP）
```

---

## 🎯 V3 评分算法详解

### 最终评分公式

```
Final Score = (
    Trend Score × 25% +        # GPTs 对比热度
    Intent Score × 35% +       # 需求强度
    Competition Score × 25% +   # 竞争度
    Buildability Score × 15%    # 可实现性
) + 降维打击(+20)
```

### Trend Score（热度评分）

| GPTs Ratio | Score | 判断 |
|-----------|-------|------|
| ≥ 20% | 100 | 极品词 |
| ≥ 10% | 85 | 优质词 |
| ≥ 5% | 75 | 良好词 |
| ≥ 3% | 70 | 合格词 |
| < 3% | 50 | 基础分 |

### Intent Score（需求强度）

| 信号类型 | 关键词模式 | 加分 |
|---------|-----------|------|
| **强痛点** | struggling with, how to fix, error | +40 |
| **工具** | calculator, generator, converter | +30 |
| **对比** | vs, alternative, better than | +25 |
| **B2B** | bulk, api, export, team | +25 |
| **速度** | fast, quick, instant, auto | +20 |
| **长尾** | 2+ 个词 | +15 |

### 用户意图深挖（V3 核心）

| 意图类型 | 关键词 | 用户真正想做什么 |
|---------|--------|-----------------|
| **calculate** | calculator | 计算某个数值 |
| **convert** | converter | 转换单位/格式 |
| **generate** | generator | 自动生成内容 |
| **check** | checker | 验证/检查某事 |
| **compare** | vs, alternative | 对比选项 |
| **find** | finder, search | 查找某物 |
| **track** | tracker | 追踪/监测 |

### Competition Score（竞争度）

| SERP 特征 | Score | 降维打击 |
|----------|-------|---------|
| **前3名有论坛** | 100 | ✅ |
| 🟢 LOW/WEAK | 90 | ✅ |
| 🟡 MEDIUM | 60 | ❌ |
| 🔴 GIANT（大厂） | 30 | ❌ |

### 决策阈值

| 评分范围 | 决策 | 行动 |
|---------|------|------|
| **≥ 65** | 🔴 BUILD NOW | 立即开发 |
| **45-65** | 🟡 WATCH | 观察或测试 |
| **< 45** | ❌ DROP | 放弃 |

---

## 🚀 使用方法

### 快速测试

```bash
python scripts/test_ultimate.py
```

**预期结果：**
- 处理 500+ 个关键词
- 发现 15-30 个"立即做"
- 耗时 5-8 分钟

### 完整运行

```bash
# V3 基础版（推荐日常使用）
python scripts/profit_hunter_ultimate.py

# 包含 Trends 深度挖掘
python scripts/profit_hunter_ultimate.py --trends

# V3 终极版（包含 Playwright）
python scripts/profit_hunter_ultimate.py --trends --playwright --max 50
```

### 定时任务

```bash
# 启动定时调度器（每 6 小时）
python scripts/scheduler.py
```

---

## 📊 V3 输出说明

### CSV 文件

```
data/
├── ultimate_final_results.csv  # ⭐ 最终结果（全部关键词）
├── step0_suggest_keywords.csv  # Google Suggest 原始数据
├── step1_trends_deep.csv       # Trends 飙升词（含二级）
├── step2_gpts_comparison.csv   # GPTs 对比数据（含 avg_ratio）
└── step3_serp_analysis.csv     # SERP 竞争分析
```

### 关键字段（V3 新增）

| 字段 | 含义 | 示例 |
|------|------|------|
| `keyword` | 关键词 | calculator online free |
| `final_score` | 最终评分 | 80.8 |
| `decision` | 决策 | 🔴 BUILD NOW |
| `avg_ratio` | vs GPTs 热度比 | 17.2% |
| `user_intent` | 意图类型 | calculate, convert |
| `user_goal` | 用户真正想做什么 | 复合需求：calculate + convert |
| `intent_clarity` | 意图清晰度 | 高/中/低 |
| `competition` | 竞争度 | 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH |
| `降维打击` | 是否有降维打击机会 | True/False |
| `intent_score` | 意图评分 | 45-100 |
| `signals` | 信号词 | 痛点:struggling, 工具:calculator |

### 终端输出示例

```
🔥 Top 10 BUILD NOW 机会（含用户意图）：
--------------------------------------------------------------------------------
   1. struggling with excel pivot table calculator (92.5分)
      GPTs热度比: 24.5% | 意图: calculate
      目标: 用户想计算某个数值
      
   2. free video converter online (88.0分)
      GPTs热度比: 18.2% | 意图: convert
      目标: 用户想转换单位/格式/语言
```

---

## 💡 实战策略

### Strategy 1：降维打击（推荐）

```
1. 运行 ULTIMATE 版本（启用 Playwright）
2. 筛选 "降维打击=True" 的词
3. 选择评分最高的前 3 个
4. 快速做工具（Next.js + Vercel）
5. 提交到 Google Search Console
6. 等待 7-14 天
7. 观察流量和排名
```

### Strategy 2：用户意图分析（V3）

```
1. 查看 user_intent 字段
2. 选择 "calculate" 或 "convert" 等清晰意图
3. 查看 user_goal 确认用户需求
4. 意图清晰度 = 高 的词优先
```

### Strategy 3：热度验证

```
1. 筛选 avg_ratio ≥ 0.1 的词
2. 看 Google Trends 曲线（是否上升）
3. 选择增长最快的词
4. 做工具 + SEO 优化
```

---

## 🆚 V3 vs V2 对比

| 特性 | V2.0 | V3.0 ⭐ |
|-----|------|--------|
| 用户意图分析 | ❌ | ✅ 深挖 |
| GPTs 热度比显示 | ❌ | ✅ 显示 |
| 全部关键词输出 | 采样30个 | ✅ 500+ |
| 痛点词库 | 基础 | ✅ NLP增强 |
| 评分阈值 | 65分 | ✅ 65分 |
| 降维打击加成 | +20分 | ✅ +20分 |

---

## ⚙️ 高级配置

### 调整评分阈值

编辑 `scripts/config.py`：

```python
THRESHOLDS = {
    "BUILD_NOW": 65,     # 立即做阈值（降低 = 更多推荐）
    "WATCH": 45,         # 观察阈值
    "MIN_GPTS_RATIO": 0.03,  # 最低 GPTs 比值
}
```

### 调整最大候选词数量

```python
MAX_CANDIDATES = 500  # 全部输出
```

### 定制用户意图

```python
USER_INTENTS = {
    'calculate': {...},
    'convert': {...},
    # 添加新的意图类型
}
```

---

## 🐛 故障排查

### 问题 1：没有 BUILD NOW 的词

**解决：**
1. 检查 `avg_ratio` 是否有数据
2. 降低 `BUILD_NOW` 阈值到 60
3. 更换种子词（`data/words.md`）

### 问题 2：Google Trends 限频

**解决：**
1. 减少种子词数量（5-10 个）
2. 增加延迟（`time.sleep(3)` → `time.sleep(10)`）

### 问题 3：Playwright 安装失败

**解决：**
```bash
pip install playwright
playwright install chromium
```

---

## 📈 成功指标

### 短期（7天）

- [ ] 发现 ≥ 10 个"立即做"的词
- [ ] 选择 1 个开始实现
- [ ] 工具上线并提交 GSC

### 中期（30天）

- [ ] 工具进入 Google 前 10 名
- [ ] 获得首批自然流量
- [ ] 设置好定时任务

### 长期（90天）

- [ ] 工具矩阵（3-5 个工具）
- [ ] 月自然流量 > 1000
- [ ] 月广告收入 > $500

---

## 💰 核心理念

```
不做大词！不做大词！不做大词！

大词 = calculator, converter
     ↓
   竞争激烈 ❌

小词 + 降维打击 = struggling with excel pivot table calculator
     ↓
   轻松占据首页 ✅
     ↓
   流量 → 广告收入 💰💰💰
```

---

## 🎁 下一步行动

### Today

```bash
python scripts/test_ultimate.py
```

查看能找到哪些"立即做"的机会。

### This Week

1. 运行完整版（包含 Trends 和 Playwright）
2. 选择 Top 1 的词
3. 快速做一个工具（Next.js + Vercel）

### This Month

```bash
python scripts/scheduler.py
```

启动定时任务，持续监控新机会。

---

**开始行动！💎🚀💰**
