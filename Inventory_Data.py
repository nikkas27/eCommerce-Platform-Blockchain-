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
    usrname = '6W6ZLsWAlg3AyQHh0Usghel0iADI2SVA'
    usrpass = 'DyYmO2ax2Stb5t2N'
    auth=HTTPBasicAuth(usrname,usrpass)
    url = "https://aero.api-beta.honeywell.com/v1/oauth/accesstoken?grant_type=client_credentials"

    response = requests.get(url,auth=auth)
    json_response = response.json()
    # access_token = '2V6Y4TYkwT1g6CFyhtbyYaw5aGM7'
    access_token = json_response["access_token"]
    print(access_token)
    headers = {"content-type": "application/json; charset=UTF-8",'Authorization':'Bearer {}'.format(access_token)}
    return headers


def blockchain(part_num, serial):   # NOT CALLED
    blockchain_url="https://www.godirecttrade.com/honeywellaerospacetrading-pn-"+part_num+"-sn-"+serial+".html"
    page = driver.get(blockchain_url)
    # tree = html.fromstring(page.content)
    driver.refresh()
    time.sleep(5)
    # text = driver.findElement(By.tagName("span")).getText()
    # prices =
    for i in range(1,3):
        for j in range(1,5):
            blockchain_path = '/html/body/div[2]/main/div[2]/div/div[1]/div/div/div[2]/div/div['+str(i)+']/div['+str(j)+']/div/span[@class="dot current"]'
            blockchain_info = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[1]/div')
            if len(blockchain_info) == 0:
                print("Skip")
                continue
            print("i",i,"j",j)
            for each_text in blockchain_info:
                print(each_text.text)



access_headers = access()
driver = webdriver.Chrome('./chromedriver')
with io.open('D:\Cleveland State University\Research_Moonwong\Inventory Data\Inventory\inventory_data.csv', 'a', encoding="utf-8", newline='\n') as dataFile:
    data_file_writer = csv.writer(dataFile, delimiter=',')
    for i in range(1,57853):
        print(i)
        if i==1:
            url = "https://www.godirecttrade.com/marketplace/seller/profile/shop/HoneywellAerospaceTrading"
            driver.get(url)
        else:
            next_url = "https://www.godirecttrade.com/marketplace/seller/profile/shop/HoneywellAerospaceTrading#"+str(i)
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
                invurl="https://aero.api-beta.honeywell.com/gdt/v1/search/inventory/part?part_number="+partnum
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
