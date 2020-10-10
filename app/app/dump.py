import json
import time
from predictors import SentimentIntensityClassifier, preprocessor, StockLowRegressor, StockHighRegressor
import pandas as pd


class NewsHeadlines:
    s = SentimentIntensityClassifier()

    def __init__(self):
        self.df = pd.read_csv("simulation_datasets\\news.csv")
        self.j=0

    @classmethod
    def sic(cls, news):
        return int(cls.s.predict([news])[0])

    @staticmethod
    def getData(headlines, predictions):
        return {"headline"+str(i):{headline:prediction} for i, (headline, prediction) in enumerate(zip(headlines, predictions), 1)}

    def getNews(self):
        news, preds = [], []
        for i in range(5+self.j, 0+self.j, -1):
            news.append("=> "+self.df.Headlines[i])
            preds.append(NewsHeadlines.sic(self.df.Headlines[i]))
        self.j+=1
        return self.getData(news, preds)


class StockQuotes:
    slr = StockLowRegressor()
    shr = StockHighRegressor()

    def __init__(self, stocks_per_file=100):
        self.bse_df = pd.read_csv(".\\simulation_datasets\\BSEForDate.csv")
        self.bse_df.drop(list(set(self.bse_df.keys()) - {'Date', 'Open', 'High', 'Low', 'Close'}), axis=1, inplace=True)
        self.comp_df = pd.read_csv(".\\simulation_datasets\\tata_steel.csv")
        self.comp_df.drop(list(set(self.comp_df.keys()) - {'Date', 'Open Price', 'High Price', 'Low Price', 'Close Price'}), axis=1, inplace=True)
        if(stocks_per_file > int(len(self.bse_df))):
            stocks_per_file =  int(len(self.bse_df))
        self.bse_df = self.bse_df[:stocks_per_file].copy()
        self.comp_df = self.comp_df[:stocks_per_file].copy()
        self.bse_i = 0
        self.comp_i = 0

    def getBseStocks(self):
        stocks = [list(self.bse_df.keys())]
        stocks.extend(self.bse_df.values.tolist()[:self.bse_i+1])
        stocks = list(map(lambda x: [x[0], x[2], x[3]], stocks))
        curr = self.bse_df.values.tolist()[self.bse_i][1:-1]
        
        for i in range(self.bse_i+1, int(len(self.bse_df.index))):
            pred_high = round(StockQuotes.shr.predict([[curr[0], curr[2]]])[0], 2)
            pred_low = round(StockQuotes.slr.predict([[curr[0], curr[1]]])[0], 2)
            stocks.append([str(self.bse_df['Date'][i]), pred_high, pred_low])
            curr = [self.bse_df.values.tolist()[i][1], pred_high, pred_low]
        
        curr = self.bse_df.values.tolist()[self.bse_i][1:]
        stocks = {'data': stocks, 
                  'current': {'open' :curr[0], 
                              'high' :curr[1], 
                              'low'  :curr[2], 
                              'close':curr[3]
                              }
                 }
        
        self.bse_i+=1
        return stocks

    def getCompanyStocks(self):
        stocks = [list(self.bse_df.keys())]
        stocks.extend(self.comp_df.values.tolist()[:self.comp_i+1])
        stocks = list(map(lambda x: [x[0], x[2], x[3]], stocks))
        curr = self.comp_df.values.tolist()[self.comp_i][1:-1]
        
        for i in range(self.comp_i+1, int(len(self.comp_df.index))):
            pred_high = round(StockQuotes.shr.predict([[curr[0], curr[2]]])[0], 2)
            pred_low = round(StockQuotes.slr.predict([[curr[0], curr[1]]])[0], 2)
            stocks.append([str(self.comp_df['Date'][i]), pred_high, pred_low])
            curr = [self.comp_df.values.tolist()[i][1], pred_high, pred_low]
       
        curr = self.comp_df.values.tolist()[self.comp_i][1:]
        stocks = {'data': stocks, 
                  'current': {'open' :curr[0], 
                              'high' :curr[1], 
                              'low'  :curr[2], 
                              'close':curr[3]
                             }
                 }
        
        self.comp_i+=1
        return stocks


def dumpData():
    STOCKS_PER_FILE = 100 #max 100 days forecast
    DUMP_INTERVAL = 5 #5 secs interval between updates
    COMPANY_NAME = "tata steel bsl ltd"
    news = NewsHeadlines()
    stocks = StockQuotes(stocks_per_file=STOCKS_PER_FILE)
    
    for i in range(STOCKS_PER_FILE):
        json.dump(stocks.getBseStocks(), open("./predicted files/market_index.json", "w"))
        json.dump(stocks.getCompanyStocks(), open("./predicted files/{}.json".format(COMPANY_NAME), "w"))
        json.dump(news.getNews(), open("./predicted files/headlines.json", "w"))
        time.sleep(DUMP_INTERVAL)
