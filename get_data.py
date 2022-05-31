""" Make a coromon csv because I can't find it online """
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

PD_AXIS_COLUMN = 0
PD_AXIS_ROW = 1


@dataclass
class CoroData:
    df: pd.DataFrame
    stats: List[str]

    def clean_data(self):
        # Drop unnessassary columns
        self.df.drop(columns=["Unnamed: 10", "#"], inplace=True)

        # Remove garbage from fields
        for col in self.stats:
            self.df[col] = self.df[col].str.replace(r"[^0-9]+", "")
            self.df[col] = pd.to_numeric(self.df[col])

    def add_bst(self):
        """Adds base stat total column."""

        self.df["BST"] = self.df.sum(axis=PD_AXIS_ROW)

    def effective_bst(self):
        """Adds effective base stat total column.

        the effective base stat total subtracts the lowest attacking stat, and
        can give a better idea of stat totals on non-mixed attackers.
        """
        bst = self.df[stats].sum(axis=PD_AXIS_ROW)
        min_atk = self.df[["Atk", "Sp.A"]].min(axis=PD_AXIS_ROW)

        self.df["eBST"] = bst - min_atk


if __name__ == "__main__":
    url = "https://coromon.wiki.gg/wiki/List_of_Coromon"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        indiatable = soup.find("table", {"class": "wikitable"})

        df = pd.read_html(str(indiatable), header=[1])
        df = pd.DataFrame(df[0])

        stats = ["HP", "Spe", "Atk", "Def", "Sp.A", "Sp.D", "SP"]

        coro_data = CoroData(df, stats)
        coro_data.clean_data()
        coro_data.add_bst()
        coro_data.effective_bst()

        print(coro_data.df.sort_values(by=["eBST"], ascending=False).head(10))

    else:
        print("Status Code: {}".format(response.status_code))
