# imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 2. Visualize store visits
# 2.a Using a tool of your choice, visualize the trend of unique visits for all places

# open final_df
final_df = pd.read_csv("./out_data/analysis.csv")
# transform column "date" into datetime object
final_df["date"] = pd.to_datetime(final_df["date"])

# create a line plot
plt.figure(figsize=(16, 9))
sns_plot = sns.lineplot(data=final_df,
                        x="date",
                        y="unique_visits",
                        hue="store_name",
                        estimator="sum",  # the default is "mean"
                        ci=None)  # disable confidence intervals
plt.title("Trend of unique visits for each store")
# save the plot
sns_plot.figure.savefig("./out_data/trend_of_unique_visits.png")
# display the plot
plt.show()
