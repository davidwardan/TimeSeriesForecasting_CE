import pandas as pd
import matplotlib.pyplot as plt
import random

from config.plot_config import setup_plotting

setup_plotting()


def main(data_dir, column_names=["volume"], detector_id=1345):

    # read data from csv file
    data = pd.read_csv(data_dir)

    # slice data for detector_id
    data = data[data["detectorid"] == detector_id]

    # plot data
    data["starttime"] = pd.to_datetime(data["starttime"], utc=True)
    data = data.set_index("starttime")
    data = data.sort_index()

    # correct time zone
    data.index = data.index.tz_convert("US/Pacific")

    fig, ax = plt.subplots(len(column_names), 1, figsize=(6, 4), sharex=True)
    for i, column_name in enumerate(column_names):
        ax[i].plot(
            data[column_name],
            label=r"$y_{true}$",
            alpha=0.8,
            linewidth=1,
            color="red",
        )
        ax[i].set_ylabel(column_name)
        ax[i].tick_params(axis="x", rotation=20)
    ax[-1].set_xlabel("Time[Y-M-D]")
    ax[0].legend(loc=(0.5, 1.1), ncol=1, frameon=False)
    plt.tight_layout()
    plt.savefig(f"out/detector_{detector_id}_timeseries")
    plt.show()

    # check for daily patterns in the data
    data["date"] = data.index.date
    data["hour"] = data.index.hour
    data["minute"] = data.index.minute

    # plot data for a random day
    random_date = random.choice(data["date"].unique())
    data_day = data[data["date"] == random_date]

    fig, ax = plt.subplots(len(column_names), 1, figsize=(6, 4), sharex=True)
    for i, column_name in enumerate(column_names):
        ax[i].plot(
            data_day[column_name],
            label=r"$y_{true}$",
            alpha=0.8,
            linewidth=1,
            color="red",
        )
        ax[i].set_ylabel(column_name)
        ax[i].tick_params(axis="x", rotation=20)
    ax[-1].set_xlabel("Time[M-D H]")
    ax[0].legend(loc=(0.5, 1.1), ncol=1, frameon=False)
    plt.tight_layout()
    plt.savefig(f"out/detector_{detector_id}_daily")
    plt.show()

    # check for weekly patterns in the data
    data["weekday"] = data.index.weekday

    # plot data for a random weekday
    random_weekday = random.choice(data["weekday"].unique())
    data_weekday = data[data["weekday"] == random_weekday]

    fig, ax = plt.subplots(len(column_names), 1, figsize=(6, 4), sharex=True)
    for i, column_name in enumerate(column_names):
        ax[i].plot(
            data_weekday[column_name],
            label=r"$y_{true}$",
            alpha=0.8,
            linewidth=1,
            color="red",
        )
        ax[i].set_ylabel(column_name)
        ax[i].tick_params(axis="x", rotation=20)
    ax[-1].set_xlabel("Time[Y-M-D]")
    ax[0].legend(loc=(0.5, 1.1), ncol=1, frameon=False)
    plt.tight_layout()
    plt.savefig(f"out/detector_{detector_id}_weekly")
    plt.show()


if __name__ == "__main__":
    # list of detectors
    ids = [1345, 1858]

    for id in ids:
        main(
            data_dir="data/freeway_loopdata5min.csv",
            column_names=["volume", "occupancy", "speed"],
            detector_id=id,
        )
