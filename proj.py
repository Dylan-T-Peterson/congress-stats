import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import fastparquet


def mass_astype(df: pd.DataFrame, series: list[str], dtype: str):
    for x in series:
        df[x] = df[x].astype(dtype)


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

    df.loc[df["Title"] != df["title"], "Title"] = df["Title"].str.cat(
        df["title"], sep=" - "
    )
    del df["title"]

    df["State"] = df["Name"].str.rsplit(n=1, expand=True)[1].str.strip("()")
    df.State = df.State.str.split(pat="-", n=1, expand=True)[1]

    df["District"] = df.State.str.rsplit(pat="-", n=1, expand=True)[1]
    df.State = df.State.str.split(pat="-", n=1, expand=True)[0]

    df.Name = df["Name"].str.split(n=1, expand=True)[1]
    df.Name = df["Name"].str.rsplit(n=1, expand=True)[0]

    mass_astype(df, ["Name", "Birth"], "string")
    mass_astype(df, ["Age", "Terms"], "Int8")
    # df = df.astype(
    #     {"Name": "string", "Birth": "string", "Age": "Int8", "Terms": "Int8"}
    # )
    print(df.dtypes)
    # Sanatize and type csv into proper df


def csv_merge():
    file1, file2 = "data/age-of-118th-congress.csv", "data/search.csv"
    pass


def main():
    pass


if __name__ == "__main__":
    Quorum_to_df()
