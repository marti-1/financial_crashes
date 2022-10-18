# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
import datetime

plt.rcParams['lines.linewidth'] = 1


# %% REMOVE OLD PLOTS

# get all files in data directory
files = os.listdir("plots")
# get all files with .svg extension
files = [file for file in files if file.endswith(".svg")]
# delete all files
for file in files:
    os.remove("plots/" + file)

# %% CREATE PRICE PLOTS

price_conf = [
    {
        'ticker': '^IXIC',
        'start': '2000-01-01',
        'end': '2003-01-01',
        'doc': 'DOTCOM.md',
        'prefix': 'nasdaq_',
        'title': 'NASDAQ'
    },
    {
        'ticker': '^IXIC',
        'start': '2021-01-01',
        'doc': 'POSTCOVID.md',
        'prefix': 'nasdaq_',
        'title': 'NASDAQ'       
    }
]

for conf in price_conf:
    today = datetime.date.today().strftime("%Y-%m-%d")
    df = yf.download(conf['ticker'], start=conf['start'], end=conf.get("end",today))
    dates = []
    with open(conf['doc'], encoding='utf8') as f:
        # read the file line by line
        for line in f:
            # check if line matches ![](nasdaq_*.svg) pattern
            if "![](./plots/nasdaq" in line:
                # get the date from the line
                date = line.split(conf['prefix'])[1].split(".svg")[0]
                # add the date to the list
                dates.append(date)
        
        for dt in dates:
            plt.figure(figsize=(5,3))

            plt.plot(
                df[df.index >= dt]["Adj Close"],
                color='lightgray'
            )

            plt.plot(
                df[df.index <= dt]["Adj Close"],
                color='k'
            )

            plt.xticks(rotation=45)
            # set x-axis to date format
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
            # title
            plt.title(conf['title'])
            plt.tight_layout()
            # save plot to file
            plt.savefig(f"plots/{conf['prefix']}{dt}.svg", format="svg")
            # close figure
            plt.close()

            
# %% GET OIL PRICES

oil = pd.read_csv("data/DCOILWTICO.csv")
oil['DATE'] = pd.to_datetime(oil['DATE'])
# convert DATE to date

# remove all rows where value = "."
oil = oil[oil['DCOILWTICO'] != "."]
# convert DCOILWTICO to float
oil['DCOILWTICO'] = oil['DCOILWTICO'].astype(float)
oil.set_index('DATE', inplace=True)

# resample oil prices to monthly
oil = oil.resample("M").last()
# add one day to oil.index
oil.index = oil.index + pd.Timedelta(days=1)

# %%
dates = [
    (
        "1998-01-01",
        "2003-01-01",
        [
            "2000-03-01",
            "2000-04-01",
            "2000-05-01",
            "2000-06-01",
            "2000-07-01",
            "2000-08-01",
            "2000-10-12"
        ]
    ),
    (
        "2021-01-01",
        "2023-01-01",
        [
            "2022-06-01"
        ]
    )
]

for start, end, midpoints in dates:
    for midpoint in midpoints:
        plt.figure(figsize=(5,3))
        # select ff from start to midpoint
        oil_start = oil[(oil.index >= start) & (oil.index <= midpoint)]
        # select ff from midpoint to end
        oil_rest = oil[(oil.index >= midpoint) & (oil.index <= end)]

        plt.plot(oil_rest['DCOILWTICO'], color='lightgray')
        plt.plot(oil_start['DCOILWTICO'], color='k')

        # set x-axis to date format
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
        # rotate x-axis labels
        plt.xticks(rotation=45)
        plt.title('Crude Oil Prices')

        plt.grid(color='#f0f0f0')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(f"plots/oil_prices_{midpoint}.svg", format="svg")
        plt.savefig(f"plots/oil_prices_{midpoint}.png", format="png")
        # close figure
        plt.close()

        
# %% PLOT CPI

df = pd.read_csv("data/CPIAUCSL.csv")
df['DATE'] = pd.to_datetime(df['DATE'])
df.set_index('DATE', inplace=True)
df['yoy'] = (df['CPIAUCSL'] - df['CPIAUCSL'].shift(12)) / df['CPIAUCSL'].shift(12) * 100
df['yoy'] = df['yoy'].round(2)

dates = [
    (
        "1998-01-01",
        "2003-01-01",
        [
            "2000-03-01",
            "2000-04-01",
            "2000-05-01"
        ]
    ),
    (
        "2021-01-01",
        "2023-01-01",
        [
            "2022-06-01"
        ]
    )
    
]

for start, end, midpoints in dates:
    for midpoint in midpoints:
        plt.figure(figsize=(5,3))
        # select df from start to midpoint
        df_start = df[(df.index >= start) & (df.index <= midpoint)]
        # select df from midpoint to end
        df_rest = df[(df.index >= midpoint) & (df.index <= end)]

        # plot df from midpoint to end
        plt.plot(df_rest['yoy'], color='lightgray')
        # plot df from start to midpoint
        plt.plot(df_start['yoy'], color='k')
        # set x-axis to date format
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
        # rotate x-axis labels
        plt.xticks(rotation=45)
        plt.title('CPI YoY Inflation')
        plt.tight_layout()

        plt.grid(color='#f0f0f0')
        plt.grid(True)

        plt.savefig(f"plots/cpi_{midpoint}.svg", format="svg")
        # close figure
        plt.close()

        
# %% PLOT FED FUNDS

ff = pd.read_csv("data/DFF.csv")
ff['DATE'] = pd.to_datetime(ff['DATE'])
ff.set_index('DATE', inplace=True)

start = "2000-01-01"
end = "2003-01-01"

midpoints = [
    "2000-03-28",
    "2000-05-23"
]

for midpoint in midpoints:
    plt.figure(figsize=(5,3))
    # select ff from start to midpoint
    ff_start = ff[(ff.index >= start) & (ff.index <= midpoint)]
    # select ff from midpoint to end
    ff_rest = ff[(ff.index > midpoint) & (ff.index <= end)]

    # plot ff from start to midpoint
    plt.plot(ff_start['DFF'], color='k')
    # plot ff from midpoint to end
    plt.plot(ff_rest['DFF'], color='lightgray')
    # set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
    # rotate x-axis labels
    plt.xticks(rotation=45)
    plt.title('FF Effective Rate')
    plt.tight_layout()
    plt.savefig(f"plots/ff_effective_rate_{midpoint}.svg", format="svg")
    # close figure
    plt.close()

# %% PLOT EARNINGS
e = pd.read_csv("data/sp500_earnings.csv", delimiter=";")
# replace "," in Date with "-"
e["Date"] = e["Date"].str.replace(",", "-")
e['Date'] = pd.to_datetime(e['Date'])
# convert Earnings to float
e['Earnings'] = e['Earnings'].str.replace(",",".").astype(float)
e.set_index('Date', inplace=True)

start = "2000-01-01"
end = "2003-01-01"

midpoints = [
    "2000-06-01",
    "2000-07-01",
    "2000-08-01"
]

for midpoint in midpoints:
    # select ff from start to midpoint
    e_start = e[(e.index >= start) & (e.index <= midpoint)]
    # select ff from midpoint to end
    e_rest = e[(e.index >= midpoint) & (e.index <= end)]

    plt.figure(figsize=(5,3))
    # plot ff from start to midpoint
    plt.plot(e_start['Earnings'], color='k')
    # plot ff from midpoint to end
    plt.plot(e_rest['Earnings'], color='lightgray')
    # set x-axis to date format
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator((1,4,7,10)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))

    # rotate x-axis labels
    plt.xticks(rotation=45)
    plt.title('S&P500 Earnings')
    # show grid
    # set grid color to lightgray
    plt.grid(color='#f0f0f0')
    plt.grid(True)
    # use tight layout
    plt.tight_layout()
    # plt.show()
    # set figure size
 
    plt.savefig(f"plots/earnings_{midpoint}.svg", format="svg")
    plt.close()

    
# %% plot EUR/USD

df = pd.read_csv("data/DEXUSEU.csv")
df['DATE'] = pd.to_datetime(df['DATE'])
df = df[df['DEXUSEU'] != "."]
df['DEXUSEU'] = df['DEXUSEU'].astype(float)
df.set_index('DATE', inplace=True)

start = "2000-01-01"
end = "2003-01-01"

midpoints = [
    "2000-05-19"
]

for midpoint in midpoints:
    plt.figure(figsize=(5,3))
    # select df from start to midpoint
    df_start = df[(df.index >= start) & (df.index <= midpoint)]
    # select df from midpoint to end
    df_rest = df[(df.index >= midpoint) & (df.index <= end)]

    # plot df from midpoint to end
    plt.plot(df_rest['DEXUSEU'], color='lightgray')
    # plot df from start to midpoint
    plt.plot(df_start['DEXUSEU'], color='k')
    # set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
    # rotate x-axis labels
    plt.xticks(rotation=45)
    plt.title('EUR/USD')
    plt.tight_layout()

    plt.grid(color='#f0f0f0')
    plt.grid(True)

    plt.savefig(f"plots/eurusd_{midpoint}.svg", format="svg")
    plt.close()
 
