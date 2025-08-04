import os
import time
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_project_root():
    # db/data_process.py 기준으로 상위 폴더(프로젝트 루트) 반환
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 스크립트 위치 기준 저장 경로
ROOT_DIR = get_project_root()

# script_dir = os.path.dirname(os.path.abspath(__file__))
# download_dir = os.path.join(script_dir, "data", "car_excels")
# os.makedirs(download_dir, exist_ok=True)

download_dir = os.path.join(ROOT_DIR, "data", "car_excels")
os.makedirs(download_dir, exist_ok=True)

# 중복 다운로드 방지를 위한 락과 다운로드 세트
download_lock = threading.Lock()
downloaded_files = set()

def get_chrome_driver(download_path):
    """Chrome 드라이버 설정 및 반환"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    
    # 다운로드 폴더 설정
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def download_single_file_parallel(year, month, download_path, thread_id):
    """병렬 처리용 단일 파일 다운로드"""
    driver = None
    
    try:
        # 예상 파일명 생성 (특별한 경우 처리)
        if year == 2021 and month == 8:
            expected_filename = f"{year}년 {month:02d}월 자동차 등록현황 통계.xlsx"
        elif year == 2021 and month == 9:
            expected_filename = f"{year}년 {month:02d}월 자동차 등록자료 통계 .xlsx"
        else:
            expected_filename = f"{year}년 {month:02d}월 자동차 등록자료 통계.xlsx"
        
        file_path = os.path.join(download_path, expected_filename)
        
        # 락을 사용하여 중복 다운로드 방지
        with download_lock:
            # 이미 다운로드 중이거나 완료된 파일인지 확인
            if expected_filename in downloaded_files:
                print(f"[T{thread_id}] ✓ 스킵: {expected_filename} (다른 스레드에서 처리됨)")
                return True
            
            # 이미 파일이 존재하고 크기가 적절하면 스킵 (여러 가능한 파일명 체크)
            possible_files = [
                f"{year}년 {month:02d}월 자동차 등록자료 통계.xlsx",
                f"{year}년 {month:02d}월 자동차 등록현황 통계.xlsx",
                f"{year}년 {month:02d}월 자동차 등록자료 통계 .xlsx"
            ]
            
            existing_file = None
            for possible_file in possible_files:
                possible_path = os.path.join(download_path, possible_file)
                if os.path.exists(possible_path):
                    existing_file = possible_file
                    file_path = possible_path
                    break
            
            if existing_file:
                file_size = os.path.getsize(file_path)
                if file_size > 10000:  # 10KB 이상인 경우만 유효한 파일로 간주
                    downloaded_files.add(existing_file)
                    print(f"[T{thread_id}] ✓ 스킵: {existing_file} (이미 존재, {file_size:,} bytes)")
                    return True
                else:
                    # 파일이 너무 작으면 삭제하고 다시 다운로드
                    os.remove(file_path)
                    print(f"[T{thread_id}] ⚠ 재시도: {existing_file} (파일 크기가 너무 작음: {file_size} bytes)")
            
            # 다운로드 중으로 표시
            downloaded_files.add(expected_filename)
        
        print(f"[T{thread_id}] 🔄 시작: {expected_filename}")
        
        # 브라우저 생성
        driver = get_chrome_driver(download_path)
        driver.get("https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58")
        
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # onclick으로 링크 찾기
        download_links = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'downFile')]")
        target_link = None
        
        for link in download_links:
            onclick = link.get_attribute("onclick") or ""
            # 여러 파일명 패턴 확인
            patterns = [
                f"{year}년 {month:02d}월 자동차 등록자료 통계.xlsx",
                f"{year}년 {month}월 자동차 등록자료 통계.xlsx",
                f"{year}년 {month:02d}월 자동차 등록현황 통계.xlsx",  # 2021년 8월
                f"{year}년 {month}월 자동차 등록현황 통계.xlsx",
                f"{year}년 {month:02d}월 자동차 등록자료 통계 .xlsx",  # 2021년 9월 (공백 추가)
                f"{year}년 {month}월 자동차 등록자료 통계 .xlsx"
            ]
            
            if any(pattern in onclick for pattern in patterns):
                target_link = link
                break
        
        if not target_link:
            print(f"[T{thread_id}] ✗ 실패: {expected_filename} - 링크를 찾을 수 없음")
            # 실패 시 다운로드 세트에서 제거
            with download_lock:
                downloaded_files.discard(expected_filename)
            return False
        
        # 다운로드 전 파일 목록 확인
        files_before = set(os.listdir(download_path)) if os.path.exists(download_path) else set()
        
        # 링크 클릭
        driver.execute_script("arguments[0].click();", target_link)
        
        # 다운로드 완료 대기 (32초, 0.5초 간격으로 체크)
        download_complete = False
        for wait_time in range(64):  # 32초 x 2 (0.5초 간격)
            time.sleep(0.5)
            files_after = set(os.listdir(download_path)) if os.path.exists(download_path) else set()
            new_files = files_after - files_before
            
            if new_files and not any(f.endswith('.crdownload') for f in files_after):
                new_file = list(new_files)[0]
                file_size = os.path.getsize(os.path.join(download_path, new_file))
                
                # 파일 크기 검증 (10KB 이상이어야 유효)
                if file_size > 10000:
                    download_complete = True
                    print(f"[T{thread_id}] ✓ 완료: {new_file} ({file_size:,} bytes)")
                    break
                else:
                    print(f"[T{thread_id}] ⚠ 파일 크기가 너무 작음: {file_size} bytes, 계속 대기...")
        
        if not download_complete:
            print(f"[T{thread_id}] ✗ 실패: {expected_filename} - 시간 초과")
            # 실패 시 다운로드 세트에서 제거
            with download_lock:
                downloaded_files.discard(expected_filename)
            return False
        
        return True
        
    except Exception as e:
        print(f"[T{thread_id}] ✗ 오류: {expected_filename} - {str(e)}")
        # 실패 시 다운로드 세트에서 제거
        with download_lock:
            downloaded_files.discard(expected_filename)
        return False
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def get_all_links():
    """모든 다운로드 링크 수집"""
    driver = None
    try:
        driver = get_chrome_driver(download_dir)
        driver.get("https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58")
        
        print("페이지 로드 완료, 다운로드 링크를 찾고 있습니다...")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        download_links = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'downFile')]")
        
        filtered_links = []
        for link in download_links:
            text = link.text.strip()
            onclick = link.get_attribute("onclick") or ""
            
            # 자동차 등록 관련 xlsx 파일 찾기 (여러 패턴 지원)
            if ("자동차 등록자료 통계.xlsx" in onclick or 
                "자동차 등록현황 통계.xlsx" in onclick or 
                "자동차 등록자료 통계 .xlsx" in onclick):
                match = re.search(r"(\d{4})년\s*(\d{1,2})월", onclick)
                if match:
                    year = int(match.group(1))
                    month = int(match.group(2))
                    if (year > 2020 or (year == 2020 and month >= 5)) and \
                       (year < 2025 or (year == 2025 and month <= 6)):
                        filtered_links.append((year, month, text, onclick))
        
        filtered_links.sort(key=lambda x: (x[0], x[1]))
        return filtered_links
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def clean_download_folder():
    """다운로드 폴더의 임시 파일들 정리"""
    if not os.path.exists(download_dir):
        return
    
    temp_files = []
    for file in os.listdir(download_dir):
        if file.endswith(('.crdownload', '.tmp', '.part')):
            temp_files.append(file)
    
    if temp_files:
        print(f"임시 파일 {len(temp_files)}개 정리 중...")
        for temp_file in temp_files:
            try:
                os.remove(os.path.join(download_dir, temp_file))
                print(f"  - 삭제: {temp_file}")
            except:
                pass

def download_worker(task_data):
    """워커 함수 - ThreadPoolExecutor에서 사용"""
    year, month, thread_id = task_data
    return download_single_file_parallel(year, month, download_dir, thread_id)

def main():
    print("국토교통부 자동차 등록자료 통계 크롤링 시작 (2020.05 ~ 2025.06)")
    print("4개 스레드로 병렬 다운로드합니다...\n")
    
    # 다운로드 폴더 정리
    clean_download_folder()
    
    # 전역 변수 초기화
    global downloaded_files
    downloaded_files.clear()
    
    # 모든 링크 수집
    all_links = get_all_links()
    
    if not all_links:
        print("대상 기간의 .xlsx 파일을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(all_links)}개 파일을 다운로드합니다.\n")
    
    # 작업 데이터 준비 (year, month, thread_id)
    tasks = [(year, month, i % 4 + 1) for i, (year, month, text, onclick) in enumerate(all_links)]
    
    # ThreadPoolExecutor로 병렬 다운로드
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 작업 제출
        future_to_task = {executor.submit(download_worker, task): task for task in tasks}
        
        # 결과 수집
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            year, month, thread_id = task
            
            try:
                result = future.result()
                if result:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"[T{thread_id}] ✗ 예외 발생: {year}년 {month:02d}월 - {str(e)}")
                fail_count += 1
    
    print(f"\n🎉 완료! 성공: {success_count}개, 실패: {fail_count}개")
    print(f"📁 모든 엑셀 파일이 '{download_dir}' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    main()
