#!/usr/bin/env python3
"""
과천중앙고등학교 시간표 - B 방향 적용 버전
- 교사 데이터에 subject 추가
- 메인 카드: 이름 + 과목 표시
- 개별 페이지 제목 개선
- 검색: 이름 + 약칭 + 과목 지원
"""

import json
from pathlib import Path

BASE = Path("/home/workdir")
ASSETS = BASE / "assets"
TEACHERS_DIR = ASSETS / "teachers"
CLASSES_DIR = ASSETS / "classes"
GRADES_DIR = ASSETS / "grades"
MASTER_DIR = ASSETS / "master"

DATA_DIR = BASE / "data"
TEACHERS_HTML = BASE / "teachers"
CLASSES_HTML = BASE / "classes"

# === 교사 매핑 (B 방향) ===
TEACHER_MAPPING = {
    "김서_": {"full_name": "김서_", "subject": "국어A"},
    "명지_": {"full_name": "명지_", "subject": "국어B"},
    "이순_": {"full_name": "이순화", "subject": "문학A"},
    "장은_": {"full_name": "장은정", "subject": "문학B"},
    "김정_": {"full_name": "김정현", "subject": "심국"},
    "배수_": {"full_name": "배수_", "subject": "언매"},
    "류형_": {"full_name": "류형주", "subject": "화작"},
    "김수_": {"full_name": "김수진", "subject": "공영A"},
    "박유_": {"full_name": "박유나", "subject": "공영B"},
    "이동_": {"full_name": "이동희", "subject": "영1A"},
    "길경_": {"full_name": "길경화", "subject": "영1B"},
    "전보_": {"full_name": "전보영", "subject": "영독작"},
    "황현_": {"full_name": "황현정", "subject": "영독작"},
    "김민_": {"full_name": "김민준", "subject": "공수1"},
    "손정_": {"full_name": "손정화", "subject": "공수1"},
    "성혜_": {"full_name": "성혜_", "subject": "공수1"},
    "정경_": {"full_name": "정경수", "subject": "대수"},
    "조혜_": {"full_name": "조혜숙", "subject": "대수"},
    "오정_": {"full_name": "오정_", "subject": "확통"},
    "이영_": {"full_name": "이영란", "subject": "확통"},
    "고주_": {"full_name": "고주미", "subject": "통사1"},
    "이인_": {"full_name": "이인혜", "subject": "여지"},
    "류진_": {"full_name": "류진무", "subject": "현사윤"},
    "박민_": {"full_name": "박민_", "subject": "윤사"},
    "김준_": {"full_name": "김준민", "subject": "사문탐"},
    "전우_": {"full_name": "전우_", "subject": "통사1"},
    "허웅_": {"full_name": "허웅구", "subject": "한사1"},
    "서예_": {"full_name": "서예_", "subject": "한사1"},
    "최재_": {"full_name": "최재_", "subject": "경제"},
    "강경_": {"full_name": "강경화", "subject": "통과1A"},
    "김희_": {"full_name": "김희_", "subject": "통과1B"},
    "강정_": {"full_name": "강정은", "subject": "물리학"},
    "이윤_": {"full_name": "이윤주", "subject": "화학가"},
    "박민_": {"full_name": "박민재", "subject": "생명가"},
    "권보_": {"full_name": "권보영", "subject": "과연"},
    "이기_": {"full_name": "이기_", "subject": "물리II"},
    "류상_": {"full_name": "류상하", "subject": "진로"},
    "목현_": {"full_name": "목현주", "subject": "생명II"},
    "민문_": {"full_name": "민문갑", "subject": "지학II"},
    "김성_": {"full_name": "김성민", "subject": "정보"},
    "오현_": {"full_name": "오현택", "subject": "체육"},
    "임태_": {"full_name": "임태경", "subject": "스생1"},
    "박시_": {"full_name": "박시민", "subject": "운건"},
    "박유_": {"full_name": "박유리", "subject": "음악"},
    "한재_": {"full_name": "한재영", "subject": "미술"},
    "류승_": {"full_name": "류승철", "subject": "일어"},
    "장윤_": {"full_name": "장윤선", "subject": "세시"},
    "장재_": {"full_name": "장재_", "subject": "교한"},
    "송근_": {"full_name": "송근화", "subject": "진로"},
}

def ensure_folders():
    for d in [TEACHERS_DIR, CLASSES_DIR, GRADES_DIR/"1학년", GRADES_DIR/"2학년", GRADES_DIR/"3학년", MASTER_DIR, DATA_DIR, TEACHERS_HTML, CLASSES_HTML]:
        d.mkdir(parents=True, exist_ok=True)

def get_teachers():
    teachers = []
    for img in sorted(TEACHERS_DIR.glob("*.png")) + sorted(TEACHERS_DIR.glob("*.jpg")):
        short = img.stem.replace("과천중앙고등학교_", "")
        mapping = TEACHER_MAPPING.get(short, {"full_name": short, "subject": "미정"})
        
        teachers.append({
            "id": short,
            "name": mapping["full_name"],
            "short": short,
            "subject": mapping["subject"],
            "image": f"assets/teachers/{img.name}",
            "html": f"teachers/{short}.html",
            "category": "teacher"
        })
    return teachers

def get_grades():
    grades = []
    for grade_folder in ["1학년", "2학년", "3학년"]:
        grade_dir = GRADES_DIR / grade_folder
        for img in sorted(grade_dir.glob("*.png")) + sorted(grade_dir.glob("*.jpg")):
            name = img.stem.replace("과천중앙고등학교_", "")
            grades.append({
                "id": f"{grade_folder}_{name}",
                "name": f"{grade_folder} {name}",
                "image": f"assets/grades/{grade_folder}/{img.name}",
                "html": f"classes/{grade_folder}_{name}.html",
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

    all_items = teachers + grades + classes

    with open(DATA_DIR / "teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "grades.json", "w", encoding="utf-8") as f:
        json.dump(grades, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "search.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    generate_index(teachers, grades, classes, master)
    generate_teacher_pages(teachers)
    generate_class_pages(classes)

    print(f"✅ 생성 완료: 교사 {len(teachers)}명, 학년별 {len(grades)}개")

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
        <h2>👨‍🏫 교사 시간표 ({len(teachers)}명)</h2>
        <div class="grid">
"""
    for t in teachers:
        html += f"""
            <div class="card">
                <div class="card-header">
                    👨‍🏫 {t['name']}<br>
                    <small>📚 {t['subject']}</small>
                </div>
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

    html += """
</div>
</body>
</html>
"""

    with open(BASE / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_teacher_pages(teachers):
    for t in teachers:
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{t['name']} 선생님 ({t['subject']}) 시간표</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div class="container">
    <a href="../index.html">← 메인으로</a>
    <h1>👨‍🏫 {t['name']} 선생님 ({t['subject']})</h1>
    <img src="../{t['image']}" style="max-width:100%; border-radius:12px; margin:20px 0;">
    <div>
        <a href="../{t['image']}" download>📥 다운로드</a>
        <button onclick="window.print()">🕹️ 인쇄</button>
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
<head>
    <meta charset="UTF-8">
    <title>{c['name']} 시간표</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div class="container">
    <a href="../index.html">← 메인으로</a>
    <h1>{c['name']}</h1>
    <img src="../{c['image']}" style="max-width:100%; border-radius:12px;">
</div>
</body>
</html>"""
        with open(CLASSES_HTML / f"{c['id']}.html", "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    generate()