from bsedata.bse import BSE
from newsapi import NewsApiClient as nac

s = BSE()
n = nac(api_key="ec672e47cdcd409db8dc987e04aa7251")

def stock():
    try:
        print("Tata Steel and BSE SENSEX values:\n")
        quote = s.getQuote("500055") #tata steel
        print("Tata Steel (500055):")
        print("\tOpen:", quote["previousOpen"])
        print("\tClose:", quote["previousClose"])
        print("\tHigh:", quote["dayHigh"])
        print("\tLow:", quote["dayLow"])
        print("\nBSE SENSEX value:", s.getIndices(category='market_cap/broad')['indices'][0]["currentValue"])
    except IndexError as ier:
        print("Failed to retrieve BSE SENSEX/TATA STEEL PVT LTD data, try after sometime.\nKeep the interval between requests greater than 5 sec")
    print("\n\n")

def news():
    print("\n\nTop 5 News Headlines:\n")
    news = n.get_top_headlines(language="en", country="in")
    for article in news['articles'][:5]:
        print("**************************************************************")
        print("News Title:", article["title"])
        print("New Description:", article["description"])
        print("News URL:", article["url"])
        print("**************************************************************\n") 
    print("\n")

stock()
news()
