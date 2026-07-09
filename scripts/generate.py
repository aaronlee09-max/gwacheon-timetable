#!/usr/bin/env python3
"""
과천중앙고등학교 시간표 - 최종 버전
assets/
├── master/
├── grades/
│   ├── 1학년/
│   ├── 2학년/
│   └── 3학년/
├── classes/
├── teachers/
└── pdf/
"""

import json
from pathlib import Path

BASE = Path("/home/workdir")
ASSETS = BASE / "assets"

MASTER_DIR = ASSETS / "master"
GRADES_DIR = ASSETS / "grades"
CLASSES_DIR = ASSETS / "classes"
TEACHERS_DIR = ASSETS / "teachers"

DATA_DIR = BASE / "data"
TEACHERS_HTML = BASE / "teachers"
CLASSES_HTML = BASE / "classes"

def ensure_folders():
    for d in [
        MASTER_DIR,
        GRADES_DIR / "1학년",
        GRADES_DIR / "2학년",
        GRADES_DIR / "3학년",
        CLASSES_DIR,
        TEACHERS_DIR,
        DATA_DIR,
        TEACHERS_HTML,
        CLASSES_HTML
    ]:
        d.mkdir(parents=True, exist_ok=True)

def get_teachers():
    teachers = []
    for img in sorted(TEACHERS_DIR.glob("*.png")) + sorted(TEACHERS_DIR.glob("*.jpg")):
        name = img.stem.replace("과천중앙고등학교_", "")
        teachers.append({
            "id": name,
            "name": name,
            "image": f"assets/teachers/{img.name}",
            "html": f"teachers/{name}.html",
            "category": "teacher"
        })
    return teachers

def get_grades():
    grades = []
    for grade in ["1학년", "2학년", "3학년"]:
        grade_dir = GRADES_DIR / grade
        for img in sorted(grade_dir.glob("*.png")) + sorted(grade_dir.glob("*.jpg")):
            name = img.stem.replace("과천중앙고등학교_", "")
            grades.append({
                "id": f"{grade}_{name}",
                "name": f"{grade} {name}",
                "grade": grade,
                "image": f"assets/grades/{grade}/{img.name}",
                "html": f"classes/{grade}_{name}.html",
                "category": "grade"
            })
    return grades

def get_classes():
    classes = []
    for img in sorted(CLASSES_DIR.glob("*.png")) + sorted(CLASSES_DIR.glob("*.jpg")):
        name = img.stem.replace("과천중앙고등학교_", "")
        classes.append({
            "id": name,
            "name": name,
            "image": f"assets/classes/{img.name}",
            "html": f"classes/{name}.html",
            "category": "class"
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
    grades = get_grades()
    classes = get_classes()
    master = get_master()

    all_timetables = teachers + grades + classes

    with open(DATA_DIR / "teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "grades.json", "w", encoding="utf-8") as f:
        json.dump(grades, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "search.json", "w", encoding="utf-8") as f:
        json.dump(all_timetables, f, ensure_ascii=False, indent=2)

    generate_index(teachers, grades, classes, master)

    print(f"✅ 구조 생성 완료")
    print(f"   - 교사: {len(teachers)}개")
    print(f"   - 학년별: {len(grades)}개")
    print(f"   - 반별: {len(classes)}개")

def generate_index(teachers, grades, classes, master):
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
        <h2>🏫 학년별 시간표 ({len(grades)}개)</h2>
        <div class="grid">
"""
    for g in grades:
        html += f"""
            <div class="card">
                <div class="card-header">{g['name']}</div>
                <a href="{g['html']}"><img src="{g['image']}" loading="lazy"></a>
            </div>
"""
    html += """
        </div>
    </div>
"""

    if classes:
        html += f"""
    <div class="section">
        <h2>📊 반별 시간표 ({len(classes)}개)</h2>
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
"""

    html += """
</div>
</body>
</html>
"""

    with open(BASE / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    generate()