#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script para verificar as funcionalidades do app.py sem usar o frontend.
Este script testa as principais rotas e funcionalidades da API.
"""

import requests
import json
import os
import sys
import time

# Configuração do ambiente de teste
BASE_URL = "http://localhost:5000"  # URL base do servidor Flask
TEST_PLAYER = {
    "name": "Monochaco",  # Nome do jogador para teste
    "tag": "BR1",         # Tag do jogador para teste
    "server": "br"        # Servidor para teste
}

def test_health_check():
    """Testa o endpoint de health check"""
    print("\n[TESTE] Verificando saúde da API...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            api_key_status = "configurada" if data.get("api_key_configured") else "NÃO configurada"
            print(f"✅ API está funcionando! Status: {data.get('status')}. RIOT_API_KEY está {api_key_status}.")
            return True
        else:
            print(f"❌ Erro ao verificar saúde da API. Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar ao servidor em {BASE_URL}. Certifique-se que o Flask está rodando.")
        return False

def test_player_get():
    """Testa o endpoint GET /player"""
    print("\n[TESTE] Buscando dados de jogador via GET...")
    params = TEST_PLAYER
    try:
        response = requests.get(f"{BASE_URL}/player", params=params)
        print(f"Status code: {response.status_code}")
        if response.status_code < 400:  # 200 ou 201
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ Sucesso! Encontrado {len(data)} partidas para o jogador {params['name']}#{params['tag']}")
                    if data:  # Se há dados, mostra a primeira partida
                        print("\nExemplo de dados da primeira partida:")
                        print(json.dumps(data[0], indent=2))
                elif isinstance(data, dict) and "error" in data:
                    print(f"⚠️ API retornou um erro: {data['error']}")
                else:
                    print(f"✅ Resposta recebida: {json.dumps(data, indent=2)}")
                return True
            except json.JSONDecodeError:
                print(f"❌ Erro ao decodificar resposta JSON: {response.text[:200]}...")
                return False
        else:
            print(f"❌ Erro ao buscar jogador. Status code: {response.status_code}")
            try:
                print(f"Resposta: {response.json()}")
            except:
                print(f"Resposta: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar ao servidor em {BASE_URL}. Certifique-se que o Flask está rodando.")
        return False

def test_player_post():
    """Testa o endpoint POST /player"""
    print("\n[TESTE] Atualizando dados de jogador via POST...")
    data = TEST_PLAYER
    try:
        response = requests.post(f"{BASE_URL}/player", json=data)
        print(f"Status code: {response.status_code}")
        if response.status_code < 400:  # 200 ou 201
            try:
                result = response.json()
                if "message" in result:
                    print(f"✅ Sucesso! Mensagem: {result['message']}")
                    if "matches" in result and result["matches"]:
                        print(f"- Partidas atualizadas: {len(result['matches'])}")
                else:
                    print(f"✅ Resposta recebida: {json.dumps(result, indent=2)}")
                return True
            except json.JSONDecodeError:
                print(f"❌ Erro ao decodificar resposta JSON: {response.text[:200]}...")
                return False
        else:
            print(f"❌ Erro ao atualizar jogador. Status code: {response.status_code}")
            try:
                print(f"Resposta: {response.json()}")
            except:
                print(f"Resposta: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Não foi possível conectar ao servidor em {BASE_URL}. Certifique-se que o Flask está rodando.")
        return False

def test_direct_database_modules():
    """Testa os módulos database.py e call_champions.py diretamente"""
    print("\n[TESTE] Testando módulos diretamente...")
    
    try:
        print("- Importando módulos...")
        from database import create_connection, create_table, query_player_matches
        from call_champions import fetch_jungle_data
        
        print("- Criando conexão com banco de dados...")
        conn = create_connection()
        
        print("- Criando tabela se não existir...")
        create_table(conn)
        
        print("- Verificando variável de ambiente RIOT_API_KEY...")
        api_key = os.getenv("RIOT_API_KEY")
        if not api_key:
            print("⚠️ RIOT_API_KEY não está definida! Definindo valor de teste temporário...")
            os.environ["RIOT_API_KEY"] = "RGAPI-TEMPORARY-TEST-KEY"
        
        print(f"- Buscando dados do jogador {TEST_PLAYER['name']}#{TEST_PLAYER['tag']}...")
        data_list = fetch_jungle_data(TEST_PLAYER['name'], TEST_PLAYER['tag'], TEST_PLAYER['server'])
        
        if data_list:
            print(f"✅ Sucesso! fetch_jungle_data retornou {len(data_list)} partidas.")
        else:
            print("⚠️ fetch_jungle_data não retornou dados. Isto pode ser normal se a API key for inválida ou não houver partidas.")
            
        player_name_with_tag = f"{TEST_PLAYER['name']}#{TEST_PLAYER['tag']}"
        matches = query_player_matches(conn, player_name_with_tag)
        
        if matches:
            print(f"✅ query_player_matches encontrou {len(matches)} partidas no banco de dados.")
        else:
            print("⚠️ Nenhuma partida encontrada no banco de dados para este jogador.")
            
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("Certifique-se de que está executando este script do diretório correto.")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar módulos diretamente: {e}")
        return False

def check_environment():
    """Verifica o ambiente e dependências"""
    print("\n[VERIFICAÇÃO] Ambiente de execução...")
    
    # Verificar Python
    print(f"- Python versão: {sys.version}")
    
    # Verificar RIOT_API_KEY
    api_key = os.getenv("RIOT_API_KEY")
    if api_key:
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        print(f"- RIOT_API_KEY: Configurada ({masked_key})")
    else:
        print("- RIOT_API_KEY: NÃO CONFIGURADA ⚠️")
        print("  Execute 'export RIOT_API_KEY=sua-chave' (Linux/Mac) ou 'set RIOT_API_KEY=sua-chave' (Windows)")
    
    # Verificar requisitos
    try:
        print("- Verificando dependências...")
        import flask
        try:
            from importlib.metadata import version
            flask_version = version('flask')
            print(f"  ✓ Flask: {flask_version}")
        except:
            print(f"  ✓ Flask: instalado (versão desconhecida)")
    except ImportError:
        print("  ✗ Flask: NÃO INSTALADO")
    
    try:
        import dotenv
        # Usar importlib.metadata para obter a versão corretamente
        try:
            from importlib.metadata import version
            dotenv_version = version('python-dotenv')
            print(f"  ✓ python-dotenv: {dotenv_version}")
        except:
            print(f"  ✓ python-dotenv: instalado (versão desconhecida)")
    except ImportError:
        print("  ✗ python-dotenv: NÃO INSTALADO")
    
    try:
        import sqlite3
        print(f"  ✓ sqlite3: {sqlite3.version}")
    except ImportError:
        print("  ✗ sqlite3: NÃO INSTALADO")
    
    try:
        # Verificar requests da mesma forma
        try:
            from importlib.metadata import version
            requests_version = version('requests')
            print(f"  ✓ requests: {requests_version}")
        except:
            print(f"  ✓ requests: instalado (versão desconhecida)")
    except ImportError:
        print("  ✗ requests: NÃO INSTALADO")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DA API FLASK PARA DADOS DE LEAGUE OF LEGENDS")
    print("=" * 60)
    
    check_environment()
    
    # Pergunta se deve executar testes
    print("\nEste script testará a API Flask e os módulos relacionados.")
    print(f"Certifique-se de que o servidor Flask está rodando em {BASE_URL}")
    print(f"Jogador de teste: {TEST_PLAYER['name']}#{TEST_PLAYER['tag']} ({TEST_PLAYER['server']})")
    
    choice = input("\nDeseja prosseguir com os testes? (s/n): ").lower()
    if choice != 's':
        print("Testes cancelados.")
        sys.exit(0)
    
    # Testes da API
    results = []
    
    results.append(("Health Check", test_health_check()))
    results.append(("GET /player", test_player_get()))
    results.append(("POST /player", test_player_post()))
    results.append(("Módulos diretos", test_direct_database_modules()))
    
    # Resumo dos testes
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        all_passed = all_passed and result
        print(f"{name}: {status}")
    
    if all_passed:
        print("\n✨ TODOS OS TESTES PASSARAM! O backend parece estar funcionando corretamente.")
        print("Se você ainda está tendo problemas com o frontend, o erro provavelmente está lá.")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM. Revise os erros acima para diagnosticar o problema.")