import os
import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--user-agent=Mozilla/5.0')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def extract_hidden_rows_js(driver):
    # table html 전체를 JS로 추출
    table_html = driver.execute_script(
        "return document.querySelector('table.datatable').outerHTML;"
    )
    soup = BeautifulSoup(table_html, "html.parser")
    headers = [th.get_text(strip=True) for th in soup.find_all("th")]
    rows = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if not tds:
            continue
        row = [td.get_text(separator=" ", strip=True) for td in tds]
        # 연도 2010~2015 범위의 row만
        first_col = row[0]
        if first_col.isdigit() and 2010 <= int(first_col) <= 2015:
            rows.append(row)
    return headers, rows

def extract_visible_rows_js(driver):
    # table html 전체를 JS로 추출
    table_html = driver.execute_script(
        "return document.querySelector('table.datatable').outerHTML;"
    )
    soup = BeautifulSoup(table_html, "html.parser")
    headers = [th.get_text(strip=True) for th in soup.find_all("th")]
    rows = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if not tds:
            continue
        row = [td.get_text(separator=" ", strip=True) for td in tds]
        # 연도 2016~2025 등 표에서 보이는 row만
        first_col = row[0]
        if first_col.isdigit() and int(first_col) >= 2016:
            rows.append(row)
    return headers, rows

def main():
    os.makedirs("../data", exist_ok=True)
    base_filename = "../data/ev_yearly_stats"
    url = "https://chargeinfo.ksga.org/front/statistics/evCar/"
    driver = setup_driver()
    driver.get(url)
    time.sleep(2)

    # 2016~2025 (보이는 데이터)
    headers, rows_visible = extract_visible_rows_js(driver)
    # 2010~2015 (숨겨진 데이터)
    headers2, rows_hidden = extract_hidden_rows_js(driver)

    all_rows = rows_visible + rows_hidden
    print(f"총 연도 데이터: {len(all_rows)} rows (2010~2025 합산)")

    driver.quit()

    # CSV 저장
    with open(f"{base_filename}.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in all_rows:
            writer.writerow(row)
    print(f"CSV 저장 완료: {base_filename}.csv")

    records = [dict(zip(headers, row)) for row in all_rows]
    with open(f"{base_filename}.json", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"JSON 저장 완료: {base_filename}.json")

if __name__ == "__main__":
    main()
