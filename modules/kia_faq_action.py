from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import json
import os

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

def extract_media_and_links(panel):
    image_urls = []
    link_urls = []
    answer_text_parts = []
    try:
        imgs = panel.find_elements(By.TAG_NAME, "img")
        for img in imgs:
            src = img.get_attribute("src")
            if src:
                image_urls.append(src)
        links = panel.find_elements(By.TAG_NAME, "a")
        for a in links:
            href = a.get_attribute("href")
            if href:
                link_urls.append(href)
        answer_text = panel.text.strip()
        answer_text_parts.append(answer_text)
    except Exception as e:
        print("extract_media_and_links error:", e)
    return answer_text_parts, image_urls, link_urls

def extract_question_text(item):
    try:
        qs = item.find_elements(By.CSS_SELECTOR, "button, h3, .cmp-accordion__header")
        for q in qs:
            t = q.text.strip()
            if t and len(t) > 5:
                return t
    except:
        pass
    return None

def extract_answer_content(driver, item):
    try:
        btn = item.find_element(By.CSS_SELECTOR, "button, .cmp-accordion__header")
        if btn.get_attribute("aria-expanded") != "true":
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            btn.click()
            time.sleep(1)
    except:
        pass
    selectors = [
        ".cmp-accordion__panel[aria-hidden='false']",
        ".cmp-accordion__panel:not([aria-hidden='true'])",
        ".cmp-accordion__panel",
        ".accordion-content",
        ".accordion-body",
        "[role='region']"
    ]
    for sel in selectors:
        panels = item.find_elements(By.CSS_SELECTOR, sel)
        for panel in panels:
            if panel.is_displayed():
                return extract_media_and_links(panel)
    return ([""], [], [])

def crawl_category(driver, category, button):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    time.sleep(0.5)
    button.click()
    time.sleep(2)
    faq_items = []
    selectors = [
        "div[data-cmp-hook-accordion='item']", ".cmp-accordion__item",
        ".accordion-item", ".faq-item"
    ]
    for sel in selectors:
        faq_items = driver.find_elements(By.CSS_SELECTOR, sel)
        if faq_items:
            break
    result = []
    for item in faq_items:
        q = extract_question_text(item)
        if not q: continue
        answer_text_parts, img_urls, link_urls = extract_answer_content(driver, item)
        answer_text = " ".join(answer_text_parts)
        img_urls_str = ",".join(img_urls)
        link_urls_str = ",".join(link_urls)
        result.append({
            "category": category,
            "question": q,
            "answer_text": answer_text,
            "image_urls": img_urls_str,
            "link_urls": link_urls_str
        })
    return result

def main():
    # 항상 프로젝트 루트(data)에 저장
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    base_filename = os.path.join(DATA_DIR, "kia_faq_data")

    driver = setup_driver()
    url = "https://www.kia.com/kr/customer-service/center/faq"
    driver.get(url)
    time.sleep(5)
    category_buttons = {}
    selectors = [
        ".tabs__btn", "button[class*='tabs']", "button[class*='btn'][class*='tab']",
        ".tab-button", "[data-tab]", "[data-category]"
    ]
    for sel in selectors:
        buttons = driver.find_elements(By.CSS_SELECTOR, sel)
        for btn in buttons:
            txt = btn.text.strip()
            if txt and txt not in category_buttons:
                category_buttons[txt] = btn
        if category_buttons:
            break

    print("카테고리:", list(category_buttons.keys()))
    all_data = []
    for cat, btn in category_buttons.items():
        data = crawl_category(driver, cat, btn)
        all_data.extend(data)

    driver.quit()

    fieldnames = ["category", "question", "answer_text", "image_urls", "link_urls"]
    with open(f"{base_filename}.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_data:
            writer.writerow(row)
    print(f"CSV 저장 완료: {base_filename}.csv")

    faq_json = {"faq_data": []}
    for row in all_data:
        faq_json["faq_data"].append({
            "category": row["category"],
            "question": row["question"],
            "answer": row["answer_text"],
            "image_urls": row["image_urls"],
            "link_urls": row["link_urls"]
        })
    with open(f"{base_filename}.json", "w", encoding="utf-8") as f:
        json.dump(faq_json, f, ensure_ascii=False, indent=2)
    print(f"JSON 저장 완료: {base_filename}.json")

if __name__ == "__main__":
    main()
