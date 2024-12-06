from PIL import ImageGrab # type: ignore

import pyscreenshot  # type: ignore
import time
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
import sqlite3  
from datetime import datetime
import re
import os
import random
import requests # type: ignore
from selenium.common.exceptions import NoSuchElementException  # type: ignore
from getpass import getpass
from mysql.connector import connect, Error # type: ignore
import paramiko # type: ignore

host = "5.83.218.232"
port = 22
jpg = ".jpg"







#Парсер
driver = webdriver.Chrome()
driver.get("https://www.amazon.com/")
time.sleep(15)
url = "https://www.amazon.com/s?i=stripbooks&rh=n%3A283155&s=featured-rank&dc&fs=true&ds=v1%3AJGYv94YsmQUZ4F3pspRQ9dF0Uws46V%2BOHrI%2BEZ8jJwM&_encoding=UTF8&pf_rd_p=dc5bf44b-97c5-4dcb-bdba-14972a9be974&pf_rd_r=XNXCYCF7FC8N15P47EA3&qid=1728501116&ref=sr_ex_n_1"
driver.get(url)
driver.set_window_size(1200, 800)
time.sleep(5)

start = 0
finish = 21
list_new = []
plus_name_model = "J2IjoiMSJ9"

while True:
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    list_name = driver.find_elements(By.CSS_SELECTOR,'h2.s-line-clamp-2 > a[href]')

    start = 0
    time.sleep(5)
    
        
        
    for list_name_model in list_name:
            if start != finish:
                time.sleep(25)
                start = start + 1
                list_name_model = list_name_model.get_attribute("href")
                list_name_model, _ = list_name_model.split('J2IjoiMSJ9', 1)
                list_name_model = list_name_model + plus_name_model
                two_driver = webdriver.Chrome()
                two_driver.set_window_size(1200, 800)
                time.sleep(2)
                two_driver.get(list_name_model)
                time.sleep(3)
                two_driver.get(list_name_model)
                try:
                    book_name = two_driver.find_element(By.ID,'productTitle')
                    book_name = book_name.text
                    book_name = book_name.replace("/", "")
                    book_name = book_name.replace(".", "")
                    print(book_name)
                except NoSuchElementException: 
                    book_name = ""
                    print("element not found")
                try:
                    imgURL = two_driver.find_element(By.CSS_SELECTOR,'div.imgTagWrapper > img[src]')
                    imgURL = imgURL.get_attribute("src")
                    print(imgURL)
                    filename = imgURL.split('/')[-1]
                    filename = filename.replace("_", "")
                    filename = filename.replace(".", "")
                    filename = filename.replace("/", "")
                    filename = filename.replace("jpg", "")
                    filename = filename + jpg
                    r = requests.get(imgURL, allow_redirects=True)
                except NoSuchElementException: 
                    imgURL = ""
                    print("element not found")
                
                try:
                    author = two_driver.find_element(By.CSS_SELECTOR,'span.author > a')
                    author = author.text
                except NoSuchElementException: 
                    author = ""
                    print("element not found")
                try:
                    description = two_driver.find_element(By.CSS_SELECTOR,'div.a-expander-content')
                    description = description.text
                    description = description
                except NoSuchElementException: 
                    description = ""
                    print("element not found")
                
                
                size = random.uniform(5, 15)
                data_publication = datetime.now()
                data_publication = str(data_publication)[:10]
                print(data_publication)
                list_name_model = ""
                two_driver.close()
                time.sleep(5)
                print(start)
                connection = connect(
                    host="5.83.218.232",
                    user="vladik",
                    password="cyberworms121315",
                    database="books",
                    auth_plugin='mysql_native_password')
                cursor = connection.cursor(buffered=True)
                print("Подключен к SQLite")
                query = "SELECT * FROM modelen WHERE book_name=%s"
                cursor.execute(query, (book_name,))
                row = cursor.fetchone()
                if not row:
                    print("Not found...")
                    try:
                        transport = paramiko.Transport((host, port))
                        transport.connect(username='root', password='q7nk2o821_p27T14DF_H5A')
                        sftp = paramiko.SFTPClient.from_transport(transport)
                        remotepath = '/var/www/myfreebooksclub.com/static/Image/' + filename
                    
                        open("/Users/cyberworms/Desktop/python/en/" + filename, 'wb').write(r.content)
                        localpath = "/Users/cyberworms/Desktop/python/en/" + filename
                    
                        sftp.put(localpath, remotepath)
                        sftp.close() 
                    except NoSuchElementException: 
                          print("element not found") 
                    add_books = (None, book_name,  author, description, size, data_publication, filename)
                    cursor.execute("INSERT INTO modelen (id, book_name,  author, description, size, data_publication, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", add_books)    
                    connection.commit()
                    print("Запись успешно вставлена ​​в таблицу ", cursor.rowcount)
                    cursor.close()
                    connection.close()
                    print("Соединение  SQLite закрыто")
                    time.sleep(5)
                    book_name = ""
                    author = ""
                    description = ""
                    size = ""
                    data_publication = ""
                    query = ""

                
                else:

                    time.sleep(3)
                    print("Found!")
                    cursor.close()
                    connection.close()
                    print("Соединение  SQLite закрыто")
                    book_name = ""
                    author = ""
                    description = ""
                    size = ""
                    data_publication = ""
                    query = ""
                    
                     
                     


            else:
                 
                try:
                    time.sleep(2)
                    next_button = driver.find_element(By.CSS_SELECTOR,'a.s-pagination-next')
                    next_button.click()
                    print("страница спаршена")
                    list_name = []
                    list_name_model = ""
                    cursor.close()
                    connection.close()
                except NoSuchElementException: 
                    cursor.close()
                    connection.close()
                    list_name = []
                    list_name_model = ""
                    print("element not found")
                    driver.close()
                    driver.get(url)
                break

   
      
