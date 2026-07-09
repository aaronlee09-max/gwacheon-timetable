#!/usr/bin/env python3
"""
과천중앙고등학교 시간표 - 최종 자동 생성기
assets/ 폴더에 이미지만 넣으면 전체 사이트 자동 생성
"""

import os
import json
from pathlib import Path
from datetime import datetime

BASE = Path("/home/workdir")

ASSETS = BASE / "assets"
MASTER_DIR = ASSETS / "master"
TEACHERS_DIR = ASSETS / "teachers"
CLASSES_DIR = ASSETS / "classes"

DATA_DIR = BASE / "data"
TEACHERS_HTML = BASE / "teachers"
CLASSES_HTML = BASE / "classes"

def ensure_folders():
    for d in [MASTER_DIR, TEACHERS_DIR, CLASSES_DIR, DATA_DIR, TEACHERS_HTML, CLASSES_HTML]:
        d.mkdir(parents=True, exist_ok=True)

def get_images(folder):
    return sorted(list(folder.glob("*.png")) + list(folder.glob("*.jpg")))

def get_teachers():
    teachers = []
    for img in get_images(TEACHERS_DIR):
        name = img.stem.replace("과천중앙고등학교_", "")
        teachers.append({
            "id": name,
            "name": name,
            "image": f"assets/teachers/{img.name}",
            "html": f"teachers/{name}.html",
            "type": "teacher"
        })
    return teachers

def get_classes():
    classes = []
    for img in get_images(CLASSES_DIR):
        name = img.stem.replace("과천중앙고등학교_", "")
        classes.append({
            "id": name,
            "name": name,
            "image": f"assets/classes/{img.name}",
            "html": f"classes/{name}.html",
            "type": "class"
        })
    return classes

def get_master():
    images = get_images(MASTER_DIR)
    if images:
        return {"image": f"assets/master/{images[0].name}", "name": "전체 시간표"}
    return None

def generate_all():
    ensure_folders()
    teachers = get_teachers()
    classes = get_classes()
    master = get_master()
    
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    
    generate_index(teachers, classes, master)
    generate_teacher_pages(teachers)
    generate_class_pages(classes)
    
    print(f"✅ 생성 완료: 교사 {len(teachers)}개, 반 {len(classes)}개")

def generate_index(teachers, classes, master):
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
        <p>2026학년도 • 실시간 조회</p>
    </header>
    
    <div class="container">
"""
    
    if master:
        html += f"""
        <div class="section">
            <h2>📋 전체 시간표</h2>
            <div style="text-align:center; background:white; padding:20px; border-radius:16px;">
                <img src="{master['image']}" alt="전체 시간표" style="max-width:100%; border-radius:12px;">
            </div>
        </div>
"""
    else:
        html += """
        <div class="section">
            <h2>📋 전체 시간표</h2>
            <p style="color:#64748b;">assets/master/ 폴더에 전체 시간표 이미지를 넣으면 여기에 표시됩니다.</p>
        </div>
"""
    
    html += f"""
        <div class="section">
            <h2>👩‍🏫 교사 시간표 ({len(teachers)}명)</h2>
"""
    if teachers:
        html += '<div class="grid">'
        for t in teachers:
            html += f"""
                <div class="card">
                    <div class="card-header">{t['name']}</div>
                    <a href="{t['html']}"><img src="{t['image']}" loading="lazy"></a>
                </div>
"""
        html += '</div>'
    else:
        html += '<p style="color:#64748b;">assets/teachers/ 폴더에 이미지를 넣으면 여기에 표시됩니다.</p>'
    html += '</div>'
    
    html += f"""
        <div class="section">
            <h2>🏫 학년별 시간표 ({len(classes)}개)</h2>
"""
    if classes:
        html += '<div class="grid">'
        for c in classes:
            html += f"""
                <div class="card">
                    <div class="card-header">{c['name']}</div>
                    <a href="{c['html']}"><img src="{c['image']}" loading="lazy"></a>
                </div>
"""
        html += '</div>'
    else:
        html += '<p style="color:#64748b;">assets/classes/ 폴더에 이미지를 넣으면 여기에 표시됩니다.</p>'
    html += '</div></div></body></html>'
    
    with open(BASE / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_teacher_pages(teachers):
    for t in teachers:
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>{t['name']} 선생님</title><link rel="stylesheet" href="../css/style.css"></head>
<body>
<div class="container">
    <a href="../index.html">← 메인</a>
    <h1>{t['name']} 선생님</h1>
    <img src="../{t['image']}" style="max-width:100%; border-radius:12px;">
    <div style="margin-top:20px;">
        <a href="../{t['image']}" download>다운로드</a>
        <button onclick="window.print()">인쇄</button>
    </div>
</div>
</body>
</html>"""
        with open(TEACHERS_HTML / f"{t['id']}.html", "w", encoding="utf-8") as f:
            f.write(html)

def generate_class_pages(classes):
    for c in classes:
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"><title>{c['name']}</title><link rel="stylesheet" href="../css/style.css"></head>
<body>
<div class="container">
        <a href="../index.html">← 메인</a>
        <h1>{c['name']}</h1>
        <img src="../{c['image']}" style="max-width:100%; border-radius:12px;">
        <div style="margin-top:20px;">
            <a href="../{c['image']}" download>다운로드</a>
            <button onclick="window.print()">인쇄</button>
        </div>
    </div>
</body>
</html>"""
        with open(CLASSES_HTML / f"{c['id']}.html", "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    generate_all()