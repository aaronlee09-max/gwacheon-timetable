#!/usr/bin/env python3
"""
과천중앙고등학교 시간표 - 풀 자동 생성기 (서비스 수준)
generate.py 한 번 실행으로 전체 사이트 구조 + 파일 생성
"""

import os
import json
from pathlib import Path
from datetime import datetime

BASE = Path("/home/workdir")

# === 폴더 경로 정의 ===
ASSETS_DIR = BASE / "assets"
MASTER_DIR = ASSETS_DIR / "master"
TEACHERS_IMG_DIR = ASSETS_DIR / "teachers"
CLASSES_IMG_DIR = ASSETS_DIR / "classes"
PDF_DIR = ASSETS_DIR / "pdf"
THUMBNAILS_DIR = ASSETS_DIR / "thumbnails"

DATA_DIR = BASE / "data"
TEACHERS_HTML_DIR = BASE / "teachers"
CLASSES_HTML_DIR = BASE / "classes"

REQUIRED_DIRS = [
    ASSETS_DIR, MASTER_DIR, TEACHERS_IMG_DIR, CLASSES_IMG_DIR,
    PDF_DIR, THUMBNAILS_DIR, DATA_DIR,
    TEACHERS_HTML_DIR, CLASSES_HTML_DIR
]

def ensure_directories():
    """ 필요한 폴더가 없으면 자동 생성 """
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        gitkeep = directory / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
    print("✅ 필요한 폴더 구조 확인/생성 완료")

def get_teachers():
    """assets/teachers/ 에서 이미지 파일 읽기"""
    teachers = []
    for img in sorted(TEACHERS_IMG_DIR.glob("*.png")) + sorted(TEACHERS_IMG_DIR.glob("*.jpg")):
        name = img.stem.replace("과천중앙고등학교_", "")
        short = name[:2]
        teachers.append({
            "id": name,
            "name": name,
            "short": short,
            "image": f"assets/teachers/{img.name}",
            "html": f"teachers/{name}.html",
            "type": "teacher"
        })
    return teachers

def get_classes():
    """assets/classes/ 에서 이미지 파일 읽기"""
    classes = []
    for img in sorted(CLASSES_IMG_DIR.glob("*.png")) + sorted(CLASSES_IMG_DIR.glob("*.jpg")):
        name = img.stem.replace("과천중앙고등학교_", "")
        classes.append({
            "id": name,
            "name": name,
            "image": f"assets/classes/{img.name}",
            "html": f"classes/{name}.html",
            "type": "class"
        })
    return classes

def generate_json_files(teachers, classes):
    DATA_DIR.mkdir(exist_ok=True)
    
    with open(DATA_DIR / "teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    
    with open(DATA_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    
    search_data = [{"id": t["id"], "name": t["name"], "short": t.get("short", ""), "type": "teacher", "html": t["html"]} for t in teachers]
    search_data += [{"id": c["id"], "name": c["name"], "type": "class", "html": c["html"]} for c in classes]
    
    with open(DATA_DIR / "search.json", "w", encoding="utf-8") as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    meta = {
        "school": "과천중앙고등학교",
        "year": 2026,
        "updated": datetime.now().isoformat(),
        "teacher_count": len(teachers),
        "class_count": len(classes)
    }
    with open(DATA_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON 파일 생성 완료 ({len(teachers)} teachers, {len(classes)} classes)")

def generate_teacher_html(teachers):
    TEACHERS_HTML_DIR.mkdir(exist_ok=True)
    for i, t in enumerate(teachers):
        prev_link = teachers[i-1]["html"] if i > 0 else "#"
        next_link = teachers[i+1]["html"] if i < len(teachers)-1 else "#"
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['name']} 선생님 시간표 | 과천중앙고등학교</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container">
        <a href="../index.html">← 메인으로</a>
        <div style="display:flex; justify-content:space-between; margin:20px 0;">
            <a href="{prev_link}">← 이전 교사</a>
            <a href="{next_link}">다음 교사 →</a>
        </div>
        
        <h1>👩‍🏫 {t['name']} 선생님</h1>
        <div style="text-align:center; margin:30px 0;">
            <img src="../{t['image']}" alt="{t['name']} 선생님 시간표" style="max-width:100%; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.15);">
        </div>
        
        <div style="text-align:center; margin-top:30px;">
            <a href="../{t['image']}" download class="btn">📥 다운로드</a>
            <button onclick="window.print()" class="btn">🕹️ 인쇄</button>
        </div>
    </div>
</body>
</html>"""
        with open(TEACHERS_HTML_DIR / f"{t['id']}.html", "w", encoding="utf-8") as f:
            f.write(html)
    print(f"✅ 교사 HTML 페이지 {len(teachers)}개 생성")

def generate_class_html(classes):
    CLASSES_HTML_DIR.mkdir(exist_ok=True)
    for i, c in enumerate(classes):
        prev_link = classes[i-1]["html"] if i > 0 else "#"
        next_link = classes[i+1]["html"] if i < len(classes)-1 else "#"
        
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{c['name']} 시간표 | 과천중앙고등학교</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="container">
        <a href="../index.html">← 메인으로</a>
        <div style="display:flex; justify-content:space-between; margin:20px 0;">
            <a href="{prev_link}">← 이전 반</a>
            <a href="{next_link}">다음 반 →</a>
        </div>
        
        <h1>📚 {c['name']}</h1>
        <div style="text-align:center; margin:30px 0;">
            <img src="../{c['image']}" alt="{c['name']} 시간표" style="max-width:100%; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.15);">
        </div>
        
        <div style="text-align:center; margin-top:30px;">
            <a href="../{c['image']}" download class="btn">📥 다운로드</a>
            <button onclick="window.print()" class="btn">🕹️ 인쇄</button>
        </div>
    </div>
</body>
</html>"""
        with open(CLASSES_HTML_DIR / f"{c['id']}.html", "w", encoding="utf-8") as f:
            f.write(html)
    print(f"✅ 반 HTML 페이지 {len(classes)}개 생성")

def generate_index_html(teachers, classes):
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
        <p>2026학년도 • 실시간 조회 시스템</p>
    </header>
    
    <div class="container">
        <div class="search-section">
            <input type="text" id="search" placeholder="교사 또는 반 검색 (예: 김성, 2학년)">
        </div>
        
        <h2>👩‍🏫 교사 시간표 ({len(teachers)}명)</h2>
        <div class="grid">
"""
    for t in teachers:
        html += f'''<div class="card">
    <div class="card-header">{t['name']}</div>
    <a href="{t['html']}"><img src="{t['image']}" alt="{t['name']}" loading="lazy"></a>
</div>'''
    
    html += """
        </div>
        
        <h2>🏫 학년별 시간표</h2>
        <div class="grid">
"""
    for c in classes:
        html += f'''<div class="card">
    <div class="card-header">{c['name']}</div>
    <a href="{c['html']}"><img src="{c['image']}" alt="{c['name']}" loading="lazy"></a>
</div>'''
    
    html += """
        </div>
    </div>
    <script src="js/main.js"></script>
</body>
</html>"""
    
    with open(BASE / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 생성 완료")

def main():
    print("🚀 과천중앙고등학교 시간표 자동 생성기 시작...")
    
    ensure_directories()
    
    teachers = get_teachers()
    classes = get_classes()
    
    if not teachers and not classes:
        print("⚠️ assets/teachers/ 또는 assets/classes/ 에 이미지가 없습니다.")
        print("   이미지를 업로드한 후 다시 실행하세요.")
        return
    
    generate_json_files(teachers, classes)
    generate_teacher_html(teachers)
    generate_class_html(classes)
    generate_index_html(teachers, classes)
    
    print("\n✅ 전체 프로젝트 생성 완료!")
    print("이제 assets/ 폴더에 이미지만 넣으면 바로 동작합니다.")

if __name__ == "__main__":
    main()