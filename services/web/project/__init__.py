from flask import Flask, jsonify
import time, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = [
    'https://repositorio.unam.mx/contenidos?f=883.%23.%23.a_lit:Repositorio%20de%20la%20Direcci%C3%B3n%20General%20de%20Bibliotecas%20y%20Servicios%20Digitales%20de%20Informaci%C3%B3n'
]

app = Flask(__name__)


@app.route("/find/<word>")
def hello_world(word):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("window-size=1920x1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get('https://repositorio.unam.mx/contenidos?f=883.%23.%23.a_lit:Repositorio%20de%20la%20Direcci%C3%B3n%20General%20de%20Bibliotecas%20y%20Servicios%20Digitales%20de%20Informaci%C3%B3n')
    time.sleep(0.5)
    print('Buscando')
    search = driver.find_element(by=By.ID,value='input-search')
    search.send_keys(str(word))
    find = driver.find_element(by= By.ID, value='btn-general-buscar')
    find.click()
    time.sleep(0.5)
    print('resultados')
    document = driver.find_element(by= By.CLASS_NAME , value='element-ing-data-record' and 'img-portada')
    print('document')
    document.click()
    time.sleep(1.75)
    openforlink = driver.find_element(by= By.CLASS_NAME, value='cont-link-resource')
    openforlink.click()
    time.sleep(1)
    driver._switch_to.window(driver.window_handles[1])
    table = driver.find_element(by= By.CLASS_NAME, value='table' and 'itemDisplayTable').text
    preLink = table.split('\n')
    numberdocument = preLink[14].replace('Fuente TESIUNAM:  ', '').split('/')
    print(numberdocument)
    link = preLink[14].replace('Fuente TESIUNAM:  ', '').replace('Index.html', numberdocument[4]+'.pdf')
    des= requests.get(link)
    pdf = open(numberdocument[4]+str()+".pdf", 'wb')
    driver.implicitly_wait(10)
    pdf.write(des.content)
    pdf.close()
    driver.close()
    # return des.json()
    return "ok"