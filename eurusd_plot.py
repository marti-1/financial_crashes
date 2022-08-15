# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%

df = pd.read_csv("data/DEXUSEU.csv")
df['DATE'] = pd.to_datetime(df['DATE'])
df = df[df['DEXUSEU'] != "."]
df['DEXUSEU'] = df['DEXUSEU'].astype(float)
df.set_index('DATE', inplace=True)

# %%

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