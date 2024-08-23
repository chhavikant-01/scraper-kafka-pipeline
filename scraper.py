from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os
import re
from kafka import KafkaProducer

# Initialize the Firefox WebDriver
driver = webdriver.Firefox()

# Open the webpage
url = "https://nciipc.gov.in/alerts_advisories_more.html"
driver.get(url)

# Allow the page to load
time.sleep(2)

# Find all the list items containing vulnerability data
vulnerability_elements = driver.find_elements(By.CLASS_NAME, "liList")

# Initialize a list to hold the extracted data
vulnerabilities = []

# Regular expressions to match the CVE ID and date
cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
date_pattern = re.compile(r"\(\d{2} \w+ \d{4}\)")

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], # Replace with your Kafka server
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic_name = 'vulnerabilities'  # Replace with your Kafka topic name

# Loop through each element and extract the relevant details
for elem in vulnerability_elements:
    title = elem.find_element(By.TAG_NAME, "b").text
    description = elem.find_element(By.CLASS_NAME, "advisoryFont").text.strip()
    link = elem.find_element(By.TAG_NAME, "a").get_attribute("href")
    
    # Extract the CVE IDs and date from the text
    cve_ids = cve_pattern.findall(description)
    date_match = date_pattern.search(title)
    date = date_match.group(0) if date_match else None
    
    # Create a dictionary for each vulnerability
    vulnerability = {
        "title": title,
        "description": description,
        "link": link,
        "cve_ids": cve_ids if cve_ids else None,
        "date": date.strip("()") if date else None
    }
    
    # Append the dictionary to the list
    vulnerabilities.append(vulnerability)
    
    # Send data to Kafka
    producer.send(topic_name, value=vulnerability)

# Optionally save the data as JSON on your Desktop
desktop_path = os.path.expanduser("~/Desktop/vulnerabilities.json")
with open(desktop_path, "w") as json_file:
    json.dump(vulnerabilities, json_file, indent=4, separators=(',', ': '))

# Close the WebDriver and Kafka producer
driver.close()
producer.flush()
producer.close()
