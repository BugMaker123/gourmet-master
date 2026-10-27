# 🍽️ Gourmet Master Pro v3.0 — 全能顶级美食研发与私厨顾问 Agent Skill（动态联网采集 · 智能组装 · 多目标优化闭环）

[![Agent Skill](https://img.shields.io/badge/Agent_Skill-v3.0_Dynamic_Loop-orange.svg)](https://github.com/BugMaker123/gourmet-master)
[![Recipes](https://img.shields.io/badge/Structured_Recipes-45%2B_Auto--Growing-green.svg)](./data/culinary_db.json)
[![Live Fetch](https://img.shields.io/badge/Live_Network_Search-Toutiao%20%7C%20Wikipedia%20%7C%20TheMealDB-blue.svg)](./scripts/gourmet_engine.py)

**`gourmet-master` v3.0** 是一套专为 **WorkBuddy、Gemini CLI / Antigravity、OpenAI Codex、Claude Code** 打造的**工业级动态自进化餐饮与私厨顾问技能包**。

不同于静态文本型 Skill，**v3.0 核心引入了「全网实时检索 -> 模糊克重清洗组装 -> 多目标分子级优化 -> 数据库自进化沉淀 -> 交互式 HTML 交付」的完整工程闭环**：
- 🌐 **实时联网抓取 (`live-fetch`)**：即使面对本地库没有的冷门地方菜、网红新菜或海外料理，CLI 引擎可直接联网检索全网菜谱（头条搜索 SSR + 中文维基百科 API + TheMealDB 全球库），提取真实配料、做法与克重配比。
- ⚖️ **模糊单位自动清洗与 BOM/热量组装 (`assemble`)**：自动将网上的 `"生抽一勺、花生油两勺、盐少许、折耳根一把"` 转化为精准商用 `g`/`ml`，并基于内置 **65 种食材营养与商业成本矩阵** 自动算出单份卡路里、蛋白质/碳水/脂肪与 BOM 原料成本（¥）。
- 🧬 **多目标智能改造优化 (`optimize`)**：支持一键对任意菜谱执行 **`fat-loss`（科学减脂降卡改造，热量直降 40%-55%）**、**`michelin-upgrade`（黑珍珠/米其林餐厅级工艺升维）** 与 **`safety-audit`（寄生虫/野生菌毒素食安红线强制注入）**。
- 💾 **知识库自进化 (`--save-to-db`)**：每次联网组装或优化的新菜谱可自动写回 `data/culinary_db.json` 并一键重新渲染交互式网页交付物，越用越强！

---

## 📦 仓库完整目录结构

```text
gourmet-master/
├── SKILL.md                                     # Agent 核心触发指令与五步动态闭环工作流规范
├── README.md                                    # 多智能体安装指南与 v3.0 动态引擎说明
├── scripts/
│   ├── gourmet_engine.py                        # 【核心引擎 v3.0】8大子命令：auto-pipeline / live-fetch / assemble / optimize / tdee / search / scale / render-html
│   └── generate_db.py                           # 结构化菜谱数据库初始化构建器
├── data/
│   └── culinary_db.json                         # 结构化美食数据库（内置45+道基准菜谱，支持联网自动扩充）
├── references/                                  # 5大领域百科级技术参考手册
│   ├── 01_fitness_nutrition_guide.md            # 科学减脂餐、TDEE精算、碳水循环与肉类水合嫩化全书
│   ├── 02_chinese_cuisines_compendium.md        # 中华八大菜系厨政总纲、20大复合味型碗汁与国宴吊汤手册
│   ├── 03_western_culinary_arts.md              # 正统西餐、法餐五大母酱公式、牛排温控与低温慢煮科学
│   ├── 04_regional_cult_delicacies.md           # 全国16+硬核区域“邪教”美食风味化学解构与食安红线全书
│   └── 05_workbuddy_monetization_sop.md         # WorkBuddy/小红书/咸鱼私厨与减脂定制商业变现全案
└── examples/
    ├── gourmet_interactive_portal.html          # 【可直接交付客户】独立离线交互式 HTML/PDF 菜谱与TDEE精算门户
    └── auto_pipeline_demo.json                  # v3.0 一键联网抓取「广西横县鱼生」->组装克重->食安审计实测输出
```

---

## ⚡ CLI 引擎 8 大子命令快速实战 (`scripts/gourmet_engine.py`)

零第三方依赖（基于 Python 3 标准库），开箱即用：

```bash
# 1. 【王牌功能】一键全自动闭环：联网抓取未知菜品 -> 提取配料组装克重 -> 食安/减脂优化 -> 写入数据库
python scripts/gourmet_engine.py auto-pipeline \
  --query "广西横县鱼生" \
  --category cult \
  --region "广西横县" \
  --optimize-mode safety-audit \
  --save-to-db \
  --output examples/auto_pipeline_demo.json

# 2. 独立联网搜索全网菜谱拆解与食材配比 (Toutiao SSR + Wikipedia ZH + TheMealDB)
python scripts/gourmet_engine.py live-fetch --query "贵州酸汤牛肉"

# 3. 模糊家常菜谱 -> 商用精准克重(g/ml) + 营养素 + BOM成本组装器
python scripts/gourmet_engine.py assemble \
  --name "家常小炒黄牛肉" \
  --category chinese \
  --region "湖南长沙" \
  --servings 2 \
  --ingredients "牛里脊 300g, 小米辣 30g, 大蒜 20g, 生抽一勺, 蚝油一勺, 菜籽油两勺, 盐少许" \
  --save-to-db

# 4. 多目标分子级改造优化 (支持 fat-loss | michelin-upgrade | safety-audit)
python scripts/gourmet_engine.py optimize --id "鱼香肉丝" --mode fat-loss --save-to-db

# 5. 计算客户 TDEE、三大营养素克重与 28 天碳水循环方案
python scripts/gourmet_engine.py tdee --gender female --age 28 --height 165 --weight 62 --activity moderate --goal cut

# 6. 检索菜谱数据库
python scripts/gourmet_engine.py search --category cult --keyword "牛瘪"

# 7. 商用/私宴批量缩放配方克重与营养汇总 (如放大至 25 人份)
python scripts/gourmet_engine.py scale --id "正宗柳州螺蛳粉" --servings 25

# 8. 重新渲染客户级交互式 HTML/PDF 交付物系统
python scripts/gourmet_engine.py render-html --output examples/gourmet_interactive_portal.html
```

---

## 🛠️ 在各大智能体中安装使用

### 1. Gemini CLI / Antigravity
```bash
git clone https://github.com/BugMaker123/gourmet-master.git ~/.gemini/config/skills/gourmet-master
```
*(Windows PowerShell)*:
```powershell
git clone https://github.com/BugMaker123/gourmet-master.git "$HOME\.gemini\config\skills\gourmet-master"
```

### 2. OpenAI Codex CLI / Claude Code
```bash
git clone https://github.com/BugMaker123/gourmet-master.git ~/.codex/skills/gourmet-master
```

### 3. WorkBuddy
将本仓库导入 WorkBuddy 技能库，将 `SKILL.md` 设为系统指令，并挂载 `scripts/`、`data/` 与 `references/`，即可接单交付 **28天减脂餐定制、私房菜爆品研发、暗黑猎奇美食复刻与交互式 HTML 手册**。
