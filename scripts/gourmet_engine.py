#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gourmet Master CLI Engine (scripts/gourmet_engine.py)
Provides programmatic tools for AI agents:
1. search      - Filter structured recipes by category, keyword, max-kcal, or region.
2. recipe      - Fetch and dynamically scale a recipe to N servings (1 to 50 servings).
3. tdee-plan   - Compute Mifflin-St Jeor BMR/TDEE, 4-stage Carb Cycling macros, and generate a personalized meal plan.
4. render-html - Generate a standalone, offline-ready, interactive HTML Culinary Portal & Client Deliverable Deck.
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = SKILL_ROOT / "data" / "culinary_db.json"


def load_db():
    if not DB_PATH.exists():
        # Auto-generate if missing
        gen_script = SKILL_ROOT / "data" / "generate_db.py"
        if gen_script.exists():
            import subprocess
            subprocess.run([sys.executable, str(gen_script)], check=True)
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_search(args):
    db = load_db()
    results = []
    for r in db["recipes"]:
        if args.category and args.category != "all" and r["category"] != args.category:
            continue
        if args.max_kcal and r["macros_per_serving"]["kcal"] > args.max_kcal:
            continue
        if args.keyword:
            kw = args.keyword.lower()
            blob = json.dumps(r, ensure_ascii=False).lower()
            if kw not in blob:
                continue
        results.append({
            "id": r["id"],
            "name": r["name"],
            "category": r["category"],
            "subcategory": r["subcategory"],
            "region": r["region"],
            "kcal_per_serving": r["macros_per_serving"]["kcal"],
            "protein_g": r["macros_per_serving"]["protein_g"],
            "difficulty": r["difficulty"]
        })

    output = {
        "total_matched": len(results),
        "filters": {"category": args.category, "keyword": args.keyword, "max_kcal": args.max_kcal},
        "results": results[:args.limit]
    }
    write_output(output, args.output)


def cmd_recipe(args):
    db = load_db()
    target = None
    for r in db["recipes"]:
        if r["id"] == args.id or args.id in r["name"]:
            target = r
            break
    if not target:
        print(f"Error: Recipe '{args.id}' not found.", file=sys.stderr)
        sys.exit(1)

    scale_factor = args.servings / target["base_servings"]
    scaled = json.loads(json.dumps(target))
    scaled["requested_servings"] = args.servings
    scaled["scale_factor"] = round(scale_factor, 2)
    for ing in scaled["ingredients"]:
        ing["scaled_amount"] = round(ing["amount"] * scale_factor, 1)
    scaled["total_batch_macros"] = {
        k: round(v * args.servings, 1) for k, v in target["macros_per_serving"].items()
    }
    write_output(scaled, args.output)


def cmd_tdee_plan(args):
    db = load_db()
    # Mifflin-St Jeor Equation
    if args.gender.lower() in ["m", "male", "男"]:
        bmr = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age + 5
    else:
        bmr = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age - 161

    activity_map = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }
    factor = activity_map.get(args.activity, 1.375)
    tdee = round(bmr * factor)
    target_kcal = max(round(bmr + 50), tdee - args.deficit)

    w = args.weight_kg
    carb_cycle_macros = {
        "high_carb_day": {
            "label": "高碳充能日 (重训/下肢日)",
            "carbs_g": round(w * 3.2),
            "protein_g": round(w * 1.8),
            "fat_g": round(w * 0.45),
            "target_kcal": round(w * 3.2 * 4 + w * 1.8 * 4 + w * 0.45 * 9)
        },
        "moderate_carb_day": {
            "label": "中碳平衡日 (上肢/有氧日)",
            "carbs_g": round(w * 2.0),
            "protein_g": round(w * 2.0),
            "fat_g": round(w * 0.65),
            "target_kcal": round(w * 2.0 * 4 + w * 2.0 * 4 + w * 0.65 * 9)
        },
        "low_carb_day": {
            "label": "低碳燃脂日 (核心/快走日)",
            "carbs_g": round(w * 0.9),
            "protein_g": round(w * 2.2),
            "fat_g": round(w * 0.85),
            "target_kcal": round(w * 0.9 * 4 + w * 2.2 * 4 + w * 0.85 * 9)
        }
    }

    fitness_recipes = [r for r in db["recipes"] if r["category"] == "fitness"]
    weekly_schedule = [
        {"day": "周一 (中碳日)", "type": "moderate_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "中碳日" in r.get("carb_cycle_day", [])][:3]},
        {"day": "周二 (低碳日)", "type": "low_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "低碳日" in r.get("carb_cycle_day", [])][:3]},
        {"day": "周三 (高碳日)", "type": "high_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "高碳日" in r.get("carb_cycle_day", [])][:3]},
        {"day": "周四 (低碳日)", "type": "low_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "低碳日" in r.get("carb_cycle_day", [])][-3:]},
        {"day": "周五 (中碳日)", "type": "moderate_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "中碳日" in r.get("carb_cycle_day", [])][-3:]},
        {"day": "周六 (高碳日)", "type": "high_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "高碳日" in r.get("carb_cycle_day", [])][-3:]},
        {"day": "周日 (低碳日)", "type": "low_carb_day", "recommended_meals": [r["name"] for r in fitness_recipes if "无碳日" in r.get("carb_cycle_day", [])][:3]}
    ]

    plan = {
        "client_profile": {
            "gender": args.gender,
            "age": args.age,
            "height_cm": args.height_cm,
            "weight_kg": args.weight_kg,
            "activity": args.activity
        },
        "metabolic_metrics": {
            "bmr_kcal": round(bmr),
            "tdee_kcal": tdee,
            "daily_average_target_kcal": target_kcal,
            "daily_deficit_kcal": tdee - target_kcal
        },
        "carb_cycling_targets": carb_cycle_macros,
        "weekly_rotation_template": weekly_schedule
    }
    write_output(plan, args.output)


def cmd_render_html(args):
    db = load_db()
    recipes_json = json.dumps(db["recipes"], ensure_ascii=False)
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{args.title} - Gourmet Master 商业交互式交付系统</title>
<style>
  :root {{
    --bg: #0f172a; --card: #1e293b; --border: #334155; --text: #f8fafc;
    --muted: #94a3b8; --accent: #f59e0b; --green: #10b981; --red: #ef4444; --purple: #a855f7;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding-bottom: 60px; }}
  header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-bottom: 1px solid var(--border); padding: 28px 24px; text-align: center; }}
  header h1 {{ font-size: 26px; color: var(--accent); margin-bottom: 8px; }}
  header p {{ color: var(--muted); font-size: 14px; max-width: 760px; margin: 0 auto; }}
  .container {{ max-width: 1240px; margin: 24px auto; padding: 0 20px; }}
  .toolbar {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; background: var(--card); padding: 16px 20px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 24px; }}
  .tabs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  .tab-btn {{ background: #0f172a; color: var(--muted); border: 1px solid var(--border); padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; transition: all 0.2s; }}
  .tab-btn.active, .tab-btn:hover {{ background: var(--accent); color: #0f172a; border-color: var(--accent); }}
  .controls {{ display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }}
  .controls input, .controls select {{ background: #0f172a; color: var(--text); border: 1px solid var(--border); padding: 8px 12px; border-radius: 8px; font-size: 13px; }}
  .btn-print {{ background: var(--green); color: #0f172a; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; }}
  .tdee-box {{ background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(245,158,11,0.08)); border: 1px solid var(--green); border-radius: 12px; padding: 20px; margin-bottom: 24px; }}
  .tdee-box h2 {{ font-size: 18px; color: var(--green); margin-bottom: 12px; }}
  .tdee-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 14px; }}
  .tdee-result {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-top: 12px; }}
  .metric-card {{ background: rgba(15,23,42,0.8); padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border); }}
  .metric-card .val {{ font-size: 20px; font-weight: 700; color: var(--accent); }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(370px, 1fr)); gap: 20px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 20px; display: flex; flex-direction: column; gap: 12px; }}
  .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }}
  .card-title {{ font-size: 18px; font-weight: 700; color: #fff; }}
  .badge {{ font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: 600; white-space: nowrap; }}
  .badge-fit {{ background: rgba(16,185,129,0.2); color: #34d399; }}
  .badge-chn {{ background: rgba(245,158,11,0.2); color: #fbbf24; }}
  .badge-west {{ background: rgba(59,130,246,0.2); color: #60a5fa; }}
  .badge-cult {{ background: rgba(168,85,247,0.2); color: #c084fc; }}
  .macros {{ display: flex; gap: 10px; flex-wrap: wrap; background: #0f172a; padding: 8px 12px; border-radius: 8px; font-size: 12px; }}
  .macros span b {{ color: var(--accent); }}
  .science {{ font-size: 12.5px; background: rgba(245,158,11,0.08); border-left: 3px solid var(--accent); padding: 8px 10px; color: #fde68a; border-radius: 0 6px 6px 0; }}
  .safety {{ font-size: 12.5px; background: rgba(239,68,68,0.12); border-left: 3px solid var(--red); padding: 8px 10px; color: #fca5a5; border-radius: 0 6px 6px 0; }}
  .section-label {{ font-size: 12px; text-transform: uppercase; color: var(--muted); font-weight: 700; letter-spacing: 0.5px; margin-top: 4px; }}
  .ing-list {{ list-style: none; font-size: 13px; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; }}
  .ing-list li {{ border-bottom: 1px dashed rgba(255,255,255,0.06); padding: 3px 0; display: flex; justify-content: space-between; }}
  .ing-amt {{ color: var(--green); font-weight: 600; }}
  .steps-list {{ padding-left: 18px; font-size: 13px; color: #e2e8f0; display: flex; flex-direction: column; gap: 5px; }}
  .tip {{ font-size: 12px; color: var(--muted); font-style: italic; border-top: 1px solid var(--border); padding-top: 8px; }}
  @media print {{
    body {{ background: #fff; color: #000; }}
    .toolbar, .btn-print {{ display: none; }}
    .card {{ border: 1px solid #ccc; page-break-inside: avoid; background: #fff; color: #000; }}
    .card-title, .steps-list {{ color: #000; }}
  }}
</style>
</head>
<body>
<header>
  <h1>🍳 {args.title}</h1>
  <p>Gourmet Master 商业级交互式配方与营养精算交付系统 | 支持实时份量缩放、TDEE 碳水循环测算与一键导出 PDF</p>
</header>

<div class="container">
  <div class="tdee-box">
    <h2>🥗 个人精准减脂 TDEE & 28天碳水循环实时精算器 (WorkBuddy 客户交付工具)</h2>
    <div class="tdee-grid">
      <div><label style="font-size:12px;color:var(--muted)">性别</label><select id="t-gender" style="width:100%;padding:6px;background:#0f172a;color:#fff;border:1px solid var(--border);border-radius:6px"><option value="f">女性</option><option value="m">男性</option></select></div>
      <div><label style="font-size:12px;color:var(--muted)">年龄 (岁)</label><input type="number" id="t-age" value="28" style="width:100%;padding:6px;background:#0f172a;color:#fff;border:1px solid var(--border);border-radius:6px"></div>
      <div><label style="font-size:12px;color:var(--muted)">身高 (cm)</label><input type="number" id="t-height" value="165" style="width:100%;padding:6px;background:#0f172a;color:#fff;border:1px solid var(--border);border-radius:6px"></div>
      <div><label style="font-size:12px;color:var(--muted)">当前体重 (kg)</label><input type="number" id="t-weight" value="62" style="width:100%;padding:6px;background:#0f172a;color:#fff;border:1px solid var(--border);border-radius:6px"></div>
      <div><label style="font-size:12px;color:var(--muted)">日常活动量</label><select id="t-act" style="width:100%;padding:6px;background:#0f172a;color:#fff;border:1px solid var(--border);border-radius:6px"><option value="1.2">久坐办公 (1.2)</option><option value="1.375" selected>轻度运动 1-3次/周 (1.375)</option><option value="1.55">中度训练 3-5次/周 (1.55)</option><option value="1.725">高强训练 6-7次/周 (1.725)</option></select></div>
    </div>
    <div class="tdee-result" id="tdee-out"></div>
  </div>

  <div class="toolbar">
    <div class="tabs">
      <button class="tab-btn active" onclick="setCat('all', this)">全部配方 ({len(db['recipes'])})</button>
      <button class="tab-btn" onclick="setCat('fitness', this)">🥗 科学减脂餐</button>
      <button class="tab-btn" onclick="setCat('chinese', this)">🥢 中华八大菜系</button>
      <button class="tab-btn" onclick="setCat('western', this)">🥩 正统西餐米其林</button>
      <button class="tab-btn" onclick="setCat('cult', this)">🦪 区域邪教美食</button>
    </div>
    <div class="controls">
      <input type="text" id="search-input" placeholder="搜索食材/菜名/地域/工艺..." oninput="renderCards()">
      <label style="font-size:13px;color:var(--accent);font-weight:700;">用餐人数/份数缩放: <span id="serv-val">1</span> 份</label>
      <input type="range" id="serv-slider" min="1" max="20" value="1" oninput="document.getElementById('serv-val').innerText=this.value; renderCards()">
      <button class="btn-print" onclick="window.print()">🖨️ 打印 / 导出客户 PDF</button>
    </div>
  </div>

  <div class="grid" id="recipe-grid"></div>
</div>

<script>
const RECIPES = {recipes_json};
let currentCat = 'all';

function calcTDEE() {{
  const g = document.getElementById('t-gender').value;
  const age = parseFloat(document.getElementById('t-age').value) || 28;
  const h = parseFloat(document.getElementById('t-height').value) || 165;
  const w = parseFloat(document.getElementById('t-weight').value) || 60;
  const act = parseFloat(document.getElementById('t-act').value) || 1.375;
  const bmr = Math.round(g === 'm' ? (10*w + 6.25*h - 5*age + 5) : (10*w + 6.25*h - 5*age - 161));
  const tdee = Math.round(bmr * act);
  const target = Math.max(bmr + 50, tdee - 400);
  document.getElementById('tdee-out').innerHTML = `
    <div class="metric-card"><div>基础代谢 (BMR) & 总消耗 (TDEE)</div><div class="val">${{bmr}} / ${{tdee}} kcal</div><div style="font-size:12px;color:var(--muted)">推荐减脂摄入: <b>${{target}} kcal/天</b></div></div>
    <div class="metric-card"><div>🔥 高碳充能日 (重训日)</div><div class="val">碳 ${{Math.round(w*3.0)}}g | 蛋 ${{Math.round(w*1.8)}}g | 脂 ${{Math.round(w*0.45)}}g</div><div style="font-size:12px;color:var(--muted)">拉升瘦素防止代谢停滞</div></div>
    <div class="metric-card"><div>⚖️ 中碳平衡日 (常规日)</div><div class="val">碳 ${{Math.round(w*2.0)}}g | 蛋 ${{Math.round(w*2.0)}}g | 脂 ${{Math.round(w*0.65)}}g</div><div style="font-size:12px;color:var(--muted)">饱腹感强，稳定掉秤</div></div>
    <div class="metric-card"><div>⚡ 低碳燃脂日 (刷脂日)</div><div class="val">碳 ${{Math.round(w*0.8)}}g | 蛋 ${{Math.round(w*2.2)}}g | 脂 ${{Math.round(w*0.85)}}g</div><div style="font-size:12px;color:var(--muted)">低胰岛素高效分解脂肪</div></div>
  `;
}}

['t-gender','t-age','t-height','t-weight','t-act'].forEach(id => document.getElementById(id).addEventListener('input', calcTDEE));
calcTDEE();

function setCat(cat, btn) {{
  currentCat = cat;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderCards();
}}

function renderCards() {{
  const kw = document.getElementById('search-input').value.trim().toLowerCase();
  const targetServings = parseInt(document.getElementById('serv-slider').value) || 1;
  const grid = document.getElementById('recipe-grid');
  const badgeMap = {{ fitness: ['badge-fit','🥗 减脂轻食'], chinese: ['badge-chn','🥢 中华名菜'], western: ['badge-west','🥩 正统西餐'], cult: ['badge-cult','🦪 区域邪教'] }};

  const filtered = RECIPES.filter(r => {{
    if (currentCat !== 'all' && r.category !== currentCat) return false;
    if (kw && !JSON.stringify(r).toLowerCase().includes(kw)) return false;
    return true;
  }});

  grid.innerHTML = filtered.map(r => {{
    const scale = targetServings / r.base_servings;
    const [bCls, bTxt] = badgeMap[r.category] || ['badge-fit', r.category];
    const m = r.macros_per_serving;
    const ings = r.ingredients.map(i => `<li><span>${{i.item}}</span><span class="ing-amt">${{Math.round(i.amount * scale * 10)/10}} ${{i.unit}}</span></li>`).join('');
    const steps = r.steps.map(s => `<li>${{s}}</li>`).join('');
    const safetyHtml = r.safety_redline ? `<div class="safety">⚠️ <b>安全红线：</b>${{r.safety_redline}}</div>` : '';
    return `
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">${{r.name}}</div>
            <div style="font-size:12px;color:var(--muted)">📍 ${{r.region}} · ${{r.subcategory}} · 难度: ${{r.difficulty}} · ⏱️ ${{r.prep_time_min+r.cook_time_min}}分钟</div>
          </div>
          <span class="badge ${{bCls}}">${{bTxt}}</span>
        </div>
        <div class="macros">
          <span>🔥 单份热量: <b>${{m.kcal}} kcal</b></span>
          <span>💪 蛋白: <b>${{m.protein_g}}g</b></span>
          <span>🍚 碳水: <b>${{m.carbs_g}}g</b></span>
          <span>🥑 脂肪: <b>${{m.fat_g}}g</b></span>
        </div>
        <div class="science">🔬 <b>分子烹饪原理：</b>${{r.science_principle}}</div>
        ${{safetyHtml}}
        <div class="section-label">⚖️ 精准物料配比 (已按 ${{targetServings}} 人份自动换算)</div>
        <ul class="ing-list">${{ings}}</ul>
        <div class="section-label">👨‍🍳 标准出品 SOP</div>
        <ol class="steps-list">${{steps}}</ol>
        <div class="tip">💡 主厨贴士：${{r.pro_tips}}</div>
      </div>
    `;
  }}).join('');
}}
renderCards();
</script>
</body>
</html>"""
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully rendered interactive HTML deliverable: {out_path.resolve()}")


def write_output(data, output_path):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output_path:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully wrote result to {p.resolve()}")
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(description="Gourmet Master Culinary & Nutrition CLI Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search structured recipes")
    p_search.add_argument("--category", choices=["all", "fitness", "chinese", "western", "cult"], default="all")
    p_search.add_argument("--keyword", type=str, default=None)
    p_search.add_argument("--max-kcal", type=int, default=None)
    p_search.add_argument("--limit", type=int, default=50)
    p_search.add_argument("--output", type=str, default=None)
    p_search.set_defaults(func=cmd_search)

    # recipe
    p_rec = sub.add_parser("recipe", help="Get and scale a specific recipe by ID or name")
    p_rec.add_argument("--id", type=str, required=True, help="Recipe ID (e.g. fit_01, cult_02) or dish name")
    p_rec.add_argument("--servings", type=int, default=1, help="Number of servings to scale ingredients to")
    p_rec.add_argument("--output", type=str, default=None)
    p_rec.set_defaults(func=cmd_recipe)

    # tdee-plan
    p_tdee = sub.add_parser("tdee-plan", help="Calculate BMR/TDEE and 28-day carb cycling plan")
    p_tdee.add_argument("--gender", type=str, required=True, help="m/f or 男/女")
    p_tdee.add_argument("--age", type=int, required=True)
    p_tdee.add_argument("--height-cm", type=float, required=True)
    p_tdee.add_argument("--weight-kg", type=float, required=True)
    p_tdee.add_argument("--activity", choices=["sedentary", "light", "moderate", "active"], default="light")
    p_tdee.add_argument("--deficit", type=int, default=400)
    p_tdee.add_argument("--output", type=str, default=None)
    p_tdee.set_defaults(func=cmd_tdee_plan)

    # render-html
    p_html = sub.add_parser("render-html", help="Render standalone interactive HTML cookbook & TDEE portal")
    p_html.add_argument("--title", type=str, default="美食大师：科学减脂·中西名菜·区域邪教料理全书")
    p_html.add_argument("--output", type=str, required=True, help="Output HTML file path")
    p_html.set_defaults(func=cmd_render_html)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
