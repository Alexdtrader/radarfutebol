
import os
import requests

# Pega as chaves que você salvou nos Secrets do GitHub
NEWS_KEY = os.getenv('NEWS_API_KEY')
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')

def buscar_noticias():
    # Procura notícias de futebol em português
    url = f'https://newsapi.org/v2/everything?q=futebol+soccer&language=pt&sortBy=publishedAt&apiKey={NEWS_KEY}'
    
    try:
        response = requests.get(url)
        dados = response.json()
        
        # Verifica se a API retornou artigos
        if "articles" in dados and len(dados["articles"]) > 0:
            return dados["articles"][:3] # Retorna as 3 notícias mais recentes
        else:
            print("Nenhuma notícia encontrada no momento.")
            return []
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return []

def enviar_para_discord(artigo):
    # Formata a mensagem para o Discord
    mensagem = {
        "content": f"**⚽ ÚLTIMA HORA:** {artigo['title']}\n{artigo['url']}"
    }
    
    try:
        requests.post(WEBHOOK_URL, json=mensagem)
        print(f"Notícia enviada: {artigo['title']}")
    except Exception as e:
        print(f"Erro ao enviar para o Discord: {e}")

# Execução do Script
if __name__ == "__main__":
    lista_noticias = buscar_noticias()
    for noticia in lista_noticias:
        enviar_para_discord(noticia)
