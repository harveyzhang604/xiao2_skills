# 💎 Profit Hunter ULTIMATE V3.0 - 超级需求挖掘引擎

## 📦 安装

```bash
cd skills/profit-hunter-ultimate
pip install -r requirements.txt
```

## 🚀 快速开始

### 1. 快速测试
```bash
cd scripts
python test_v3.py
```

### 2. 运行 V3 超级挖掘（推荐）
```bash
python profit_hunter_v3.py --max 50
```

### 3. 运行 V2 完整版
```bash
python profit_hunter_ultimate.py --trends --playwright
```

### 4. 启动定时任务
```bash
python scheduler.py  # 每6小时自动运行
```

## 📁 文件说明

```
profit-hunter-ultimate/
├── SKILL.md              # Skill 定义（触发器 + 核心说明）
├── requirements.txt      # Python 依赖
├── references/
│   └── REFERENCES.md     # 详细技术文档
├── scripts/
│   ├── profit_hunter_v3.py      # V3 超级挖掘（推荐）
│   ├── profit_hunter_ultimate.py # V2 完整版
│   ├── scheduler.py              # 定时任务
│   ├── test_v3.py               # V3 测试
│   ├── test_ultimate.py         # V2 测试
│   └── words.md                 # 种子词配置
└── data/                 # 输出目录（运行后生成）
    ├── super_results.csv        # V3 结果
    ├── ultimate_final_results.csv # V2 结果
    └── ...
```

## 🎯 核心功能对比

| 功能 | V2.0 | V3.0 ⭐ |
|-----|------|--------|
| 平台数量 | 1 (Google) | **6 (全平台)** |
| 痛点分析 | 基础 | **NLP 增强** |
| 商业价值 | 无 | **自动评估** |
| 评分阈值 | 65 | **60** |
| 推荐数量 | 5-10 | **15-30** |

## 💡 使用建议

1. **日常挖掘**：使用 V3 (`profit_hunter_v3.py`)
2. **深度分析**：使用 V2 + Playwright
3. **定时监控**：启动 `scheduler.py`

## 📊 输出示例

```
🏆 Top 15 推荐需求：
   🔴 BUILD NOW ai headshot generator
      痛点:85 商业:65 竞争:LOW 降维:True
   🔴 BUILD NOW excel pivot table helper
      痛点:90 商业:70 竞争:LOW 降维:True
   🟡 WATCH video converter online
      痛点:55 商业:60 竞争:MEDIUM 降维:False
```

## ⚙️ 配置

修改 `scripts/words.md` 添加种子词：
```markdown
ai calculator
video converter
online tool
```

## 📚 文档

- **快速指南**：见 SKILL.md
- **技术细节**：见 references/REFERENCES.md

---

**💎 用 V3 挖掘真实需求，精准打击降维机会！🚀💰**
