# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
# set linewidth to 1
plt.rcParams['lines.linewidth'] = 1
# get nasdaq data from yahoo finance
nasdaq = yf.download("^IXIC", start="2000-01-01", end="2003-01-01")
nasdaq.head()

# %%
# get price up to 2001-01

dates = [
    "2000-03-28",
    "2000-05-11",
    "2000-05-19",
]

for dt in dates:
    plt.plot(
        nasdaq[nasdaq.index <= dt]["Adj Close"],
        color='k'
    )
    plt.plot(
        nasdaq[nasdaq.index > dt]["Adj Close"],
        color='lightgray'
    )

    plt.xticks(rotation=45)
    # set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
    # plt.set_major_formatter(mdates.DateFormatter('%y-%m'))
    # title
    plt.title("NASDAQ")
    # save plot to file
    plt.savefig(f"plots/nasdaq_{dt}.svg", format="svg")