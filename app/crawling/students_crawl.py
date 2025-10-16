from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os
import sys

driver = None

CSV_OUTPUT = 'raw_students_data.csv'

def connect_webdriver(url):
    global driver
    try:
        # Creates an options object.
        options = webdriver.ChromeOptions()

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Opens the browser in the incognito mode.
        options.add_argument("--incognito")

        driver = webdriver.Chrome(options=options)

        # Sets window size.
        driver.set_window_size(1400, 900)

        # Sets window position.
        driver.set_window_position(500, 0)

        # Sets timeout threshold.
        driver.set_page_load_timeout(30)
        print(f"Opening {url} ...")
        driver.get(url)
    except Exception as e:
        print("Failed to start Chrome WebDriver:", e)
        raise

def write_to_csv(file_path, rows):
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for cells in rows:
            writer.writerow(cells)

def scrape_students(output_csv: str = CSV_OUTPUT):
    global driver
    try:
        time.sleep(2)
        tbody_th = driver.find_elements(By.CSS_SELECTOR, 'table thead tr th')
        headers = [th.text.strip() for th in tbody_th if th.text.strip()]
        write_to_csv(output_csv, [headers])
        rows_written = 0
        while True:
            time.sleep(3)
            rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')

            page_rows = []
            for tr in rows:
                tds = tr.find_elements(By.TAG_NAME, 'td')
                cells = [td.text for td in tds]
                page_rows.append(cells)

            # Append rows to CSV
            with open(output_csv, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for cells in page_rows:
                    writer.writerow(cells)
                    rows_written += 1

            print(f"Wrote {len(page_rows)} rows (total {rows_written}).")

            next_btn = driver.find_element(By.XPATH, "//button[text()='Sau']")

            # If the button is disabled via attribute or not enabled, stop
            disabled_attr = next_btn.get_attribute('disabled')
            if disabled_attr is not None and disabled_attr != 'false':
                print("Next button is disabled; finished paging.")
                break
            if not next_btn.is_enabled():
                print("Next button is not enabled; finished paging.")
                break

            # Click Next
            next_btn.click()

            time.sleep(0.3)

        print(f"Done. Total rows written: {rows_written}. CSV saved to: {output_csv}")
        return rows_written

    finally:
        if driver:
            driver.quit()

def crawl_students(url: str, output_csv: str = CSV_OUTPUT):
    global driver
    raw_data_dir = os.path.join(os.path.dirname(__file__), 'raw_data')
    os.makedirs(raw_data_dir, exist_ok=True)
    output_csv = os.path.join(raw_data_dir, CSV_OUTPUT)
    # clear existing CSV
    if os.path.exists(output_csv):
        os.remove(output_csv)

    try:
        connect_webdriver(url)
        count = scrape_students(output_csv)
        print(f"Scraped {count} rows")
        return output_csv
    except Exception as e:
        print("Error during scraping:", e)
        sys.exit(1)
