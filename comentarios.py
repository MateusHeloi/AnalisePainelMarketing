
import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()

chave = os.environ["YOUTUBE_API_KEY"]

youtube = build("youtube", "v3", developerKey=chave)

videos = pd.read_csv("videos.csv")

linhas = []

for i, video in videos.iterrows():
    print("Comentários do vídeo", i + 1, "de", len(videos))

    try:
        resposta = youtube.commentThreads().list(
            part="snippet",
            videoId=video["video_id"],
            maxResults=100,
            order="time",
            textFormat="plainText",
        ).execute()
    except HttpError:
        print("  sem comentáriios diponiveis, pulando de comentarios ....")
        continue

    for item in resposta["items"]:
        comentario = item["snippet"]["topLevelComment"]["snippet"]
        linhas.append({
            "marca": video["marca"],
            "video_id": video["video_id"],
            "texto": comentario["textDisplay"],
            "data": comentario["publishedAt"][:10],
            "curtidas": comentario["likeCount"],
                                    })

tabela = pd.DataFrame(linhas)
tabela.to_csv("comentarios.csv", index=False, encoding="utf-8-sig")

print("finalizado", len(tabela), "comentários salvos em comentarios.csv")
