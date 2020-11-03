from selectorlib import Extractor
import requests 
import json 
from time import sleep
import datetime
import sys

e = Extractor.from_yaml_file('selectors.yml')

def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)

    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    return e.extract(r.text)

def createJsonDump():
    with open("urls.txt",'r') as urllist, open('output.json','w') as outfile:
        lineAmount = len(open("urls.txt").readlines())
        print(lineAmount)
        count = 1
        outfile.write("[ \n")
        for url in urllist.readlines():
            data = scrape(url)
            if data:
                json.dump(data,outfile)
                if(count == lineAmount):
                    outfile.write("\n")
                else:
                    outfile.write(", \n")
                    count = count + 1 
        outfile.write("]")

def readJson():
    date = getDate()
    todayDate = (date.day,date.month,date.year)
    with open('output.json', 'r') as f:
        products = json.load(f)
    for product in products:
        print(product['name'],',',product['price'],',',  product['price2'],',', todayDate)


def getDate():
    now = datetime.datetime.now()
    return now

def ScrapeData():
    createJsonDump()
    readJson()

def AddUrl():
    newUrl = input("Enter the URL address:")
    file_object = open("urls.txt", "a")
    file_object.write("\n" +newUrl)
    file_object.close()

def Exit():
    sys.exit("program terminating")

def main():
    while(True):
        print("1. Add URL")
        print("2. Scrape Data")
        print("3. Exit")
        function = input("What would you like to do?")
        if(function == "2"):
            ScrapeData()
        elif(function == "1"):
            AddUrl()
        else:
            Exit()

main()