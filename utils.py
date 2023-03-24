import pandas as pd
import matplotlib.dates as mdates

def extract_plot_dates(prefix, lines):
    # find all lines that start with ![](./plots/gold_
    gold_lines = [line for line in lines if line.startswith(f"![](./plots/{prefix}")]
    # write regex that extracts date from line
    import re
    # extract dates from lines
    pattern = rf"!.*{prefix}(\d{{4}}-\d{{2}}-\d{{2}}).*"
    xs = [re.search(pattern, line, re.IGNORECASE).group(1) for line in gold_lines]
    return [pd.Timestamp(x) for x in xs]

def generate_gold_plots(dates, delta=pd.Timedelta('365 days')):
    gold = pd.read_csv('data/gold_prices_historical.csv')
    gold['Date'] = pd.to_datetime(gold['Date'])
    gold = gold.set_index('Date')
    for dt in dates:
        # subtract 1 year from a date
        d1 = dt - delta
        d2 = dt + delta

        # get gold price from d1 to d2
        gold1 = gold.loc[d1:d2]

        import matplotlib.pyplot as plt
        plt.figure(figsize=(5,3))
        plt.plot(
            gold1[gold1.index >= dt],
            color='lightgray'
        )

        plt.plot(
            gold1[gold1.index <= dt],
            color='k'
        )

        plt.xticks(rotation=45)
        # set x-axis to date format
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('\'%y-%m'))
        # title
        plt.title('Gold')
        plt.tight_layout()

        plt.savefig(f"plots/gold_{dt.strftime('%Y-%m-%d')}.svg", format="svg")
        # close figure
        plt.close()