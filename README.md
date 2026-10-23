# Social Listening Ambev

Painel que mostra como o público percebe a Ambev, a Brahma, a Skol e a Budweiser, usando comentários do YouTube e o interesse de busca do Google Trends.

**Painel online:** https://painelambev.streamlit.app/

## O que o projeto faz

- Coleta vídeos e comentários das marcas pela API do YouTube
- Classifica o sentimento dos comentários (positivo, negativo ou neutro) com o pysentimiento
- Pega o interesse de busca das marcas no Google Trends (últimos 5 anos)
- Mostra tudo em um painel feito com Streamlit

## Tecnologias

Python 3.11, pandas, Streamlit, Plotly, pysentimiento, pytrends e API do YouTube.

## Como rodar

```bash
git clone https://github.com/MateusHeloi/AnalisePainelMarketing.git
cd AnalisePainelMarketing
python -m venv venv
venv\Scripts\activate        # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Para só abrir o painel, basta rodar:

```bash
streamlit run dash.py
```

Para coletar os dados de novo, crie um arquivo `.env` com a sua chave da API do YouTube (veja o `.env.example`) e rode os scripts nesta ordem:

```bash
python videos.py
python comentarios.py
python googletrends.py
python sentimento.py
```

Não precisa de GPU. O modelo de sentimento é baixado automaticamente na primeira vez que o `sentimento.py` roda.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `videos.py` | Busca os vídeos e as métricas (gera `videos.csv`) |
| `comentarios.py` | Coleta os comentários (gera `comentarios.csv`) |
| `googletrends.py` | Pega o interesse de busca (gera `google_trends.csv`) |
| `sentimento.py` | Classifica o sentimento (gera `comentarios_sentimento.csv`) |
| `dash.py` | Painel em Streamlit |

## Resultados

Foram analisados 80 vídeos e 3.699 comentários: 36,3% positivos, 43,6% neutros e 20,1% negativos.

## Limitações

- Só YouTube, com até 100 comentários por vídeo
- O modelo de sentimento pode errar com ironia e gírias
- O Google Trends mostra interesse relativo (0 a 100), não o número de buscas

## Autor

Mateus Heloi - [GitHub](https://github.com/MateusHeloi)
