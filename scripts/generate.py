#!/usr/bin/env python3
"""
과천중앙고등학교 시간표 웹사이트 완전 자동 생성기
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path("/home/workdir")
TIMETABLES = BASE / "timetables"
ASSETS = BASE / "assets"
TEACHERS_HTML = BASE / "teachers"
CLASSES_HTML = BASE / "classes"
DATA = BASE / "data"

def clean_name(name):
    return name.replace('.png', '').replace('.jpg', '').replace('과천중앙고등학교_', '')

def get_teachers():
    teachers = []
    for img in sorted((TIMETABLES / "teachers").glob("*.png")):
        name = clean_name(img.name)
        short = name[:2] if len(name) > 2 else name
        teachers.append({
            "name": name,
            "short": short,
            "file": img.name,
            "html": f"{name}.html"
        })
    return teachers

def get_classes():
    classes = []
    for img in sorted((TIMETABLES / "classes").glob("*.png")):
        name = clean_name(img.name)
        classes.append({
            "name": name,
            "file": img.name,
            "html": f"{name}.html"
        })
    return classes

def generate_data_json(teachers, classes):
    DATA.mkdir(exist_ok=True)
    with open(DATA / "teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    with open(DATA / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    meta = {
        "school": "과천중앙고등학교",
        "year": "2026",
        "updated": datetime.now().isoformat(),
        "teacher_count": len(teachers),
        "class_count": len(classes)
    }
    with open(DATA / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("✅ JSON 데이터 생성 완료")

def generate_teacher_pages(teachers):
    TEACHERS_HTML.mkdir(exist_ok=True)
    for t in teachers:
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['name']} 선생님 시간표 - 과천중앙고등학교</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="timetable-page">
        <a href="../index.html" class="back-btn">← 메인으로</a>
        
        <div class="timetable-container">
            <div class="timetable-header">
                <h2>👩‍🏫 {t['name']} 선생님</h2>
                <p>과천중앙고등학교 • 2026학년도 주간 시간표</p>
            </div>
            
            <div class="timetable-image" style="padding: 30px; text-align: center; background: #f8fafc;">
                <img src="../assets/teachers/{t['file']}" 
                     alt="{t['name']} 선생님 시간표" 
                     style="max-width: 100%; max-height: 85vh; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 10px solid white;">
            </div>
            
            <div style="padding: 20px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; background: white;">
                <a href="../assets/teachers/{t['file']}" download class="btn">📥 다운로드</a>
                <button onclick="window.print()" class="btn" style="background:#1976D2;">🕹️ 인쇄</button>
                <a href="../index.html" class="btn" style="background:#64748b;">← 목록으로</a>
            </div>
        </div>
    </div>
</body>
</html>"""
        with open(TEACHERS_HTML / t['html'], "w", encoding="utf-8") as f:
            f.write(html)
    print(f"✅ 교사 페이지 {len(teachers)}개 생성")

def generate_class_pages(classes):
    CLASSES_HTML.mkdir(exist_ok=True)
    for c in classes:
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{c['name']} 시간표 - 과천중앙고등학교</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <div class="timetable-page">
        <a href="../index.html" class="back-btn">← 메인으로</a>
        
        <div class="timetable-container">
            <div class="timetable-header">
                <h2>📚 {c['name']}</h2>
                <p>과천중앙고등학교 • 2026학년도 주간 시간표</p>
            </div>
            
            <div class="timetable-image" style="padding: 30px; text-align: center; background: #f8fafc;">
                <img src="../assets/classes/{c['file']}" 
                     alt="{c['name']} 시간표" 
                     style="max-width: 100%; max-height: 85vh; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 10px solid white;">
            </div>
            
            <div style="padding: 20px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; background: white;">
                <a href="../assets/classes/{c['file']}" download class="btn">📥 다운로드</a>
                <button onclick="window.print()" class="btn" style="background:#1976D2;">🕹️ 인쇄</button>
                <a href="../index.html" class="btn" style="background:#64748b;">← 목록으로</a>
            </div>
        </div>
    </div>
</body>
</html>"""
        with open(CLASSES_HTML / c['html'], "w", encoding="utf-8") as f:
            f.write(html)
    print(f"✅ 반 페이지 {len(classes)}개 생성")

def generate_index(teachers, classes):
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
        <div class="container">
            <h1>🏫 과천중앙고등학교</h1>
            <p>시간표 조회 시스템 • 2026학년도</p>
        </div>
    </header>

    <div class="container">
        <div class="search-section">
            <h2 style="margin-bottom:15px;">🔍 교사 / 반 검색</h2>
            <input type="text" id="search" placeholder="교사 이름 또는 반 (예: 김성, 2학년, 월)" 
                   style="width:100%; padding:16px; font-size:1.1rem; border:2px solid #e2e8f0; border-radius:12px;">
        </div>

        <div class="search-section">
            <h2 style="margin-bottom:15px;">🕒 최근 조회</h2>
            <div id="recent"></div>
        </div>

        <h2 class="section-title">👩‍🏫 교사 시간표 ({len(teachers)}명)</h2>
        <div class="grid" id="teachers">
"""
    for t in teachers:
        html += f'''<div class="card" data-name="{t['name']} {t['short']}">
    <div class="card-header">👩‍🏫 {t['name']}</div>
    <div class="card-body">
        <a href="teachers/{t['html']}">
            <img src="assets/teachers/{t['file']}" alt="{t['name']}" loading="lazy">
        </a>
    </div>
</div>'''

    html += """</div>

        <h2 class="section-title">🏫 학년별 시간표</h2>
        <div class="grid" id="classes">
"""
    for c in classes:
        html += f'''<div class="card" data-name="{c['name']}">
    <div class="card-header">📚 {c['name']}</div>
    <div class="card-body">
        <a href="classes/{c['html']}">
            <img src="assets/classes/{c['file']}" alt="{c['name']}" loading="lazy">
        </a>
    </div>
</div>'''

    html += f"""</div>
    </div>

    <footer>
        <p>과천중앙고등학교 시간표 • 자동 생성 {datetime.now().strftime('%Y-%m-%d')}</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""
    
    with open(BASE / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 갱신 완료")

def main():
    print("🚀 과천중앙고등학교 시간표 사이트 완전 재생성 시작...")
    
    teachers = get_teachers()
    classes = get_classes()
    
    generate_data_json(teachers, classes)
    generate_teacher_pages(teachers)
    generate_class_pages(classes)
    generate_index(teachers, classes)
    
    print("\n✅ 완료! 이제 GitHub에 Push하면 자동 배포됩니다.")

if __name__ == "__main__":
    main()