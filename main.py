#TODO Fix the part about checking for a quote instead of the whole option chain
#TODO Maybe remove the first check for connectivity

#class TestTransaction():
    #symbol = '"'
    #askSize = ""
    #def createTDA(self, eachStrike, strike):
        #strikeElements = strike[eachStrike]
        #self.askSize = strikeElements[0]['askSize']
        #print('askSize')
        #print(self.askSize)
#
#def update():
    #chainPEDM = {'2019-11-01:5': {'125.0': [{'putCall': 'PUT', 'symbol': 'MMM_110119P125', 'description': 'MMM Nov 1 2019 125 Put (Weekly)', 'exchangeName': 'OPR', 'bid': 0.0, 'ask': 0.13, 'last': 0.04, 'mark': 0.07, 'bidSize': 0, 'askSize': 41, 'bidAskSize': '0X41', 'lastSize': 0, 'highPrice': 0.0, 'lowPrice': 0.0, 'openPrice': 0.0, 'closePrice': 0.0, 'totalVolume': 0, 'tradeDate': 'None', 'tradeTimeInLong': 1571925760082, 'quoteTimeInLong': 1572033567836, 'netChange': 0.04, 'volatility': 89.06, 'delta': -0.009, 'gamma': 0.001, 'theta': -0.036, 'vega': 0.006, 'rho': 0.0, 'openInterest': 7, 'timeValue': 0.04, 'theoreticalOptionValue': 0.065, 'theoreticalVolatility': 29.0, 'optionDeliverablesList': 'None', 'strikePrice': 125.0, 'expirationDate': 1572656400000, 'daysToExpiration': 5, 'expirationType': 'S', 'lastTradingDay': 1572580800000, 'multiplier': 100.0, 'settlementType': ' ', 'deliverableNote': '', 'isIndexOption': 'None', 'percentChange': 39600.0, 'markChange': 0.06, 'markPercentChange': 64900.0, 'inTheMoney': 'False', 'mini': 'False', 'nonStandard': 'False'}], '130.0': [{'putCall': 'PUT', 'symbol': 'MMM_110119P130', 'description': 'MMM Nov 1 2019 130 Put (Weekly)', 'exchangeName': 'OPR', 'bid': 0.0, 'ask': 0.03, 'last': 0.05, 'mark': 0.02, 'bidSize': 0, 'askSize': 4, 'bidAskSize': '0X4', 'lastSize': 0, 'highPrice': 0.0, 'lowPrice': 0.0, 'openPrice': 0.0, 'closePrice': 0.0, 'totalVolume': 0, 'tradeDate': 'None', 'tradeTimeInLong': 1571751475087, 'quoteTimeInLong': 1572010220604, 'netChange': 0.05, 'volatility': 65.784, 'delta': -0.003, 'gamma': 0.001, 'theta': -0.01, 'vega': 0.002, 'rho': 0.0, 'openInterest': 51, 'timeValue': 0.05, 'theoreticalOptionValue': 0.015, 'theoreticalVolatility': 29.0, 'optionDeliverablesList': 'None', 'strikePrice': 130.0, 'expirationDate': 1572656400000, 'daysToExpiration': 5, 'expirationType': 'S', 'lastTradingDay': 1572580800000, 'multiplier': 100.0, 'settlementType': ' ', 'deliverableNote': '', 'isIndexOption': 'None', 'percentChange': 46600.0, 'markChange': 0.01, 'markPercentChange': 14900.0, 'inTheMoney': 'False', 'mini': 'False', 'nonStandard': 'False'}]}}

    #xaction = TestTransaction()
    #xaction.symbol = 'MMM'

    #listToPut = []
    #for eachDate in chainPEDM.keys():
        #strikeDate = eachDate[0:10]
        #print('strikeDate')
        #print(strikeDate)
        #strike = chainPEDM[eachDate]
        #print('strike')
        #print(strike)
        #print(strike.keys())
        #for eachStrike in strike.keys():
            #xaction = TestTransaction()
            #xaction.symbol = 'MMM'
            #print('eachStrike')
            #print(eachStrike)
            #xaction.createTDA(eachStrike, strike)
            #listToPut.append(xaction)
            #print('len(listToPut)')
            #print(len(listToPut))
            #print(listToPut)
        #for item in listToPut:
            #print(item.askSize)
#
#UD = update()
#exit(0)

### END PRACTICE AREA

#!/usr/bin/env python3
# Copyright 2019 Bryan Chase

from urllib.request import Request, urlopen
from time import sleep
#import urllib.request
#import urllib.parse
import json
import logging

logger = logging.getLogger('bmc')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
logger.debug('log debug')
logger.info('log info')
logger.warning('log warning')

class GetAuthorized():
    """Class to get authorization from TDA"""
    def __init__(self):
        print('GetAuthorized')
        self.client_id_key_tdameritrade = '2HYD7NRWUCZZ7GU3GOU7H1RFCXWQ22KS' # Client ID / Consumer Key for BMCApp1

        # Get authorized (get POST access token)

        import requests
        address = 'https://api.tdameritrade.com/v1/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': '4rUwAtxbGNh6nEry9dMntUeVc2Qp+WTqR2I0WAYdJQmqiIb6z5siLh2K2wDOPCEXbItU/Te97plW7JVETZZaVLtNPFAjzou7pF3xUFN9NWOaiUCF0wqCjm3bPAcXCu9yE9S4jVN7oa4baEDLofChcE9V7B2bPzlEaFpUl9TKTeZRRIIjHZmAKasJTaftEF/Qph5Gn0EM7o5Em+vkcEcJwHWjN2yQxWJOoDCFdGbJRn8STlYx6lSRNFon+sHfyc/kvJO7kY85Lz1ck0wlkCEgkk3uNMvVRCAM2QQEzwgaCx89PYSEF4WnU0PHv+HCdRdXqxcqmLXpsBxEJDapnJp2LiD2jSIZAce/z5aaEyLkS9zkuZljiUMNC/7HYODRQBiZ4fdnimS2fnXoVHLrRDXCSLimr5+HiNHRzZyPbRmnhWtvC+FRO1v+rNUHQxe100MQuG4LYrgoVi/JHHvl6XIT8ZYOtUDkBEHu0aPE/D1TLZbTp64VKpn+0WKTbifuxULUIwxAA5Mm0hQbC0IgC3OwFcSeuV/SHown4g0jjiQ3bWddNoIHFFNcaGjTBmFQl5lCW7efOGW9kyUpn60EgU7xmQQlPAZhHy0QI0qcv3tb8/CPSuFP7vh83tRVGPQ3fbfL6GPOx8P2JFuK64CjLxxJ7sYKeV5eTR4rBwoctSLI6qPKr5jnZNKbZainlWDnmGvDsC428EK8nG4qmj2iBN42ds0RFn0sbEK8AkIOudMifEfef17/wQK44LhASSsh5Jsz/wGhGb6GqNCZ3ksvcqNaLki9tGjz7CE/Ttbnk2N5xpCxN+lxXFHvDhrTNDiBSCcbJQ+7jH2Xz7jHfyqNttAKr91tAMBKmPYgTBwddPun8Mvf9aroUSSM9pse/dJn+8l0EzbmHfENu5Q=212FD3x19z9sWBHDJACbC00B75E',
            'access_type': '',
            'code': 'MOLXZowDpB0VbxmTNkl7wa6QkDSMVvRPmn%2FhasJX1qkzW10hj928LySeb%2BB7S5Rk29t8pL%2B68KeNqpopEpGYBPsoNsRdmz3rKXBLxEjxlXlSAMa6YPbCJIHJa7ZI2LtqoJZ1Y0IKZZem4EkEvUr1XuZHfZHRZmqO4S8ma%2BGmX4z0qH84IFkqHQe3eVi1%2FPgJobN0LZ8ITpaWRSHnS8lp1B8RDzPieFLEuIhipCrsjhhEkp%2F5bhY6EH7Mvj86B%2BIRL%2FYyxOXOnM%2Bh5nTaJSXsAyJcKxas3g3AdK%2BC0yRvvltG%2BGBU1ZN2X%2BEqVo%2Bi1X85nrDjz0Q9Q0v0w%2FZ%2BLc%2BjZg%2FaQmeVVw76Ahx8D4DfAJuuBOZhGdpFAHIfv8u5jRtZ2b0ZjSA9sU57qDXirvdi2s7P20TmvPSyldisNkk%2FKOcsiX3HY5RFFblXs3c100MQuG4LYrgoVi%2FJHHvlbfxsCZS71cclwp5AWekBkfr%2FWo2XTGiRe0aWRpyC%2B56lb99iVT1bUuBOUDcDg6Aask7ujUXNhaGL9SbaYaHCmOekvz9%2FHEUMijqohUwSYIBaYHBL3wlKzOmlO7woF2ZnuS5Za23vXMhbrF0IaVK9UTIVCBu4QoWfsv%2B0iWJdJdbptAYS%2FehiLBYs1cAgLP0j7DakD4JEjyvRIGkZnJtsDp4585lWGGioYTBSlguiCsdAagTLVu3dN9j5dVIf4inGs3%2FFj%2FufENJ2ImEJwVhNkFcd9yIDzETUrXpaSB0u75oPVwNkHkyyC2ngGk6pmE8WZcGlakPK80ORd8Mnxos5NZol6ZDmJX3%2BO8DrAnpPwJXlQZSX90pxW2p6T2PMR4om5yI57oYTtToBvgh%2B0ORLBBumqpYIPZyQuoYBZHD6SF%2BgSU%2Fi%2FcYcBUh3NNo%3D212FD3x19z9sWBHDJACbC00B75E',
            'client_id': '2HYD7NRWUCZZ7GU3GOU7H1RFCXWQ22KS',
            #'redirect_uri': 'http://localhost'
            'redirect_uri': 'http%3A%2F%2Flocalhost'
        }
        response = requests.post(address, headers=headers, data=data)
        #print(response)
        content = json.loads(response.content.decode('utf-8'))
        #print(content)
        self.access_token = content['access_token']
        #print(self.access_token)
        token_type = content['token_type']
        #print(token_type)
        #print(response.headers)
        #print(response.request)


    def GetChain(self,ticker):
        #Get a quote just to test it
        print('GetChain')
        #ticker = 'MMM'
        urlpath1 = "https://api.tdameritrade.com/v1/marketdata/chains"
        api_key = '?api_key=' + self.client_id_key_tdameritrade
        tail = '&symbol=' + ticker
        urlFullPath = urlpath1 + api_key + tail
        #print(urlFullPath)
        self.bearer_header = 'Bearer' + ' ' + self.access_token
        #print(self.bearer_header)
        req = Request(urlFullPath)
        req.add_header('Authorization', self.bearer_header)
        r = urlopen(req).read()
        #print(r)
        d = r.decode('utf-8')
        e = json.loads(d)
        return e
        #print(e) # It better print out a successful value

class PracticGet():
    """ Get ticker data from the web """

    def getOptionsListTDA(self, ticker, client_id, access_token):
        print('PracticeGet:getOptionsListTDA')
        urlpath1 = "https://api.tdameritrade.com/v1/marketdata/chains"
        api_key = '?api_key=' + client_id
        tail = '&symbol=' + ticker
        urlFullPath = urlpath1 + api_key + tail
        print('getOptionsListTDA')
        #print(urlFullPath)
        bearer_header = 'Bearer ' + access_token
        #print(bearer_header)
        req = Request(urlFullPath)
        req.add_header('Authorization', bearer_header)
        r = urlopen(req).read()
        #print(r)
        d = r.decode('utf-8')
        e = json.loads(d)
        #print(e)
        return e

ga = GetAuthorized()

P1 = PracticGet()
P1.getOptionsListTDA('MMM', ga.client_id_key_tdameritrade, ga.access_token)

####### END PRACTICE AREA

import logging
import urllib
import urllib.parse # 3.7
import json
from time import sleep
from datetime import datetime, timedelta
from google.cloud import ndb
from flask import Flask, render_template, request, escape, redirect

app = Flask(__name__)

#logging.basicConfig(filename='locallog.txt')
#logging.basicConfig(level=logging.INFO)
#logging.info('Hello Log World')

#Intrinio API Keys:
#Sandbox: OmU4NTM0OWI2MTI3ZTkzYmYzYjllNzE5ZWM0NWVjMDlh
#Production: OjIyNmY5OWJlODUzNDk1NTAwYzZlMzI0NzM2NjM4MTFh

#api_key_intrinio = 'OmU4NTM0OWI2MTI3ZTkzYmYzYjllNzE5ZWM0NWVjMDlh'
api_key_tdameritrade = '2HYD7NRWUCZZ7GU3GOU7H1RFCXWQ22KS' # Consumer Key for BMCApp1

DEFAULT_XACTIONBOOK_NAME = 'default_xactionbook'

dashboardContentCall = [
    ('Symbol', 'Sym', '%s', 'Yes'),
    ('MyQty', 'My Qty', '%.0f', 'No'),
    ('MyCost', 'My Cost', '%.0f', 'No'),
    ('MyCostPerShare', 'My Cost/Sh', '%.2f', 'No'),
    ('LastStockPrice', 'Last Shr', '%.2f', 'No'),
    ('LastOptionPrice', 'Last Opt', '%.2f', 'No'),
    ('ChgToday', 'Chg Today', '%.2f', 'No'),
    ('Contracts', 'Ctrs', '%.0f', 'No'),
    ('ContractDate', 'Exp Date', '%s', 'No'),
    ('OpenInt', 'OI', '%0.f', 'No'),
    ('Strike', 'Strike', '%.1f', 'No'),
    # ('PutMaintenance', 'Put Mtnc', '%.0f', 'No'),
    ('CostBid', 'Bid', '%.2f', 'No'),
    ('CostAsk', 'Ask', '%.2f', 'No'),
    ('IncomeBid', 'Inc Bid', '%.0f', 'No'),
    ('IncomeAsk', 'Inc Ask', '%.0f', 'No'),
    ('ProfitBid', 'Profit Bid', '%.0f', 'Yes'),
    ('ProfitAsk', 'Profit Ask', '%.0f', 'Yes'),
    ('ROIForOneBid', 'ROI/1 Bid%', '%.1f', 'Yes'),
    ('ROIForOneAsk', 'ROI/1 Ask%', '%.1f', 'Yes'),
    ('IncPerYearBid', 'IPY Bid', '%.0f', 'Yes'),
    ('IncPerYearAsk', 'IPY Ask', '%.0f', 'Yes'),
    ('ROIPerYearBid', 'ROI/Yr Bid%', '%.1f', 'Yes'),
    ('ROIPerYearAsk', 'ROI/Yr Ask%', '%.1f', 'Yes'),
    ('QF', 'QF', '%.1f', 'Yes')
]

dashboardContentPut = [
    ('Symbol', 'Sym', '%s', 'Yes'),
    ('MyQty', 'My Qty', '%.0f', 'No'),
    ('MyCost', 'My Cost', '%.0f', 'No'),
    ('MyCostPerShare', 'My Cost/Sh', '%.2f', 'No'),
    ('LastStockPrice', 'Last Shr', '%.2f', 'No'),
    ('LastOptionPrice', 'Last Opt', '%.2f', 'No'),
    ('ChgToday', 'Chg Today', '%.2f', 'No'),
    ('Contracts', 'Ctrs', '%.0f', 'No'),
    ('ContractDate', 'Exp Date', '%s', 'No'),
    ('OpenInt', 'OI', '%0.f', 'No'),
    ('Strike', 'Strike', '%.1f', 'No'),
    ('PutMaintenance', 'Put Mtnc', '%.0f', 'No'),
    ('CostBid', 'Bid', '%.2f', 'No'),
    ('CostAsk', 'Ask', '%.2f', 'No'),
    ('IncomeBid', 'Inc Bid', '%.0f', 'No'),
    ('IncomeAsk', 'Inc Ask', '%.0f', 'No'),
    ('ProfitBid', 'Profit Bid', '%.0f', 'Yes'),
    ('ProfitAsk', 'Profit Ask', '%.0f', 'Yes'),
    ('ROIForOneBid', 'ROI/1 Bid%', '%.1f', 'Yes'),
    ('ROIForOneAsk', 'ROI/1 Ask%', '%.1f', 'Yes'),
    ('IncPerYearBid', 'IPY Bid', '%.0f', 'Yes'),
    ('IncPerYearAsk', 'IPY Ask', '%.0f', 'Yes'),
    ('ROIPerYearBid', 'ROI/Yr Bid%', '%.1f', 'Yes'),
    ('ROIPerYearAsk', 'ROI/Yr Ask%', '%.1f', 'Yes'),
    ('QF', 'QF', '%.1f', 'Yes')
]

class Fee(object):
    """Class containing various fees and taxes"""
    #i = 123
    def __init__(self):
        self.trade = 10.85
        self.taxCA = 0.095
        self.taxFED = 0.395

class TransactionNDB(ndb.Model):
    """A main model for representing an individual stock ticker."""
    symbol = ndb.StringProperty(indexed=True)
    #companyName = ndb.StringProperty(indexed=False)
    lastOptionPrice = ndb.FloatProperty(indexed=False)
    lastStockPrice = ndb.FloatProperty(indexed=False)
    optionChange = ndb.FloatProperty(indexed=False)
    volume = ndb.FloatProperty(indexed=False)
    bid = ndb.FloatProperty(indexed=False)
    ask = ndb.FloatProperty(indexed=False)
    openInt = ndb.FloatProperty(indexed=False)
    strikePrice = ndb.FloatProperty(indexed=False)
    strikeMonth = ndb.StringProperty()
    strikeDate = ndb.DateProperty(indexed=False)
    strikeMonthNum = ndb.IntegerProperty(indexed=False)
    strikeYear = ndb.IntegerProperty(indexed=False)
    optionType = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    pastPnL = ndb.FloatProperty(indexed=False, default=0.00)

    def createTDA(self, eachStrike, strike):
        #for eachDate in chain.keys():
            ##self.strikeDate = each[0:10]
            ##print(self.strikeDate)
            #strikeDate = eachDate[0:10]
            #print(strikeDate)
            #strike = chain[eachDate]
            ##print(strikeDate)
            ##print(strike)
            #listToPut = []
            #for eachStrike in strike.keys():
        #print(eachStrike)
        strikeElements = strike[eachStrike]
        #print(strikeElements)
        self.lastOptionPrice = strikeElements[0]['last']
        self.optionChange = strikeElements[0]['delta']
        print('delta')
        print(self.optionChange)
        self.volume = strikeElements[0]['totalVolume']
        #print(self.volume)
        self.bid = strikeElements[0]['bid']
        self.ask = strikeElements[0]['ask']
        self.openInt = strikeElements[0]['openInterest']
        self.strikePrice = strikeElements[0]['strikePrice']
        expDate = strikeElements[0]['expirationDate'] / 1000
        expDate_dt = datetime.fromtimestamp(expDate)
        self.strikeDate = expDate_dt
        self.strikeMonth = expDate_dt.strftime("%b")
        self.optionType = strikeElements[0]['putCall']
        #print(self.optionType)

        #print(strikeElements[0]['bid'])
        #print(strikeElements[0]['ask'])
        #print(strikeElements[0]['totalVolume'])
        #print(strikeElements[0]['openInterest'])

    def create(self, callOrPut, type):
        from time import strptime

        callOrPutArray = callOrPut.split(',')
        # If the length of the call or put entry is 13 the#n it's missing
        # the CS and CP elements. So, to index to the others, add 2.
        if (len(callOrPutArray) == 13):
            oRecordOffset = 0
        elif (len(callOrPutArray) == 15):
            oRecordOffset = 2
        else:
            oRecordOffset = 0
            print("ERROR: Option record not 13 or 15 length. Check the source file from the website.")
        # logging.info("oRecordOffset: " + oRecordOffset.__str__())
        # logging.info("Length of callOrPutArray: " + len(callOrPutArray).__str__())

        self.lastOptionPrice = self.conv(callOrPutArray[4])
        self.optionChange = self.conv(callOrPutArray[5 + oRecordOffset/2]) # add only 1 if it's longer
        self.volume = self.conv(callOrPutArray[9 + oRecordOffset])
        self.bid = self.conv(callOrPutArray[6 + oRecordOffset])
        self.ask = self.conv(callOrPutArray[7 + oRecordOffset])
        self.openInt = self.conv(callOrPutArray[8 + oRecordOffset])
        self.strikePrice = self.conv(callOrPutArray[10 + oRecordOffset])
        self.strikeMonth = callOrPutArray[11 + oRecordOffset].split('"')[1][0:3]
        # logging.info("|| self.strikeMonth")
        # logging.info(self.strikeMonth)
        # logging.info(strptime(self.strikeMonth,'%b').tm_mon)

        self.strikeMonthNum = strptime(self.strikeMonth,'%b').tm_mon
        self.strikeYear = int(callOrPutArray[12 + oRecordOffset].split('"')[0][1:5])
        self.optionType = type
        # logging.info('|| self.strikeMonth, self.strikeYear')
        # logging.info(self.strikeMonth)
        # logging.info(self.strikeYear)
        self.strikeDate = datetime.strptime(self.strikeMonth + " " +
                                            str(thirdFriday(self.strikeYear, self.strikeMonthNum)) + " " +
                                            str(self.strikeYear), '%b %d %Y')
        #self.lastStockPrice = float(list[list.find('price')+6:-1])

    def conv(self, x):
        # logging.info("conv1")
        if (len(x) == 0):
            # logging.info("conv1.1")
            return 0
        else:
            # logging.info("conv1.2")
            # logging.info(x)
            # logging.info(x.split('"')[1])
            try:
                a = float(x.split('"')[1])
                return a
            except:
                if (x.split('"')[1] == '-'):
                    return 0
                else:
                    return -1

class TickerNDB(ndb.Model):
#class TickerNDB(ndb.Client):
    """A main model for storing tickers we are interested in."""
    symbol = ndb.StringProperty()
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    color = ndb.StringProperty(default='white')
    colorShow = ndb.BooleanProperty(indexed=False)
    myQty = ndb.FloatProperty(indexed=False)
    myCost = ndb.FloatProperty(indexed=False)
    myAcqDate = ndb.DateProperty(indexed=False)
    pnl = ndb.FloatProperty(indexed=False)
    shareChange = ndb.FloatProperty(indexed=False)

class SortColumn():
    #''' Select which column will be used for sorting, and reload
    #'''

    def setSC(self, sC):
        self.sortColumn = sC

#class PropFromSymbol():
    ## Get the given property value from the symbol
    #def pfs(self, symbol, property):
        ##logging.info("|| PropfromSymbol")
        ##print(symbol, property)
#
        #with mynclient.context():
            #ticker_query = TickerNDB.query(
                #TickerNDB.symbol == symbol )
            ## logging.info("|| pfs:ticker_query")
            ## logging.info(ticker_query)
#
            #entity = ticker_query.get()  # Get the entity with that symbol
            ##print(entity)
            ##logging.info("|| pfs:entity")
            ##logging.info(entity)
#
        ## entity.symbol
        ## logging.info("|| pfs:entity.symbol")
        ## logging.info(entity.symbol)
#
        ## logging.info(dir(entity))
#
        ## logging.info(getattr(entity, property))
        #return getattr(entity, property)

class PropFromSymbolLocal():
    # Get the given property value from symbol, 1 DB access

    def bringlocal(self): # Bring info into a local dictionary
        self.TickerLocal = []

        with mynclient.context():
            #b = TickerNDB()
            ticker_query = TickerNDB.query()
            self.localfetch = ticker_query.fetch() # Get everything
            for ticker in self.localfetch:
                entry = {'symbol' : ticker.symbol,
                         'myQty' : ticker.myQty,
                         'myCost' : ticker.myCost,
                         'colorShow' : ticker.colorShow,
                         'myAcqDate' : ticker.myAcqDate}
                #print(entry)
                self.TickerLocal.append(entry)
            #print('TickerLocal: '+ self.TickerLocal.__str__())
            #print(self.TickerLocal.__class__)

    def pfs(self, symbol, property): # Look up from local version
        #print('symbol: ' + symbol)
        #print('property ' + property)
        #print(self.TickerLocal)
        #print(len(self.TickerLocal))
        #sleep(0.2)
        retprop = None
        for t in range(len(self.TickerLocal)):
            #print(t)
            if (self.TickerLocal[t]['symbol'] == symbol):
                retsymbol = symbol
                retprop = self.TickerLocal[t][property]
        #print(retsymbol)
        #print(retprop)
        return retprop

    def deleteTicker(self, tickerToRemove):
        with mynclient.context():
            entityQ = TickerNDB.query(TickerNDB.symbol == tickerToRemove)
            entity = entityQ.get()
            entity.key.delete()

class GetTicker():
    """ Get ticker data from the web """

    def getOptionsListTDA(self, ticker, client_id, access_token):
        print('GetTicker:getOptionsListTDA')
        urlpath1 = "https://api.tdameritrade.com/v1/marketdata/chains"
        api_key = '?api_key=' + client_id
        tail = '&symbol=' + ticker
        urlFullPath = urlpath1 + api_key + tail
        print('getOptionsListTDA')
        #print(urlFullPath)
        bearer_header = 'Bearer ' + access_token
        #print(bearer_header)
        req = Request(urlFullPath)
        req.add_header('Authorization', bearer_header)
        try:
            r = urlopen(req).read()
        except urllib.error.HTTPError as e:
            logging.info('HTTPError = ' + str(e.code))
            print('HTTPError = ' + str(e.code))
            # except urllib2.URLError, e: # python 2.7
        except urllib.error.URLError as e:  # python 3.7
            logging.info('URLError = ' + str(e.reason))
            print('URLError = ' + str(e.reason))
            # except httplib.HTTPException, e: # python 2.7
            # logging.info('HTTPException')
        except Exception:
            import traceback
            logging.info('generic exception: ' + traceback.format_exc())
            print('generic exception: ' + traceback.format_exc())
        else:
            d = r.decode('utf-8')
            e = json.loads(d)
            #print(e)
            return e

    #def getContentOne(self, ticker):
        ##https: // api - v2.intrinio.com / options / chain / {symbol} / {expiration}
        ##tail = '&output=json'
        #tail = '?api_key=' + api_key_intrinio
        ##urlpath1 = 'http://www.google.com/finance/option_chain?q='
        #urlpath1 = 'https://api-v2.intrinio.com/options/'
        ## urlpath1 = 'https://www.google.com/finance?q=NASDAQ%3AACET&output=json'
        #self.valid = -1  # default to not tradeable, set it with tryTheLink
        #self.tryTheLink(urlpath1, ticker, tail)
        ##if self.valid:
            #self.getExpirations()

    #def getContentDate(self, ticker, date):
        ## Format is: http://www.google.com/finance/option_chain?q=watt&expd=4&expm=4&expy=2014&output=json
        ##expy = '&expy=' + date.split(',')[0][2:]
        ##expm = '&expm=' + date.split(',')[1][2:]
        ##expd = '&expd=' + date.split(',')[2][2:]
##
        ##tail = expd + expm + expy + '&output=json'
        #tail = '?api_key=' + api_key_intrinio
        ##urlpath1 = 'http://www.google.com/finance/option_chain?q='
        #urlpath1 = 'https://api-v2.intrinio.com/options/'
        #self.valid = -1  # default to not tradeable, set it with tryTheLink
        #self.tryTheLink(urlpath1, ticker, tail)
        ## if self.valid:
        ##     self.getExpirations()

    #def tryTheLink(self, path, ticker, tail):
        #urlpath = path + ticker + tail
        #logging.info(urlpath)
        #print('GetTicker Trying Link:')
        ##print (urlpath)
#
        #try:
            ##response = urllib2.urlopen(urlpath) #python 2.7
            #response = urllib.request.urlopen(urlpath) #python 3.7
        ##except urllib2.HTTPError, e: # python 2.7
        #except urllib.error.HTTPError as e: # python 3.7
            #logging.info('HTTPError = ' + str(e.code))
            #print('HTTPError = ' + str(e.code))
        ##except urllib2.URLError, e: # python 2.7
        #except urllib.error.URLError as e: # python 3.7
            #logging.info('URLError = ' + str(e.reason))
            #print('URLError = ' + str(e.reason))
        ##except httplib.HTTPException, e: # python 2.7
            ##logging.info('HTTPException')
        #except Exception:
            #import traceback
            #logging.info('generic exception: ' + traceback.format_exc())
            #print('generic exception: ' + traceback.format_exc())
        #else:
            #self.content = response.read().decode('utf-8')
            #print(self.content)
#
            ## TODO Decode JSON to see valid option data
            #if json.loads(self.content)['options'] != []:
                #self.valid = 1
#
            ## 1 = valid. -1 = options not available (set above)
            ##self.valid = self.content.find('id', 10, 20)
            #print('self.valid')
            ##print(self.valid)
            # logging.info('|| content')
            # logging.info(self.content)

    #def getExpirations(self):
        #print('getExpirations')
        ## Also add the upcoming expiration dates for options
        ##qrs = self.content.find('expiration:') + 14
        ##qre = self.content.find('}],put')
        #qrs = self.content.find('expiration:') + 14
        #qre = self.content.find('","strike')
        ##print(qrs)
        ##print(qre)
#
        #self.expirations = self.content[qrs:qre].split('},{')
        #print(self.expirations)

def thirdFriday(year, month):
    """Calculatest the 3rd Friday of any given month and year.
    Option contracts expire on the 3rd Friday of the month"""
    import calendar
    logging.info("|| year, month")
    logging.info(year)
    logging.info(month)
    if(calendar.monthcalendar(year,month)[0][4]==0):
        return calendar.monthcalendar(year,month)[3][4]
    else:
        return calendar.monthcalendar(year,month)[2][4]

def xactionbook_key(xactionbook_name=DEFAULT_XACTIONBOOK_NAME):
    """Constructs a Datastore key for a xaction entity.
    """
    return ndb.Key('xactionbook', xactionbook_name)

# Web page layout area:

@app.route('/hello')
def hello():
    return 'Hello bcss15-main.py world'

@app.route('/test')
def test():
    return f'Hello, test World!'

@app.route('/updateTicker', methods=['GET','POST'])
def updateTicker():
    ''' Only valid tickers were added originally, but we
    can check it here as a assert, for example if a ticker
    is no longer trading options
    '''

    # Get the ticker value needing update from the webpage
    # Remove existing transactions in the list for that ticker
    # Add new transactions for that ticker to the list
    # Redisplay the page of all results

    logging.info("|| UpdateTicker")
    # logging.info("|| Go through tickers to make transactions")
    # logging.info(tickers)

    #toU = self.request.get("toUpdate") #2.7
    toU = request.form["toUpdate"] #3.7
    toUpdate = toU.split(' /')[0]
    print('toUpdate:')
    print(toUpdate)
    #print(toUpdate)
    logging.info('|| toUpdate')
    logging.info(toUpdate)

    # ndb cache only caches entities that you get by key/id. Queries are not cached.
    # http://stackoverflow.com/questions/14205763/gae-put-multi-entities-using-backend-ndb

    with mynclient.context():
        deleteQ = TransactionNDB.query(TransactionNDB.symbol ==
                                       toUpdate).fetch(keys_only=True)
        ndb.delete_multi(deleteQ)

    gt = GetTicker() # Pull the options for the ticker, stored in gt.content
    chain = gt.getOptionsListTDA(toUpdate, api_key_tdameritrade, credential.access_token)
    print('chain')
    #print(chain)

    chainPEDM = chain['putExpDateMap']
    print('chainPEDM.keys()')
    print(len(chainPEDM.keys()))

    listToPut = []
    for eachDate in chainPEDM.keys():
        strikeDate = eachDate[0:10]
        print('strikeDate')
        print(strikeDate)
        strike = chainPEDM[eachDate]
        print('strike')
        #print(strike) # Very long
        print('strike.keys()')
        print(strike.keys())
        for eachStrike in strike.keys():
            xactionbook_name = DEFAULT_XACTIONBOOK_NAME
            with mynclient.context():
                xaction = TransactionNDB(parent=xactionbook_key(xactionbook_name))
                xaction.symbol = toUpdate
            print('eachStrike')
            print(eachStrike)
            xaction.strike = eachStrike
            xaction.createTDA(eachStrike, strike)
            listToPut.append(xaction)
            #print('len(listToPut)')
            #print(len(listToPut))
            #with mynclient.context():
                #xaction.put()
                #xaction.put_async
                #print(listToPut)

    with mynclient.context():
        ndb.put_multi(listToPut)

    #with mynclient.context(): # After all transactions are in the list, add it to the ndb cloud database
        #ndb.put_multi(listToPut)

    return redirect('/')

# TODO Delete this likely leftover stuff:
    #gt2 = GetTicker()
    #gt2.getContentOne(toUpdate)
    #logging.info("|| gt2.content")
    #logging.info(str(gt2.content))
#
    #if gt2.valid == -1:
        #logging.info('|| Update: Something is wrong. Cant find ticker!')
    #else:
        #if (len(gt2.expirations) > 10):
            #logging.info('|| Update: >10 expirations!')
        #for e in gt2.expirations:
            #gt2.getContentDate(toUpdate, e)
            #EnterTicker(gt2.content, toUpdate)
            #logging.info("|| gt2.content entered")
            #entityQ = TickerNDB.query(TickerNDB.symbol == toUpdate)
            #entity = entityQ.get()
            #logging.info('|| entity in Update')
            #logging.info(entity)
#
        #entity.color = "white"
        #entity.put()  # Update it
        #logging.info("|| white put")
#
        #sleep(0.2)
    #return redirect('/')

    # # TODO: Somewhere update the colors to be cleared if not updated in awhile

#def EnterTicker():
    #pass

@app.route('/updateShowHide', methods=['GET', 'POST'])
def updateShowHide():
    #class UpdateShowHide(webapp2.RequestHandler):

    #TODO: It requires 2 clicks to refresh WATT to HIDE
    #TODO: Make Income and the 2 ROI column values to be green or red <>0
    #TODO: Add after-tax values??? Maybe include as an option
    #TODO: Store the sort-by field
    #TODO: Add in some column to show what-if the option doesn't execute
    logging.info("|| UpdateShowHide up")
    #def post(self):
    logging.info("|| UpdateShowHide post")
    pfs = PropFromSymbolLocal()
    pfs.bringlocal()
    print('In updateShowHide')
    #print(pfs.TickerLocal)

    for t in range(len(pfs.TickerLocal)):
        #print(t)
        symbol = pfs.TickerLocal[t]['symbol']
        #print(symbol)
        tSH = request.form[pfs.TickerLocal[t]['symbol']]
        #print(tSH)
        #print(tSH.split(' /')[0])
        tq = TickerNDB.query(TickerNDB.symbol==symbol)
        with mynclient.context():
            t = tq.get()
            #print(t)
            #print(t.colorShow)
            if (tSH) == "Show":
                t.colorShow = True
            else:
                t.colorShow = False
            t.put()
    return redirect('/')

@app.route('/')
@app.route('/index')
def index():
    fee = Fee()
    xForDisplayC = []
    xForDisplayP = []
    contracts = 1 # Just compare the value of 1 contract (100 shares)

    # TODO: Add ability to sort main page by certain fields
    # TODO: Add company name
    # TODO: Somehow allow contracts to be changed dynamically, during analysis

    # logging.info("|| fee.trade")
    # logging.info(fee.trade)

    with mynclient.context():
        ticker_query = TickerNDB.query()
        tickers = ticker_query.fetch() # Get the whole list of tickers

    # logging.info("|| tickers")
    # logging.info(tickers)

    # For each transaction, update my qty and my cost for each ticker
    # Fetch the top transactions and prepare them for display

    xactionbook_name = DEFAULT_XACTIONBOOK_NAME

    print('point1')

    with mynclient.context():
        xaction_queryC = TransactionNDB.query(
            TransactionNDB.optionType=="C", # "C" or "P"
            ancestor=xactionbook_key(xactionbook_name)).order(-TransactionNDB.date)

        xactions = xaction_queryC.fetch()

        logging.info("|| Showing xactions:")
        # logging.info(xactions)
        # logging.info(len(xactions))
        #print(tickers)
        #print(xactions)
        #print(contracts)
        #print(fee.__str__())
        #print(xForDisplayC)
        addXactions(tickers, xactions, contracts, fee, xForDisplayC)

    print('point2')

    with mynclient.context():
        xaction_queryP = TransactionNDB.query(
            TransactionNDB.optionType == "PUT",  # "CALL" or "PUT" in the TDA datastructure
            ancestor=xactionbook_key(xactionbook_name)).order(-TransactionNDB.date)

        print('point3')

        xactions = xaction_queryP.fetch()
        print('point4')
        addXactions(tickers, xactions, contracts, fee, xForDisplayP)

        print('point5')

    logging.info("|| xP and xC len")
    logging.info(len(xForDisplayC))
    logging.info(len(xForDisplayP))

    xC = sortXactions(xForDisplayC, tickers, sortColumn.sortColumn)
    xP = sortXactions(xForDisplayP, tickers, sortColumn.sortColumn)

    # xC = sorted(xForDisplayC, reverse=True, key=itemgetter('ROIForOneBid'))
    # xP = sorted(xForDisplayP, reverse=True, key=itemgetter('ROIForOneBid'))

    logging.info("|| len(xC)")
    logging.info(len(xC))

    d = datetime.now() + timedelta(hours=+3)

    localDatetime = d.strftime("%A, %d. %B %Y %I:%M%p")
    spacer = ' / '

    template_values = {
        'localDatetime': localDatetime,
        #'xactionbook_name': urllib.quote_plus(xactionbook_name), # 2.7
        'xactionbook_name': urllib.parse.quote(xactionbook_name), # 3.7
        'transactionsC': xC,
        'transactionsP': xP,
        'tickers': tickers,
        'spacer' : spacer,
        'sc': sortColumn,
        'dashboardContentCall': dashboardContentCall,
        'dashboardContentPut': dashboardContentPut
    }

    #template = JINJA_ENVIRONMENT.get_template('index.html')
    # logging.info("|| template_values")
    # logging.info(template_values)
    # logging.info("|| sandList")
    # logging.info(sandList)

    #self.response.write(template.render(template_values)) # Jinja

    return render_template('index.html',
                           localDatetime=localDatetime,
                           xactionbook_name=urllib.parse.quote(xactionbook_name),
                           transactionsC=xC,
                           transactionsP=xP,
                           tickers=tickers,
                           spacer=spacer,
                           sc=sortColumn,
                           dashboardContentCall=dashboardContentCall,
                           dashboardContentPut=dashboardContentPut,
                           #template_values=template_values,
                           title='Home')

#def EnterTickerI(content, toU):
    #xactionbook_name = DEFAULT_XACTIONBOOK_NAME
    #xaction = TransactionNDB(parent=xactionbook_key(xactionbook_name))
    #xaction.symbol = toU
    #xaction.createInt()

#def addXactions(self, tickers, xactions, contracts, fee, xForDisplay):
def addXactions(tickers, xactions, contracts, fee, xForDisplay):
    logging.info("|| addXactions")

    if (len(xactions) > 0):
        pfs = PropFromSymbolLocal()
        pfs.bringlocal()
        print('len(xactions)')
        print(len(xactions))

        for i in range(0, len(xactions)):
            #print(i)
            # Do the math first, then make the dictionary cleanly. Otherwise have to repeat
            # all the text from the equations and it is harder to read.

            # logging.info("|| xactions[i]:")
            # logging.info(xactions[i])

            dContracts = contracts
            dSymbol = xactions[i].symbol
            #print('dSymbol:' + dSymbol)
            # dcompanyName = xactions[i].companyName
                # logging.info("|| dSymbol:")
                # logging.info(dSymbol)
            dMyQty = pfs.pfs(dSymbol, "myQty")
            if dMyQty is None:
                dMyQty = 0
            dMyCost = pfs.pfs(dSymbol, "myCost")
            if dMyCost is None:
                dMyCost = 0
            # logging.info("|| MyQty MyCost")
            # logging.info(dMyQty)
            # logging.info(dMyCost)
            if (dMyQty == 0): # Watch for divide by zero
                dMyCostPerShare = 0
            else:
                dMyCostPerShare = dMyCost / dMyQty
            dLastOptionPrice = xactions[i].lastOptionPrice
            dLastStockPrice = xactions[i].lastStockPrice
            dChgToday = xactions[i].optionChange
            dContractDate = xactions[i].strikeMonth
            dOpenInt = xactions[i].openInt
            dStrike = xactions[i].strikePrice
            dCostBid = xactions[i].bid
            dCostAsk = xactions[i].ask
            dIncomeBid = 100 * xactions[i].bid - fee.trade
            dIncomeAsk = 100 * xactions[i].ask - fee.trade
            # Not sure about PutMaintenance
            dPutMaintenance = 100 * contracts * xactions[i].strikePrice
            # TODO: Figure out how to calculate profit for potential PUTS. dMyCostPerShare is zero!
            # With dMyCostPerShare == 0 may be OK
            dProfitBid = (xactions[i].pastPnL + dIncomeBid + xactions[i].strikePrice * contracts * 100) - \
                         (dMyCostPerShare * contracts * 100 + fee.trade)
            dProfitAsk = (xactions[i].pastPnL + dIncomeAsk + xactions[i].strikePrice * contracts * 100) - \
                         (dMyCostPerShare * contracts * 100 + fee.trade)
            #print(dProfitAsk)

            dMyAcqDate = pfs.pfs(dSymbol, "myAcqDate")
            #logging.info("|| MyAcqDate")
            # logging.info(dMyAcqDate)
            # Next lines are percentages, so multiply by 100
            if (xactions[i].optionType == "C"): # percent, so multiply by 100
                if dMyAcqDate is not None:
                    dROIForOneBid = 100 * 365 * (dProfitBid / (dMyCostPerShare * contracts * 100)/((xactions[i].strikeDate - dMyAcqDate)).days)
                    dROIForOneAsk = 100 * 365 * (dProfitAsk / (dMyCostPerShare * contracts * 100)/((xactions[i].strikeDate - dMyAcqDate)).days)
                else:
                    dROIForOneBid = 0
                    dROIForOneAsk = 0
            else: # if it's a put, then assume the acquisition date is today
                dROIForOneBid = 100 * 365 * (
                dProfitBid / (dStrike * contracts * 100) / ((xactions[i].strikeDate - datetime.now().date())).days)
                dROIForOneAsk = 100 * 365 * (
                dProfitAsk / (dStrike * contracts * 100) / ((xactions[i].strikeDate - datetime.now().date())).days)

            dIncPerYearBid = dIncomeBid * 365 / (xactions[i].strikeDate - datetime.now().date()).days
            dIncPerYearAsk = dIncomeAsk * 365 / (xactions[i].strikeDate - datetime.now().date()).days
            if (xactions[i].optionType == "C"): # percent, so multiply by 100
                #if dMyCost <> 0: # python 2.7
                if dMyCost != 0: # python 3.7
                    dROIPerYearBid = 100 * dIncPerYearBid / dMyCost
                else:
                    dROIPerYearBid = 0
            else: # it's not a call, so it's a put
                dROIPerYearBid = 100 * dIncPerYearBid / dPutMaintenance
            if (xactions[i].optionType == "C"): # percent, so multiply by 100
                #if dMyCost <> 0: # python 2.7
                if dMyCost != 0: # python 3.7
                    dROIPerYearAsk = 100 * dIncPerYearAsk / dMyCost
                else:
                    dROIPerYearAsk = 0
            else: # it's not a call, so it's a put
                dROIPerYearAsk = 100 *dIncPerYearAsk / dPutMaintenance
            # QF is a "Quality Factor" which should help to find the
            # best transaction to execute
            if (abs(abs(dROIForOneBid) - abs(dROIPerYearBid )) == 0):
                dQF = 0
            else:
                dQF = 100 / abs(abs(dROIForOneBid) - abs(dROIPerYearBid ))

#http://jinja.pocoo.org/docs/dev/templates/
            an_item = dict(
                Contracts=dContracts,
                Symbol=dSymbol,
                MyQty = dMyQty,
                MyCost = dMyCost,
                MyCostPerShare = dMyCostPerShare,
                LastStockPrice=dLastStockPrice,
                LastOptionPrice=dLastOptionPrice,
                ChgToday=dChgToday,
                ContractDate=dContractDate,
                OpenInt=dOpenInt,
                Strike=dStrike,
                PutMaintenance = dPutMaintenance,
                CostBid=dCostBid,
                CostAsk=dCostAsk,
                IncomeBid=dIncomeBid,
                IncomeAsk=dIncomeAsk,
                ProfitBid = dProfitBid,
                ProfitAsk = dProfitAsk,
                ROIForOneBid = dROIForOneBid,
                ROIForOneAsk = dROIForOneAsk,
                IncPerYearBid=dIncPerYearBid,
                IncPerYearAsk=dIncPerYearAsk,
                ROIPerYearBid=dROIPerYearBid,
                ROIPerYearAsk=dROIPerYearAsk,
                QF=dQF
            )
            xForDisplay.append(an_item)

#def sortXactions(self, xactions, tickers, sortField):
def sortXactions(xactions, tickers, sortField):
    import operator
    # sorted_x = sorted(x.items(), key=operator.itemgetter)
    #xC = sorted(xForDisplayC, reverse=True, key=itemgetter('ROIForOneBid'))
    logging.info("|| sortXactions")
    # logging.info(len(x))
    includeList = []

    for t in tickers:
        if t.colorShow: # and if it's TRUE, then include it
            #print('including: ' + t.symbol)
            includeList.append(t.symbol)
            # logging.info('|| Added to includeList:')
            # logging.info(t.symbol)
        #else:
            # logging.info('|| Not Included:')
            # logging.info(t.symbol)

    # logging.info("|| includeList")
    # logging.info(includeList)

    # logging.info("|| len(xactions)")
    # logging.info(len(xactions))

    i = 0
    out = []
    while i < len(xactions): # Go through and include or skip certain ones
        # logging.info("|| xactions[i].get('Symbol')")
        # logging.info(xactions[i].get('Symbol'))

        if xactions[i].get('Symbol') in includeList: # Check which tickers to include
            # logging.info("|| xactions[i].get('CostBid')")
            # logging.info(xactions[i].get('CostBid'))
            #include = [xactions[i] for xactions[i].get('Symbol') in includeList]
            if xactions[i].get('CostBid') > 0:
                out.append(xactions[i])
        # logging.info("|| xactions[i].get('Symbol')")
        # logging.info(xactions[i].get('Symbol'))
        i += 1
        # logging.info('|| i:')
        # logging.info(i)
    # logging.info("|| len(out)")
    # logging.info(len(out))

    out2 = sorted(out, reverse=True, key=operator.itemgetter(sortField))
    return out2

# [END main_page]

# [START AddRemUpdTicker]
#class AddRemUpdTicker(webapp2.RequestHandler):
@app.route('/addRemUpdTicker', methods=['GET','POST'])
def AddRemUpdTicker():
    """Add a ticker to the list"""

    if request.method == "POST":
    #def post(self):
        logging.info("|| addRemUpdTicker post")
        print('post-addRemUpdTicker')

        # Which action: View, Edit or Delete?

        #removeCheck = self.request.get("ViewDelete")
        removeCheck = request.form['ViewDelete']
        #print(removeCheck)

        logging.info("|| removeCheck")
        logging.info(removeCheck)

        if (removeCheck == "View"):
            #tickerToView = self.request.get("buttonticker")
            #tickerToView = request.form['buttonticker']
            #https://finance.yahoo.com/quote/CRON?p=CRON
            tickerToView = request.form['AddTicker'].upper()
            redirectLink = "https://finance.yahoo.com/quote/" + tickerToView + "?p=" + tickerToView
            logging.info(str(redirectLink))
            #return redirect(url_for(str(redirectLink)))
            return redirect(str(redirectLink))

        elif (removeCheck == "Edit"):
            #tickerToAdd = self.request.get("AddTicker")
            tickerToAdd = request.form['AddTicker'].upper()
            logging.info(tickerToAdd)
            #print(tickerToAdd)

            if(tickerToAdd):
                ticker = TickerNDB()
                ticker.symbol = tickerToAdd
                ticker.myQty = float(request.form["myQty"])
                ticker.myCost = float(request.form["myCost"])
                ticker.myAcqDate = datetime.strptime(request.form["myAcqDate"],'%Y-%m-%d')

                with mynclient.context():
                    ticker.put()
            sleep(2)
            pfs = PropFromSymbolLocal()
            pfs.bringlocal()

            return redirect('/addRemUpdTicker')

        elif(removeCheck == "Delete"):
            #tickerToRemove = request.args.get("buttonticker", default_value="default_value") # 2.7
            tickerToRemove = request.form["buttonticker"].upper() # 3.7
#            logging.info(tickerToRemove)

            #print(tickerToRemove)
            pfs = PropFromSymbolLocal()
            pfs.deleteTicker(tickerToRemove)
            sleep(2) # Let the cloud settle
            pfs.bringlocal()

            return redirect('/addRemUpdTicker')

        else:
            logging.info("|| None of the radio buttons were set")
            ticker_query = TickerNDB.query()
            tickers = ticker_query.fetch() # Get the whole list

            template_values = {
                'tickers': tickers,
            }

            return (render_template('AddRemTicker.html', template_values))

    if request.method == "GET":
        logging.info("|| AddRemUpdTicker get")
        print('get')

        with mynclient.context():
            ticker_query = TickerNDB.query()
            tickers = ticker_query.fetch() # Get the whole list

        template_values = {
            'tickers': tickers,
        }

        return (render_template('AddRemTicker.html', tickers=tickers))
# [END AddRemUpdTicker]

# [START AddTicker]
#class AddTicker(webapp2.RequestHandler):
#@app.route('/AddTicker', methods = ['POST'])
#def AddTicker():
    #if request.method == "POST":
    ##def post(self):
        #logging.info("|| AddTicker")
        #print('AddTicker / POST')
#
        #ticker = TickerNDB()
        ##ticker.symbol = self.request.get('AddTicker')
        #ticker.symbol = request.form['AddTicker'].upper() # Get the symbol from the html form
        #logging.info(ticker.symbol)
        #print(ticker.symbol)
#
        #gt = GetTicker()
        #gt.getContentOne(ticker.symbol)
        #logging.info("|| gt.content")
        #logging.info(str(gt.content))
#
        #if (gt.valid == 1): # Only add option-tradeable tickers
            #ticker.put()
##            tkey = ticker.put()
##            logging.info("|| tkey: " + str(tkey))
            #sleep(0.2)
        ##self.redirect('/addRemUpdTicker')
        #return redirect('/addRemUpdTicker')

# TODO: Not sure if I really need this addtickeradd code
#def AddTickerAdd(self, tickerToAdd):
    #ticker = TickerNDB()
    #ticker.symbol = tickerToAdd
    #gt = GetTicker()
    #gt.getContentOne(ticker.symbol)
    #logging.info("|| gt.content")
    #logging.info(str(gt.content))
#
    #if (gt.valid == 1):  # Only add option-tradeable tickers
        #ticker.put()
        #sleep(0.2)
        #self.valid = 1
# [END AddTicker]

#client = datastore.Client()
mynclient = ndb.Client()

sortColumn = SortColumn()
sortColumn.setSC('ROIForOneBid')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    print('define credential')
    credential = GetAuthorized()
    #print(credential.access_token)
    #print(credential.GetChain('MMM')) # Very long
    #sleep(0.2)
    #print(credential.GetChain('AAPL'))

    #app.run(host='127.0.0.1', port=8081, debug=True)
    app.run(host='127.0.0.1', port=8081, debug=True, use_reloader=False)

    #DEFAULT_XACTIONBOOK_NAME = 'default_xactionbook'

