# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%

e = pd.read_csv("sp500_earnings.csv", delimiter=";")
# replace "," in Date with "-"
e["Date"] = e["Date"].str.replace(",", "-")
e['Date'] = pd.to_datetime(e['Date'])
# convert Earnings to float
e['Earnings'] = e['Earnings'].str.replace(",",".").astype(float)
e.set_index('Date', inplace=True)

# %%

# get all files in data directory
import os
files = os.listdir("plots")
# get all files with .svg extension
files = [file for file in files if file.endswith(".svg")]
# delete all files
for file in files:
    if "earnings_" in file:
        os.remove("plots/" + file)

# %%

start = "2000-01-01"
end = "2003-01-01"

midpoints = [
    "2000-06-01"
]

for midpoint in midpoints:
    # select ff from start to midpoint
    e_start = e[(e.index >= start) & (e.index <= midpoint)]
    # select ff from midpoint to end
    e_rest = e[(e.index >= midpoint) & (e.index <= end)]

    # plot ff from start to midpoint
    plt.plot(e_start['Earnings'], color='k')
    # plot ff from midpoint to end
    plt.plot(e_rest['Earnings'], color='lightgray')
    # set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
    # rotate x-axis labels
    plt.xticks(rotation=45)
    plt.title('Earnings')
    plt.savefig(f"plots/earnings_{midpoint}.svg", format="svg")