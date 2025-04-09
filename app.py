from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def buscar_dados_jogo(nome):
    try:
        # Configuração para evitar bloqueios
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}

        # Busca no HowLongToBeat para tempo médio
        url_hltb = f"https://howlongtobeat.com/?q={nome}"
        response_hltb = requests.get(url_hltb, headers=headers)
        soup_hltb = BeautifulSoup(response_hltb.text, "html.parser")
        tempo = 50  # Valor padrão

        # Busca revisões no Reddit para vício e visual
        url_reddit = f"https://www.reddit.com/r/gaming/search?q={nome}&restrict_sr=on"
        response_reddit = requests.get(url_reddit, headers=headers)
        soup_reddit = BeautifulSoup(response_reddit.text, "html.parser")

        # Análise básica (simulada, pois NLP seria ideal)
        visual = 70  # Estimativa inicial
        vicio = 80   # Estimativa inicial
        
        # Ajustes baseados em conteúdo encontrado
        texto_hltb = soup_hltb.text.lower()
        texto_reddit = soup_reddit.text.lower()

        # Critério 1: Estímulo Visual e Sensorial (45%)
        if "graphics" in texto_reddit or "beautiful" in texto_reddit:
            visual = 85
        elif "bad graphics" in texto_reddit:
            visual = 50

        # Critério 2: Comentários sobre Vício (45%)
        if "addictive" in texto_reddit or "can’t stop" in texto_reddit:
            vicio = 90
        elif "boring" in texto_reddit:
            vicio = 60

        # Critério 3: Tempo Médio (10%)
        if "hours" in texto_hltb or "long" in texto_hltb:
            tempo = 90

        # Cálculo da pontuação
        pontuacao = (visual * 0.45) + (vicio * 0.45) + (tempo * 0.10)
        return {"nome": nome, "visual": visual, "vicio": vicio, "tempo": tempo, "pontuacao": pontuacao}

    except Exception as e:
        return {"erro": "Erro ao buscar dados", "detalhe": str(e)}

@app.route("/buscar", methods=["POST"])
def buscar():
    data = request.get_json()
    nome = data.get("nome")
    resultado = buscar_dados_jogo(nome)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
