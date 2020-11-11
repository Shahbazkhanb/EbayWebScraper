from bs4 import BeautifulSoup
import requests as rq
import csv
from os import path as pt
import time

def pageurls(url):
    """
    Extracts all the links on a search page (from the given url) and collects them into a list
    """

    req = rq.get(url)
    html = req.text
    soup = BeautifulSoup(html, "lxml")

    datalinks = []
    links = soup.find_all("a", class_ = "s-item__link")
    
    datalinks = [i.get("href") for i in links]
    return datalinks


def items(url):
    """
    Takes a link from the list returned from the function "pageurls" and collects item information 
    from product info page and returns a dictionary of item details
    """

    req = rq.get(url)
    html = req.text
    soup = BeautifulSoup(html, "lxml")

    try:
        title = soup.find("span", id = "vi-lkhdr-itmTitl").text.strip()
    except:
        title = ""
    try:
        try:
            currency, price = soup.find("span", class_ = "notranslate", id = "prcIsum").text.strip().replace("$","").replace("\xa0","").split(" ")
        except:
            currency, price = soup.find("span", itemprop = "price").text.strip().replace("$","").replace("\xa0","").split(" ")
    except:
        currency, price = ["",""]

    try:
        sold = soup.find("a", class_ = "vi-txt-underline").text.strip().split(" ")[0]
    except:
        sold = "N/A"

    dictionary = {
        "Title":title, 
        "Currency": currency, 
        "Price":price,
        "Sold": sold,
        "Url": url
        }
    return(dictionary)

def csv_write(data, path):
    """
    Writes the data from the dictionary produced from the funtion 'items' to a csv file
    """

    with open(path, "a", newline = "", encoding = "utf-8") as csvfile:
        writer = csv.writer(csvfile)
        row = [data["Title"], data["Currency"], data["Price"], data["Sold"], data["Url"]]

        writer.writerow(row)

def final_write(url, path):
    """
    takes an input url, returns all the links from a search page, writes each product to a csv
    """
    urls = pageurls(url)

    for i in urls:
        data = items(i)
        csv_write(data, path)

def collate():
    """
    Asks for the item the user would like info on, which directory to output results and then iterates the csv writing of the previous functions for the number 
    of search result pages the user defines. Then outputs using the user defined path
    """

    item = input("What would you like to search for")

    exiter = True

    while exiter == True:
        pathtest = input("Enter the path you would like the file to input") 
        try:
            if pt.exists(pt.normpath(pathtest)):
                path = pt.normpath(pathtest) + "\\results.csv"
                exiter = False
            else:
                print("lets try again, that path doesnt exist")
        except:
            print("Wrong format! please use '\' to separate directories and files in file path \n for example type the file path like this (no quotes): 'C:/Users/User/Desktop'")

          
    pages = int(input("Enter the number of search pages you'd like to scrape - I reccommend 10 pages or less else this will be a lengthy runtime"))

    print("Please wait while we fetch results")
    
    start_time = time.time()

    initializer = "https://www.ebay.ca/sch/i.html?_from=R40&_nkw=" + item + "&LH_BIN=1&_pgn=1"

    with open(path, "a", newline = "", encoding = "utf-8") as csvfile:
        writer = csv.writer(csvfile)
        row = ["Title", "Currency", "Price", "Number Sold", "Url"]
        writer.writerow(row)
        
    for i in range(1,(pages + 1)):
        url = initializer
        urlusable = url[:url.rfind("1")] + str(i)
        final_write(urlusable, path)
    
    print("Results complete! \n That took %s seconds to collect that info. Damn slow!" %round(time.time() - start_time, 2))


collate()