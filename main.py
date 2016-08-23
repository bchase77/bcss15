#!C:\\Python27\\python

from __future__ import print_function

# Copyright 2016 Bryan Chase
#
# [START imports]
import logging
import os
import urllib
import urllib2

from datetime import datetime, date, timedelta
import time
from operator import itemgetter
from time import sleep

#from google.appengine.lib.requests import requests
#from google.appengine.dist27 import httplib

import requests
#from google.appengine.api import users
#from google.appengine.datastore.acl_pb import Entry
#from google.appengine.dist27.python_std_lib import httplib
from google.appengine.ext import ndb
import jinja2
import webapp2
from webapp2_extras import json
import sys

#from google.appengine.dist27 import httplib
import httplib
logging.info(sys.version)
logging.info("_START")

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

# TODO: The update still doesn't work right. Sometimes doesn't set
# the radio buttons right. It requires 2 selections to set the radio buttons.

DEFAULT_XACTIONBOOK_NAME = 'default_xactionbook'
#1 DEFAULT_TICKERBOOK_NAME = 'default_tickerbook'

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

def xactionbook_key(xactionbook_name=DEFAULT_XACTIONBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('xactionbook', xactionbook_name)

class SortColumn(webapp2.RequestHandler):
    ''' Select which column will be used for sorting, and reload
    '''
    # def __init__(self):
    #     self.sortColumn = 'ROIForOneBid'
    #     self.refresh = True

    def setSC(self, sC):
        self.sortColumn = sC

    def setRefresh(self, refresh):
        self.refresh = refresh

    def post(self):
        toUpdate = self.request.get("Sort")
        logging.info("|| sortColumn")
        logging.info(toUpdate)
        sc.setSC(toUpdate)
        self.redirect('/')

sc = SortColumn()
sc.setSC('ROIForOneBid')

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

# TODO: Redo or delete these comments
# Mainpage:
#    Show the current list of tickers under analysis
#       Show total put maintenance required
#       Show total cash on hand (for covered puts sales)
#       Show Qty of long shares (for covered calls sales)
#       Show upcoming expirations
#    Show top put prospects
#       Show current positions and upcoming expirations
#       Show total cash on hand (for covered puts sales)
#       Show ROI in various ways
#       Show Put Maintenance required per ticker
#    Show top call prospects
#       Show current positions and upcoming expirations
#       Show Qty of long shares (for covered calls sales)
#       Show original costs and ROI if sold
#       Show cash which would come in if sold

class GetTicker():
    """Get ticker data from finance.googlecom and check if it's an
     option tradeable security. Returns .valid==1 if found, along with
     good content; .valid==-1 if not found"""

    def getShareInfo(self, ticker):
        tail = '&output=json'
        urlpath1 = 'https://www.google.com/finance?q='
        self.valid = -1 #default is bad ticker
        self.tryTheLink(urlpath1, ticker, tail)
        if self.valid == 1:
            urlFullPath = urlpath1 + ticker + tail
            r = urllib2.urlopen(urlFullPath)
            c = r.read()
            d = c.split('"c"')
            logging.info("|| d")
            logging.info(d)
            self.shareChange = d[1].split('"')[1]

    def getContentOne(self, ticker):
        tail = '&output=json'
        urlpath1 = 'http://www.google.com/finance/option_chain?q='
        # urlpath1 = 'https://www.google.com/finance?q=NASDAQ%3AACET&output=json'
        self.valid = -1  # default to not tradeable, set it with tryTheLink
        self.tryTheLink(urlpath1, ticker, tail)
        if self.valid:
            self.getExpirations()

    def getContentDate(self, ticker, date):
        # Format is: http://www.google.com/finance/option_chain?q=watt&expd=4&expm=4&expy=2014&output=json
        expy = '&expy=' + date.split(',')[0][2:]
        expm = '&expm=' + date.split(',')[1][2:]
        expd = '&expd=' + date.split(',')[2][2:]

        tail = expd + expm + expy + '&output=json'
        urlpath1 = 'http://www.google.com/finance/option_chain?q='
        self.valid = -1  # default to not tradeable, set it with tryTheLink
        self.tryTheLink(urlpath1, ticker, tail)
        # if self.valid:
        #     self.getExpirations()

    def tryTheLink(self, path, ticker, tail):
        urlpath = path + ticker + tail
        logging.info(urlpath)
        print (urlpath)

        try:
            response = urllib2.urlopen(urlpath)
        except urllib2.HTTPError, e:
            logging.info('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            logging.info('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            logging.info('HTTPException')
        except Exception:
            import traceback
            logging.info('generic exception: ' + traceback.format_exc())
        else:
            self.content = response.read()
            # 1 = valid. -1 = options not available (set above)
            self.valid = self.content.find('expiry', 0, 10)
            # logging.info('|| content')
            # logging.info(self.content)

    def getExpirations(self):
            # Also add the upcoming expiration dates for options
            qrs = self.content.find('expirations:') + 14
            qre = self.content.find('}],puts')

            self.expirations = self.content[qrs:qre].split('},{')

class AddRemUpdTicker(webapp2.RequestHandler):
    """Add a ticker to the list"""

    def post(self):
        logging.info("|| AddRemUpdTicker post")

        # Which action: View, Edit or Delete?

        removeCheck = self.request.get("ViewDelete")
        logging.info("|| removeCheck")
        logging.info(removeCheck)

        if (removeCheck == "View"):
            tickerToView = self.request.get("buttonticker")
            redirectLink = "http://www.google.com/finance?q=" + tickerToView
            logging.info(str(redirectLink))
            self.redirect(str(redirectLink))

        elif (removeCheck == "Edit"):
            tickerToAdd = self.request.get("AddTicker")
            logging.info(tickerToAdd)
            if(tickerToAdd):
                at = AddTicker()
                at.add(tickerToAdd)

                if(at.valid <> 1): # Invalid symbol; Return
                    self.redirect('/addRemUpdTicker')
                else: # It's a valid symbol and has been added
                    tickerToEdit = tickerToAdd
            else:
                tickerToEdit = self.request.get("buttonticker")

            logging.info(tickerToEdit)

            entityQ = TickerNDB.query(TickerNDB.symbol == tickerToEdit)
            entity = entityQ.get()

            logging.info('|| entity in Edit RemTicker')
            logging.info(entity)

            myQty = self.request.get("myQty")
            myCost = self.request.get("myCost")
            myAcqDate = self.request.get("myAcqDate")

            logging.info("|| my Updates")
            logging.info(myQty)
            logging.info(myCost)
            logging.info(myAcqDate)

            if(myQty):
                logging.info(myQty)
                entity.myQty = float(myQty)
            if(myCost):
                logging.info(myCost)
                logging.info(entity.symbol)
                entity.myCost = float(myCost)
            if(myAcqDate):
                logging.info(myAcqDate)
                logging.info(entity.symbol)
                entity.myAcqDate = datetime.strptime(myAcqDate, '%Y-%m-%d')

            entity.put() # Update it
            sleep(0.2)
            self.redirect('/addRemUpdTicker')

        elif(removeCheck == "Delete"):
            tickerToRemove = self.request.get("buttonticker", default_value="default_value")
#            logging.info(tickerToRemove)

            entityQ = TickerNDB.query(TickerNDB.symbol == tickerToRemove)
            # logging.info('entityQ')
            # logging.info(entityQ)

            entity = entityQ.get()
            # logging.info('entity')
            # logging.info(entity)

            entity.key.delete()
            sleep(0.2)
            self.redirect('/addRemUpdTicker')

        else:
            logging.info("|| None of the radio buttons were set")
            ticker_query = TickerNDB.query()
            tickers = ticker_query.fetch() # Get the whole list

            template_values = {
                'tickers': tickers,
            }

            template = JINJA_ENVIRONMENT.get_template('AddRemTicker.html')
            self.response.write(template.render(template_values))

    def get(self):
        logging.info("|| AddRemUpdTicker get")

        ticker_query = TickerNDB.query()
        tickers = ticker_query.fetch() # Get the whole list

        template_values = {
            'tickers': tickers,
        }

        template = JINJA_ENVIRONMENT.get_template('AddRemTicker.html')
        self.response.write(template.render(template_values))

class AddTicker(webapp2.RequestHandler):

    def post(self):
        logging.info("|| AddTicker")
        ticker = TickerNDB()
        ticker.symbol = self.request.get('AddTicker')
        logging.info(ticker.symbol)


        gt = GetTicker()
        gt.getContentOne(ticker.symbol)
        logging.info("|| gt.content")
        logging.info(str(gt.content))

        if (gt.valid == 1): # Only add option-tradeable tickers
            ticker.put()
#            tkey = ticker.put()
#            logging.info("|| tkey: " + str(tkey))
            sleep(0.2)
        self.redirect('/addRemUpdTicker')

    def add(self, tickerToAdd):
        ticker = TickerNDB()
        ticker.symbol = tickerToAdd
        gt = GetTicker()
        gt.getContentOne(ticker.symbol)
        logging.info("|| gt.content")
        logging.info(str(gt.content))

        if (gt.valid == 1):  # Only add option-tradeable tickers
            ticker.put()
            sleep(0.2)
            self.valid = 1

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
    strikeMonth = ndb.StringProperty(indexed=False)
    strikeDate = ndb.DateProperty(indexed=False)
    strikeMonthNum = ndb.IntegerProperty(indexed=False)
    strikeYear = ndb.IntegerProperty(indexed=False)
    optionType = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    pastPnL = ndb.FloatProperty(indexed=False, default=0.00)

    def create(self, callOrPut, type):
        from time import strptime

        callOrPutArray = callOrPut.split(',')
        # If the length of the call or put entry is 13 then it's missing
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
    """A main model for storing tickers we are interested in."""
    symbol = ndb.StringProperty(indexed=True)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    color = ndb.StringProperty(indexed=False, default='white')
    colorShow = ndb.BooleanProperty(indexed=False)
    myQty = ndb.FloatProperty(indexed=False)
    myCost = ndb.FloatProperty(indexed=False)
    myAcqDate = ndb.DateProperty(indexed=False)
    pnl = ndb.FloatProperty(indexed=False)
    shareChange = ndb.FloatProperty(indexed=False)

    # def __init__(self):
    #     self.colorShow = True # By default, show all tickers
    # def updateDate(self, myAcqStr):
    #     def ud(myAcqStr):
    #         return datetime.strptime(myAcqStr, '%m/%d/%y')

class PropFromSymbol():
    def pfs(self, symbol, property):
        #logging.info("|| PropfromSymbol")

        ticker_query = TickerNDB.query(
            TickerNDB.symbol == symbol
        )
        # logging.info("|| pfs:ticker_query")
        # logging.info(ticker_query)

        entity = ticker_query.get()  # Get the entity with that symbol
        # logging.info("|| pfs:entity")
        # logging.info(entity)

        # entity.symbol
        # logging.info("|| pfs:entity.symbol")
        # logging.info(entity.symbol)

        # logging.info(dir(entity))

        # logging.info(getattr(entity, property))
        return getattr(entity, property)

class MainPage(webapp2.RequestHandler):
    ''' Show the top level dashboard
    '''
    def get(self):
        fee = Fee()
        xForDisplayC = []
        xForDisplayP = []
        contracts = 1

        # TODO: Add ability to sort main page by certain fields
        # TODO: Add company name
        # TODO: Somehow allow contracts to be changed dynamically, during analysis

        # logging.info("|| fee.trade")
        # logging.info(fee.trade)

        ticker_query = TickerNDB.query()
        tickers = ticker_query.fetch() # Get the whole list of tickers

        # logging.info("|| tickers")
        # logging.info(tickers)

        # For each transaction, update my qty and my cost for each ticker
        # Fetch the top transactions and prepare them for display

        xactionbook_name = self.request.get('xactionbook_name',
                                          DEFAULT_XACTIONBOOK_NAME)
        xaction_queryC = TransactionNDB.query(
            TransactionNDB.optionType=="C", # "C" or "P"
            ancestor=xactionbook_key(xactionbook_name)).order(-TransactionNDB.date)

        xactions = xaction_queryC.fetch()

        logging.info("|| Showing xactions:")
        # logging.info(xactions)
        # logging.info(len(xactions))

        self.addXactions(tickers, xactions, contracts, fee, xForDisplayC)

        xaction_queryP = TransactionNDB.query(
            TransactionNDB.optionType == "P",  # "C" or "P"
            ancestor=xactionbook_key(xactionbook_name)).order(-TransactionNDB.date)

        xactions = xaction_queryP.fetch()
        self.addXactions(tickers, xactions, contracts, fee, xForDisplayP)

        logging.info("|| xP and xC len")
        logging.info(len(xForDisplayC))
        logging.info(len(xForDisplayP))

        xC = self.sortXactions(xForDisplayC, tickers, sc.sortColumn)
        xP = self.sortXactions(xForDisplayP, tickers, sc.sortColumn)

        # xC = sorted(xForDisplayC, reverse=True, key=itemgetter('ROIForOneBid'))
        # xP = sorted(xForDisplayP, reverse=True, key=itemgetter('ROIForOneBid'))

        logging.info("|| len(xC)")
        logging.info(len(xC))

        d = datetime.now() + timedelta(hours=-4)

        localDatetime = d.strftime("%A, %d. %B %Y %I:%M%p")
        spacer = ' / '

        template_values = {
            'localDatetime': localDatetime,
            'xactionbook_name': urllib.quote_plus(xactionbook_name),
            'transactionsC': xC,
            'transactionsP': xP,
            'tickers': tickers,
            'spacer' : spacer,
            'sc': sc,
            'dashboardContentCall': dashboardContentCall,
            'dashboardContentPut': dashboardContentPut
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        # logging.info("|| template_values")
        # logging.info(template_values)
        # logging.info("|| sandList")
        # logging.info(sandList)


        self.response.write(template.render(template_values))

        # user = users.get_current_user()
        # if user:
        #     url = users.create_logout_url(self.request.uri)
        #     url_linktext = 'Logout'
        # else:
        #     url = users.create_login_url(self.request.uri)
        #     url_linktext = 'Login'

    def addXactions(self, tickers, xactions, contracts, fee, xForDisplay):
        logging.info("|| addXactions")

        if (len(xactions) > 0):
            pfs = PropFromSymbol()

            for i in range(0, len(xactions)):
                # Do the math first, then make the dictionary cleanly. Otherwise have to repeat
                # all the text from the equations and it is harder to read.

                # logging.info("|| xactions[i]:")
                # logging.info(xactions[i])

                dContracts = contracts
                dSymbol = xactions[i].symbol
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
                    if dMyCost <> 0:
                        dROIPerYearBid = 100 * dIncPerYearBid / dMyCost
                    else:
                        dROIPerYearBid = 0
                else: # it's not a call, so it's a put
                    dROIPerYearBid = 100 * dIncPerYearBid / dPutMaintenance
                if (xactions[i].optionType == "C"): # percent, so multiply by 100
                    if dMyCost <> 0:
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

    def sortXactions(self, xactions, tickers, sortField):
        import operator
        # sorted_x = sorted(x.items(), key=operator.itemgetter)
        #xC = sorted(xForDisplayC, reverse=True, key=itemgetter('ROIForOneBid'))
        logging.info("|| sortXactions")
        # logging.info(len(x))
        includeList = []

        for t in tickers:
            if t.colorShow: # and if it's TRUE, then include it
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

        # x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
        # Sort by values:
        #   sorted_x = sorted(x.items(), key=operator.itemgetter(1))
        #
        # Sort by keys:
        #   sorted_x = sorted(x.items(), key=operator.itemgetter(0))
        # Change order:
        #   sorted_x.reverse()
        # or  pass in reverse=True argument to sorted

# [END main_page]
class UpdateShowHide(webapp2.RequestHandler):

    #TODO: It requires 2 clicks to refresh WATT to HIDE
    #TODO: Make Income and the 2 ROI column values to be green or red <>0
    #TODO: Add after-tax values??? Maybe include as an option
    #TODO: Store the sort-by field
    #TODO: Add in some column to show what-if the option doesn't execute
    logging.info("|| UpdateShowHide up")
    def post(self):
        logging.info("|| UpdateShowHide post")
        entityQ = TickerNDB.query()
        entities = entityQ.fetch()

        listToPut = []

        for e in entities:
            tSH = self.request.get(e.symbol)
            tickerShowHide = tSH.split(' /')[0]
            if (tickerShowHide) == "Show":
                e.colorShow = True
            else:
                e.colorShow = False
            listToPut.append(e)
        logging.info(listToPut)
        ndb.put_multi(listToPut)
        self.redirect('/')

# class ShowHideTicker(webapp2.RequestHandler):
#     logging.info("|| ShowHideTicker up")
#     def post(self):
#         logging.info("|| ShowHideTicker post")
#         toShowHide = self.request.get("updateShowHide")
#         entityQ = TickerNDB.query(TickerNDB.symbol == toShowHide)
#         entity = entityQ.get()
#         logging.info(entity)
#         logging.info(entity.symbol)
#         logging.info(entity.colorShow)
#         entity.colorShow = not entity.colorShow
#         logging.info(entity.colorShow)
#         entity.put()  # Update it

class UpdateTicker(webapp2.RequestHandler):
    ''' Only valid tickers were added originally, but we
    can check it here as a assert, for example if a ticker
    is no longer trading options
    '''
    logging.info("|| UpdateTicker")
    # logging.info("|| Go through tickers to make transactions")
    # logging.info(tickers)

    def post(self):
        toU = self.request.get("toUpdate")
        toUpdate = toU.split(' /')[0]
        logging.info('|| toUpdate')
        logging.info(toUpdate)

        # Get the option chain for the ticker
        # gt.ticker
        # gt.content
        # gt.valid
        # gt.expirations[]
        # gt = GetTicker(toUpdate)
        # logging.info("|| gt.content")
        # logging.info(str(gt.content))

        # ndb cache only caches entities that you get by key/id. Queries are not cached.
        # http://stackoverflow.com/questions/14205763/gae-put-multi-entities-using-backend-ndb

        # book_keys = Book.query().fetch(keys_only=True)
        # ndb.delete_multi(book_keys)
        deleteQ = TransactionNDB.query(TransactionNDB.symbol ==
                                       toUpdate).fetch(keys_only=True)
        ndb.delete_multi(deleteQ)

        gt2 = GetTicker()
        gt2.getContentOne(toUpdate)
        logging.info("|| gt2.content")
        logging.info(str(gt2.content))

        if gt2.valid == -1:
            logging.info('|| Update: Something is wrong. Cant find ticker!')
        else:
            if (len(gt2.expirations) > 10):
                logging.info('|| Update: >10 expirations!')
            for e in gt2.expirations:
                gt2.getContentDate(toUpdate, e)
                EnterTicker(gt2.content, toUpdate)
                logging.info("|| gt2.content entered")
                entityQ = TickerNDB.query(TickerNDB.symbol == toUpdate)
                entity = entityQ.get()
                logging.info('|| entity in Update')
                logging.info(entity)

            entity.color = "white"
            entity.put()  # Update it
            logging.info("|| white put")

            sleep(0.2)
            self.redirect('/')

        # # TODO: Somewhere update the colors to be cleared if not updated in awhile

class EnterTicker():

    def __init__(self, content, symbol):
        # This example file is almost JSON output (not quite, see http://www.jarloo.com/google-stock-options-api/)
        # Format is from Google, one of these:
        # http://www.google.com/finance/option_chain?q=watt&output=json
        # http://www.google.com/finance/option_chain?q=sid&expd=16&expm=9&expy=2016&output=json
        # For testing, do it in a browser and read from file:
        # f = open("f-1.txt", 'rb')
        # s = f.read()
        # list1 = s

        logging.info("|| EnterTicker")
        listToPut = []

        list1 = content
        # logging.info("|| list1:")
        # logging.info(list1)

        # Parse the file and pull out the transaction info
        a = 'puts:['
        b = '}],calls'
        puts2 = list1.split(a,1)[-1].split(b)[0]
        puts3 = puts2.split('},')

        for each in puts3:
            logging.info("puts3")

            xactionbook_name = DEFAULT_XACTIONBOOK_NAME
            xaction = TransactionNDB(parent=xactionbook_key(xactionbook_name))
            xaction.symbol = symbol
            xaction.create(each[1:], "P")  # Create a transaction for each
            xaction.lastStockPrice = float(list1[list1.find('price')+6:-1])

            listToPut.append(xaction)
            # sleep(1)
            # xaction.put()

            # tr.pL = pL
            # tr.pL(self, each[1:])
            # pL(self, tr.Ask.__str__())
            # pL(self, tr.Bid.__str__())

            # Uncomment this to check the details of the transactions
            # for attr, value in tr.__dict__.iteritems():
            #    print(str(attr) + ": " + str(value))
            #    # print("Value: " + str(value))
            #    pL(self,str(attr) + ": " + str(value))

        # Good below start
        a = 'calls:['
        b = '}],under'
        calls2 = list1.split(a,1)[-1].split(b)[0]
        calls3 = calls2.split('},')

        # print(len(calls3))
        # print("")
        # print("Calls:")
        # pL(self,".")
        # pL(self,"Calls:")
        for each in calls3:
            # logging.info(each[1:])

            xaction = TransactionNDB(parent=xactionbook_key(xactionbook_name))
            xaction.symbol = symbol
            xaction.create(each[1:], "C")  # Create a transaction for each
            xaction.lastStockPrice = float(list1[list1.find('price')+6:-1])

            logging.info("|| len(xaction.symbol)")
            logging.info(len(xaction.symbol))
            # logging.info(len(ticker.symbol))

            # xq = TransactionNDB.query(
            #     ancestor=xactionbook_key(xactionbook_name)).order(-TransactionNDB.date)
            # tqs = tq.fetch(2)
            # xqs = xq.fetch(2)
            # logging.info("2")
            # logging.info(len(xqs))

            listToPut.append(xaction)
            # time.sleep(1)
            # xaction.put()
        # All xactions are in the listToPut now, so put it multi:
        logging.info("|| listToPut:")
        logging.info(listToPut)
        ndb.put_multi(listToPut)
        sleep(1)

        # Uncomment this to check the details of the transactions
            # for attr, value in tr.__dict__.iteritems():
            #    print(str(attr) + ": " + str(value))
            #    # print("Value: " + str(value))
            #    pL(self,str(attr) + ": " + str(value))
        # Good above end
# [END EnterTicker]

class deleteAll(webapp2.RequestHandler):
    # For debugging, delete transaction with a ticker
    def post(self):
        logging.info("|| multidelete")
        entityKeys = TransactionNDB.query().fetch(keys_only=True)
        logging.info(entityKeys)
        ndb.delete_multi(entityKeys)
        sleep(0.2)
        logging.info("|| end multidelete")

headers = {'to':'asc',
         'date':'asc',
         'type':'asc',}

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addRemUpdTicker', AddRemUpdTicker),
    # ('/showHideTicker', ShowHideTicker),
    ('/updateShowHide', UpdateShowHide),
    ('/deleteAll', deleteAll),
    ('/sortColumn', SortColumn),
    ('/updateTicker', UpdateTicker)
], debug=True)
# [END app]

# TODO: Allow change # of contracts
# TODO: Put database in another structure that can be sorted quickly
# TODO: Mouse-over to show equation. Add it to the dashboardContentPut?
# <span title="I am hovering over the text">Click to update now:</span>
