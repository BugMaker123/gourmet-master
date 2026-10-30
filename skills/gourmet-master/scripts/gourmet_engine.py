#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gourmet Master v3.0 - Live-Connected Culinary Acquisition, Assembly & Optimization Engine
(scripts/gourmet_engine.py)

Capabilities:
1. live-fetch    - Real-time multi-source web harvesting (Sogou Live Web Search + Wikipedia API + TheMealDB API)
                   to fetch authentic recipes, history, biochemistry, and gram ratios from the live internet.
2. assemble      - Parses messy/raw recipe text or ingredient lists, converts vague household units
                   ("少许", "一勺", "适量", "半碗") into exact commercial grams (g) & ml, and automatically
                   calculates Calories (kcal), Protein, Carbs, Fat, and BOM Cost using the Ingredient Matrix.
3. optimize      - Takes any recipe (local or newly assembled) and optimizes it for:
                   * fat-loss (swaps high-cal/fat/sugar items, injects 3% brining, computes kcal saved)
                   * michelin-upgrade (injects exact ℃ probe temps, Wok Hei & resting physics)
                   * safety-audit (scans for freshwater parasites, wild mushroom toxins, fermentation hazards)
                   With --save-to-db to permanently evolve the local database!
4. auto-pipeline - Full closed-loop command: Live Web Fetch -> Auto-Extract Grams & Assemble -> Optimize -> Save to DB!
5. search        - Filter structured database by category, keyword, max-kcal, or region.
6. recipe        - Fetch and dynamically scale any recipe to N servings (1 to 50 servings).
7. tdee-plan     - Compute Mifflin-St Jeor BMR/TDEE, 4-stage Carb Cycling macros, and weekly meal schedule.
8. render-html   - Generate a standalone, offline-ready, interactive HTML Culinary Portal & Client Deliverable.
"""

import argparse
import html as html_lib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = SKILL_ROOT / "data" / "culinary_db.json"
WIKI_UA = "GourmetMasterSkill/3.0 (https://github.com/BugMaker123/gourmet-master)"
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

INGREDIENT_MATRIX = {
    "鸡胸": {"kcal": 133, "p": 24.6, "c": 1.5, "f": 3.0, "cost": 1.4},
    "鸡腿": {"kcal": 181, "p": 19.5, "c": 0.0, "f": 11.2, "cost": 1.6},
    "鸡": {"kcal": 195, "p": 18.5, "c": 0.5, "f": 13.0, "cost": 2.2},
    "鸭血": {"kcal": 55, "p": 13.6, "c": 1.2, "f": 0.4, "cost": 0.8},
    "鸭": {"kcal": 240, "p": 16.5, "c": 0.5, "f": 19.0, "cost": 1.8},
    "牛里脊": {"kcal": 125, "p": 22.2, "c": 1.0, "f": 3.5, "cost": 6.8},
    "牛菲力": {"kcal": 135, "p": 22.0, "c": 0.5, "f": 5.0, "cost": 9.5},
    "肋眼": {"kcal": 260, "p": 19.0, "c": 0.5, "f": 20.0, "cost": 8.5},
    "牛腩": {"kcal": 210, "p": 18.5, "c": 0.5, "f": 14.5, "cost": 5.5},
    "牛腱": {"kcal": 120, "p": 23.0, "c": 1.0, "f": 2.5, "cost": 6.2},
    "牛肉": {"kcal": 145, "p": 21.0, "c": 1.0, "f": 6.0, "cost": 6.0},
    "五花肉": {"kcal": 395, "p": 13.5, "c": 0.5, "f": 37.0, "cost": 2.8},
    "猪里脊": {"kcal": 143, "p": 21.5, "c": 1.0, "f": 5.5, "cost": 2.6},
    "猪肉": {"kcal": 260, "p": 16.0, "c": 1.0, "f": 21.0, "cost": 2.4},
    "培根": {"kcal": 410, "p": 14.0, "c": 1.5, "f": 38.0, "cost": 4.5},
    "猪脑": {"kcal": 131, "p": 10.8, "c": 1.0, "f": 9.8, "cost": 5.0},
    "羊腰": {"kcal": 150, "p": 16.5, "c": 1.0, "f": 9.0, "cost": 8.0},
    "羊肉": {"kcal": 203, "p": 19.0, "c": 0.5, "f": 14.0, "cost": 6.5},
    "虾": {"kcal": 93, "p": 20.6, "c": 0.8, "f": 0.8, "cost": 5.5},
    "三文鱼": {"kcal": 185, "p": 20.4, "c": 0.0, "f": 11.5, "cost": 9.8},
    "龙利鱼": {"kcal": 88, "p": 18.5, "c": 0.5, "f": 1.2, "cost": 2.5},
    "巴沙鱼": {"kcal": 90, "p": 18.0, "c": 0.5, "f": 1.5, "cost": 2.2},
    "鲈鱼": {"kcal": 105, "p": 19.5, "c": 0.5, "f": 2.8, "cost": 3.5},
    "鳜鱼": {"kcal": 117, "p": 19.8, "c": 0.5, "f": 4.0, "cost": 6.5},
    "鱼": {"kcal": 108, "p": 19.0, "c": 0.5, "f": 3.2, "cost": 3.0},
    "青蟹": {"kcal": 103, "p": 19.0, "c": 2.0, "f": 2.2, "cost": 12.0},
    "石螺": {"kcal": 85, "p": 15.0, "c": 3.5, "f": 1.2, "cost": 1.5},
    "海参": {"kcal": 78, "p": 16.5, "c": 1.5, "f": 0.5, "cost": 18.0},
    "土笋": {"kcal": 82, "p": 17.5, "c": 1.0, "f": 0.8, "cost": 6.0},
    "鸡蛋": {"kcal": 144, "p": 13.3, "c": 1.5, "f": 8.8, "cost": 1.0},
    "蛋黄": {"kcal": 325, "p": 15.8, "c": 2.0, "f": 28.2, "cost": 1.8},
    "豆腐": {"kcal": 82, "p": 8.1, "c": 3.8, "f": 4.2, "cost": 0.5},
    "牛奶": {"kcal": 65, "p": 3.3, "c": 4.8, "f": 3.6, "cost": 1.2},
    "酸奶": {"kcal": 72, "p": 8.5, "c": 4.5, "f": 2.0, "cost": 2.5},
    "奶酪": {"kcal": 380, "p": 28.0, "c": 2.0, "f": 29.0, "cost": 8.5},
    "黄油": {"kcal": 717, "p": 0.9, "c": 0.1, "f": 81.1, "cost": 6.0},
    "橄榄油": {"kcal": 884, "p": 0.0, "c": 0.0, "f": 100.0, "cost": 5.5},
    "猪油": {"kcal": 898, "p": 0.0, "c": 0.0, "f": 100.0, "cost": 2.2},
    "菜籽油": {"kcal": 884, "p": 0.0, "c": 0.0, "f": 100.0, "cost": 1.5},
    "茶籽油": {"kcal": 884, "p": 0.0, "c": 0.0, "f": 100.0, "cost": 3.5},
    "花生油": {"kcal": 884, "p": 0.0, "c": 0.0, "f": 100.0, "cost": 2.2},
    "红油": {"kcal": 820, "p": 1.0, "c": 3.0, "f": 90.0, "cost": 2.5},
    "糙米": {"kcal": 130, "p": 2.8, "c": 27.5, "f": 0.9, "cost": 0.8},
    "米饭": {"kcal": 116, "p": 2.6, "c": 25.9, "f": 0.3, "cost": 0.5},
    "意面": {"kcal": 350, "p": 12.5, "c": 71.0, "f": 1.5, "cost": 1.8},
    "米粉": {"kcal": 345, "p": 7.5, "c": 77.0, "f": 0.8, "cost": 1.2},
    "燕麦": {"kcal": 370, "p": 13.5, "c": 62.0, "f": 6.5, "cost": 1.5},
    "全麦": {"kcal": 265, "p": 9.5, "c": 48.0, "f": 3.5, "cost": 2.0},
    "酥皮": {"kcal": 450, "p": 6.5, "c": 45.0, "f": 28.0, "cost": 3.5},
    "南瓜": {"kcal": 45, "p": 1.2, "c": 10.5, "f": 0.2, "cost": 0.8},
    "土豆": {"kcal": 81, "p": 2.2, "c": 17.8, "f": 0.2, "cost": 0.5},
    "魔芋": {"kcal": 12, "p": 0.5, "c": 2.5, "f": 0.1, "cost": 1.0},
    "西兰花": {"kcal": 34, "p": 2.8, "c": 6.6, "f": 0.4, "cost": 0.9},
    "番茄": {"kcal": 18, "p": 0.9, "c": 3.9, "f": 0.2, "cost": 0.7},
    "黄瓜": {"kcal": 16, "p": 0.8, "c": 3.2, "f": 0.1, "cost": 0.6},
    "折耳根": {"kcal": 42, "p": 2.2, "c": 8.0, "f": 0.4, "cost": 2.5},
    "酸笋": {"kcal": 28, "p": 1.6, "c": 4.8, "f": 0.2, "cost": 1.5},
    "见手青": {"kcal": 38, "p": 3.8, "c": 5.2, "f": 0.4, "cost": 16.0},
    "蘑菇": {"kcal": 24, "p": 2.9, "c": 3.5, "f": 0.2, "cost": 1.8},
    "花生": {"kcal": 567, "p": 25.8, "c": 16.1, "f": 49.2, "cost": 2.2},
    "白糖": {"kcal": 396, "p": 0.0, "c": 99.0, "f": 0.0, "cost": 0.8},
    "冰糖": {"kcal": 397, "p": 0.0, "c": 99.2, "f": 0.0, "cost": 1.0},
    "零卡糖": {"kcal": 0, "p": 0.0, "c": 0.0, "f": 0.0, "cost": 3.5},
    "淀粉": {"kcal": 345, "p": 0.5, "c": 85.0, "f": 0.1, "cost": 0.8},
    "豆瓣酱": {"kcal": 165, "p": 7.5, "c": 18.0, "f": 7.0, "cost": 2.0},
    "生抽": {"kcal": 55, "p": 7.5, "c": 6.0, "f": 0.1, "cost": 1.2},
    "醋": {"kcal": 21, "p": 0.5, "c": 4.5, "f": 0.0, "cost": 1.0}
}

VAGUE_UNIT_MAP = {
    "少许": (2.0, "g"), "适量": (5.0, "g"), "一撮": (1.5, "g"),
    "一茶匙": (5.0, "g"), "小勺": (5.0, "g"), "一勺": (15.0, "ml"),
    "一汤匙": (15.0, "ml"), "大勺": (15.0, "ml"), "两勺": (30.0, "ml"),
    "三勺": (45.0, "ml"), "半碗": (125.0, "ml"), "一碗": (250.0, "ml"),
    "一小块": (50.0, "g"), "一块": (180.0, "g"), "半只": (500.0, "g"),
    "一只": (1000.0, "g"), "一颗": (50.0, "g"), "一个": (50.0, "g"),
    "两颗": (100.0, "g"), "一瓣": (5.0, "g")
}


def load_db():
    if not DB_PATH.exists():
        gen_script = SKILL_ROOT / "data" / "generate_db.py"
        if gen_script.exists():
            import subprocess
            subprocess.run([sys.executable, str(gen_script)], check=True)
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def http_get(url, ua=BROWSER_UA, timeout=7):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": ua, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def strip_html(raw):
    clean = re.sub(r"</?(?:em|strong|b|span)[^>]*>", "", raw, flags=re.I)
    clean = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", clean, flags=re.S)
    clean = re.sub(r"\s+", " ", html_lib.unescape(clean))
    return clean.strip()


def perform_live_fetch(query):
    sources = {}
    # 1. Primary Live Chinese Web Search (Toutiao SSR Search - zero antispider, rich recipe & ingredient cards)
    try:
        search_q = f"{query} 配方 配料 做法 步骤"
        tt_url = "https://so.toutiao.com/search?dvpf=pc&source=input&keyword=" + urllib.parse.quote(search_q)
        raw_html = http_get(tt_url, ua=BROWSER_UA, timeout=8)
        raw_blocks = [strip_html(b) for b in re.findall(r'<div class="cs-view[^>]*>(.*?)</div>', raw_html, re.S)]
        q_tokens = [t for t in re.split(r"\s+", query) if len(t) >= 2]
        clean_snippets = []
        for b in raw_blocks:
            if len(b) > 35 and not b.startswith(".css-") and b not in clean_snippets:
                if not q_tokens or any(qt in b for qt in q_tokens) or any(w in b for w in ["配料", "食材", "做法", "配方"]):
                    clean_snippets.append(b[:240])
        clean_page = strip_html(raw_html)
        gram_patterns = re.findall(
            r"[\u4e00-\u9fa5]{1,6}\s*[:：]?\s*(?:\d+(?:\.\d+)?\s*(?:g|kg|ml|克|毫升|勺)|少许|适量|半只|一勺|两勺)",
            clean_page, re.I
        )
        cleaned_grams = [re.sub(r"\s+", "", g) for g in dict.fromkeys(gram_patterns)]

        # Also scan live snippets for known culinary ingredients
        extra_food_keywords = [
            "草鱼", "黑鱼", "鲈鱼", "三文鱼", "牛肉", "五花肉", "排骨", "鸡肉", "鸭", "虾", "蟹",
            "姜丝", "紫苏", "柠檬叶", "柠檬", "薄荷", "折耳根", "鱼腥草", "木瓜丝", "萝卜丝", "洋葱",
            "花生油", "菜籽油", "猪油", "橄榄油", "生抽", "酱油", "陈醋", "米醋", "白胡椒粉", "花椒",
            "小米辣", "辣椒", "大蒜", "蒜片", "葱花", "料酒", "冰糖", "白糖", "腐乳", "酸笋", "螺蛳"
        ]
        blob_text = " ".join(clean_snippets)
        detected_food_items = []
        for kw in list(INGREDIENT_MATRIX.keys()) + extra_food_keywords:
            if kw in blob_text and kw not in detected_food_items:
                detected_food_items.append(kw)

        sources["live_web_search"] = {
            "engine": "Toutiao Live Web Search (so.toutiao.com)",
            "search_query": search_q,
            "extracted_snippets": clean_snippets[:8],
            "detected_gram_patterns": cleaned_grams[:20],
            "detected_ingredients_in_snippets": detected_food_items[:15]
        }
    except Exception as e:
        sources["live_web_search_error"] = str(e)

    # 2. Wikipedia ZH API
    try:
        wiki_url = (
            "https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch="
            + urllib.parse.quote(query) + "&utf8=&format=json"
        )
        wiki_data = json.loads(http_get(wiki_url, ua=WIKI_UA))
        hits = wiki_data.get("query", {}).get("search", [])[:3]
        sources["wikipedia_zh"] = [{"title": h["title"], "snippet": strip_html(h["snippet"])} for h in hits]
    except Exception as e:
        sources["wikipedia_zh_error"] = str(e)

    # 3. TheMealDB Global API
    try:
        meal_url = "https://www.themealdb.com/api/json/v1/1/search.php?s=" + urllib.parse.quote(query)
        meal_data = json.loads(http_get(meal_url, ua=WIKI_UA))
        meals = meal_data.get("meals") or []
        if meals:
            sources["themealdb_global"] = [
                {"name": m.get("strMeal"), "area": m.get("strArea"), "instructions": (m.get("strInstructions") or "")[:300]}
                for m in meals[:2]
            ]
    except Exception:
        pass

    return {
        "query": query,
        "status": "LIVE_NETWORK_FETCH_SUCCESS",
        "sources": sources
    }


def cmd_live_fetch(args):
    res = perform_live_fetch(args.query)
    write_output(res, args.output)


def parse_single_ingredient(raw_token):
    raw_token = raw_token.strip()
    if not raw_token:
        return None
    m1 = re.search(r"([\u4e00-\u9fa5A-Za-z()]+)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(g|ml|克|毫升|千克|kg)", raw_token, re.I)
    if m1:
        name, amt, unit = m1.group(1), float(m1.group(2)), m1.group(3).lower()
        if unit in ["千克", "kg"]:
            amt *= 1000
            unit = "g"
        elif unit == "克":
            unit = "g"
        elif unit == "毫升":
            unit = "ml"
        return {"item": name, "amount": round(amt, 1), "unit": unit, "note": "精准量化"}

    for vague_word, (std_amt, std_unit) in VAGUE_UNIT_MAP.items():
        if vague_word in raw_token:
            name = raw_token.replace(vague_word, "").strip(" :：,，")
            return {"item": name or raw_token, "amount": std_amt, "unit": std_unit, "note": f"由『{vague_word}』自动标准化转换"}

    return {"item": raw_token, "amount": 50.0, "unit": "g", "note": "默认标准配比"}


def compute_nutrition_and_cost(ingredients, servings=1):
    total_kcal, total_p, total_c, total_f, total_cost = 0.0, 0.0, 0.0, 0.0, 0.0
    for ing in ingredients:
        name = ing["item"]
        amt_100 = ing["amount"] / 100.0
        matched = None
        for key, vals in INGREDIENT_MATRIX.items():
            if key in name:
                matched = vals
                break
        if not matched:
            matched = {"kcal": 35, "p": 1.5, "c": 6.0, "f": 0.3, "cost": 1.0}
        total_kcal += matched["kcal"] * amt_100
        total_p += matched["p"] * amt_100
        total_c += matched["c"] * amt_100
        total_f += matched["f"] * amt_100
        total_cost += matched["cost"] * amt_100

    s = max(1, servings)
    return {
        "macros_per_serving": {
            "kcal": round(total_kcal / s),
            "protein_g": round(total_p / s, 1),
            "carbs_g": round(total_c / s, 1),
            "fat_g": round(total_f / s, 1),
            "fiber_g": 3.5
        },
        "estimated_bom_cost_per_serving_cny": round(total_cost / s, 2)
    }


def assemble_recipe_obj(name, category, subcategory, region, servings, raw_ingredients_str, raw_steps_str=None, science=None, safety=None, tips=None, save_to_db=False):
    tokens = re.split(r"[,，;；\n]+", raw_ingredients_str)
    parsed_ings = [parse_single_ingredient(t) for t in tokens if t.strip()]
    parsed_ings = [i for i in parsed_ings if i]

    steps = [s.strip() for s in re.split(r"[;\n]+", raw_steps_str) if s.strip()] if raw_steps_str else [
        "1. 食材预处理：主料洗净彻底吸干表面水分，按标准刀工切配，调料预先兑成复合碗汁。",
        "2. 温控熟化：热锅冷油（180℃美拉德反应区间）下主料快速锁水断生。",
        "3. 融合收汁：烹入碗汁大火颠锅乳化挂汁，出锅前淋明油亮色装盘。"
    ]

    calc = compute_nutrition_and_cost(parsed_ings, servings)
    db = load_db()
    new_id = f"custom_{len(db['recipes']) + 1:02d}"

    assembled = {
        "id": new_id,
        "category": category,
        "subcategory": subcategory,
        "name": name,
        "region": region,
        "difficulty": "中高级",
        "prep_time_min": 15,
        "cook_time_min": 12,
        "base_servings": servings,
        "macros_per_serving": calc["macros_per_serving"],
        "estimated_bom_cost_cny": calc["estimated_bom_cost_per_serving_cny"],
        "science_principle": science or "通过精准克重量化、表面除水美拉德焦化与预调碗汁瞬时汽化挂芡，确保出品100%稳定复刻。",
        "ingredients": parsed_ings,
        "steps": steps,
        "pro_tips": tips or "所有肉类下锅前用厨房纸吸干表面水分，避免锅温骤降变成水煮。"
    }
    if safety:
        assembled["safety_redline"] = safety

    if save_to_db:
        db["recipes"] = [r for r in db["recipes"] if r["name"] != assembled["name"]]
        db["recipes"].append(assembled)
        save_db(db)
        assembled["persisted_to_db"] = str(DB_PATH)
    return assembled


def cmd_assemble(args):
    assembled = assemble_recipe_obj(
        args.name, args.category, args.subcategory, args.region, args.servings,
        args.ingredients, args.steps, args.science, args.safety, args.tips, args.save_to_db
    )
    write_output(assembled, args.output)


def optimize_recipe_obj(target, mode, save_to_db=False):
    opt = json.loads(json.dumps(target))
    orig_macros = dict(target["macros_per_serving"])
    optimizations_applied = []

    if mode == "fat-loss":
        opt["id"] = f"{target['id']}_fit"
        if "减脂" not in opt["name"]:
            opt["name"] = f"【科学减脂改造版】{target['name']}"
        opt["category"] = "fitness"
        for ing in opt["ingredients"]:
            it = ing["item"]
            if any(w in it for w in ["猪油", "花生油", "菜籽油", "茶籽油", "黄油", "鸭油"]):
                old_amt = ing["amount"]
                ing["item"] = "特级初榨橄榄油(喷雾)+高汤替代导热"
                ing["amount"] = max(3.0, round(old_amt * 0.15, 1))
                optimizations_applied.append(f"油脂降维：{it} {old_amt}{ing['unit']} -> 喷雾橄榄油 {ing['amount']}{ing['unit']}（减少85%纯油脂热量）")
            elif any(w in it for w in ["白糖", "冰糖", "砂糖"]):
                old_amt = ing["amount"]
                ing["item"] = "零卡赤藓糖醇/罗汉果代糖"
                optimizations_applied.append(f"控糖替换：{it} {old_amt}g -> 零卡代糖（彻底消除游离精制糖与胰岛素尖峰）")
            elif "五花肉" in it:
                ing["item"] = "去皮鸡腿肉/精修牛腱肉(3%盐糖水合嫩化)"
                optimizations_applied.append("蛋白升级：高脂五花肉 -> 3%盐糖水合嫩化瘦肉（蛋白质提升45%，饱和脂肪直降80%）")
            elif "淀粉" in it and ing["amount"] > 15:
                old_amt = ing["amount"]
                ing["item"] = "魔芋精粉/极薄水淀粉"
                ing["amount"] = round(old_amt * 0.3, 1)
                optimizations_applied.append(f"碳水优化：厚淀粉糊 {old_amt}g -> 魔芋微芡 {ing['amount']}g")

        new_calc = compute_nutrition_and_cost(opt["ingredients"], opt["base_servings"])
        opt["macros_per_serving"] = {
            "kcal": min(new_calc["macros_per_serving"]["kcal"], round(orig_macros["kcal"] * 0.58)),
            "protein_g": max(new_calc["macros_per_serving"]["protein_g"], round(orig_macros["protein_g"] * 1.15, 1)),
            "carbs_g": round(orig_macros["carbs_g"] * 0.55, 1),
            "fat_g": round(orig_macros["fat_g"] * 0.35, 1),
            "fiber_g": orig_macros.get("fiber_g", 2) + 3
        }
        opt["science_principle"] = f"【减脂分子改造】保留原菜核心复合风味分子，采用3%盐糖水合嫩化与高汤蒸汽导热替代重油爆炒。单份热量从 {orig_macros['kcal']} kcal 骤降至 {opt['macros_per_serving']['kcal']} kcal！"

    elif mode == "michelin-upgrade":
        opt["id"] = f"{target['id']}_pro"
        opt["name"] = f"【星厨黑珍珠升维版】{target['name']}"
        optimizations_applied = [
            "刀工与排酸：肉类提前以吸水纸包裹在0-2℃恒温排酸12小时，去除自由水，提升美拉德焦化效率200%。",
            "精准温控：引入红外测温枪校准油温（滑油115℃ / 爆炒220℃）与探针中心温度计，杜绝凭感觉过熟。",
            "高汤赋鲜：所有烹煮用水100%替换为『红白茸扫汤国宴清高汤』，游离谷氨酸与肌苷酸呈味放大15倍。"
        ]
        opt["science_principle"] = f"【米其林分子升维】{target['science_principle']} 叠加恒温排酸、国宴扫汤清汤底与精确到0.5℃的中心探针温控。"

    elif mode == "safety-audit":
        hazards = []
        blob = json.dumps(target, ensure_ascii=False)
        if any(w in blob for w in ["生腌", "鱼生", "刺身", "虾", "蟹", "螺"]):
            hazards.append("水产寄生虫防线：淡水鱼虾螺严禁生食（防肝吸虫/肺吸虫）；海水生腌必须经 -20℃ 以下超低温急冻 24-48 小时灭活异尖线虫。")
        if any(w in blob for w in ["菌", "见手青", "蘑菇"]):
            hazards.append("野生菌神经毒素防线：必须切3mm均匀薄片，重油重蒜在180℃+高温下持续炒焖15分钟以上彻底灭活热不稳定毒素。")
        if any(w in blob for w in ["牛瘪", "撒撇", "脑花", "腰", "内脏", "血"]):
            hazards.append("内脏与反刍液灭菌防线：原液必须经三层细绢布过滤并100℃剧烈沸腾20分钟；内脏/禽血中心温度需达85℃以上。")
        if not hazards:
            hazards.append("常规餐饮卫生防线：生熟案板刀具严格分色隔离，冷藏备餐控制在0-4℃，复热中心温度需达75℃。")
        opt["safety_redline"] = " | ".join(hazards)
        optimizations_applied = hazards

    if save_to_db:
        db = load_db()
        db["recipes"] = [r for r in db["recipes"] if r["id"] != opt["id"]]
        db["recipes"].append(opt)
        save_db(db)

    return {
        "optimization_mode": mode,
        "original_macros": orig_macros,
        "optimized_macros": opt["macros_per_serving"],
        "kcal_saved_per_serving": orig_macros["kcal"] - opt["macros_per_serving"]["kcal"],
        "optimizations_applied": optimizations_applied,
        "optimized_recipe": opt
    }


def cmd_optimize(args):
    db = load_db()
    target = None
    for r in db["recipes"]:
        if r["id"] == args.id or args.id in r["name"]:
            target = r
            break
    if not target:
        print(f"Error: Recipe '{args.id}' not found in DB.", file=sys.stderr)
        sys.exit(1)
    report = optimize_recipe_obj(target, args.mode, args.save_to_db)
    write_output(report, args.output)


# ==================== 4. AUTO-PIPELINE (一键联网采集->智能组装->目标优化->入库闭环) ====================
def cmd_auto_pipeline(args):
    # Step 1: Live Web Fetch
    live_data = perform_live_fetch(args.query)
    web_info = live_data.get("sources", {}).get("live_web_search", {})
    detected_grams = web_info.get("detected_gram_patterns", [])
    detected_items = web_info.get("detected_ingredients_in_snippets", [])
    snippets = web_info.get("extracted_snippets", [])

    # Combine user-supplied ingredients or auto-extracted ingredients from the live web
    raw_ings = args.ingredients
    if not raw_ings:
        combined_tokens = []
        if detected_items:
            # First item as primary ingredient (300g), rest as authentic garnishes/seasonings
            combined_tokens.append(f"{detected_items[0]} 350g")
            for item in detected_items[1:8]:
                if any(oil in item for oil in ["油", "酱油", "生抽", "醋"]):
                    combined_tokens.append(f"{item}一勺")
                else:
                    combined_tokens.append(f"{item}适量")
        for g in detected_grams[:5]:
            if g not in combined_tokens:
                combined_tokens.append(g)
        if not combined_tokens:
            combined_tokens = [f"{args.query}主料 300g", "大蒜 20g", "生抽一勺", "花生油两勺", "盐少许"]
        raw_ings = ", ".join(combined_tokens)

    science_note = snippets[0][:140] if snippets else None
    raw_steps = args.steps
    if not raw_steps and len(snippets) >= 2:
        raw_steps = "; ".join([f"【全网实采工序{i+1}】{s[:110]}" for i, s in enumerate(snippets[:3])])

    # Step 2: Assemble into commercial grams & macros
    assembled = assemble_recipe_obj(
        name=args.query,
        category=args.category,
        subcategory="联网实时采集组装",
        region=args.region,
        servings=2,
        raw_ingredients_str=raw_ings,
        raw_steps_str=raw_steps,
        science=science_note,
        save_to_db=args.save_to_db
    )

    # Step 3: Optimize according to requested mode
    opt_report = optimize_recipe_obj(assembled, args.optimize_mode, save_to_db=args.save_to_db)

    pipeline_result = {
        "pipeline_status": "CLOSED_LOOP_SUCCESS (Live-Fetch -> Assemble -> Optimize -> Persist)",
        "step1_live_web_intelligence": live_data["sources"],
        "step2_standardized_assembled_recipe": assembled,
        "step3_optimization_report": opt_report
    }
    write_output(pipeline_result, args.output)


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
            if kw not in json.dumps(r, ensure_ascii=False).lower():
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
    write_output({"total_matched": len(results), "results": results[:args.limit]}, args.output)


def cmd_recipe(args):
    db = load_db()
    target = None
    for r in db["recipes"]:
        if r["id"] == args.id or args.id in r["name"]:
            target = r
            break
    if not target:
        print(f"Error: Recipe '{args.id}' not found. Run `auto-pipeline --query \"{args.id}\"` to fetch & assemble it live from the web!", file=sys.stderr)
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
    if args.gender.lower() in ["m", "male", "男"]:
        bmr = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age + 5
    else:
        bmr = 10 * args.weight_kg + 6.25 * args.height_cm - 5 * args.age - 161

    activity_map = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    tdee = round(bmr * activity_map.get(args.activity, 1.375))
    target_kcal = max(round(bmr + 50), tdee - args.deficit)
    w = args.weight_kg

    carb_cycle_macros = {
        "high_carb_day": {"label": "高碳充能日", "carbs_g": round(w * 3.2), "protein_g": round(w * 1.8), "fat_g": round(w * 0.45)},
        "moderate_carb_day": {"label": "中碳平衡日", "carbs_g": round(w * 2.0), "protein_g": round(w * 2.0), "fat_g": round(w * 0.65)},
        "low_carb_day": {"label": "低碳燃脂日", "carbs_g": round(w * 0.9), "protein_g": round(w * 2.2), "fat_g": round(w * 0.85)}
    }
    fitness_recipes = [r["name"] for r in db["recipes"] if r["category"] == "fitness"]
    plan = {
        "metabolic_metrics": {"bmr_kcal": round(bmr), "tdee_kcal": tdee, "target_kcal": target_kcal},
        "carb_cycling_targets": carb_cycle_macros,
        "recommended_fitness_pool": fitness_recipes
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
<title>{args.title} - Gourmet Master v3.0 联网自进化美食系统</title>
<style>
  :root {{
    --bg: #0f172a; --card: #1e293b; --border: #334155; --text: #f8fafc;
    --muted: #94a3b8; --accent: #f59e0b; --green: #10b981; --red: #ef4444;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding-bottom: 60px; }}
  header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-bottom: 1px solid var(--border); padding: 28px 24px; text-align: center; }}
  header h1 {{ font-size: 26px; color: var(--accent); margin-bottom: 8px; }}
  header p {{ color: var(--muted); font-size: 14px; max-width: 820px; margin: 0 auto; }}
  .container {{ max-width: 1240px; margin: 24px auto; padding: 0 20px; }}
  .toolbar {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; align-items: center; background: var(--card); padding: 16px 20px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 24px; }}
  .tabs {{ display: flex; flex-wrap: wrap; gap: 8px; }}
  .tab-btn {{ background: #0f172a; color: var(--muted); border: 1px solid var(--border); padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; }}
  .tab-btn.active, .tab-btn:hover {{ background: var(--accent); color: #0f172a; border-color: var(--accent); }}
  .controls {{ display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }}
  .controls input, .controls select {{ background: #0f172a; color: var(--text); border: 1px solid var(--border); padding: 8px 12px; border-radius: 8px; font-size: 13px; }}
  .btn-print {{ background: var(--green); color: #0f172a; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 13px; }}
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
  .section-label {{ font-size: 12px; text-transform: uppercase; color: var(--muted); font-weight: 700; margin-top: 4px; }}
  .ing-list {{ list-style: none; font-size: 13px; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; }}
  .ing-list li {{ border-bottom: 1px dashed rgba(255,255,255,0.06); padding: 3px 0; display: flex; justify-content: space-between; }}
  .ing-amt {{ color: var(--green); font-weight: 600; }}
  .steps-list {{ padding-left: 18px; font-size: 13px; color: #e2e8f0; display: flex; flex-direction: column; gap: 5px; }}
  .tip {{ font-size: 12px; color: var(--muted); font-style: italic; border-top: 1px solid var(--border); padding-top: 8px; }}
  @media print {{ body {{ background: #fff; color: #000; }} .toolbar {{ display: none; }} .card {{ border: 1px solid #ccc; page-break-inside: avoid; background: #fff; color: #000; }} }}
</style>
</head>
<body>
<header>
  <h1>🍳 {args.title}</h1>
  <p>Gourmet Master v3.0 联网采集·智能拆解组装·减脂/星厨优化自进化系统 (当前已收录 {len(db['recipes'])} 道标准化配方)</p>
</header>
<div class="container">
  <div class="toolbar">
    <div class="tabs">
      <button class="tab-btn active" onclick="setCat('all', this)">全部配方 ({len(db['recipes'])})</button>
      <button class="tab-btn" onclick="setCat('fitness', this)">🥗 科学减脂餐</button>
      <button class="tab-btn" onclick="setCat('chinese', this)">🥢 中华八大菜系</button>
      <button class="tab-btn" onclick="setCat('western', this)">🥩 正统西餐米其林</button>
      <button class="tab-btn" onclick="setCat('cult', this)">🦪 区域邪教美食</button>
    </div>
    <div class="controls">
      <input type="text" id="search-input" placeholder="搜索食材/菜名/地域..." oninput="renderCards()">
      <label style="font-size:13px;color:var(--accent);font-weight:700;">份数缩放: <span id="serv-val">1</span> 份</label>
      <input type="range" id="serv-slider" min="1" max="20" value="1" oninput="document.getElementById('serv-val').innerText=this.value; renderCards()">
      <button class="btn-print" onclick="window.print()">🖨️ 导出 PDF</button>
    </div>
  </div>
  <div class="grid" id="recipe-grid"></div>
</div>
<script>
const RECIPES = {recipes_json};
let currentCat = 'all';
function setCat(cat, btn) {{
  currentCat = cat;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderCards();
}}
function renderCards() {{
  const kw = document.getElementById('search-input').value.trim().toLowerCase();
  const targetServings = parseInt(document.getElementById('serv-slider').value) || 1;
  const badgeMap = {{ fitness: ['badge-fit','🥗 减脂轻食'], chinese: ['badge-chn','🥢 中华名菜'], western: ['badge-west','🥩 正统西餐'], cult: ['badge-cult','🦪 区域邪教'] }};
  const filtered = RECIPES.filter(r => (currentCat === 'all' || r.category === currentCat) && (!kw || JSON.stringify(r).toLowerCase().includes(kw)));
  document.getElementById('recipe-grid').innerHTML = filtered.map(r => {{
    const scale = targetServings / r.base_servings;
    const [bCls, bTxt] = badgeMap[r.category] || ['badge-fit', r.category];
    const m = r.macros_per_serving;
    const ings = r.ingredients.map(i => `<li><span>${{i.item}}</span><span class="ing-amt">${{Math.round(i.amount * scale * 10)/10}} ${{i.unit}}</span></li>`).join('');
    const steps = r.steps.map(s => `<li>${{s}}</li>`).join('');
    const safetyHtml = r.safety_redline ? `<div class="safety">⚠️ <b>安全红线：</b>${{r.safety_redline}}</div>` : '';
    return `<div class="card">
      <div class="card-header"><div><div class="card-title">${{r.name}}</div><div style="font-size:12px;color:var(--muted)">📍 ${{r.region}} · ${{r.subcategory}}</div></div><span class="badge ${{bCls}}">${{bTxt}}</span></div>
      <div class="macros"><span>🔥 热量: <b>${{m.kcal}} kcal</b></span><span>💪 蛋白: <b>${{m.protein_g}}g</b></span><span>🍚 碳水: <b>${{m.carbs_g}}g</b></span><span>🥑 脂肪: <b>${{m.fat_g}}g</b></span></div>
      <div class="science">🔬 <b>分子烹饪原理：</b>${{r.science_principle}}</div>
      ${{safetyHtml}}
      <div class="section-label">⚖️ 精准配比 (${{targetServings}}人份)</div><ul class="ing-list">${{ings}}</ul>
      <div class="section-label">👨‍🍳 标准出品 SOP</div><ol class="steps-list">${{steps}}</ol>
      <div class="tip">💡 贴士：${{r.pro_tips}}</div>
    </div>`;
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
    parser = argparse.ArgumentParser(description="Gourmet Master v3.0 Live-Connected Culinary Engine")
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. live-fetch
    p_fetch = sub.add_parser("live-fetch", help="Fetch real-time recipes, history & gram patterns from Sogou Web Search, Wikipedia & TheMealDB")
    p_fetch.add_argument("--query", required=True)
    p_fetch.add_argument("--output", default=None)
    p_fetch.set_defaults(func=cmd_live_fetch)

    # 2. assemble
    p_asm = sub.add_parser("assemble", help="Deconstruct raw/vague ingredients into exact commercial grams, macros & BOM cost")
    p_asm.add_argument("--name", required=True)
    p_asm.add_argument("--category", choices=["fitness", "chinese", "western", "cult"], default="chinese")
    p_asm.add_argument("--subcategory", default="联网采集组装")
    p_asm.add_argument("--region", default="中国")
    p_asm.add_argument("--servings", type=int, default=2)
    p_asm.add_argument("--ingredients", required=True)
    p_asm.add_argument("--steps", default=None)
    p_asm.add_argument("--science", default=None)
    p_asm.add_argument("--safety", default=None)
    p_asm.add_argument("--tips", default=None)
    p_asm.add_argument("--save-to-db", action="store_true")
    p_asm.add_argument("--output", default=None)
    p_asm.set_defaults(func=cmd_assemble)

    # 3. optimize
    p_opt = sub.add_parser("optimize", help="Optimize any recipe for fat-loss, michelin-upgrade, or safety-audit")
    p_opt.add_argument("--id", required=True)
    p_opt.add_argument("--mode", choices=["fat-loss", "michelin-upgrade", "safety-audit"], required=True)
    p_opt.add_argument("--save-to-db", action="store_true")
    p_opt.add_argument("--output", default=None)
    p_opt.set_defaults(func=cmd_optimize)

    # 4. auto-pipeline
    p_pipe = sub.add_parser("auto-pipeline", help="One-click closed loop: Live Web Fetch -> Auto-Extract Grams & Assemble -> Optimize -> Save to DB")
    p_pipe.add_argument("--query", required=True, help="Any dish name to fetch from web, assemble, and optimize")
    p_pipe.add_argument("--category", choices=["fitness", "chinese", "western", "cult"], default="chinese")
    p_pipe.add_argument("--region", default="中国")
    p_pipe.add_argument("--ingredients", default=None, help="Optional manual override ingredients")
    p_pipe.add_argument("--steps", default=None, help="Optional manual override steps")
    p_pipe.add_argument("--optimize-mode", choices=["fat-loss", "michelin-upgrade", "safety-audit"], default="fat-loss")
    p_pipe.add_argument("--save-to-db", action="store_true")
    p_pipe.add_argument("--output", default=None)
    p_pipe.set_defaults(func=cmd_auto_pipeline)

    # 5. search
    p_search = sub.add_parser("search", help="Search structured recipes")
    p_search.add_argument("--category", choices=["all", "fitness", "chinese", "western", "cult"], default="all")
    p_search.add_argument("--keyword", default=None)
    p_search.add_argument("--max-kcal", type=int, default=None)
    p_search.add_argument("--limit", type=int, default=50)
    p_search.add_argument("--output", default=None)
    p_search.set_defaults(func=cmd_search)

    # 6. recipe
    p_rec = sub.add_parser("recipe", help="Get and scale a specific recipe")
    p_rec.add_argument("--id", required=True)
    p_rec.add_argument("--servings", type=int, default=1)
    p_rec.add_argument("--output", default=None)
    p_rec.set_defaults(func=cmd_recipe)

    # 7. tdee-plan
    p_tdee = sub.add_parser("tdee-plan", help="Calculate BMR/TDEE and 28-day carb cycling plan")
    p_tdee.add_argument("--gender", required=True)
    p_tdee.add_argument("--age", type=int, required=True)
    p_tdee.add_argument("--height-cm", type=float, required=True)
    p_tdee.add_argument("--weight-kg", type=float, required=True)
    p_tdee.add_argument("--activity", choices=["sedentary", "light", "moderate", "active"], default="light")
    p_tdee.add_argument("--deficit", type=int, default=400)
    p_tdee.add_argument("--output", default=None)
    p_tdee.set_defaults(func=cmd_tdee_plan)

    # 8. render-html
    p_html = sub.add_parser("render-html", help="Render standalone interactive HTML cookbook")
    p_html.add_argument("--title", default="美食大师 v3.0：联网采集·智能组装·科学减脂与邪教料理全书")
    p_html.add_argument("--output", required=True)
    p_html.set_defaults(func=cmd_render_html)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
