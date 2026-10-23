
import pandas as pd
from pysentimiento import create_analyzer

comentarios = pd.read_csv("comentarios.csv")


comentarios["texto"] = comentarios["texto"].fillna("").astype(str).str.slice(0, 300)
comentarios = comentarios[comentarios["texto"].str.strip() != ""]


analisador = create_analyzer(task="sentiment", lang="pt")

resultados = analisador.predict(comentarios["texto"].tolist())

traducao = {"POS": "Positivo", "NEG": "Negativo", "NEU": "Neutro"}

sentimentos = []
for resultado in resultados:
    sentimentos.append(traducao[resultado.output])

comentarios["sentimento"] = sentimentos

comentarios.to_csv("comentarios_sentimento.csv", index=False, encoding="utf-8-sig")

resumo = pd.crosstab(comentarios["marca"], comentarios["sentimento"], normalize="index")
print((resumo * 100).round(1))

print("finalizado", len(comentarios), "salvos em comentarios_sentimento.csv")