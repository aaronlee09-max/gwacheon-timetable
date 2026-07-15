#!/usr/bin/env python3
"""
과천중앙고등학교 용 코름시간 파서 (Name-based, 개선버전)
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://comci.net:4082"


def search_school(school_name: str):
    """ 학교 이름으로 검색 (Name-based) """ 
    print(f"[1] '{school_name}' 학교 검색 중...")
    
    try:
        # 다양한 엔드포인트 시도
        endpoints = [
            f"{BASE_URL}/st",
            f"{BASE_URL}/search",
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, params={"name": school_name}, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and 'school' in data and data['school']:
                        schools = data['school']
                        print(f"   → {len(schools)}개 학교 발견")
                        
                        # 정확 매칭 우선
                        for school in schools:
                            if school_name == school.get('name', ''):
                                print(f"   ✓ 정확 매칭: {school['name']}")
                                return school
                        
                        # 부분 매칭
                        for school in schools:
                            if school_name in school.get('name', ''):
                                print(f"   → 부분 매칭: {school['name']}")
                                return school
                        
                        # 첫 번째 결과 반환
                        if schools:
                            school = schools[0]
                            print(f"   → 첫 번째 결과 사용: {school['name']}")
                            return school
                            
            except Exception as e:
                print(f"   {endpoint} 실패: {e}")
                continue
        
        print("   ✗ 학교를 찾을 수 없습니다.")
        return None
        
    except Exception as e:
        print(f"   검색 에러: {e}")
        return None


def get_timetable(school):
    """ 시간표 데이터 가져오기 """ 
    school_code = school.get('code')
    if not school_code:
        print("   ✗ 학교 코드가 없습니다.")
        return None
    
    print(f"[2] 시간표 데이터 가져오기 (Code: {school_code})...")
    
    try:
        # 다양한 파라미터 조합 시도
        params_list = [
            {"sc": school_code},
            {"sc": school_code, "gr": 1},
            {"sc": school_code, "gr": 2},
            {"sc": school_code, "gr": 3},
        ]
        
        for params in params_list:
            try:
                response = requests.get(f"{BASE_URL}/tt", params=params, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        print(f"   ✓ 파라미터 {params} 로 성공")
                        return data
            except:
                continue
        
        print("   ✗ 시간표 데이터를 가져올 수 없습니다.")
        return None
        
    except Exception as e:
        print(f"   시간표 가져오기 에러: {e}")
        return None


def save_data(data, filename):
    """ 데이터 저장 """ 
    try:
        output_path = Path("data") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✓ {filename} 저장 완료")
        return True
    except Exception as e:
        print(f"   저장 실패: {e}")
        return False


def main():
    school_name = "과천중앙고등학교"
    
    print("=" * 50)
    print(f"{school_name} 코름시간 파서 시작")
    print("=" * 50)
    
    # 1. 학교 검색
    school = search_school(school_name)
    if not school:
        print("\n학교 검색 실패. 파서 종료.")
        return
    
    # 2. 시간표 가져오기
    timetable_data = get_timetable(school)
    
    if timetable_data:
        save_data(timetable_data, "timetable.json")
        save_data(school, "school_info.json")
        print("\n파싱 성공!")
    else:
        print("\n파싱 실패.")

if __name__ == "__main__":
    main()