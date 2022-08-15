# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%
ff = pd.read_csv("data/DCOILWTICO.csv")
ff['DATE'] = pd.to_datetime(ff['DATE'])
# remove all rows where value = "."
ff = ff[ff['DCOILWTICO'] != "."]
# convert DCOILWTICO to float
ff['DCOILWTICO'] = ff['DCOILWTICO'].astype(float)
ff.set_index('DATE', inplace=True)
ff.head()

# %%

start = "1998-01-01"
end = "2003-01-01"

midpoints = [
    "2000-03-28",
    "2000-07-14"
]

for midpoint in midpoints:
    plt.figure(figsize=(5,3))
    # select ff from start to midpoint
    ff_start = ff[(ff.index >= start) & (ff.index <= midpoint)]
    # select ff from midpoint to end
    ff_rest = ff[(ff.index > midpoint) & (ff.index <= end)]

    # plot ff from start to midpoint
    plt.plot(ff_start['DCOILWTICO'], color='k')
    # plot ff from midpoint to end
    plt.plot(ff_rest['DCOILWTICO'], color='lightgray')
    # set x-axis to date format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
    # rotate x-axis labels
    plt.xticks(rotation=45)
    plt.title('Crude Oil Prices')
    plt.tight_layout()
    plt.savefig(f"plots/oil_prices_{midpoint}.svg", format="svg")