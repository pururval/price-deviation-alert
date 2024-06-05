# price-deviation-alert
Generate a log alert if the standard deviation from the hourly prices of a currency pair for past 24 hours is more than 1 (or any indicated value in the CLI parameter defined in the tool)

## Deliverables:
### 1. Instructions for running your script
- Make the python script executable. 
    
    ```bash
    chmod 755 apiAlerts.py
    ```
- Create and activate the virtual environment `myenv`. 
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```
- Get the dependencies from `requirements.txt`.

    ```bash
    pip3 install -r requirements.txt
    ```
- Deactivate the virtual environment when finished testing the apiAlerts.py script.

    ```bash
    deactivate 
    ```
    Example 1: using default deviation=1 for currency=btcusd

          
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

    Example 2: using deviation=3.2 for currency=btcusd
        
    ```bash
    ./apiAlerts.py -d 3.2 -c btcusd | jq .
    ```    
    ```JSON
    {
        "timestamp": "2024-06-05T08:57:55.553131",
        "trading_pair": "btcusd",
        "level": "INFO",
        "deviation": false
    }
    ```


### 2. Dependencies

Install the dependencies specified in `requirements.txt`.

```bash
pip3 install -r requirements.txt
```
    
    
### 3. Optional: A dockerfile to run the script
### 4. What you would do next to further improve it
- 
### 5. Other interesting checks you might implement to alert on market behaviour
- 
### 6. Approach to solving the task, and any issues you faced with implementation
    
1. Started with the search on gemini api for relavant endpoints
2. Found ticker/v2 which provided past 24 hr values for a currencypair
3. Implemented the basic math for mean, SD and change using ticker/v2 api call.
    - Was confused in technicality of SD vs sdevs (z index) and meaning of notional value. Youtube saved the day.
    - The ticker/v2 api call didnt have timestamp so would need ticker/v1 to retrieve that but things got rough when there was data descrepency in response of closing val from v1 and v2. Ended up realising that timestamp refers to the log time as hourly time closing value wouldnt really help in alert feature.
4. Implemented args for custom sdev and currency
5. Testing on various cases of faulty inputs
6. Code restructuring and redundancy removal
7. Documentation with examples on how to use the script 

### 7. The time taken to write it
- ~4 hrs

### 8. Example cases
- Example: Help page

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

- Example: Deviation true on custom SD and currency:btcusd

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
- Example: Deviation False on default SD and currency:btcusd

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

- Example: Invalid currency symbol

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

- Example: Invalid argument - missing currency symbol

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