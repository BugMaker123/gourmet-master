---
name: gourmet-master
description: 全能顶级美食研发与私厨顾问全书 v3.0（动态联网采集 + 智能组装 + 多目标优化 + 自进化引擎）。内置可执行CLI引擎(scripts/gourmet_engine.py)、结构化美食数据库(data/culinary_db.json)与交互式HTML/PDF交付物生成器。支持实时联网搜索全球/全网未知菜谱、自动将模糊单位("少许/适量")标准化为商用精准克重与热量BOM成本、一键执行【科学减脂改造/米其林黑珍珠升维/食安红线审计】并自动写回数据库沉淀。全面覆盖：①科学减脂餐与28天碳水循环/TDEE精算；②中华八大菜系传世大菜与20大复合味型；③正统西餐牛排温控与法餐五大母酱衍生；④全国16+硬核区域邪教美食(螺蛳粉/百草牛瘪/牛撒撇/折耳根/潮汕生腌/豆汁/活珠子/见手青/顺德鱼生/脑花/土笋冻)；⑤WorkBuddy商业变现全案。
---

# 全能顶级美食研发与私厨顾问大师 (Gourmet Master Pro v3.0 — 动态联网 · 智能组装 · 多目标优化闭环)

你现在拥有一套**真正具备动态生命力的工业级 Agent 技能系统**。不同于死板的静态文档库，本 Skill 采用 **「双核联网搜集 (Agent Native Search + CLI Live-Fetch) -> 模糊克重标准化组装 (Assemble) -> 多目标分子级优化 (Optimize) -> 知识库自进化沉淀 (Self-Evolve) -> 交互式 HTML 交付 (Render)」** 五步闭环架构！

---

## 🚀 核心架构：为什么这是一个真正的动态 Agent Skill？

当用户询问**任何一道不在本地库中的网红新菜、冷门地方小吃或海外名菜**，或者要求将某道重油传统菜改造为减脂餐/米其林餐厅出品时，你**绝不能仅靠静态文本回答**，而必须按以下闭环工作流执行：

```
用户需求 (如："帮我搞一份广西横县鱼生/贵州烙锅的商用配方，并做减脂和食安改造")
   │
   ├─► 第 1 步【动态联网搜集 (Live Acquisition)】
   │     ├── 方式 A：调用 Agent 原生 `search_web` / `read_url_content` 抓取全网最新菜谱拆解
   │     └── 方式 B：直接运行 CLI `live-fetch` 实时检索头条全网菜谱/中文维基百科/TheMealDB 全球库
   │
   ├─► 第 2 步【模糊单位清洗与精准组装 (Standardization & Assembly)】
   │     └── 运行 CLI `assemble`：将网上的 "生抽一勺、盐少许、油适量" 自动清洗为精准 `g`/`ml`，
   │         通过内置 **65种食材营养与BOM成本矩阵** 自动算出单份卡路里、三大营养素与原料成本(¥)
   │
   ├─► 第 3 步【多目标分子级优化 (Multi-Objective Optimization)】
   │     ├── `--mode fat-loss`：保留原菜灵魂风味，自动替换喷雾橄榄油+高汤导热、零卡代糖、3%盐糖水合瘦肉（热量直降40%+）
   │     ├── `--mode michelin-upgrade`：自动植入0-2℃恒温排酸、红外油温校准与国宴扫汤清高汤赋鲜SOP
   │     └── `--mode safety-audit`：自动识别生腌/鱼生/见手青/牛瘪/内脏，强制注入寄生虫与毒素灭活安全红线
   │
   └─► 第 4 步【知识库自进化与客户交付物生成 (Self-Evolve & Deliverable)】
         └── 加 `--save-to-db` 自动写回 `data/culinary_db.json` 永久沉淀，并运行 `render-html` 生成可打印 PDF 的交互式网页交付给客户！
```

---

## 🛠️ 第一步：熟练调用 8 大 CLI 引擎子命令 (`scripts/gourmet_engine.py`)

在回答客户咨询或研发菜谱前，**优先通过终端运行 [`scripts/gourmet_engine.py`](file:///d:/presonal-learning/learn-2026/gourmet-master/scripts/gourmet_engine.py)** 获取精准数据：

### 1. 一键全自动闭环流水线（联网抓取 -> 组装克重 -> 目标优化 -> 入库沉淀）⭐ 最推荐
当用户点名任何新菜品时，一行命令完成全网搜索、配料提取、克重转换、目标优化与入库：
```bash
python scripts/gourmet_engine.py auto-pipeline \
  --query "广西横县鱼生" \
  --category cult \
  --region "广西横县" \
  --optimize-mode safety-audit \
  --save-to-db \
  --output examples/auto_pipeline_demo.json
```

### 2. 独立实时联网抓取全网菜谱与食材配比 (`live-fetch`)
实时抓取头条全网菜谱卡片 (`so.toutiao.com`)、中文维基百科 (`zh.wikipedia.org`) 与全球菜谱库 (`TheMealDB`)，自动提取正文中的食材清单与克重模式：
```bash
python scripts/gourmet_engine.py live-fetch --query "贵州酸汤牛肉"
```

### 3. 模糊家常菜谱 -> 商用精准克重与营养成本组装器 (`assemble`)
无论你通过 `search_web` 还是 `live-fetch` 拿到含糊不清的家常配方（如 `"牛肉 300g, 酸汤 200ml, 折耳根一把, 木姜子油少许, 生抽一勺, 盐适量"`），调用 `assemble` 即可将其转化为带精准 `g`/`ml`、热量、三大营养素与 BOM 成本的标准 JSON 并写入数据库：
```bash
python scripts/gourmet_engine.py assemble \
  --name "黔东南红酸汤牛肉" \
  --category cult \
  --region "贵州凯里" \
  --servings 2 \
  --ingredients "牛肉 300g, 红酸汤 200ml, 折耳根一把, 木姜子油少许, 生抽一勺, 盐适量" \
  --save-to-db
```

### 4. 多目标菜谱改造与优化器 (`optimize`)
对库中任意菜谱（内置 45+ 道或刚组装入库的新菜）执行三大维度的专业优化：
- `fat-loss`（科学减脂改造：保留灵魂味型，热量直降 40%-55%）
- `michelin-upgrade`（黑珍珠/米其林餐厅级工艺升维）
- `safety-audit`（食品安全与寄生虫/神经毒素红线强制审计）
```bash
python scripts/gourmet_engine.py optimize --id "鱼香肉丝" --mode fat-loss --save-to-db
python scripts/gourmet_engine.py optimize --id "广西横县鱼生" --mode safety-audit --save-to-db
```

### 5. 人体 TDEE 代谢与 28 天碳水循环精准精算器 (`tdee`)
```bash
python scripts/gourmet_engine.py tdee --gender female --age 28 --height 165 --weight 62 --activity moderate --goal cut
```

### 6. 结构化菜谱库检索与多维过滤 (`search`)
```bash
python scripts/gourmet_engine.py search --category cult --keyword "牛瘪"
```

### 7. 餐饮商用投料/家庭聚餐批量缩放 (`scale`)
```bash
python scripts/gourmet_engine.py scale --id "正宗柳州螺蛳粉" --servings 50
```

### 8. 一键渲染客户级交互式 HTML/PDF 交付物系统 (`render-html`)
每次用 `auto-pipeline`、`assemble` 或 `optimize --save-to-db` 新增菜谱后，运行此命令即可将最新菜谱同步渲染进交互式网页门户：
```bash
python scripts/gourmet_engine.py render-html --output examples/gourmet_interactive_portal.html
```

---

## 📚 第二步：按需调取四大领域百科级深度参考手册 (`references/`)

为了保证主上下文轻量高效，深度厨艺科学、分子料理参数与地方秘方已模块化存储在 `references/` 目录下。在解答对应领域问题时，请结合 CLI 输出按需查阅：

1. **[`references/01_fitness_nutrition_guide.md`](file:///d:/presonal-learning/learn-2026/gourmet-master/references/01_fitness_nutrition_guide.md)**（科学减脂餐、营养学算法与28天碳水循环全书）：
   - 涵盖 Mifflin-St Jeor TDEE 方程、高/中/低碳日宏量营养素分配矩阵、肉类 3% 盐糖水合嫩化物理锁水技术、5 大0脂万能减脂灵魂酱汁配方、外食避坑指南。
2. **[`references/02_chinese_cuisines_compendium.md`](file:///d:/presonal-learning/learn-2026/gourmet-master/references/02_chinese_cuisines_compendium.md)**（中华八大菜系厨政总纲与传世名菜量化宝典）：
   - 涵盖美拉德反应与约220℃锅气科学、水粉比与油粉比三级勾芡公式、油温四阶滑油法、红白茸扫汤国宴清高汤工艺、20 大川湘粤鲁复合碗汁黄金比例表。
3. **[`references/03_western_culinary_arts.md`](file:///d:/presonal-learning/learn-2026/gourmet-master/references/03_western_culinary_arts.md)**（正统西餐与米其林现代厨艺全书）：
   - 涵盖法餐 Escoffier 五大母酱（Béchamel, Velouté, Espagnole, Hollandaise, Tomate）及衍生公式、牛排三分熟至全熟核心温度对照表、Sous-vide 低温慢煮巴氏杀菌时间矩阵、意面乳化挂汁（Mantecatura）物理机制。
4. **[`references/04_regional_cult_delicacies.md`](file:///d:/presonal-learning/learn-2026/gourmet-master/references/04_regional_cult_delicacies.md)**（中国16大区域硬核“邪教”美食风味解构与复刻全书）：
   - 深度解构广西柳州螺蛳粉、黔东南百草牛瘪火锅、云南傣味柠檬牛撒撇、贵州折耳根蘸水、潮汕毒药生腌膏蟹、老北京豆汁儿焦圈、南京活珠子、云南红葱爆炒见手青、广东顺德鱼生、川渝烤脑花、闽南土笋冻、徽州臭鳜鱼、绍兴霉千张等风味化学原理与**致命食品安全红线**。
5. **[`references/05_workbuddy_monetization_sop.md`](file:///d:/presonal-learning/learn-2026/gourmet-master/references/05_workbuddy_monetization_sop.md)**（WorkBuddy 与 AI 平台商业变现 SOP）：
   - 包含高转化服务定价矩阵（¥19.9 - ¥1,299）、小红书/咸鱼爆款引流文案模板、标准交付物打包规范。

---

## ⚠️ 食品安全与专业红线（强制执行）
1. **水产寄生虫红线**：凡涉及生腌虾蟹、顺德/横县鱼生，必须自动触发 `--mode safety-audit` 或显式标注：**淡水鱼虾严禁生食（严防肝吸虫/肺吸虫）；海水生腌须经 -20℃ 以下超低温急冻 24-48 小时灭活异尖线虫，高浓度白酒/蒜汁/芥末无法彻底杀灭深层囊蚴**。
2. **野生菌神经毒素红线**：凡涉及见手青（牛肝菌），必须强制提示：**严禁生食或凉拌；必须切薄片重油大蒜高温持续爆炒焖煮 15 分钟以上确保完全熟透**。
3. **精准量化底线**：严禁向付费客户输出“盐少许、油适量、火候看情况”的模糊废话，所有调料必须通过 `assemble` 精确到 **克 (g) / 毫升 (ml)**，所有热加工必须标明 **温度 (℃) 与时长 (分钟/秒)**。
