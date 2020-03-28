from slre.slre import RemoteSelenium
from bs4 import BeautifulSoup
import js2py
import requests
import os

import functools

class Comics:
    def __init__(self):
        self.rs = RemoteSelenium()
        self.driver = self.rs.driver
        self.issue_name = None
        self.image_url_list = None

    def gethomepage(self,link):
        self.driver.get(link)
        input("Hit Enter To Continue when page is fully loaded : ")
    
    def evaljs(self,js):
        beginpoint = js.find('var lstImages = new Array();')
        endpoint = js.find('var currImage = 0;')
        jsc = js[beginpoint:endpoint]
        jsc = 'function gelinks() {' + jsc + 'return lstImages'+ '}' 
        jobj = js2py.eval_js(jsc)
        all_links = jobj()
        return all_links

    def getallimages(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        final_script = None
        jscripts = soup.findAll('script')
    
        for sc in jscripts:
            if 'lstImages' in sc.text:
                final_script = sc.text
                break
        alllinks =  self.evaljs(final_script)
        return alllinks


    def download_image(self,image_url):
        print(f'Downloading {image_url}')
        issue_name= self.issue_name
        page_number = self.image_url_list.index(image_url)
        image_name = os.path.join(issue_name, f'{issue_name}-{page_number}.jpg')
        image_url = image_url.strip()
        img_byte = requests.get(image_url).content
        with open(image_name,'wb') as img_file:
            img_file.write(img_byte)
        print(f'Downloaded {image_url}')




def download_all_images(fnme ='Issue-60.csv'):
    
    all_image_links =list()
    foldername = fnme.split('.')[0]
    if not os.path.exists(foldername):
        os.mkdir(foldername)

    with open(fnme,'r',encoding='utf-8') as f:
        all_image_links = f.readlines()


    for i in range(len(all_image_links)):
        image_name = os.path.join(foldername,f'{foldername}-{i}.jpg')
        image_link = all_image_links[i].strip()
        print(image_link)
        img_byte = requests.get(image_link).content
        with open(image_name,'wb') as img_file:
            img_file.write(img_byte)
        
                

        
        





