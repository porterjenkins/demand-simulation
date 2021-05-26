import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


df = pd.read_csv("output.csv")
df['day'] = pd.to_datetime(df['day'])
agg = df[['quantity', "day", "product"]].groupby(["day", "product"]).sum().reset_index()

ax = plt.figure(figsize=(12, 8))

for key, group in agg.groupby("product"):
    plt.plot(group["day"].values, group["quantity"].values, marker='o', linestyle='--', label=key)

plt.legend(loc='best')
plt.xlabel("Time")
plt.ylabel("Quantity Sold")
plt.savefig("time-series.png")