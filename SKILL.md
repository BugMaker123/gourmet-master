---
name: gourmet-master
description: "全能顶级美食研发与私厨顾问全书。内置可执行CLI计算引擎(scripts/gourmet_engine.py)、结构化美食数据库(data/culinary_db.json)与交互式HTML/PDF客户交付物生成器。全面覆盖：①科学减脂餐与28天碳水循环/TDEE精算；②中华八大菜系传世大菜与20大复合味型；③正统西餐牛排温控与法餐五大母酱衍生；④全国16+硬核区域邪教美食(螺蛳粉/百草牛瘪/牛撒撇/折耳根/潮汕生腌/豆汁/活珠子/见手青/顺德鱼生/脑花/土笋冻)；⑤WorkBuddy商业变现全案。"
---

# 美食大师：可执行算法引擎 + 结构化配方库 + 交互式客户交付系统 (Gourmet Master v2.0)

本 Skill 是集**可执行 CLI 精算脚本 (`scripts/`) + 结构化 JSON 数据库 (`data/`) + 离线交互式 HTML/PDF 交付物渲染器 (`examples/`) + 25,000字深度厨艺百科 (`references/`)**于一体的工业级智能体技能。

当前 `SKILL.md` 所在目录记为 `<skill-root>`。

---

## 一、 核心可执行工具链 (Executable CLI Engine)

当用户需要查询菜谱、按用餐人数动态缩放克重、计算个人减脂 TDEE 与 28 天碳水循环方案、或生成可交付给付费客户的交互式 HTML/PDF 报告时，**优先调用内置 CLI 引擎**：

### 1. 检索结构化配方库 (`search`)
支持按分类（`fitness` 减脂餐 / `chinese` 八大菜系 / `western` 正统西餐 / `cult` 区域邪教美食）、食材关键词或最高卡路里检索：
```bash
python <skill-root>/scripts/gourmet_engine.py search --category all --keyword "牛"
python <skill-root>/scripts/gourmet_engine.py search --category fitness --max-kcal 380
python <skill-root>/scripts/gourmet_engine.py search --category cult
```

### 2. 单品配方提取与任意人数动态克重缩放 (`recipe`)
支持从 1 人减脂独食自动等比放大至 20 人高端私厨家宴（自动换算所有主辅料克重与总宏量营养素）：
```bash
python <skill-root>/scripts/gourmet_engine.py recipe --id cult_02 --servings 6
python <skill-root>/scripts/gourmet_engine.py recipe --id "惠灵顿牛排" --servings 4 --output wellington_4p.json
```

### 3. 个人精准减脂 TDEE & 28天碳水循环方案生成器 (`tdee-plan`)
输入客户性别、年龄、身高、体重与运动系数，利用 Mifflin-St Jeor 方程自动核算 BMR、TDEE、高碳/中碳/低碳日精确克重指标，并匹配一周循环食谱：
```bash
python <skill-root>/scripts/gourmet_engine.py tdee-plan --gender 女 --age 28 --height-cm 165 --weight-kg 62 --activity light --deficit 400 --output client_plan.json
```

### 4. 一键渲染商业级交互式 HTML/PDF 客户交付系统 (`render-html`)
生成可离线在浏览器打开、内置实时 TDEE 计算器、1~20 人份量拖动滑块、分类筛选与**一键打印导出客户 PDF** 的完整交互式前端页面：
```bash
python <skill-root>/scripts/gourmet_engine.py render-html --title "VIP客户专属减脂与私厨料理全书" --output ./gourmet_deliverable.html
```
- 预渲染演示成品：[`examples/gourmet_interactive_portal.html`](./examples/gourmet_interactive_portal.html)

---

## 二、 技能目录架构

```text
<skill-root>/
├── SKILL.md                              # 核心指令与 CLI 调度规范
├── scripts/
│   └── gourmet_engine.py                 # 多子命令 CLI 引擎 (search / recipe / tdee-plan / render-html)
├── data/
│   ├── culinary_db.json                  # 43+ 道结构化大师级完整配方库 (含宏量营养/科学原理/安全红线)
│   └── generate_db.py                    # 数据库构建与扩展脚本
├── examples/
│   ├── gourmet_interactive_portal.html   # 可直接浏览器打开的交互式食谱与TDEE精算Web系统
│   └── sample_tdee_plan.json             # 客户28天碳水循环交付JSON样例
└── references/                           # 5 大深层领域百科全书
    ├── 01_fitness_diet.md                # 28天碳水循环、3%盐糖水合嫩肉、20款0卡酱汁、15款减脂食谱
    ├── 02_chinese_cuisine.md             # 八大菜系代表作、刀工浆糊芡、国宴红白茸扫汤、20大复合味型
    ├── 03_western_cuisine.md             # 干式熟成、反向慢煎Reverse Sear、法餐五大母酱及15款衍生汁
    ├── 04_cult_regional_food.md          # 全国16+硬核区域邪教美食生化机理、非遗原方与寄生虫安全红线
    └── 05_monetization_and_content.md    # WorkBuddy收费咨询模板、上门私厨SOP、75%毛利轻食外卖与爆款脚本
```

---

## 三、 核心指导原则与安全铁律

1. **量化与分子烹饪优先**：所有配方输出必须包含精准克重（g/ml）、油温成数（℃）、中心探针温度（Core Temp）及背后的分子料理原理（如美拉德反应、水合渗透 Brining、淀粉糊化与蛋白质乳化）。
2. **邪教美食安全底线（生命红线）**：
   - **潮汕生腌 / 顺德鱼生**：严禁使用淡水水产（防肝吸虫/肺吸虫）！必须声明选用深海鱼蟹并经 **-20℃ 超低温急冻 24~48 小时**灭活寄生虫囊蚴。
   - **云南见手青**：必须强调切均匀 3mm 薄片、重猪油、重蒜，并在 **180℃+ 高温下持续炒焖 12~15 分钟以上**彻底破坏热不稳定神经致幻毒素。
   - **贵州百草牛瘪 / 德宏牛撒撇**：必须强调三层细绢布精滤并在 **100℃ 剧烈翻滚煮沸 15~20 分钟以上**彻底灭菌。
