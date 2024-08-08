import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import re

# Set up logging
logging.basicConfig(filename='gmap_script_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def open_google_maps_and_search(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return

    chrome_driver_path = r"C:\selenium driver\chromedriver-win32\chromedriver.exe"
    chrome_service = ChromeService(executable_path=chrome_driver_path)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    browser.get("https://maps.google.com")
    time.sleep(5)

    search_dir = os.path.dirname(file_path)
    result_file_path = os.path.join(search_dir, 'gmap_results.txt')
    failed_queries_file_path = os.path.join(search_dir, 'failed_queries.txt')

    with open(result_file_path, 'a', encoding='utf-8') as result_file, open(failed_queries_file_path, 'a',
                                                                            encoding='utf-8') as failed_file:
        while True:
            with open(file_path, 'r') as file:
                search_terms = file.readlines()

            if not search_terms:
                break  # Exit the loop if there are no more terms to process

            for term in search_terms:
                term = term.strip()
                if not term:
                    continue

                attempts = 0
                success = False
                printed_websites = set()  # To keep track of printed website URLs
                query_results = []  # Collect results for the current query

                while attempts < 3 and not success:
                    try:
                        search_box = WebDriverWait(browser, 15).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "searchboxinput"))
                        )
                        search_box.clear()
                        search_box.send_keys(term)
                        search_box.send_keys(u'\ue007')  # Press Enter key

                        time.sleep(5)

                        try:
                            clickable_div = WebDriverWait(browser, 15).until(
                                EC.element_to_be_clickable((By.CLASS_NAME, "Nv2PK"))
                            )
                            clickable_div.click()
                            print(f"Clicked on the div for search term: {term}")

                            time.sleep(5)

                            # Wait for the business name to be available
                            business_name_element = WebDriverWait(browser, 15).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[class*="DUwDvf"]'))
                            )
                            business_name = business_name_element.text
                            query_results.append(f"Business Name: {business_name}")

                            # Try to get the business type first
                            business_type_element = None
                            try:
                                business_type_element = WebDriverWait(browser, 15).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class*="DkEaL"]'))
                                )
                                business_type = business_type_element.text
                                query_results.append(f"Category: {business_type}")
                            except (NoSuchElementException, TimeoutException):
                                # If not found, attempt to get the category with class mgr77e
                                try:
                                    business_type_element = WebDriverWait(browser, 15).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, "mgr77e"))
                                    )
                                    business_type = business_type_element.text
                                    query_results.append(f"Category: {business_type}")
                                except (NoSuchElementException, TimeoutException):
                                    query_results.append("Business category not found.")
                                    logging.error(f"Business category not found for search term '{term}'.")

                            # Wait for the elements with class Io6YTe
                            elements = WebDriverWait(browser, 15).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, "Io6YTe"))
                            )

                            if elements:
                                query_results.append(f"Address: {elements[0].text}")

                            phone_found = False
                            website_found = False
                            plus_code_found = False

                            for element in elements[1:]:
                                element_text = element.text
                                if any(junk in element_text for junk in
                                       ["Find a table", "Menu", "Place an order", "linktr.ee",
                                        "Identifies as women-owned", "Claim this business"]):
                                    continue
                                if re.search(r'\.(com|org|net|edu|gov|info|biz|io|me|edu.gh|co|us)', element_text):
                                    if element_text not in printed_websites:
                                        query_results.append(f"Website: {element_text}")
                                        printed_websites.add(element_text)
                                        website_found = True
                                elif re.search(r'\b\d{3} \d{3} \d{4}\b', element_text):
                                    query_results.append(f"Phone: {element_text}")
                                    phone_found = True
                                elif '+' in element_text:
                                    query_results.append(f"Plus Code: {element_text}")
                                    plus_code_found = True
                                else:
                                    query_results.append(f"{element_text}")

                            if not phone_found:
                                query_results.append("Phone: N/A")
                            if not website_found:
                                query_results.append("Website: N/A")
                            if not plus_code_found:
                                query_results.append("Plus Code: N/A")

                            success = True

                        except (NoSuchElementException, TimeoutException) as e:
                            logging.error(f"Error during search for term '{term}': {str(e)}")
                            logging.error("Current page URL: " + browser.current_url)
                            browser.save_screenshot(f"error_{term}.png")
                            attempts += 1

                    except (NoSuchElementException, TimeoutException) as e:
                        logging.error(f"Error during search for term '{term}': {str(e)}")
                        attempts += 1

                if not success:
                    query_results.append(f"Failed to process search term '{term}' after 3 attempts")
                    failed_file.write(term + '\n')

                # Write results for the current query to the result file
                if query_results:
                    result_file.write('\n'.join(query_results) + '\n\n')

                print(f"Completed search for term '{term}'\n")
                time.sleep(3)

                # Remove the successfully processed term from the original file
                with open(file_path, 'r') as file:
                    remaining_terms = file.readlines()

                with open(file_path, 'w') as file:
                    for line in remaining_terms:
                        if line.strip() != term:
                            file.write(line)

    browser.quit()


file_path = r"C:\search term\search_querries.txt"
open_google_maps_and_search(file_path)