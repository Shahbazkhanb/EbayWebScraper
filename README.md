# Ebay Web Scraper

Here I tried my first hand at using Python's Requests and BeautifulSoup libraries to scrape product info for items listed on ebay.com (specifically the buy it now section - not items on auction) 
  
The inspiration for this project came from this video (https://www.youtube.com/watch?v=m4hEAhHHykI) and i tried to add my own flair!  
  
The program will ask what item you want to search for on Ebay, where you want the results file to output and how many pagess of informaton to scrape the information (item title, currency item is in, pricce of item and number sold) from. It will then compile the data to a CSV file called "results.csv" in the location that you specify.
  
I know the program is quite slow (its making a lot of requests to different pages on ebay); averaging around 45 seconds per search page of data, so if you have any improvements at all please feel free to add!
