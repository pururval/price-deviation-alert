# price-deviation-alert
Generate an alert if the standard deviation from the hourly prices for past 24 hours is more than 1 (or any indicated value if there’s a CLI parameter defined in the tool)

## Deliverables:
- Instructions for running your script
- Dependencies
- Optional: A dockerfile to run the script
- What you would do next to further improve it
- Other interesting checks you might implement to 
alert on market behaviour
- Approach to solving the task, and any issues you faced with implementation
- The time taken to write it

`./apiAlerts.py -h`

```2024-06-04 21:51:51,657420 - AlertingTool - INFO - Parsing args

usage: apiAlerts.py [-h] [-c CURRENCY] [-d DEVIATION]

Runs checks on API

optional arguments:
-h, --help                               show this help message and exit
-c CURRENCY, --currency CURRENCY         The currency trading pair, or ALL
-d DEVIATION, --deviation DEVIATION      standard deviation threshold. eg. 1
```

`./apiAlerts.py -d 0.0011 -c btcusd | jq .`
```{
  "timestamp": "2024-06-04T21:51:58.349331",
  "trading_pair": "btcusd",
  "level": "INFO",
  "deviation": true,
  "data": {
    "last_price": "69185.27",
    "average": "69697.24875",
    "change": "-511.97874999999476",
    "sdev": "0.632127516883148"
  }
}
```

`./apiAlerts.py -d 0.0011 -c xyz | jq .`   
```{
  "level": "ERROR",
  "deviation": "-",
  "data": {
    "error_desc": "Supplied value 'XYZ' is not a valid symbol"
  }
}
```

`./apiAlerts.py -d 0.0011 -c`
```
ERROR: GetoptError was raised: option -c requires argument
```

`./apiAlerts.py -c btcusd | jq .` 
```{
  "timestamp": "2024-06-04T22:13:31.436689",
  "trading_pair": "btcusd",
  "level": "INFO",
  "deviation": false
}
```