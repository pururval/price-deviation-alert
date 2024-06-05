# price-deviation-alert
Generate a log alert if the standard deviation from the hourly prices of a currency pair for past 24 hours is more than 1 (or any indicated value in the CLI parameter defined in the tool)

## Deliverables:
### 1. Instructions for running the script

The main command to run the script and get the expected result:   
    
```
./apiAlerts.py -c btcusd | jq .
```    
```JSON
{
  "timestamp": "2024-06-05T11:32:27.084487",
  "trading_pair": "btcusd",
  "level": "INFO",
  "deviation": true,
  "data": {
    "last_price": "70454.62",
    "average": "70806.03375",
    "change": "-351.413750000007",
    "sdev": "1.5625445321221245"
  }
}
```
 If you face issues with file permissions or dependencies, try using a python virtual environment or making the file executable using the troubleshooting steps below. 
- Specify to use python interpretter if it errors with `import not found` (Optional)
    ```bash
    python3 apiAlerts.py -c btcusd | jq .
    ```    

- To make the python script executable if there are permission errors. (Optional)
    
    ```bash
    chmod 755 apiAlerts.py
    ```
- Create and activate the virtual environment `myenv`. 
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```
- Get the dependencies from `requirements.txt`, mainly for `import requests`.

    ```bash
    pip3 install -r requirements.txt
    ```
- After this, run `./apiAlerts.py -c btcusd | jq .` to test the script.
- Deactivate the virtual environment when finished testing.

    ```bash
    deactivate 
    ```
    
    >Example 1: using default deviation (1) for currency=btcusd

          
    ```bash
    ./apiAlerts.py -c btcusd | jq .
    ```
        
    ```JSON
    {
        "timestamp": "2024-06-05T08:57:03.645215",
        "trading_pair": "btcusd",
        "level": "INFO",
        "deviation": true,
        "data": {
            "last_price": "68927.87",
            "average": "70621.04791666666",
            "change": "-1693.1779166666674",
            "sdev": "3.118404410304019"
        }
    }
    ```

    >Example 2: using deviation=3.2 for currency=ethusd
        
    ```bash
    ./apiAlerts.py -d 3.2 -c ethusd | jq .
    ```    
    ```JSON
    {
        {
        "timestamp": "2024-06-05T11:28:30.532493",
        "trading_pair": "ethusd",
        "level": "INFO",
        "deviation": false
        }
    }
    ```


### 2. Dependencies

Install the dependencies specified in `requirements.txt`.

```bash
pip3 install -r requirements.txt
```
    
    
### 3. Optional: A dockerfile to run the script

### 4. What next to further improve it
- Add unit tests
- Improve logging by ouput to file and flags for various levels like DEBUG, WARNING to be set as argument.
- Optimize api call and calculations for performance
- Dockerize the app
- Improve documenation with better formatting and API refrences

### 5. Other interesting checks to implement to alert on market behaviour
- Implement a cache for unusual spikes or changes since the app was started and compare with general behavior
- Find correlations on different currency trends
- Extend daily results and add fields for weekly or monthly results
- Alert when price reaches peaks or when it reverses

### 6. Approach to solving the task, and any issues faced with implementation
    
- Started with the search on gemini api for relavant endpoints
- Found ticker/v2 which provided past 24 hr values for a currencypair
- Implemented the basic math for mean, SD and change using ticker/v2 api call.
    - Was confused in technicality of SD vs sdevs (z index) and meaning of notional value. Youtube saved the day.
    - The ticker/v2 api call didnt have timestamp so would need ticker/v1 to retrieve that but things got rough when there was data descrepency in response of closing val from v1 and v2. Ended up realising that timestamp refers to the log time as hourly time closing value wouldnt really help in alert feature.
- Implemented args for custom sdev and currency
- Testing on various cases of faulty inputs
- Code restructuring and redundancy removal
- Documentation with examples on how to use the script 

### 7. The time taken to write it
&nbsp;&nbsp;&nbsp;&nbsp; ~4 hrs

### 8. Examples
>Example 3: Help page

```bash
./apiAlerts.py -h
```

```bash
2024-06-04 21:51:51,657420 - AlertingTool - INFO - Parsing args

usage: apiAlerts.py [-h] [-c CURRENCY] [-d DEVIATION]

Runs checks on API

optional arguments:
-h, --help                               show this help message and exit
-c CURRENCY, --currency CURRENCY         The currency trading pair, or ALL
-d DEVIATION, --deviation DEVIATION      standard deviation threshold. eg. 1
```

>Example 4: Deviation true on custom SD and currency:btcusd

```bash
./apiAlerts.py -d 0.0011 -c btcusd | jq .
```
```JSON
{
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
>Example 5: Deviation False on default SD and currency:btcusd

```bash
./apiAlerts.py -c btcusd | jq . 
```
```JSON
{
    "timestamp": "2024-06-04T22:13:31.436689",
    "trading_pair": "btcusd",
    "level": "INFO",
    "deviation": false
}
```

>Example 6: Invalid currency symbol

```bash
./apiAlerts.py -d 0.0011 -c xyz | jq .
```   
```JSON
{
    "level": "ERROR",
    "deviation": "-",
    "data": {
        "error_desc": "Supplied value 'XYZ' is not a valid symbol"
    }
}
```

>Example 7: Invalid argument - missing currency symbol

```bash
./apiAlerts.py -d 3 -c | jq .
```

```bash
parse error: Invalid numeric literal at line 1, column 6
```

```bash
./apiAlerts.py -d 3 -c
```

```bash
ERROR: GetoptError was raised: option -c requires argument
```