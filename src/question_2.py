import pandas as pd
import matplotlib.pyplot as plt

from config.plot_config import setup_plotting

setup_plotting()

def main(data_dir, column_name):

    # Load the CSV into a DataFrame
    data = pd.read_csv(data_dir)

    # Convert "starttime" to pandas datetime (UTC)
    data["starttime"] = pd.to_datetime(data["starttime"], utc=True)
    # Sort by time
    data = (
        data.groupby("detectorid", group_keys=False)
        .apply(lambda g: g.sort_values("starttime"))
        .reset_index(drop=True)
    )
    # Convert UTC to US/Pacific
    data["starttime"] = data["starttime"].dt.tz_convert("US/Pacific")

    # Create a pivot table where each "detectorid" is a column
    pivot_df = data.pivot_table(
        index="starttime", columns="detectorid", values=column_name
    )

    # Compute the correlation matrix
    corr_matrix = pivot_df.corr()

    # Plot the correlation matrix using only matplotlib
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(corr_matrix, cmap="coolwarm", aspect="auto")
    fig.colorbar(im, ax=ax)

    # Set tick labels
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.index)))
    # Show x tick labels for every 2nd tick only
    xticks = list(range(len(corr_matrix.columns)))
    xlabels = [
        label if i % 2 == 0 else "" for i, label in enumerate(corr_matrix.columns)
    ]
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=60)

    # Show y tick labels for every 2nd tick only
    yticks = list(range(len(corr_matrix.index)))
    ylabels = [label if i % 2 == 0 else "" for i, label in enumerate(corr_matrix.index)]
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, rotation=30)

    plt.tight_layout()
    plt.savefig("out/correlation_matrix.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    main(
        data_dir="data/freeway_loopdata5min.csv",
        column_name="volume",
    )
