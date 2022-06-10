import requests
from bs4 import BeautifulSoup
import pandas as pd



# universe (change this for filters)
universe = "https://mlb.candy.com/marketplace/sold-listings?page="



# columns in csv
names = []
tiers = []
prices = []
dates = []
editions = []



# return list of each NFT on page
def getNFTs(soup):
    
    NFTTags = soup.find_all("div", {"class": "w-full pb-4"})
    return NFTTags



# scrapes player name and adds to names column
def getName(soup):
    
    nameTag = soup.find("h1", {"class", "text-white tw-2xl:leading-10 line-clamp-3 text-2xl leading-8"})

    if nameTag is not None:
        names.append(nameTag.contents[0])
    else:
        names.append("na")



# scrapes player tier and adds to tier column
def getTier(soup):
    
    coreTag = soup.find("span", {"class": "bg-tags-core text-white inline-block font-bold px-2 py-1 rounded text-center text-xs uppercase inline-flex"})
    uncommonTag = soup.find("span", {"class": "bg-tags-uncommon text-white inline-block font-bold px-2 py-1 rounded text-center text-xs uppercase inline-flex"})
    rareTag = soup.find("span", {"class": "bg-tags-rare text-white inline-block font-bold px-2 py-1 rounded text-center text-xs uppercase inline-flex"})
    variousTag = soup.find("span", {"class": "holographic text-black inline-block font-bold px-2 py-1 rounded text-center text-xs uppercase inline-flex"})
    epicTag = soup.find("span", {"class": "bg-tags-epic text-white inline-block font-bold px-2 py-1 rounded text-center text-xs uppercase inline-flex"})
    legendaryTag = soup.find("span", {"class": "bg-tags-legendary text-white inline-block font-bold px-2 py-1 rounded text-center text-xs uppercase inline-flex"})
    
    if coreTag is not None:
        tiers.append(coreTag.contents[0])    
    elif uncommonTag is not None:
        tiers.append(uncommonTag.contents[0])  
    elif rareTag is not None:
        tiers.append(rareTag.contents[0])   
    elif variousTag is not None:
        tiers.append(variousTag.contents[0])
    elif epicTag is not None:
        tiers.append(epicTag.contents[0])
    elif legendaryTag is not None:
        tiers.append(legendaryTag.contents[0])
    else:
        tiers.append("na")



# scrapes price and adds to price column (removes "$")
def getPrice(soup):
    
    spanTags = soup.find_all("span", {"class": "text-white text-xl font-normal"})

    if spanTags[0] is not None:
        price = spanTags[0].contents[0].replace("$", "")
        prices.append(price)
    else:
        prices.append("na")



# scrapes transaction date and adds to date column (mm/dd/yyyy format) 
def getDate(soup):
    
    spanTags = soup.find_all("span", {"class": "text-white text-xl font-normal"})
    
    if spanTags[1] is not None:
        dates.append(spanTags[1].contents[0])
    else:
        dates.append("na")



# scrapes number of NFTs in circulation and adds to edition column
def getEdition(soup):
    
    spanTags = soup.find_all("span", {"class": "text-white text-xl font-normal"})

    if spanTags[2] is not None:
        edition = spanTags[2].contents[0].split(" ")[2]
        editions.append(edition)
    else:
        editions.append("na")



# create and return pandas dataframe (using our lists)
def getDataFrame(tiers, names, prices, dates, editions):
    
    df = pd.DataFrame()
    df["tiers"] = tiers
    df["names"] = names
    df["prices"] = prices
    df["dates"] = dates
    df["editions"] = editions
    return df



# display pandas dataframe with a specified number of rows
def previewCSV(dataFrame, numRows=5):
    
    pd.set_option('display.max_columns', None)
    print(dataFrame.head(numRows))



# export dataframe to csv file in the same directory given a filename
def writeCSV(dataFrame, fileName):

    fileName += ".csv"
    dataFrame.to_csv(fileName)



# scrapes website for data (columns above) given a universe url and number of pages to scrape
def scrape(universe, numPages):

    # max pages for mlb.candy is 833 as of 06/10/2022
    for i in range(1, numPages):
        
        page = requests.get(universe + str(i))
        soup = BeautifulSoup(page.text, 'html.parser')

        NFTTags = getNFTs(soup)
        for NFTTag in NFTTags:
            getName(NFTTag)
            getTier(NFTTag)
            getPrice(NFTTag)
            getDate(NFTTag)
            getEdition(NFTTag)



# call scrape() and preview 
scrape(universe, 5)
df = getDataFrame(tiers, names, prices, dates, editions)
previewCSV(df, 20)



# WARNING: writes file, take about 6 minutes per 10,000 rows
#writeCSV(df, candy-data1)


    
