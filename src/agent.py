import json
import os
from google import genai
from src.prompts import SYSTEM_PROMPT, montar_prompt_usuario

def obter_caminho_base_conhecimento() -> str:
    """Busca o arquivo JSON testando os locais mais comuns da estrutura."""
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.abspath(os.path.join(diretorio_atual, ".."))
    
    # Lista de locais possíveis para tentar encontrar o JSON
    caminhos_possiveis = [
        os.path.join(raiz_projeto, "data", "mercado_financeiro.json"),
        os.path.join(diretorio_atual, "data", "mercado_financeiro.json"),
        os.path.join(diretorio_atual, "mercado_financeiro.json"),
        os.path.join(raiz_projeto, "mercado_financeiro.json")
    ]
    
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return caminho
            
    return caminhos_possiveis[0] # Retorna o padrão caso nenhum exista

def carregar_base_conhecimento() -> str:
    caminho_json = obter_caminho_base_conhecimento()
    try:
        if not os.path.exists(caminho_json):
            return f"Erro: O arquivo de base de conhecimento não foi localizado em '{caminho_json}'."
            
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return json.dumps(dados, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Erro ao carregar base de conhecimento: {e}"

def gerar_recomendacao(perfil: str, prazo_meses: int, valor: float, duvida: str = "") -> str:
    base_conhecimento = carregar_base_conhecimento()
    
    if "Erro" in base_conhecimento:
        return base_conhecimento

    system_instruction = SYSTEM_PROMPT.format(contexto_base_conhecimento=base_conhecimento)
    user_prompt = montar_prompt_usuario(perfil, prazo_meses, valor, duvida)
    
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_prompt,
            config={"system_instruction": system_instruction}
        )
        return response.text
    except Exception as e:
        return f"Erro ao consultar o agente virtual: {e}\n(Certifique-se de que a variável GEMINI_API_KEY está configurada)."