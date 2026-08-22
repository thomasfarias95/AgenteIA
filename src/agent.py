"""
Módulo do Agente Inteligente FinAssist.
Gerencia a carga de dados, resolução de caminhos dinâmicos e comunicação com Gemini.
"""

import os
import json
import time
from pathlib import Path
from google import genai
from google.genai import errors
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
    Executa a chamada ao modelo Gemini aplicando o RAG estático, guardrails e retry para 429/503.
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
        
        # Tentativas de reconexão automática
        max_tentativas = 3
        
        for tentativa in range(1, max_tentativas + 1):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt_usuario,
                    config={
                        "system_instruction": system_prompt_formatado,
                        "temperature": 0.2,
                    }
                )
                return response.text

            except errors.APIError as api_err:
                # Se bater no limite de requisições por minuto (429) ou sobrecarga (503), espera 15s antes de tentar novamente
                if api_err.code in (429, 503) and tentativa < max_tentativas:
                    time.sleep(15)
                    continue
                raise api_err

    except errors.APIError as e:
        if e.code == 429:
            return (
                "⏳ **Joaquim está temporariamente ocupado.**\n\n"
                "Atingimos o limite de requisições por minuto da cota gratuita da API. "
                "Aguarde cerca de 30 segundos e envie sua mensagem novamente."
            )
        if e.code == 503:
            return "⚠️ O serviço está instável no momento. Aguarde alguns instantes e tente novamente."
            
        return f"Erro na API do Gemini ({e.code}): {e.message}"

    except Exception as e:
        return f"Ocorreu um erro ao processar sua solicitação: {str(e)}"