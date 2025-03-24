import pandas as pd
import matplotlib.pyplot as plt
import random
import os

from config.plot_config import setup_plotting

setup_plotting()


def main(data_dir, column_names=["volume"], detector_id=1345):

    # read data from csv file
    data = pd.read_csv(data_dir)

    # slice data for detector_id
    data = data[data["detectorid"] == detector_id]

    # plot data
    data["starttime"] = pd.to_datetime(data["starttime"], utc=True)

    # sort starttime
    data = data.sort_values("starttime")

    # convert UTC to US/Pacific
    data["starttime"] = data["starttime"].dt.tz_convert("US/Pacific")

    # split data into training and testing
    data_train = data.iloc[: int(0.9 * len(data))]
    data_test = data.iloc[int(0.9 * len(data)) :]

    # plot data
    plt.figure(figsize=(6, 3))
    plt.plot(data_train["starttime"], data_train[column_names], label="train")
    plt.plot(data_test["starttime"], data_test[column_names], label="test")
    plt.xlabel("Time")
    plt.ylabel("Volume")
    plt.xticks(rotation=20)
    plt.legend(loc=(0.3, 1.01), ncol=2, frameon=False)
    plt.tight_layout()
    plt.savefig(f"out/detector_{detector_id}_weekly")
    plt.show()

    # save only column name into a csv file
    data_train[column_names].to_csv(f"out/train_{detector_id}_timeseries.csv", index=False)

    # save only the dates into a csv file
    data_train["starttime"].to_csv(f"out/train_{detector_id}_dates.csv", index=False)

    # save only column name into a csv file
    data_test[column_names].to_csv(f"out/test_{detector_id}_timeseries.csv", index=False)

    # save only the dates into a csv file
    data_test["starttime"].to_csv(f"out/test_{detector_id}_dates.csv", index=False)
    

if __name__ == "__main__":
    # list of detectors
    ids = [1345]

    for id in ids:
        main(
            data_dir="data/freeway_loopdata5min.csv",
            column_names=["volume"],
            detector_id=id,
        )
