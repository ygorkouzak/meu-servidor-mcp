import os
import requests
from dotenv import load_dotenv

load_dotenv("C:/Projetos/meu-servidor-mcp/MEU-SERVIDOR-MCP.env")

print("=== DIAGNÓSTICO DE BUSCA POR CPF ===")
# Endpoint confirmado na imagem image_da8acd.png
url = "https://amigobot-api.amigoapp.com.br/patients/exists"

headers = {
    "Authorization": f"Bearer {os.getenv('AMIGO_API_TOKEN')}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# CPF de teste (remova pontuação se necessário, vamos testar com e sem)
cpf_teste = "701.103.601-68"
cpf_limpo = "70110360168"

def testar_cpf(param_nome, valor):
    print(f"\n--- Testando ?{param_nome}={valor} ---")
    try:
        response = requests.get(url, headers=headers, params={param_nome: valor}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ SUCESSO! Resposta: {response.text}")
            return True
        else:
            print(f"❌ Falha: {response.text}")
            return False
    except Exception as e:
        print(f"Erro: {e}")
        return False

# 1. Teste com CPF formatado
testar_cpf("cpf", cpf_teste)

# 2. Teste com CPF apenas números
testar_cpf("cpf", cpf_limpo)

# 3. Teste genérico (as vezes o parametro é 'value' ou 'document')
testar_cpf("value", cpf_limpo)