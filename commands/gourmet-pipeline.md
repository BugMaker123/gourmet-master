---
name: gourmet-pipeline
description: "一键联网搜索任意菜品、组装精准克重与营养BOM成本、执行减脂/米其林/食安优化并生成交互式菜谱"
args:
  - name: dish
    description: "想吃的菜品名称（如：水煮牛肉、广西横县鱼生、惠灵顿牛排）"
    required: true
  - name: mode
    description: "优化模式（fat-loss 科学减脂 | michelin-upgrade 星厨升维 | safety-audit 食安审计）"
    required: false
---

# 美食全链路研发与优化命令 (`/gourmet-pipeline`)

针对用户指定的菜品 **{{dish}}**，执行动态联网搜集、精准克重组装与多目标优化闭环：

1. 运行 `python scripts/gourmet_engine.py auto-pipeline --query "{{dish}}" --optimize-mode {{mode}} --save-to-db`
2. 运行 `python scripts/gourmet_engine.py render-html --output examples/gourmet_interactive_portal.html`
3. 向用户完整展示【原教旨正宗精准配方（精确到g/ml、温度℃、时长）】与【优化改造后对比表（热量、蛋白质、碳水、脂肪、BOM成本）】。
