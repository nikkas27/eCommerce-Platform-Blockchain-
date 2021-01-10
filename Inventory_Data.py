from requests.auth import HTTPBasicAuth
import requests
import json
import csv
import io
from selenium import webdriver
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
import time


def access():
    usrname = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    usrpass = 'YYYYYYYYYYYYYYYYYYYYY'
    auth=HTTPBasicAuth(usrname,usrpass)
    url = "https://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=client_credentials"

    response = requests.get(url,auth=auth)
    json_response = response.json()
    access_token = json_response["access_token"]
    print(access_token)
    headers = {"content-type": "application/json; charset=UTF-8",'Authorization':'Bearer {}'.format(access_token)}
    return headers


access_headers = access()
driver = webdriver.Chrome('./chromedriver')
with io.open('D:\inventory_data.csv', 'a', encoding="utf-8", newline='\n') as dataFile:
    data_file_writer = csv.writer(dataFile, delimiter=',')
    for i in range(1,57853):
        print(i)
        if i==1:
            url = "https://www.XXXTrading"
            driver.get(url)
        else:
            next_url = "https://www.XXXTrading#"+str(i)
            driver.get(next_url)
            driver.refresh()
            time.sleep(5)
        link_list = []

        for j in range(1,20):
            time.sleep(5)
            path='/html/body/div[2]/main/div[3]/div/div[1]/div[3]/section[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/table/tbody/tr['+str(j)+']/td[1]/div/div/a'
            video_links = driver.find_elements_by_xpath(path)
            for x in video_links:
                partnum = x.text
                print(partnum)
                invurl="https://XXX/part?part_number="+partnum
                response = requests.get(invurl,headers=access_headers).json()
                try:
                    for dict_num in range(len(response)):
                        total_data=[]
                        dict=response[dict_num]
                        # print(dict.keys())
                        key=[]
                        for keys in dict:
                            key.append(keys)
                            # if keys == 'part_number':
                            #     part_num_blkchain = dict[keys]
                            #     # print(part_num_blkchain)
                            # elif keys == 'serial_number':
                            #     serial = dict[keys]
                            #     print("Serial: ",serial)
                            #     blockchain(part_num_blkchain,serial)

                        # ------------------ First Header -----------------------------
                        # data_file_writer.writerow(key)
                        for each_keys in dict:
                            total_data.append(dict[each_keys])

                        data_file_writer.writerow(total_data)

                        # blockchain_path = '/html/body/div[2]/main/div[2]/div/div[1]/div/div/div[2]'
                        # blockchain_data = driver.find_element_by_xpath(blockchain_path)
                        # # print(blockchain_data.text)
                except Exception as e:
                    print("exception '{}'".format(e))
                    print(response)
                    dict=response
                    key=[]
                    for keys in dict:
                        if keys == 'fault':
                            access_headers = access()
                            i=i-1
                            continue
                        key.append(keys)
                    # ------------------ First Header -----------------------------
                    # data_file_writer.writerow(key)

                    for each_keys in dict:
                        total_data.append(dict[each_keys])
                    data_file_writer.writerow(total_data)

        print("Page: ", i,"Inventory Updated!")
