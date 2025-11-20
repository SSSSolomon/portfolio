import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os
import time
import random
import requests
import re

def init_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    return uc.Chrome(options=options)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip("_")

def download_image(img_url, save_path):
    try:
        clean_url = img_url.split(";")[0].split("?")[0]
        img_ext = re.search(r'\.(jpg|jpeg|png|gif|webp)', clean_url)
        img_ext = img_ext.group(0) if img_ext else ".jpg"
        save_path = save_path.rsplit(".", 1)[0] + img_ext  

        response = requests.get(clean_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        
    except Exception:
        pass  # Silent error handling

def scrape_inventory():
    url_template = "https://specialauto.autovit.ro/inventory?page={}"
    title_xpath = "//article//h2"
    desc_xpath = "//article//p[contains(@class, 'description') or contains(@class, 'text')]"
    image_xpath = "//article//img"

    output_folder = "scraped_data"
    os.makedirs(output_folder, exist_ok=True)
    all_parts = []

    driver = init_driver()
    try:
        for page in range(1, 6):
            url = url_template.format(page)
            print(f"Scraping page {page}...")
            driver.get(url)
            time.sleep(random.uniform(3, 6))

            titles = driver.find_elements(By.XPATH, title_xpath)
            descriptions = driver.find_elements(By.XPATH, desc_xpath)
            images = driver.find_elements(By.XPATH, image_xpath)

            for i, title_element in enumerate(titles):
                title_text = title_element.text.strip()
                if not title_text:
                    continue

                part_name = sanitize_filename("_".join(title_text.split()[:3]))
                part_folder = os.path.join(output_folder, part_name)
                os.makedirs(part_folder, exist_ok=True)

                desc_text = descriptions[i].text.strip() if i < len(descriptions) else "No description available."
                
                text_file_path = os.path.join(part_folder, f"{part_name}.txt")
                with open(text_file_path, "w", encoding="utf-8") as f:
                    f.write(f"Title: {title_text}\n\nDescription: {desc_text}")
                
                all_parts.append(title_text)
                
                if i < len(images):
                    img_url = images[i].get_attribute("src")
                    if img_url:
                        img_save_path = os.path.join(part_folder, f"{part_name}")
                        download_image(img_url, img_save_path)
    
    except Exception:
        pass  # Silent error handling
    finally:
        driver.quit()
        print("✅ Scraping complete. Data saved.")
        save_part_list(all_parts)

def save_part_list(parts):
    parts.sort()
    with open("scraped_parts_list.txt", "w", encoding="utf-8") as f:
        for part in parts:
            f.write(part + "\n")
    print("✅ Parts list saved as 'scraped_parts_list.txt'")

if __name__ == "__main__":
    print("🚀 Starting the scraping process...")
    scrape_inventory()
    print("✅ Process finished.")
