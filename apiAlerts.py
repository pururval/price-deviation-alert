#! /usr/bin/env python
import json
import statistics
import datetime
import sys
import getopt
import requests

argument_list = sys.argv[1:]
options = "hc:d:"   #Argument options
long_options = "help, currency=, deviation="
reqSDs = 1          #Input standard deviations (default=1)
currency = ""       #Input currency trade
log_level = ""      #Type of logs (INFO, ERROR, DEBUG)
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')

try:
    arguments, values = getopt.getopt(argument_list, options, long_options)
    for arg, val in arguments:
        if arg in ("-h", "help"):
            print("\n"+timestamp + " - AlertingTool - INFO - Parsing args\n")
            print("usage: apiAlerts.py [-h] [-c CURRENCY] [-d DEVIATION]\n")
            print("Runs checks on API\n")
            print("optional arguments:")
            print("-h, --help \t\t\t\t show this help message and exit")
            print("-c CURRENCY, --currency CURRENCY \t The currency trading pair, or ALL")
            print("-d DEVIATION, --deviation DEVIATION \t standard deviation threshold. eg. 1")
        elif arg in ("-c", "currency"):
            currency = val

        elif arg in ("-d", "deviation"):
            reqSDs = float(val)
except Exception as err:
    print(f"ERROR: {type(err).__name__} was raised: {err}")


base_url_v2 = "https://api.gemini.com/v2"
if currency != "" :
    response = requests.get(base_url_v2 + "/ticker/" + currency, timeout=5)
    retval = {}                                                 #Initialize the JSON return object
    retval['timestamp'] = datetime.datetime.now().isoformat()   #Field that shows in all cases
    retval['trading_pair'] = currency                           #Field that shows in all cases

    if response.status_code == 200:
        log_level = "INFO"
        res_data_v2 = response.json()
        # log_level = "DEBUG"
        # retval['res_data'] = res_data_v2
        data = list(map(float, res_data_v2["changes"]))
        last_price = res_data_v2["close"]                   #Closing value found as a field on JSON response res_data_v2
        average = statistics.mean(data)                     #Calculate mean of past 24 hourly prices
        stDev = statistics.stdev(data)                      #Using standard sd over population sd as its not entirety of currency but a sample set
        sdevs = abs(float(last_price) - average ) / stDev   #Absolute of Z number(SDs) as it can be negative
        change = float(last_price) - average                #Deviation as a notional value

        retval['level'] = log_level
        if sdevs > reqSDs : #Price deviation alert condition
            retval['deviation'] = True
            retval['data'] = {
                "last_price": last_price,
                "average": str(average),
                "change": str(change),
                "sdev": str(sdevs)
            }
        else:
            retval['deviation'] = False
    else:
        retval['level'] = "ERROR"
        retval['deviation'] = '-'
        retval['data'] = {
            "ERROR": str(response.text),
        }
    json_retval = json.dumps(retval)
    print(json_retval)