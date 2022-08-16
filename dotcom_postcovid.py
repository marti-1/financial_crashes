import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import yfinance as yf

def plot_cape_peak_chart():
    df = pd.read_csv('./data/CAPE.csv', delimiter=';')
    # replace "," in Date with "-"
    df['Date'] = df["Date"].str.replace(",", "-")
    df['Date'] = pd.to_datetime(df['Date'])
    # convert Earnings to float
    df['CAPE'] = df['CAPE'].str.replace(",",".").astype(float)
    df.set_index('Date', inplace=True)
    # sort df by index
    df.sort_index(inplace=True)
    plt.plot(df.CAPE, color='gray')
    # plot median CAPE as horizontal line
    plt.axhline(df.CAPE.median(), color='k', linestyle='--')
    # plot red dot on 2000-01
    plt.plot(pd.to_datetime('2000-01'), df.CAPE['2000-01-01'], 'ro')
    plt.plot(pd.to_datetime('2021-11'), df.CAPE['2021-11-01'], 'ro')
    # title "CAPE"
    plt.title('CAPE')

def plot_cpi_charts(mid1, mid2):
    df = pd.read_csv("data/CPIAUCSL.csv")
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.set_index('DATE', inplace=True)
    df['yoy'] = (df['CPIAUCSL'] - df['CPIAUCSL'].shift(12)) / df['CPIAUCSL'].shift(12) * 100
    df['yoy'] = df['yoy'].round(2)

    cpi_dotcom = df[(df.index >= '1999-01-01') & (df.index <= '2002-01-01')]
    # filter cpi_dotcom up to 2000-01-01
    cpi_dotcom_head = cpi_dotcom[(cpi_dotcom.index <= mid1)]
    # filter cpi_dotcom from 2000-01-01 to 2020-01-01
    cpi_dotcom_tail = cpi_dotcom[(cpi_dotcom.index >= mid1)]
    # cpi_dotcom_head = 
    cpi_postcovid = df[(df.index >= '2021-01-01')]
    cpi_postcovid_head = cpi_postcovid[(cpi_postcovid.index <= mid2)]
    cpi_postcovid_tail = cpi_postcovid[(cpi_postcovid.index >= mid2)]

    # plot cpi_dotcom and cpi_postcovid as 1,2 subplot
    fig, axs = plt.subplots(1, 2, figsize=(7,3))
    # set major formatter
    axs[0].xaxis.set_major_locator(mdates.YearLocator())
    axs[0].plot(cpi_dotcom_head['yoy'], color='k')
    axs[0].plot(cpi_dotcom_tail['yoy'], color='lightgray')
    axs[0].set_title('Dot-com Inflation')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('YoY Inflation')

    axs[1].xaxis.set_major_locator(mdates.YearLocator())
    axs[1].plot(cpi_postcovid_head['yoy'], color='k')
    axs[1].plot(cpi_postcovid_tail['yoy'], color='lightgray')
    axs[1].set_title('Post-Covid Inflation')
    axs[1].set_xlabel('Year')

def plot_oil_charts(mid1, mid2):
    df = pd.read_csv("data/DCOILWTICO.csv")
    df['DATE'] = pd.to_datetime(df['DATE'])
    # convert DATE to date

    # remove all rows where value = "."
    df = df[df['DCOILWTICO'] != "."]
    # convert DCOILWTICO to float
    df['DCOILWTICO'] = df['DCOILWTICO'].astype(float)
    df.set_index('DATE', inplace=True)

    # resample oil prices to monthly
    df = df.resample("M").last()
    # add one day to oil.index
    df.index = df.index + pd.Timedelta(days=1)

    oil_dotcom = (df[(df.index >= '1999-01-01') & (df.index <= '2002-01-01')].pct_change()+1).cumprod()
    # filter cpi_dotcom up to 2000-01-01
    oil_dotcom_head = oil_dotcom[(oil_dotcom.index <= mid1)]
    # filter cpi_dotcom from 2000-01-01 to 2020-01-01
    oil_dotcom_tail = oil_dotcom[(oil_dotcom.index >= mid1)]
    # cpi_dotcom_head = 
    oil_postcovid = (df[(df.index >= '2021-01-01')].pct_change()+1).cumprod()
    oil_postcovid_head = oil_postcovid[(oil_postcovid.index <= mid2)]
    oil_postcovid_tail = oil_postcovid[(oil_postcovid.index >= mid2)]

    # plot cpi_dotcom and cpi_postcovid as 1,2 subplot
    fig, axs = plt.subplots(1, 2, figsize=(7,3))
    # set major formatter
    axs[0].xaxis.set_major_locator(mdates.YearLocator())
    axs[0].plot(oil_dotcom_head['DCOILWTICO'], color='k')
    axs[0].plot(oil_dotcom_tail['DCOILWTICO'], color='lightgray')
    axs[0].set_title('Dot-com Oil Prices')
    axs[0].set_xlabel('Year')

    axs[1].xaxis.set_major_locator(mdates.YearLocator())
    axs[1].plot(oil_postcovid_head['DCOILWTICO'], color='k')
    axs[1].plot(oil_postcovid_tail['DCOILWTICO'], color='lightgray')
    axs[1].set_title('Post-Covid Oil Prices')
    axs[1].set_xlabel('Year')

def plot_ff_effective_charts(m1, m2):
    ff = pd.read_csv("data/DFF.csv")
    ff['DATE'] = pd.to_datetime(ff['DATE'])
    ff.set_index('DATE', inplace=True)

    # filter cpi_dotcom up to 2000-01-01
    ff_dotcom_head = ff[(ff.index >= '1999-01-01') & (ff.index <= m1)]
    # filter cpi_dotcom from 2000-01-01 to 2020-01-01
    ff_dotcom_tail = ff[(ff.index >= m1) & (ff.index <= '2002-01-01')]
    # cpi_dotcom_head = 
    ff_postcovid = ff[(ff.index >= '2021-01-01')]
    ff_postcovid_head = ff_postcovid[(ff_postcovid.index <= m2)]
    ff_postcovid_tail = ff_postcovid[(ff_postcovid.index >= m2)]

    # plot cpi_dotcom and cpi_postcovid as 1,2 subplot
    fig, axs = plt.subplots(1, 2, figsize=(7,3))
    # set major formatter
    axs[0].xaxis.set_major_locator(mdates.YearLocator())
    axs[0].plot(ff_dotcom_head['DFF'], color='k')
    axs[0].plot(ff_dotcom_tail['DFF'], color='lightgray')
    axs[0].set_title('Dot-com FF Efective Rate')
    axs[0].set_xlabel('Year')

    axs[1].xaxis.set_major_locator(mdates.YearLocator())
    axs[1].plot(ff_postcovid_head['DFF'], color='k')
    axs[1].plot(ff_postcovid_tail['DFF'], color='lightgray')
    axs[1].set_title('Post-Covid FF Efective Rate')
    axs[1].set_xlabel('Year')

def plot_nasdaq_charts_aligned():
    nasdaq = yf.download('^IXIC', start='1998-01-01')
    # filter df from 2000-01-03 to 2000-11-01
    dotcom = nasdaq.loc['1999-12-31':'2000-11-01']
    # get numpy array of closing prices
    dotcom_r = (dotcom['Adj Close'].pct_change()+1).cumprod()
    # replace NaN with 1
    dotcom_r.fillna(1, inplace=True)

    postcovid = nasdaq.loc['2021-02-12':]
    postcovid_r = (postcovid['Adj Close'].pct_change()+1).cumprod()
    postcovid_r.fillna(1, inplace=True)

    fig, ax1 = plt.subplots()
    ax1.plot(dotcom_r.values, label='dotcom', color='gray')
    ax1.set_ylabel('Dot-com')

    ax2 = ax1.twinx()
    # create a list of numbers from 0 to postcovid_r.shape[0] with step size of 3.5
    x = np.floor(np.arange(0, postcovid_r.shape[0], 3.5))
    # convert x to int
    x = x.astype(int)
    ax2.plot(postcovid_r.values[x], color='tab:red')
    ax2.set_ylabel('Post-Covid')
    # color y-axis red
    ax2.tick_params(axis='y', labelcolor='tab:red')
    # color y-axis ticks red
    ax2.tick_params(axis='y', colors='tab:red')
    # color y-axis label red
    ax2.yaxis.label.set_color('tab:red')
    # title
    plt.title('NASDAQ')
    plt.show()