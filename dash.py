import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Painel Ambev", layout="wide")


videos = pd.read_csv("videos.csv", encoding="utf-8-sig")
comentarios = pd.read_csv(
      "comentarios_sentimento.csv",
      encoding="utf-8-sig",
      engine="python",
      on_bad_lines="skip",
  )
trends = pd.read_csv("google_trends.csv", encoding="utf-8-sig")


comentarios["data"] = pd.to_datetime(comentarios["data"], errors="coerce")
trends["date"] = pd.to_datetime(trends["date"], errors="coerce")
comentarios = comentarios.dropna(subset=["data"])
trends = trends.dropna(subset=["date"])

st.sidebar.header("Filtros")
marcas_disponiveis = sorted(videos["marca"].unique())
marcas_selecionadas = st.sidebar.multiselect(
    "Selecione as marcas", marcas_disponiveis, default=marcas_disponiveis
)

videos = videos[videos["marca"].isin(marcas_selecionadas)]
comentarios = comentarios[comentarios["marca"].isin(marcas_selecionadas)]
trends = trends[trends["marca"].isin(marcas_selecionadas)]

if comentarios.empty:
  st.warning("Selecione pelo menos uma marca")
  st.stop()

total_comentarios = len(comentarios)
pct_positivos = (
    (comentarios["sentimento"] == "Positivo").mean() * 100
)
pct_negativos = (
    (comentarios["sentimento"] == "Negativo").mean() * 100
)

str_positivo = f"{pct_positivos:.1f}".replace(".", ",") + "%"
str_negativo = f"{pct_negativos:.1f}".replace(".", ",") + "%"

col_logo, col_titulo = st.columns([1, 6])  

with col_logo:
  st.image("logo.png", width=100)
st.title("AGENCIA LK - Painel de Monitoramento Ambev")


col1, col2, col3, col4 = st.columns(4)
col1.metric("Vídeos Analisados", f"{len(videos):,}".replace(",", "."))
col2.metric("Comentários Analisados", f"{total_comentarios:,}".replace(",", "."))
col3.metric("% Positivos", str_positivo)
col4.metric("% Negativos", str_negativo)

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
  st.subheader("Percepção de Sentimento")
  df_sentimento = (
      comentarios["sentimento"].value_counts(normalize=True).reset_index()
  )
  df_sentimento.columns = ["Sentimento", "Proporcao"]
  df_sentimento["Percentual"] = df_sentimento["Proporcao"] * 100

  fig_sentimento = px.bar(
      df_sentimento,
      x="Sentimento",
      y="Percentual",
      text=df_sentimento["Percentual"].apply(
          lambda x: f"{x:.1f}%".replace(".", ",")
      ),
      color="Sentimento",
      color_discrete_sequence=["#1f77b4", "#aec7e8", "#ff7f0e"],
  )
  fig_sentimento.update_traces(
      textposition="outside"
  ) 
  fig_sentimento.update_layout(
      showlegend=False,
      xaxis_title="",
      yaxis_title="%",
      margin=dict(t=20, b=20, l=20, r=20),
  )
  st.plotly_chart(fig_sentimento, use_container_width=True)

with col_b:
  st.subheader("Interesses de buscas no google")
  if not trends.empty:
    fig_trends = px.line(
        trends, x="date", y="interesse", color="marca", markers=False
    )
    fig_trends.update_layout(
        xaxis_title="",
        yaxis_title="Buscas",
        legend_title="Marca",
        margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig_trends, use_container_width=True)
  else:
    st.info("Sem dados de Google Trends disponíveis.")

st.markdown("---")

st.subheader("Vídeos com Maior Engajamento")
top_videos = videos.sort_values("engajamento", ascending=False).head(5)
st.dataframe(
    top_videos[
        ["marca", "titulo", "canal", "views", "likes", "comentarios", "engajamento"]
    ],
    use_container_width=True,
)