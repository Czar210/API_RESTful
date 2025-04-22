# novo_bd_retrieve.py

import requests
import statistics
import json

BASE_URL = "http://localhost:5000"

# Permitir entrada interativa do jogador
PLAYER_NAME = input("Nome do jogador (ex: Monochaco): ") or "Monochaco"
PLAYER_TAG = input("Tag do jogador (ex: BR1): ") or "BR1"
SERVER = input("Servidor (ex: br): ") or "br"

def fetch_player_data():
    """Faz a requisição GET para a API Flask."""
    url = f"{BASE_URL}/player"
    params = {
        "name": PLAYER_NAME,
        "tag": PLAYER_TAG,
        "server": SERVER
    }

    print(f"\n🔄 Buscando dados para {PLAYER_NAME}#{PLAYER_TAG} no servidor {SERVER}...\n")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao consultar a API: {e}")
        return None

def calcular_estatisticas(matches):
    """Calcula médias e exibe estatísticas das partidas."""
    if not matches:
        print("⚠️ Nenhum dado recebido da API.")
        return

    print(f"✅ {len(matches)} partidas recebidas da API.\n")

    # Coletar valores para estatísticas
    kills = [m["kills"] for m in matches]
    deaths = [m["deaths"] for m in matches]
    assists = [m["assists"] for m in matches]
    gold = [m["goldEarned"] for m in matches]
    vitorias = [m["win"] for m in matches]

    print("🎮 Primeiras 5 partidas:")
    for i, m in enumerate(matches[:5], 1):
        print(f"[{i}] {m['championName']} - {m['kills']}/{m['deaths']}/{m['assists']} - "
              f"Ouro: {m['goldEarned']} - Vitória: {'✅' if m['win'] else '❌'}")

    # Estatísticas
    print("\n📊 Estatísticas gerais:")
    print(f"- Média de kills: {statistics.mean(kills):.2f}")
    print(f"- Média de deaths: {statistics.mean(deaths):.2f}")
    print(f"- Média de assists: {statistics.mean(assists):.2f}")
    print(f"- Média de ouro ganho: {statistics.mean(gold):,.0f}")
    print(f"- Taxa de vitórias: {sum(vitorias) / len(vitorias) * 100:.1f}%")

if __name__ == "__main__":
    partidas = fetch_player_data()
    if partidas:
        calcular_estatisticas(partidas)
