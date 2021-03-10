# imports
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 2. Visualize store visits
# 2.a Using a tool of your choice, visualize the trend of unique visits for all places

# open final_df
final_df = pd.read_csv("./out_data_full/analysis.csv")
# transform column "date" into datetime object
final_df["date"] = pd.to_datetime(final_df["date"])


def plot_all_sores():
    """Plot and save the unique visits of each sotre."""
    # create a line plot
    plt.figure(figsize=(16, 9))
    sns_plot = sns.lineplot(data=final_df,
                            x="date",
                            y="unique_visits",
                            hue="store_name",
                            estimator="sum",  # the default is "mean"
                            ci=None)  # disable confidence intervals
    plt.title("Trend of unique visits for each store")
    plt.legend(loc="upper right")
    # save the plot
    sns_plot.figure.savefig("./out_data_full/trend_of_unique_visits.png")
    # display the plot
    plt.show()


def plot_a_store(name):
    """Plot and save the unique visits of the selected store."""
    s_name = name
    df = final_df.loc[final_df["store_name"] == s_name]
    # create a line plot
    plt.figure(figsize=(16, 9))
    sns_plot = sns.lineplot(data=df,
                            x="date",
                            y="unique_visits",
                            hue=None,
                            estimator="sum",  # the default is "mean"
                            ci=None)  # disable confidence intervals
    plt.title(f"Trend of unique visits for {s_name}")
    # save the plot
    sns_plot.figure.savefig(f"./out_data_full/unique_visits_of_{name}.png")
    # display the plot
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "plot_all_stores":
            plot_all_sores()
    elif len(sys.argv) == 3:
        command = sys.argv[1]
        store = sys.argv[2]
        if sys.argv[2] == "McDonald":
            store = "McDonald's"
        if command == "plot_a_store":
            plot_a_store(store)
    elif len(sys.argv) == 4:
        command = sys.argv[1]
        store_part_1 = sys.argv[2]
        store_part_2 = sys.argv[3]
        store = f"{store_part_1} {store_part_2}"
        if command == "plot_a_store":
            plot_a_store(store)
    else:
        print("""
        python(3) plot_full.py $params
        e.g. python(3) plot_full.py plot_all_stores (Plot and save the unique visits of each sotre.)
             python(3) plot_full.py plot_a_store Aldi (Plot and save the unique visits of the selected store.)
             available options as third parameter: Aldi, Burger King, McDonald, Renault, Rewe, Kaufland, Mercedes, Lexus, Subway
             (be precise by typing the name of the store)
             """)
