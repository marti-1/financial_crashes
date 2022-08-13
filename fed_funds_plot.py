# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# %%
ff = pd.read_csv("DFF.csv")
ff['DATE'] = pd.to_datetime(ff['DATE'])
ff.set_index('DATE', inplace=True)
ff.head()

# %%

start = "2000-01-01"
end = "2003-01-01"

midpoints = [
    "2000-05-30"
]

for midpoint in midpoints:
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
    plt.savefig(f"plots/ff_effective_rate_{midpoint}.svg", format="svg")