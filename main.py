import os
import requests

NEWS_KEY = os.getenv('NEWS_API_KEY')
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK')

def buscar_noticias():
    # Aumentamos a busca para incluir "soccer" e "futebol" para garantir resultados
    url = f'https://newsapi.org/v2/everything?q=futebol+OR+soccer&language=pt&sortBy=publishedAt&apiKey={NEWS_KEY}'
    
    print(f"Buscando notícias em: {url.replace(NEWS_KEY, 'ESCONDIDO')}") # Log de depuração
    
    try:
        response = requests.get(url)
        print(f"Status da API: {response.status_code}") # Deve ser 200
        
        dados = response.json()
        
        if response.status_code != 200:
            print(f"Erro da API: {dados.get('message', 'Erro desconhecido')}")
            return []

        artigos = dados.get('articles', [])
        print(f"Total de notícias encontradas: {len(artigos)}")
        return artigos[:3] 
    except Exception as e:
        print(f"Falha na conexão: {e}")
        return []

def enviar_para_discord(artigo):
    mensagem = {"content": f"⚽ **{artigo['title']}**\n{artigo['url']}"}
    r = requests.post(WEBHOOK_URL, json=mensagem)
    if r.status_code == 204:
        print("Mensagem enviada com sucesso para o Discord!")
    else:
        print(f"Erro ao enviar para o Discord: {r.status_code} - Texto: {r.text}")

if __name__ == "__main__":
    if not NEWS_KEY or not WEBHOOK_URL:
        print("ERRO: Variáveis de ambiente NEWS_API_KEY ou DISCORD_WEBHOOK não encontradas!")
    else:
        noticias = buscar_noticias()
        for n in noticias:
            enviar_para_discord(n)
