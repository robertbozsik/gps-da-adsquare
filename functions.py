import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pytz  # python timezones


def date_from_utc_ms_ts(utc_ms_ts) -> str:
    """Return a date (yyyy-mm-dd) from a string of utc timestamp in milliseconds (timezone = Europe/Berlin).

    :param utc_ms_ts: Unix UTC timestamp in milliseconds (int or str)
    :return: date yyyy-mm-dd (str)
    """
    # convert from time stamp to datetime
    utc_datetime = dt.datetime.utcfromtimestamp(int(utc_ms_ts) / 1000)
    # set the timezone to UTC, and then convert to desired timezone
    date = (utc_datetime
            .replace(tzinfo=pytz.timezone('UTC'))
            .astimezone(pytz.timezone('Europe/Berlin'))
            .strftime('%Y-%m-%d'))
    return date


def list_from_affinities(aff_name: str) -> list:
    """Return a list created from the given user_affinity csv file."""
    aff_name = pd.read_csv(
        f"../assignment_data/affinities/{aff_name}.csv", header=None, names=[aff_name])
    aff_name = list(aff_name.iloc[:, 0])  # all rows, first column
    return aff_name


def plot_all_sores(final_df):
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
    plt.legend(loc="upper right")  # legend positioning
    # save the plot
    sns_plot.figure.savefig("./out_data_sample/trend_of_unique_visits.png")
    # display the plot
    plt.show()


def plot_a_store(name: str, final_df):
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
    sns_plot.figure.savefig(f"./out_data_sample/unique_visits_of_{name}.png")
    # display the plot
    plt.show()
