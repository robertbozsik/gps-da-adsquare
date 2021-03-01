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
                        ci=None)  # disable confidence intervals
plt.title("Trend of unique visits for each store")
# save the plot
sns_plot.figure.savefig("./out_data/trend_of_unique_visits.png")
# display the plot
plt.show()

# Visualizing the unique visits for each store id caused a huge mess on the plot as
# there are 186 unique store ids, for this reason, I decided to plot the trend for each store name.

# 2.b Is there any anomaly? Add a comment about your observation
# Based on the sample data (smaller dataset):
# There is a significant drop in the number of unique visits on the 17th of January by Kaufland, Lexus,
# Burger King, Rewe, and Aldi. Almost all the shops must have been closed that day, as it was Sunday.
# The Chancellor announced extended lockdown, what was already expected a couple of days before.
# It could explain the rising trend before the 17th, the drop on the day, and the increase right after.
