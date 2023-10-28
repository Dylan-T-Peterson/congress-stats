import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def mass_astype(df: pd.DataFrame, series: list[str] | pd.Index, dtype: str):
    for x in series:
        df[x] = df[x].astype(dtype)


def roundup(num: int, up: int) -> int:
    return (num) - (num % up) + up


def Quorum_to_df():
    file = "data/age-of-118th-congress.csv"
    df = pd.read_csv(file)
    df.rename(
        columns={
            "Age of 118th Congress": "Name",
            "Birth Month & Day": "Birth",
            "Number of Terms": "Terms",
        },
        inplace=True,
    )
    df["title"] = (
        df["Name"]
        .str.split(n=1, expand=True)[0]
        .replace(
            to_replace={
                "Sen.": "US Senator",
                "Rep.": "US Representative",
                "Commish.": "US Resident Commissioner",
                "Del.": "US Delegate",
            }
        )
    )

    df.loc[df.Title != df.title, "Title"] = df.Title.str.cat(df.title, sep=" - ")
    del df["title"]

    df["State"] = df.Name.str.rsplit(n=1, expand=True)[1].str.strip("()")
    df.State = df.State.str.split(pat="-", n=1, expand=True)[1]

    df["District"] = df.State.str.rsplit(pat="-", n=1, expand=True)[1]
    df.State = df.State.str.split(pat="-", n=1, expand=True)[0]

    df.Name = df.Name.str.split(n=1, expand=True)[1]
    df.Name = df.Name.str.rsplit(n=1, expand=True)[0]

    mass_astype(df, ["Name", "Birth"], "string")
    mass_astype(df, ["Age", "Terms"], "Int8")
    df.to_parquet(
        "data/118th-congress-ages.snappy.parq",
        engine="fastparquet",
        compression="snappy",
    )
    # df.to_excel("data/118th-congress-ages.xlsx") # needs openpyxl


def Census_to_df():
    df = pd.read_csv("data/2022agesex-census.csv")
    df.Age = df.Age.astype("string")
    mass_astype(df, df.columns[1:], dtype="float32")
    df.loc[0:26, ["Bnumber", "Mnumber", "Fnumber"]] = df.loc[
        0:26, ["Bnumber", "Mnumber", "Fnumber"]
    ].mul(1000)
    df.to_parquet(
        "data/2022agesex-census.snappy.parq", engine="fastparquet", compression="snappy"
    )


def main():
    congress = pd.read_parquet("data/118th-congress-ages.snappy.parq")
    census = pd.read_parquet("data/2022agesex-census.snappy.parq")
    fig, (ax1, ax2) = plt.subplots(nrows=2)

    # congress.Age.value_counts().sort_index().plot(kind="bar", ax=ax1)
    def congress_graph(ax):
        bins = pd.cut(x=congress.Age, bins=range(25, 91, 5), right=False)
        sns.barplot(data=bins.value_counts(normalize=True) * 100, ax=ax)

        labels = [
            str(x) for x in pd.interval_range(start=25, end=85, freq=5, closed="left")
        ]
        labels.append("85+")
        ax.set_xticks(ticks=np.arange(13), labels=labels)
        ax.set_xlabel("Age of Congress")

    def uspop_0plus(ax):
        sns.barplot(
            x=range(0, 86, 5),
            y=census.Bpercent.iloc[1:19],
            ax=ax,
            # native_scale=True,
        )

        labels = [
            str(x) for x in pd.interval_range(start=0, end=85, freq=5, closed="left")
        ]
        labels.append("85+")
        ax.set_xticks(
            ticks=range(18),
            labels=labels,
        )
        ax.set_xlabel("Age of US Population")

    def uspop_25plus(ax):
        sns.barplot(
            x=range(25, 86, 5),
            y=census.Bpercent.iloc[6:19],
            ax=ax,
        )

        labels = [
            str(x) for x in pd.interval_range(start=25, end=85, freq=5, closed="left")
        ]
        labels.append("85+")
        ax.set_xticks(
            ticks=range(13),
            labels=labels,
        )
        ax.set_xlabel("Age of US Population")

    congress_graph(ax1)
    uspop_25plus(ax2)
    # print(census.iloc[6:19])
    plt.show()

    # print(congress.loc[df.Age.isna(), "Name"]) # Find birthdays for these Congress members
    # use fig.canvas.mpl to create eventhandler for button press to swap between uspop 0 plus and 25 plus


if __name__ == "__main__":
    main()
