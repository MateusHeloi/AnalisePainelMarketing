
import pandas as pd
from pytrends.request import TrendReq

marcas = ["Ambev", "Brahma", "Skol", "Budweiser"]

pytrends = TrendReq(hl="pt-BR", tz=180)

pytrends.build_payload(marcas, timeframe="today 5-y", geo="BR")

tabela = pytrends.interest_over_time().reset_index()

tabela = tabela.drop(columns=["isPartial"])

tabela = tabela.melt(id_vars="date", var_name="marca", value_name="interesse")

tabela.to_csv("google_trends.csv", index=False, encoding="utf-8-sig")

print("finalizado", len(tabela), "linhas salvas em google_trends.csv")
