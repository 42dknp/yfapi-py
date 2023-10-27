# Yahoo Finance API Client for Python

This is an unofficial API Client for Yahoo Finance written in Python. 


## Use it in your project


### Get Similar Stocks for a given Stock Symbol

```python
from client.api.similar_securities import SimilarSecurities

get_similar_securities = SimilarSecurities()

# Setup Security (e.g. AMD Stock)
symbol = "AAPL"

similar_securities_data = get_similar_securities.get_similar_securities(symbol)

print(similar_securities_data)
```

Output:
```bash
['AMZN', 'TSLA', 'GOOG', 'META', 'NFLX']
```


### Get a Yahoo Finance API Crumb

You will need a valid crumb for usage of certain API calls (or at least if you want to reuse your crumb instead of getting a new one if not necessary).

```python
from client.api.crumb import Crumb

getCrumb = Crumb()

newCrumb = getCrumb.get_crumb()

print(newCrumb)
```


### Get Historic Data / Chart Data for Stock Symbols

getStocksCharts expect 3 parameters:
1. **Stock Symbol**: e.g. "AMD"
2. **Start Date**: the function expects a timestamp. You can use DateTime() to generate it.
3. **End Date**: a second timestamp greater than Start Date.

```python
from datetime import datetime
from client.api.historic_data import HistoricData

get_historic_data = HistoricData()

# Setup Start Date and End Date (range of dates for historic data)
start_date = datetime.strptime("2023-10-01", "%Y-%m-%d")  # creates a datetime object
end_date = datetime.strptime("2023-10-13", "%Y-%m-%d")  # creates a datetime object

# Setup Security (e.g. AMD Stock)
symbol = "NVDA"

historic_data = get_historic_data.get_historic_data(symbol, start_date, end_date)
```

#### Helper Functions for Historic Data

You can also use different Helper Functions:

```php
// Get Historic Data for last week
historic_data = get_historic_data.get_historic_data_last_week(symbol)
```
```php
// Get Historic Data for last month
historic_data = get_historic_data.get_historic_data_last_month(symbol)
```
```php
// Get Historic Data for last 30 Days
historic_data = get_historic_data.get_historic_data_last_30_days(symbol)
```
```php
// Get Historic Data for last year
historic_data = get_historic_data.get_historic_data_last_year(symbol)
```
```php
// Get Historic Data for YTD
historic_data = get_historic_data.get_historic_data_ytd(symbol)
```

**Output**
The above code will output a list of dictionaries ```[{...},{...},{...}] ``` you can easily iterate through, that includes:
- timestamp
- open Price
- low Price
- high Price
- close Price
- adjusted Price

```bash
....
[{'timestamp': 1696253400, 'open': 102.20999908447266, 'low': 101.69999694824219, 'high': 103.70999908447266, 'close': 103.2699966430664, 'adjclose': 103.2699966430664}, 
{...}]
```

### Get Quote Data for Stock Symbols

getStocksCharts expect 3 parameters:
1. **Stock Symbol**: e.g. "AMD"
2. **Start Date**: the function expects a timestamp. You can use DateTime() to generate it.
3. **End Date**: a second timestamp > than Start Date.

```python
from client.api.quote import Quote

get_quote = Quote()

symbol = "GS"

quote_data = get_quote.get_quote(symbol)

print(quote_data)
```

Output:
Here is a dictionary with these Elements:

- fullExchangeName
- symbol
- language
- uuid
- quoteType
- typeDisp
- currency
- exchangeTimezoneName
- exchangeTimezoneShortName
- customPriceAlertConfidence
- marketState
- market
- quoteSourceName
- messageBoardId
- exchange
- shortName
- region
- longName
- fiftyTwoWeekLowChangePercent
- regularMarketOpen
- regularMarketTime
- regularMarketChangePercent
- regularMarketDayRange
- fiftyTwoWeekLowChange
- fiftyTwoWeekHighChangePercent
- regularMarketDayHigh
- sharesOutstanding
- fiftyTwoWeekHigh
- regularMarketPreviousClose
- fiftyTwoWeekHighChange
- marketCap
- regularMarketChange
- fiftyTwoWeekRange
- fiftyTwoWeekLow
- regularMarketPrice
- regularMarketVolume
- regularMarketDayLow

```bash
{'fullExchangeName': 'NYSE', 'symbol': 'GS', 'fiftyTwoWeekLowChangePercent': 0.003757112, 'regularMarketOpen': 298.29, 'language': 'en-US', 'regularMarketTime': 1698091202, ...
```


## Output Formats
Here is a list of default Output formats:

#### Historic Data
**Default**: dict (its a list with dicts) | **Optional**: raw (json text string)

#### Quote
**Default**: dict | **Optional**: raw (json text string)

#### Similar Securities
**Default**: list | **Optional**: raw (json text string)

#### Crumb
**Default**: string (you can´t change the output attribute) | **Optional**: none



## By changing the instance attribute "output" you can get a different output format

Example:

```python
from client.api.similar_securities import SimilarSecurities

get_similar_securities = SimilarSecurities()

# you can also this to "raw" or "list" (default for Similar Securities)
get_similar_securities.output = "raw"

symbol = "AAPL"

similar_securities_data = get_similar_securities.get_similar_securities(symbol)

print(similar_securities_data)
```
So we change the instance attribute ```get_similar_securities.output = "raw"``` and now we get the raw json string from the API.

## Testing
You can use my Makefile to run Unit Tests and Code Validation Tests:
```shell
// run unittest
make test
```
```shell
// run pylint, mypy + flake8
make validate
```


### Coming soon
- Search 
- Dividend History
- Ownerships
- Financial Statements Yearly / Quarterly (Income Statement, Balance Sheets & Cash Flow)
- ESG Scores
- more Helper Functions
- more Test Functions (especially Integration & in-deph API)


# Legal Disclaimer

Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc.

This project is for research purposes only! It is not affiliated, endorsed, or vetted by Yahoo, Inc!
yfapi-php is an open-source API Client for PHP that uses Yahoo's publicly available APIs.
