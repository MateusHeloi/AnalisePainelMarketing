
import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

chave = os.environ["YOUTUBE_API_KEY"]

youtube = build("youtube", "v3", developerKey=chave)

marcas = ["Ambev", "Brahma", "Skol", "Budweiser"]

linhas = []

for marca in marcas:
    print("Buscando vídeos de", marca)

    busca = youtube.search().list(
        part="snippet",
        q=marca + " propaganda",
        type="video",
        maxResults=20,
        regionCode="BR",
        relevanceLanguage="pt",
    ).execute()

    ids = []
    for item in busca["items"]:
        ids.append(item["id"]["videoId"])

    detalhes = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(ids),
    ).execute()

    for video in detalhes["items"]:
        estatisticas = video["statistics"]
        linhas.append({
            "marca": marca,
            "video_id": video["id"],
            "titulo": video["snippet"]["title"],
            "canal": video["snippet"]["channelTitle"],
            "data_publicacao": video["snippet"]["publishedAt"][:10],
            "views": int(estatisticas.get("viewCount", 0)),
            "likes": int(estatisticas.get("likeCount", 0)),
            "comentarios": int(estatisticas.get("commentCount", 0)),
        })

tabela = pd.DataFrame(linhas)

print(tabela.head())
tabela["engajamento"] = tabela["likes"] + tabela["comentarios"]

tabela.to_csv("videos.csv", index=False, encoding="utf-8-sig")

print("finalizao", len(tabela), "vsalvos em videos.csv")
