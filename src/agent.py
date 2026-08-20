"""
Módulo do Agente Inteligente FinAssist.
Gerencia a carga de dados, resolução de caminhos dinâmicos e comunicação com Gemini.
"""

import os
import json
from pathlib import Path
from google import genai
from src.prompts import SYSTEM_PROMPT, montar_prompt_usuario

def carregar_base_conhecimento() -> str:
    """
    Carrega o arquivo JSON da base de conhecimento usando caminhos relativos robustos.
    """
    diretorio_atual = Path(__file__).parent.resolve()
    caminho_json = diretorio_atual.parent / "data" / "mercado_financeiro.json"
    
    if not caminho_json.exists():
        raise FileNotFoundError(f"Base de conhecimento não encontrada em: {caminho_json}")
        
    with open(caminho_json, "r", encoding="utf-8") as f:
        dados = json.load(f)
        
    return json.dumps(dados, ensure_ascii=False, indent=2)

def executar_agente(
    perfil: str = "", 
    prazo_meses: int = 0, 
    valor: float = 0.0, 
    mensagem_usuario: str = ""
) -> str:
    """
    Executa a chamada ao modelo Gemini aplicando o RAG estático e guardrails.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Erro de Configuração: A variável de ambiente GEMINI_API_KEY não foi encontrada."

    try:
        base_conhecimento = carregar_base_conhecimento()
        
        system_prompt_formatado = SYSTEM_PROMPT.format(
            contexto_base_conhecimento=base_conhecimento
        )
        
        prompt_usuario = montar_prompt_usuario(
            perfil=perfil,
            prazo_meses=prazo_meses,
            valor=valor,
            mensagem_usuario=mensagem_usuario
        )
        
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_usuario,
            config={
                "system_instruction": system_prompt_formatado,
                "temperature": 0.2,
            }
        )
        
        return response.text

    except Exception as e:
        return f"Ocorreu um erro ao processar sua solicitação: {str(e)}"