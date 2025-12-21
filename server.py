import os
import requests
import re
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Carrega variáveis
env_path = "C:/Projetos/meu-servidor-mcp/MEU-SERVIDOR-MCP.env"
load_dotenv(dotenv_path=env_path)

mcp = FastMCP("AmigoRenoirServer")
API_BASE_URL = "https://amigobot-api.amigoapp.com.br"

def get_headers():
    return {
        "Authorization": f"Bearer {os.getenv('AMIGO_API_TOKEN')}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# --- TOOL 1: LISTAR TIPOS DE ATENDIMENTO ---
@mcp.tool()
def listar_tipos_atendimento() -> str:
    """Lista os serviços disponíveis para descobrir o ID correto."""
    url = f"{API_BASE_URL}/events"
    params = {
        "place_id": os.getenv("PLACE_ID"), # Usa 7480
        "user_id": os.getenv("DOCTOR_ID"),
        "insurance_id": os.getenv("INSURANCE_ID")
    }
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code == 200:
            dados = response.json()
            lista = dados.get('data', dados)
            if not lista: return "Nenhum serviço encontrado."
            res = f"Serviços Disponíveis:\n"
            for item in lista:
                eid = item.get('id')
                nome = item.get('name') or item.get('title')
                res += f"- ID: {eid} | Serviço: {nome}\n"
            return res
        return f"Erro ao listar eventos: {response.text}"
    except Exception as e:
        return f"Erro de conexão: {str(e)}"

# --- TOOL 2: BUSCAR PACIENTE POR CPF ---
@mcp.tool()
def buscar_paciente(cpf: str) -> str:
    """Busca paciente pelo CPF (somente números)."""
    cpf_limpo = re.sub(r'\D', '', cpf)
    if len(cpf_limpo) != 11: return "Erro: O CPF deve ter 11 dígitos."

    url = f"{API_BASE_URL}/patients/exists"
    params = {"cpf": cpf_limpo}
    
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code == 200:
            dados = response.json()
            p = dados.get('data')
            if not p: return f"CPF {cpf} não encontrado."
            return f"✅ PACIENTE ENCONTRADO:\n- Nome: {p.get('name')}\n- ID: {p.get('id')}\n- Email: {p.get('email')}"
        elif response.status_code == 404:
            return f"CPF {cpf} não possui cadastro."
        return f"Erro na busca: {response.text}"
    except Exception as e:
        return f"Erro de conexão: {str(e)}"

# --- TOOL 3: CONSULTAR DIAS DISPONÍVEIS ---
@mcp.tool()
def consultar_horarios(mes_ano: str, event_id: int = None) -> str:
    """Lista dias com vagas em 'YYYY-MM'."""
    url = f"{API_BASE_URL}/doctors/{os.getenv('DOCTOR_ID')}/available-dates"
    id_evento = event_id if event_id else int(os.getenv("EVENT_ID"))

    params = {
        "place_id": os.getenv("PLACE_ID"), # IMPORTANTE: Vai enviar 7480
        "event_id": id_evento,
        "insurance_id": os.getenv("INSURANCE_ID"),
        "start_date": f"{mes_ano}-01",
        "end_date": f"{mes_ano}-31"
    }
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code == 200:
            dias = response.json().get('data', [])
            return f"Dias livres em {mes_ano}: {dias}" if dias else f"Sem vagas em {mes_ano}."
        return f"Erro na agenda: {response.text}"
    except Exception as e:
        return f"Erro: {str(e)}"

# --- TOOL 4: AGENDAR CONSULTA ---
@mcp.tool()
def agendar_consulta(data_hora: str, patient_id: int, event_id: int = None) -> str:
    """Agenda consulta. Data: 'YYYY-MM-DD HH:MM'. Exige patient_id."""
    url = f"{API_BASE_URL}/attendances"
    id_evento = event_id if event_id else int(os.getenv("EVENT_ID"))

    payload = {
        "insurance_id": None,
        "event_id": int(id_evento),
        "user_id": int(os.getenv("DOCTOR_ID")),
        "place_id": int(os.getenv("PLACE_ID")),    # 7480
        "account_id": int(os.getenv("ACCOUNT_ID")), # 6955 (Aqui usamos o da empresa)
        "start_date": data_hora,
        "patient_id": int(patient_id),
        "chat_id": "mcp_lia_final",
        "is_dependent_schedule": False
    }
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        if response.status_code in [200, 201]:
            return f"✅ Agendamento Confirmado! {response.text}"
        return f"❌ Falha ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Erro crítico: {str(e)}"

if __name__ == "__main__":
    mcp.run()