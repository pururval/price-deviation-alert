#! /usr/bin/env python
'''Module that generates a log alert if the standard deviation from the hourly 
prices of a currency pair for past 24 hours is more than the indicated value'''
import json
import statistics
import datetime
import sys
import getopt
import requests

def api_alert():
    '''Function that prints out an alert when SD is more than input/default value'''
    req_sds = 1          #Input standard deviations (default=1)
    currency = ""        #Input currency trade
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')

    try:
        arguments, _ = getopt.getopt(sys.argv[1:], "hc:d:", "help, currency=, deviation=")
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
                req_sds = float(val)
    except Exception as err:
        print(f"ERROR: {type(err).__name__} was raised: {err}")

    base_url_v2 = "https://api.gemini.com/v2"
    if currency != "" :
        response = requests.get(base_url_v2 + "/ticker/" + currency, timeout=5)
        #Initialize the JSON return object
        retval = {}
        retval['timestamp'] = datetime.datetime.now().isoformat()
        retval['trading_pair'] = currency

        if response.status_code == 200:
            res_data_v2 = response.json()
            # retval['level'] = "DEBUG"
            # retval['res_data'] = res_data_v2
            #Get the list of hourly values from JSON response and convert string to float
            data = list(map(float, res_data_v2["changes"]))
            #Get the closing value from JSON response res_data_v2
            last_price = res_data_v2["close"]
            #Absolute of Z(SDs) as it can be negative and wont meet our req conditions
            sdevs = abs(float(last_price) - statistics.mean(data) ) / statistics.stdev(data)
            #Deviation as a notional value
            change = float(last_price) - statistics.mean(data)

            retval['level'] = "INFO"                            #Type of logs (INFO, ERROR, DEBUG)
            if sdevs > req_sds :                                #Price deviation alert condition
                retval['deviation'] = True
                retval['data'] = {
                    "last_price": last_price,
                    "average": str(statistics.mean(data)),
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
        print(json.dumps(retval))

if __name__ == '__main__':
    api_alert()
