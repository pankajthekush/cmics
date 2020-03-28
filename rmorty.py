from cmics import Comics
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from cmics import download_all_images
import concurrent.futures
comic= Comics()
driver = comic.driver
import os
import glob

def gethomepage(homepage='https://readcomiconline.to/Comic/Rick-and-Morty'):
    comic.gethomepage(link=homepage)
    source = driver.page_source
    soup = BeautifulSoup(source,'html.parser')
    table = soup.find('table',{'class':'listing'})
    allcomicslinks  = table.findAll('a',href=True)
    links =  [ urljoin( driver.current_url, link['href']) for link in allcomicslinks]
    return links
    




def download_comics_pages():
    all_links = gethomepage()
    for link in all_links:
        current_url = driver.current_url
        current_url = link
        issue_number =  current_url.split('/')[-1].split('?')[0].strip()
    
        if not os.path.exists(issue_number+'.csv'):
            comic.gethomepage(link)
            all_images = comic.getallimages()
                
            with open(issue_number+'.csv','a',encoding='utf-8') as f:
                for image_link in all_images:
                    f.write(f'{image_link}\n')
        else:
            print(f'{issue_number} Already Exits')
    


   


def download_whole_issue(issue_name ='Issue-60.csv'):

    fnme = issue_name
    all_image_links =list()
    foldername = fnme.split('.')[0]
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    
    with open(fnme,'r',encoding='utf-8') as f:
        all_image_links = f.readlines()
    
        
    comic.issue_name = foldername
    comic.image_url_list = all_image_links


    with concurrent.futures.ThreadPoolExecutor() as executer:
        executer.map(comic.download_image,all_image_links)

     
    
if __name__ == "__main__":
    #download_comics_pages()
    all_csv = glob.glob('*.csv')
    for csv in all_csv:
        print(f'Started {csv}')
        download_whole_issue(csv)
   