#!/usr/bin/env python3
"""
과천중앙고등학교 용 코름시간 파서 (Name-based)
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://comci.net:4082"


def search_school(school_name: str):
    """ 학교 이름으로 검색 """ 
    try:
        url = f"{BASE_URL}/st"
        params = {"name": school_name}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or 'school' not in data:
            print(f"경고: '{school_name}' 학교를 찾을 수 없습니다.")
            return None
            
        schools = data['school']
        
        # 정확한 이름 매칭 우선 찾기
        for school in schools:
            if school_name in school.get('name', ''):
                print(f"검색 성공: {school['name']} (Code: {school.get('code', 'N/A')})")
                return school
                
        # 찾지 못했으면 첫 번째 결과 반환
        if schools:
            school = schools[0]
            print(f"경고: 정확한 이름을 찾지 못했습니다. 첫 번째 결과를 사용합니다: {school['name']}")
            return school
            
        return None
        
    except Exception as e:
        print(f"에러 발생: {e}")
        return None


def get_timetable(school_code: str, grade: int = None, class_num: int = None):
    """ 시간표 데이터 가져오기 """ 
    try:
        url = f"{BASE_URL}/tt"
        params = {
            "sc": school_code,
        }
        
        if grade:
            params["gr"] = grade
        if class_num:
            params["cl"] = class_num
            
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        return data
        
    except Exception as e:
        print(f"시간표 가져오기 실패: {e}")
        return None


def save_timetable(data, filename="timetable.json"):
    """ 시간표 데이터를 JSON으로 저장 """ 
    try:
        output_path = Path("data") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"저장 완료: {output_path}")
        return True
    except Exception as e:
        print(f"저장 실패: {e}")
        return False


def main():
    school_name = "과천중앙고등학교"
    
    print(f"=== {school_name} 시간표 파서 ===\n")
    
    # 1. 학교 검색
    school = search_school(school_name)
    if not school:
        print("학교 검색 실패")
        return
    
    school_code = school.get("code")
    if not school_code:
        print("학교 코드를 찾을 수 없습니다.")
        return
    
    print(f"\n학교 코드: {school_code}")
    
    # 2. 시간표 가져오기 (전체)
    print("\n시간표 데이터를 가져오는 중...")
    timetable_data = get_timetable(school_code)
    
    if timetable_data:
        save_timetable(timetable_data, "timetable.json")
        print("\n시간표 파싱 성공!")
    else:
        print("\n시간표 가져오기 실패")

if __name__ == "__main__":
    main()