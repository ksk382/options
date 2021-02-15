import yfinance as yf
import json
import pandas as pd

msft = yf.Ticker("VERI")

# get stock info
d = msft.info
print(json.dumps(d, indent=4, sort_keys=True))



