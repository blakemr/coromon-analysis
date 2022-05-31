""" Make a coromon csv because I can't find it online """
import pandas as pd
import requests
from bs4 import BeautifulSoup


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop unnessassary columns
    df.drop(columns=["Unnamed: 10", "#"], inplace=True)

    # Remove garbage from fields
    for col in ["HP", "Spe", "Atk", "Def", "Sp.A", "Sp.D", "SP"]:
        df[col] = df[col].str.replace(r"[^0-9]+", "")
        df[col] = pd.to_numeric(df[col])

    return df


def add_bst(df: pd.DataFrame) -> pd.DataFrame:

    df["BST"] = df.apply(lambda x: df.sum())

    return df


if __name__ == "__main__":
    url = "https://coromon.wiki.gg/wiki/List_of_Coromon"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        indiatable = soup.find("table", {"class": "wikitable"})

        df = pd.read_html(str(indiatable), header=[1])
        df = pd.DataFrame(df[0])

        df = clean_data(df)

        print(df.dtypes)

    else:
        print("Status Code: {}".format(response.status_code))
