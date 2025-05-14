import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

input_file = "objidlist.txt"
output_file = "SensorsList.csv"

# You have to change this Settings
PRTG_URL = "http://127.0.0.1"
PRTG_Username = "prtgadmin"
PRTG_Password = "prtgadmin"

driver = webdriver.Chrome()
driver.get(f"{PRTG_URL}/index.htm")
time.sleep(2)

WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "loginusername"))).send_keys({PRTG_Username})
driver.find_element(By.ID,"loginpassword").send_keys({PRTG_Password})
time.sleep(2)
driver.find_element(By.ID,"submitter1").click()
time.sleep(2)

with open(input_file, "r", encoding="utf-8") as f:
    objids = [line.strip() for line in f if line.strip()]

with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["objid", "name", "Query", "Database", "Username", "warn_mode", "warning_value", "down_mode", "down_value"])
        for objid in objids:
            url = f"{PRTG_URL}/sensor.htm?id={objid}&tabid=8"
            driver.get(url)
            time.sleep(2)
# --------------- Name
            n = driver.find_element(By.ID, "name_")
            name = n.get_attribute("value")
# --------------- Database
            try:
                db = driver.find_element(By.ID, "database_")
                db_value = db.get_attribute("value")
            except:
                db_value = "-"
# --------------- Username
            try:
                u = driver.find_element(By.ID, "user_")
                user_value = u.get_attribute("value")
            except:
                user_value = "-"
# --------------- Query
            try:
                q = driver.find_element(By.ID, "sql_")
                query_value = q.get_attribute("value")
            except:
                query_value = "-"
# --------------- Warning
            try:
                warning_element = Select(driver.find_element(By.NAME, "datawarningmode_"))
                warning_selected = warning_element.first_selected_option.text
                w = driver.find_element(By.ID, "datalimitwarning_")
                warning_value = w.get_attribute("value")
            except:
                warning_selected = "-"
                warning_value = "-"
# --------------- Down
            try:
                down_element = Select(driver.find_element(By.NAME, "datadownmode_"))
                down_selected = down_element.first_selected_option.text
                d = driver.find_element(By.ID, "datalimitdown_")
                down_value = d.get_attribute("value")
            except:
                down_selected = "-"
                down_value = "-"

            writer.writerow([objid, name, query_value, db_value, user_value, warning_selected, warning_value, down_selected, down_value])

driver.quit()