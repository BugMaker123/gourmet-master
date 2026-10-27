# 🍳 美食大师 (Gourmet Master Skill)

> **全能顶级美食研发与私厨顾问**：科学减脂餐、中华大厨大菜、正统西餐米其林技法与硬核区域“邪教美食”全书。  
> 专为 **Gemini、Codex、Claude Code、WorkBuddy、OpenDevin** 等 AI 智能体打造的商业级美食知识体系。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/AI_Agents-Gemini_|_Codex_|_Claude_|_WorkBuddy-orange.svg)](#一键安装与使用指南)

---

## 🌟 四大核心美食板块

不同于普通菜谱 AI 模糊含混的“油适量、盐少许”，**Gourmet Master** 坚持物理与分子级烹饪精确标准：

| 专题板块 | 核心硬核内容 | 包含代表代表作 |
| :--- | :--- | :--- |
| 🥗 [**科学减脂与轻食备餐**](./references/01_fitness_diet.md) | 能量缺口精确计算、高蛋白保肌防掉代谢、3%盐糖水合渗透嫩肉术（彻底告别干柴水煮鸡胸）、5 款低卡自制万能酱汁、上班族 5 天备餐 Meal Prep 储存与复热。 | 柠檬黑椒爆汁鸡胸肉便当、低卡牛肉彩椒荞麦抱蛋卷、泰式青柠鲜虾魔芋高纤沙拉。 |
| 🥢 [**中华料理大厨秘籍**](./references/02_chinese_cuisine.md) | 火候油温成数（三成至八成热换算）、镬气 (Wok Hei) 物理成因与家庭复刻法、中厨不忙乱的大厨黄金万能碗汁库（鱼香汁/糖醋54321/潮汕百年老卤水秘方）。 | 汉源大红袍古法麻婆豆腐（三次推铲挂芡）、顺德白切鸡（虾眼水三提三浸+冰水激脆）、古法本帮红烧肉（全程不加一滴水）。 |
| 🥩 [**正统西餐与米其林技法**](./references/03_western_cuisine.md) | 牛排四大部位特征、美拉德反应控温秘诀、中心温度探针熟度表（Rare 至 Well-Done）、黄油淋油裹香法 (Basting)、**5~8分钟醒肉 (Resting) 回汁物理学**、经典法餐五大母酱、意式手工意面。 | 经典罗马风味培根蛋黄面 (Spaghetti alla Carbonara 传统无淡奶油版)、三分熟香煎肋眼牛排、荷兰母酱。 |
| 🦪 [**硬核区域邪教美食全书**](./references/04_cult_regional_food.md) | 为什么“邪教料理”让人极度上瘾（厌氧发酵挥发性硫化物、游离谷氨酸鲜味爆炸、良性自虐内啡肽奖励）、地道非遗原方与**深度食品卫生寄生虫防范生命线**。 | 柳州老坛酸笋石螺原汤螺蛳粉、贵州黔东南百草牛瘪火锅、云南苦撒撇、西南野生折耳根拌万物、潮汕红膏生腌青蟹、老北京传统绿豆酸浆豆汁、南京原汁活珠子。 |
| 💰 [**商业变现与流量密码**](./references/05_monetization_and_content.md) | WorkBuddy 线上付费私厨营养顾问、小红书/抖音百万爆款选题与 60 秒黄金分镜脚本、轻食沙拉与特色外卖低成本启动、数字菜谱无本知识付费。 | 商业化全流程落地方案。 |

---

## 📦 项目目录结构

```text
gourmet-master/
├── SKILL.md                          # 智能体核心技能入口 (包含YAML元数据与执行工作流)
├── README.md                         # 详细安装与使用说明
├── WORKBUDDY_SETUP_GUIDE.md          # WorkBuddy / Dify 等平台部署指南
├── install.ps1                       # Windows 一键自动安装脚本
├── install.sh                        # macOS / Linux 一键自动安装脚本
└── references/                       # 5 大商用级专业参考知识库
    ├── 01_fitness_diet.md            # 科学减脂餐与轻食备餐指南
    ├── 02_chinese_cuisine.md         # 中华大厨烹调秘籍
    ├── 03_western_cuisine.md         # 正统西餐与米其林级技法
    ├── 04_cult_regional_food.md      # 区域“邪教美食”全书
    └── 05_monetization_and_content.md# 美食内容创业与商业变现攻略
```

---

## 🚀 一键安装与使用指南 (Installation)

### 1. 在 Gemini / Antigravity 中安装

#### 方式 A：命令行一键安装

**Windows (PowerShell)**:
```powershell
irm https://raw.githubusercontent.com/BugMaker123/gourmet-master/main/install.ps1 | iex
```

**macOS / Linux (Bash)**:
```bash
curl -fsSL https://raw.githubusercontent.com/BugMaker123/gourmet-master/main/install.sh | bash
```

#### 方式 B：手动 Git Clone
```bash
# Windows
git clone https://github.com/BugMaker123/gourmet-master.git "$env:USERPROFILE\.gemini\config\skills\gourmet-master"

# macOS / Linux
git clone https://github.com/BugMaker123/gourmet-master.git ~/.gemini/config/skills/gourmet-master
```

---

### 2. 在 Codex / ChatGPT / OpenAI Custom GPTs 中使用

1. 打开 [OpenAI Custom GPTs Editor](https://chat.openai.com/gpts/editor) 或 Codex 项目控制台。
2. 在 **Instructions (系统提示词)** 中：直接复制粘贴本仓库中的 [`SKILL.md`](./SKILL.md) 全文。
3. 在 **Knowledge (知识库文件)** 中：上传 `references/` 目录下的 5 份 `.md` 文档。
4. 保存发布，即可获得兼具米其林星厨技艺与营养师认证的美食智能体！

---

### 3. 在 WorkBuddy / Dify / 微信智能体中配置

详细配置指南与高客单私厨咨询变现玩法，请查阅专属指南：
👉 [**WorkBuddy 部署与变现全攻略**](./WORKBUDDY_SETUP_GUIDE.md)

---

## 📄 许可证 (License)

本项目采用 [MIT 许可证](LICENSE)。欢迎个人研习厨艺、家庭烹饪、开店实操与商业化定制！
