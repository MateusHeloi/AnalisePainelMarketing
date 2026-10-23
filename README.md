# Social Listening Ambev: Painel de Monitoramento de Reputação de Marca

Pipeline de dados e painel interativo que medem **como o público percebe a Ambev e suas marcas (Brahma, Skol e Budweiser)**. O projeto coleta vídeos e comentários do YouTube, classifica o sentimento de cada comentário com um modelo de linguagem em português, cruza esses dados com o interesse de busca do Google Trends e apresenta tudo em um dashboard em Streamlit.

> Projeto de portfólio de análise de reputação de marca. Os dados são públicos (YouTube e Google Trends) e este repositório não tem vínculo oficial com a Ambev, o YouTube ou o Google.

**Painel online:** https://painelambev.streamlit.app/

## Sumário

- [O problema que resolve](#o-problema-que-resolve)
- [Tecnologias e modelos de IA](#tecnologias-e-modelos-de-ia)
- [Pré-requisitos](#pré-requisitos)
- [Como executar](#como-executar)
- [Exemplo de uso](#exemplo-de-uso)
- [Principais resultados](#principais-resultados)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Limitações](#limitações)
- [Próximos passos](#próximos-passos)

## O problema que resolve

Equipes de marketing e comunicação precisam saber, de forma rápida, **o que o público está falando sobre uma marca, em que tom e quando algo foge do normal**. Ler milhares de comentários à mão não escala, e olhar só views ou likes não mostra a percepção real.

Este projeto automatiza esse acompanhamento (o chamado *social listening*) e responde a três perguntas:

1. **Qual é o tom das conversas?** Quantos comentários são positivos, negativos ou neutros, por marca.
2. **Quais conteúdos geram mais engajamento?** Ranking de vídeos por likes e comentários.
3. **Quando o interesse por uma marca dispara?** Evolução semanal do interesse de busca e identificação de picos que merecem investigação (possíveis crises de imagem ou campanhas de sucesso).

## Tecnologias e modelos de IA

| Camada | Ferramenta | Uso |
|---|---|---|
| Coleta | **YouTube Data API v3** (`google-api-python-client`) | Busca de vídeos, métricas e comentários |
| Coleta | **pytrends** | Interesse de busca no Google Trends (biblioteca não oficial) |
| Processamento | **pandas** | Limpeza, junção e agregação dos dados |
| IA | **pysentimiento** + **PyTorch** / **Transformers** | Classificação de sentimento |
| Visualização | **Streamlit** + **Plotly** | Dashboard interativo |
| Configuração | **python-dotenv** | Leitura segura da chave de API |

### Modelo de IA: análise de sentimento

O sentimento é calculado com o [`pysentimiento`](https://github.com/pysentimiento/pysentimiento), usando o modelo **`pysentimiento/bertweet-pt-sentiment`** (carregado por `create_analyzer(task="sentiment", lang="pt")`):

- Modelo de linguagem do tipo **RoBERTa**, baseado no BERTabaporu, pré-treinado em tweets em português, com cerca de 135 milhões de parâmetros.
- Classifica cada texto como **POS** (positivo), **NEG** (negativo) ou **NEU** (neutro).
- Roda **localmente**, sem custo e sem enviar os comentários a uma API de terceiros. Nenhum treinamento é necessário, já que o modelo vem pré-treinado.
- Na primeira execução, os pesos (cerca de 540 MB) são baixados do Hugging Face e ficam em cache.

## Pré-requisitos

| Item | Detalhe |
|---|---|
| **Python** | 3.11 (versão em que o projeto foi desenvolvido e testado) |
| **Chave da API do YouTube** | Obrigatória apenas para **coletar dados novos**. Crie no [Google Cloud Console](https://console.cloud.google.com/), ative a **YouTube Data API v3** e gere uma chave de API |
| **Google Trends** | Não exige chave (o `pytrends` acessa o serviço de forma não oficial) |
| **Hugging Face** | Não exige conta nem token. O download do modelo funciona sem login |
| **GPU / CUDA** | **Não é necessária.** O modelo é pequeno e roda em CPU. Com uma GPU NVIDIA e o PyTorch com suporte a CUDA instalado, a inferência pode ser mais rápida, mas o projeto não depende disso |
| **Internet** | Necessária para a coleta e para o primeiro download do modelo |
| **Espaço em disco** | Alguns GB livres (PyTorch, Transformers e pesos do modelo) |

**Cota da API:** a YouTube Data API tem cota diária gratuita (10.000 unidades por padrão). Cada busca de vídeos custa 100 unidades, e cada consulta de detalhes ou de comentários custa 1. Uma execução completa deste projeto (4 buscas, 4 consultas de detalhes e 80 consultas de comentários) usa em torno de 500 unidades.

**Se você só quer ver o painel**, não precisa de chave de API: os CSVs já estão no repositório.

## Como executar

### 1. Clonar e instalar as dependências

```bash
git clone https://github.com/MateusHeloi/AnalisePainelMarketing.git
cd AnalisePainelMarketing

python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configurar a chave da API (apenas para coletar dados novos)

Copie o `.env.example` para `.env` e preencha a chave:

```
YOUTUBE_API_KEY=sua_chave_aqui
```

> O `.env` já está no `.gitignore`. **Nunca** publique sua chave no GitHub. Se ela vazar, apague-a no Google Cloud e crie outra. Recomenda-se restringir a chave à YouTube Data API v3.

### 3. Rodar o pipeline de dados

Execute os scripts nesta ordem:

```bash
python videos.py          # 1. busca vídeos e métricas        -> videos.csv
python comentarios.py     # 2. coleta comentários             -> comentarios.csv
python googletrends.py    # 3. interesse de busca (5 anos)    -> google_trends.csv
python sentimento.py      # 4. classifica o sentimento (IA)   -> comentarios_sentimento.csv
```

Observações:

- `sentimento.py` baixa o modelo na primeira execução e pode levar alguns minutos em CPU, dependendo do número de comentários.
- `googletrends.py` pode falhar com o **erro 429** (limite de requisições do Google). Espere alguns minutos e tente de novo, ou baixe o CSV direto do site do Google Trends.

### 4. Abrir o painel

```bash
streamlit run dash.py
```

O Streamlit abre o painel no navegador (por padrão em `http://localhost:8501`).

## Exemplo de uso

### Saída do pipeline

`videos.csv` (uma linha por vídeo):

| marca | titulo | canal | views | likes | comentarios | engajamento |
|---|---|---|---|---|---|---|
| Ambev | Zé Neto e Cristiano - ALÔ AMBEV - Clipe oficial | Zé Neto e Cristiano | 76.806.566 | 798.272 | 15.190 | 813.462 |

`comentarios_sentimento.csv` (uma linha por comentário), com as colunas:

```
marca, video_id, texto, data, curtidas, sentimento
```

onde `sentimento` é `Positivo`, `Negativo` ou `Neutro`.

### Usando o modelo de sentimento isoladamente

```python
from pysentimiento import create_analyzer

analisador = create_analyzer(task="sentiment", lang="pt")

resultado = analisador.predict("isto é bonito")
print(resultado.output)   # POS
```

### Usando o painel

1. Abra o painel (online ou com `streamlit run dash.py`).
2. Na barra lateral, escolha as marcas que quer comparar.
3. Veja os números principais (vídeos e comentários analisados, % de positivos e de negativos), o gráfico de sentimento e a evolução do interesse de busca.
4. Consulte a tabela dos 5 vídeos com maior engajamento.
5. No gráfico do Google Trends, procure picos: eles indicam semanas em que vale investigar o que aconteceu com a marca.

## Principais resultados

Amostra: **80 vídeos** (20 por marca) e **3.699 comentários**.

| Sentimento | % dos comentários |
|---|---|
| Neutro | 43,6% |
| Positivo | 36,3% |
| Negativo | 20,1% |

Sentimento por marca:

| Marca | Positivo | Neutro | Negativo |
|---|---|---|---|
| Ambev | 41,2% | 43,7% | 15,1% |
| Brahma | 39,6% | 36,1% | 24,3% |
| Skol | 38,6% | 35,2% | 26,2% |
| Budweiser | 28,7% | 52,8% | 18,4% |

- O vídeo mais engajado é o clipe "Alô Ambev", com mais de 76 milhões de views e cerca de 813 mil interações.
- No Google Trends, o interesse é estável, com picos pontuais. O maior é o da Ambev na semana de 29/01/2023. A Budweiser tem o menor interesse das quatro marcas.
- Os números são uma amostra da data da coleta (outubro de 2026) e mudam se o pipeline for executado de novo.

## Estrutura do repositório

```
.
├── videos.py                    # coleta de vídeos e métricas (YouTube)
├── comentarios.py               # coleta de comentários (YouTube)
├── googletrends.py              # interesse de busca (Google Trends)
├── sentimento.py                # classificação de sentimento (pysentimiento)
├── dash.py                      # painel em Streamlit
├── videos.csv                   # saída de videos.py
├── comentarios.csv              # saída de comentarios.py
├── comentarios_sentimento.csv   # saída de sentimento.py
├── google_trends.csv            # saída de googletrends.py
├── requirements.txt
├── .env.example                 # modelo do arquivo de configuração
└── .gitignore                   # ignora .env, venv/ e __pycache__/
```

## Limitações

- Só o **YouTube** foi coletado, com até **100 comentários recentes por vídeo**. O volume de comentários por data reflete a amostra, não o total de menções.
- O **engajamento** é likes + comentários. A API do YouTube não fornece compartilhamentos.
- A busca por "[marca] propaganda" traz conteúdo oficial e também de canais de terceiros, que não são campanhas oficiais das marcas.
- O modelo de sentimento pode **errar com ironia, sarcasmo e gírias**. Os resultados devem ser lidos como uma estimativa, e vale conferir uma amostra à mão.
- O Google Trends mostra **interesse relativo** (0 a 100, em relação ao maior pico do período), não o número de buscas.
- O `pytrends` é uma biblioteca não oficial e pode deixar de funcionar ou ser bloqueada pelo Google.

## Próximos passos

- Incluir outras redes sociais.
- Coletar mais comentários por vídeo e filtrar canais oficiais das marcas.
- Identificar os assuntos mais comentados.
- Investigar a causa dos picos de interesse.
- Criar alertas automáticos para aumento de comentários negativos.

## Autor

**Mateus Heloi**

- GitHub: [github.com/MateusHeloi](https://github.com/MateusHeloi)

<!-- Adicione aqui o link do seu LinkedIn, se quiser -->
