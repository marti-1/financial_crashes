# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%

df = pd.read_csv("data/CPIAUCSL.csv")
df['DATE'] = pd.to_datetime(df['DATE'])
df.set_index('DATE', inplace=True)
df['yoy'] = (df['CPIAUCSL'] - df['CPIAUCSL'].shift(12)) / df['CPIAUCSL'].shift(12) * 100
df['yoy'] = df['yoy'].round(2)

# %%

dates = [
    (
        "1998-01-01",
        "2003-01-01",
        [
            "2000-03-01",
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