import os
import time
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 스크립트 위치 기준 저장 경로
script_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(script_dir, "car_excels")
os.makedirs(download_dir, exist_ok=True)

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

def download_files_batch(batch_data):
    """배치 단위로 파일 다운로드"""
    batch_idx, links_batch, download_path = batch_data
    
    driver = None
    results = []
    
    try:
        # 각 배치마다 별도의 브라우저 인스턴스 생성
        driver = get_chrome_driver(download_path)
        driver.get("https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58")
        
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # onclick으로 링크 다시 찾기
        download_links = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'downFile')]")
        onclick_to_element = {}
        
        for link in download_links:
            onclick = link.get_attribute("onclick") or ""
            onclick_to_element[onclick] = link
        
        print(f"배치 {batch_idx}: {len(links_batch)}개 파일 다운로드 시작")
        
        for idx, (year, month, text, original_onclick) in enumerate(links_batch, 1):
            try:
                # onclick으로 해당 링크 찾기
                target_link = None
                for onclick, element in onclick_to_element.items():
                    if f"{year}년 {month:02d}월 자동차 등록자료 통계.xlsx" in onclick or \
                       f"{year}년 {month}월 자동차 등록자료 통계.xlsx" in onclick:
                        target_link = element
                        break
                
                if not target_link:
                    results.append(f"배치 {batch_idx}-{idx}: 링크를 찾을 수 없음")
                    continue
                
                # 다운로드 전 파일 목록 확인
                files_before = set(os.listdir(download_path)) if os.path.exists(download_path) else set()
                
                # 링크 클릭
                driver.execute_script("arguments[0].click();", target_link)
                
                # 다운로드 완료 대기
                download_complete = False
                for wait_time in range(30):
                    time.sleep(1)
                    files_after = set(os.listdir(download_path)) if os.path.exists(download_path) else set()
                    new_files = files_after - files_before
                    
                    if new_files and not any(f.endswith('.crdownload') for f in files_after):
                        download_complete = True
                        new_file = list(new_files)[0]
                        file_size = os.path.getsize(os.path.join(download_path, new_file))
                        results.append(f"배치 {batch_idx}-{idx}: {new_file} ({file_size:,} bytes)")
                        break
                
                if not download_complete:
                    results.append(f"배치 {batch_idx}-{idx}: 시간 초과")
                
                # 다음 다운로드 전 잠시 대기
                time.sleep(1)
                
            except Exception as e:
                results.append(f"배치 {batch_idx}-{idx}: 오류 - {str(e)}")
        
        return results
        
    except Exception as e:
        return [f"배치 {batch_idx}: 전체 오류 - {str(e)}"]
    
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
            
            if "자동차 등록자료 통계.xlsx" in onclick:
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

def main():
    print("국토교통부 자동차 등록자료 통계 크롤링 시작 (2020.05 ~ 2025.06)")
    print("병렬 처리로 5개씩 동시 다운로드합니다...\n")
    
    # 모든 링크 수집
    all_links = get_all_links()
    
    if not all_links:
        print("대상 기간의 .xlsx 파일을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(all_links)}개 파일을 다운로드합니다.\n")
    
    # 5개씩 배치로 나누기
    batch_size = 5
    batches = []
    for i in range(0, len(all_links), batch_size):
        batch = all_links[i:i + batch_size]
        batches.append((i // batch_size + 1, batch, download_dir))
    
    print(f"{len(batches)}개 배치로 나누어 병렬 처리합니다...\n")
    
    # 병렬 처리 실행
    with ProcessPoolExecutor(max_workers=5) as executor:
        future_to_batch = {executor.submit(download_files_batch, batch): batch for batch in batches}
        
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                results = future.result()
                for result in results:
                    print(result)
            except Exception as e:
                print(f"배치 {batch[0]} 처리 중 오류: {e}")
    
    print(f"\n완료! 모든 엑셀 파일이 '{download_dir}' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    main()
