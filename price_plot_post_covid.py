# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
# set linewidth to 1
plt.rcParams['lines.linewidth'] = 1
# get nasdaq data from yahoo finance
nasdaq = yf.download("^IXIC", start="2021-01-01")


# %% clear plots directory of all old plots

# # get all files in data directory
# import os
# files = os.listdir("plots")
# # get all files with .svg extension
# files = [file for file in files if file.endswith(".svg")]
# # delete all files
# for file in files:
#     if "nasdaq_" in file:
#         os.remove("plots/" + file)

# %% get the dates for the plots

dates = []
with open("POSTCOVID.md") as f:
    # read the file line by line
    for line in f:
        # check if line matches ![](nasdaq_*.svg) pattern
        if "![](./plots/nasdaq" in line:
            # get the date from the line
            date = line.split("nasdaq_")[1].split(".svg")[0]
            # add the date to the list
            dates.append(date)

# %% generate the plots

for dt in dates:
    plt.figure(figsize=(5,3))
    plt.plot(
        nasdaq[nasdaq.index <= dt]["Adj Close"],
        color='k'
    )
    plt.plot(
        nasdaq[nasdaq.index >= dt]["Adj Close"],
        color='lightgray'
    )

    plt.xticks(rotation=45)
    # set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
    # plt.set_major_formatter(mdates.DateFormatter('%y-%m'))
    # title
    plt.title("NASDAQ")
    plt.tight_layout()
    # save plot to file
    plt.savefig(f"plots/nasdaq_{dt}.svg", format="svg")
    # close figure
    plt.close()