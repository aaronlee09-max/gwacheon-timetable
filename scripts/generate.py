#!/usr/bin/env python3
"""
과천중앙고등학교 시간표 - 최종 버전
- assets/teachers/ : 교사 49명
- assets/classes/ : 1학년_월~금, 2학년_월~금, 3학년_월~금 (15개)
"""

import json
from pathlib import Path

BASE = Path("/home/workdir")
ASSETS = BASE / "assets"
TEACHERS_DIR = ASSETS / "teachers"
CLASSES_DIR = ASSETS / "classes"
MASTER_DIR = ASSETS / "master"

DATA_DIR = BASE / "data"
TEACHERS_HTML = BASE / "teachers"
CLASSES_HTML = BASE / "classes"

def ensure_folders():
    for d in [TEACHERS_DIR, CLASSES_DIR, MASTER_DIR, DATA_DIR, TEACHERS_HTML, CLASSES_HTML]:
        d.mkdir(parents=True, exist_ok=True)

def get_teachers():
    teachers = []
    for img in sorted(TEACHERS_DIR.glob("*.png")) + sorted(TEACHERS_DIR.glob("*.jpg")):
        name = img.stem.replace("과천중앙고등학교_", "")
        teachers.append({
            "id": name,
            "name": name,
            "image": f"assets/teachers/{img.name}",
            "html": f"teachers/{name}.html"
        })
    return teachers

def get_classes():
    classes = []
    for img in sorted(CLASSES_DIR.glob("*.png")) + sorted(CLASSES_DIR.glob("*.jpg")):
        name = img.stem.replace("과천중앙고등학교_", "")
        classes.append({
            "id": name,
            "name": name,
            "image": f"assets/classes/{img.name}",
            "html": f"classes/{name}.html"
        })
    return classes

def get_master():
    imgs = sorted(MASTER_DIR.glob("*.png")) + sorted(MASTER_DIR.glob("*.jpg"))
    if imgs:
        return {"image": f"assets/master/{imgs[0].name}"}
    return None

def generate():
    ensure_folders()
    teachers = get_teachers()
    classes = get_classes()
    master = get_master()

    with open(DATA_DIR / "teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>과천중앙고등학교 시간표</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<header>
    <h1>🏫 과천중앙고등학교 시간표</h1>
    <p>2026학년도</p>
</header>
<div class="container">
"""

    if master:
        html += f"""
    <div class="section">
        <h2>📋 전체 시간표</h2>
        <img src="{master['image']}" style="max-width:100%; border-radius:12px;">
    </div>
"""
    else:
        html += """
    <div class="section">
        <h2>📋 전체 시간표</h2>
        <p style="color:#64748b;">assets/master/ 에 전체 시간표 이미지를 넣으면 여기에 표시됩니다.</p>
    </div>
"""

    html += f"""
    <div class="section">
        <h2>👩‍🏫 교사 시간표 ({len(teachers)}명)</h2>
        <div class="grid">
"""
    for t in teachers:
        html += f"""
            <div class="card">
                <div class="card-header">{t['name']}</div>
                <a href="{t['html']}"><img src="{t['image']}" loading="lazy"></a>
            </div>
"""
    html += """
        </div>
    </div>
"""

    html += f"""
    <div class="section">
        <h2>🏫 학년별 시간표 ({len(classes)}개)</h2>
        <div class="grid">
"""
    for c in classes:
        html += f"""
            <div class="card">
                <div class="card-header">{c['name']}</div>
                <a href="{c['html']}"><img src="{c['image']}" loading="lazy"></a>
            </div>
"""
    html += """
        </div>
    </div>
</div>
</body>
</html>
"""

    with open(BASE / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    for t in teachers:
        page = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{t['name']}</title><link rel="stylesheet" href="../css/style.css"></head>
<body><div class="container">
<a href="../index.html">← 메인</a>
<h1>{t['name']} 선생님</h1>
<img src="../{t['image']}" style="max-width:100%; border-radius:12px;">
<div style="margin-top:20px;">
<a href="../{t['image']}" download>다운로드</a>
<button onclick="window.print()">인쇄</button>
</div>
</div></body></html>"""
        with open(TEACHERS_HTML / f"{t['id']}.html", "w", encoding="utf-8") as f:
            f.write(page)

    for c in classes:
        page = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{c['name']}</title><link rel="stylesheet" href="../css/style.css"></head>
<body><div class="container">
<a href="../index.html">← 메인</a>
<h1>{c['name']}</h1>
<img src="../{c['image']}" style="max-width:100%; border-radius:12px;">
<div style="margin-top:20px;">
<a href="../{c['image']}" download>다운로드</a>
<button onclick="window.print()">인쇄</button>
</div>
</div></body></html>"""
        with open(CLASSES_HTML / f"{c['id']}.html", "w", encoding="utf-8") as f:
            f.write(page)

    print(f"✅ 완료: 교사 {len(teachers)}개, 학년별 {len(classes)}개 생성")

if __name__ == "__main__":
    generate()