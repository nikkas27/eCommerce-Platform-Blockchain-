from requests.auth import HTTPBasicAuth
import requests
import json
import csv
import io
import pandas as pd
from selenium import webdriver
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
import time


def access():
    usrname = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    usrpass = 'YYYYYYYYYYYYYY'
    auth=HTTPBasicAuth(usrname,usrpass)
    url = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    response = requests.get(url,auth=auth)
    json_response = response.json()
    access_token = json_response["access_token"]
    print(access_token)
    headers = {"content-type": "application/json; charset=UTF-8",'Authorization':'Bearer {}'.format(access_token)}
    return headers


def blockchain(part, serial_info):
    blockchain_url="https://www.XXXXXXXXXXXXXXXXXXX"+part+"-sn-"+serial_info+".html"
    page = driver.get(blockchain_url)
    # tree = html.fromstring(page.content)
    driver.refresh()
    time.sleep(5)
    text_description = []
    text_description.append(part)
    text_description.append(serial_info)
    for i in range(1,3):
        for j in range(1,10):
            blockchain_info_other = driver.find_elements_by_xpath('//*[@id="content"]/div['+str(i)+']/div['+str(j)+']/div')
            if len(blockchain_info_other) == 0:
                continue
            for each_text in blockchain_info_other:
                if each_text.text in text_description:
                    continue
                print("Remaining:",each_text.text)
                text_description.append(each_text.text)
    print(text_description)
    return text_description


access_headers = access()
driver = webdriver.Chrome('./chromedriver')
with io.open('D:\Blockchain_info.csv', 'a', encoding="utf-8", newline='\n') as dataFile:
    data_file_writer = csv.writer(dataFile, delimiter=',')
    with open('inventory_data.csv') as f:
        inventory_data = csv.reader(f)
        i=0
        for row_data in inventory_data:
            part_number = row_data[1]
            serial = row_data[2]
            print ("Part number: ",part_number,"Serial: ", serial)
            if serial == '' or part_number == 'No Data Found.':
                continue
            parts_blockchain_info = blockchain(part_number, serial)
            # print(parts_blockchain_info)
            data_file_writer.writerow(parts_blockchain_info)
            i+=1
