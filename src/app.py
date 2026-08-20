"""
Interface Web Interativa (Chat) para o Agente Virtual Financeiro FinAssist.
"""

import sys
from pathlib import Path

# Adiciona a raiz do projeto ao PYTHONPATH para resolver importações no Streamlit Cloud
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (chave GEMINI_API_KEY)
load_dotenv()

from src.agent import executar_agente

# Função auxiliar para cálculo de juros compostos
def calcular_projecao(valor_inicial: float, aporte_mensal: float, taxa_anual_pct: float, prazo_meses: int) -> pd.DataFrame:
    taxa_mensal = (1 + taxa_anual_pct / 100) ** (1/12) - 1
    saldo = valor_inicial
    dados = []
    
    for mes in range(1, prazo_meses + 1):
        rendimento = saldo * taxa_mensal
        saldo += rendimento + aporte_mensal
        total_investido = valor_inicial + (aporte_mensal * mes)
        
        dados.append({
            "Mês": mes,
            "Total Investido (R$)": round(total_investido, 2),
            "Saldo Estimado (R$)": round(saldo, 2)
        })
        
    return pd.DataFrame(dados)

# Configuração da Página
st.set_page_config(
    page_title="FinAssist - Consultor Virtual",
    page_icon="💡",
    layout="centered"
)

st.title("💡 FinAssist - Seu Assistente Financeiro")
st.caption("Consultoria personalizada com Inteligência Artificial e segurança de dados.")

# Barra Lateral (Sidebar) para Parâmetros Financeiros
with st.sidebar:
    st.header("⚙️ Dados do Investimento")
    st.write("Preencha estes campos e clique no botão abaixo para gerar sua análise:")
    
    perfil = st.selectbox(
        "Perfil do Investidor",
        options=["Não especificado", "Conservador", "Moderado", "Arrojado"]
    )
    
    prazo = st.number_input(
        "Prazo Pretendido (em meses)",
        min_value=1,
        max_value=360,
        value=12,
        step=1
    )
    
    valor = st.number_input(
        "Aporte Inicial (R$)",
        min_value=0.0,
        value=1000.0,
        step=100.0,
        format="%.2f"
    )

    aporte_mensal = st.number_input(
        "Aporte Mensal (R$)",
        min_value=0.0,
        value=100.0,
        step=50.0,
        format="%.2f"
    )

    taxa_anual = st.number_input(
        "Taxa Anual Estimada (%)",
        min_value=0.0,
        value=10.5,
        step=0.5,
        format="%.2f"
    )

    # Botão para enviar os dados da Sidebar
    btn_enviar_dados = st.button("📊 Enviar Dados para Análise", use_container_width=True)

    st.markdown("---")

    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Olá! Seja muito bem-vindo ao FinAssist. Como você se chama e como posso te ajudar hoje?"}
        ]
        st.rerun()

# Inicialização do Histórico de Mensagens no State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Seja muito bem-vindo ao FinAssist. Como você se chama e como posso te ajudar hoje?"}
    ]

# Exibição do Histórico do Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Renderiza o Gráfico de Projeção na tela se houver prazo e valor definidos
if prazo > 0 and (valor > 0 or aporte_mensal > 0):
    st.markdown("---")
    st.subheader("📈 Projeção do Crescimento Patrimonial")
    
    df_chart = calcular_projecao(valor, aporte_mensal, taxa_anual, prazo)
    
    # Exibe o gráfico de linhas interativo
    st.line_chart(
        df_chart, 
        x="Mês", 
        y=["Total Investido (R$)", "Saldo Estimado (R$)"],
        color=["#888888", "#29B6F6"]
    )
    
    # Aviso Legal de oscilação das taxas
    st.caption(
        "⚠️ **Observação:** Esta simulação considera a taxa de juros atual informada "
        f"({taxa_anual:.2f}% a.a.). As taxas de mercado oscilam ao longo do tempo "
        "(podendo subir ou cair), portanto os valores finais reais podem variar."
    )
    st.markdown("---")

# Processamento quando o usuário clica no botão da Sidebar
if btn_enviar_dados:
    prompt_simulado = (
        f"Gostaria de uma recomendação para o meu perfil {perfil}, com prazo de {prazo} meses, "
        f"aporte inicial de R$ {valor:,.2f} e aportes mensais de R$ {aporte_mensal:,.2f}."
    )
    
    st.session_state.messages.append({"role": "user", "content": prompt_simulado})
    with st.chat_message("user"):
        st.markdown(prompt_simulado)

    with st.chat_message("assistant"):
        with st.spinner("Analisando perfil e consultando base de conhecimento..."):
            perfil_param = perfil if perfil != "Não especificado" else ""
            resposta_agente = executar_agente(
                perfil=perfil_param,
                prazo_meses=prazo,
                valor=valor,
                mensagem_usuario=prompt_simulado
            )
            st.markdown(resposta_agente)
            
    st.session_state.messages.append({"role": "assistant", "content": resposta_agente})

# Entrada de Texto Livre via Chat
elif user_prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("FinAssist está pensando..."):
            perfil_param = perfil if perfil != "Não especificado" else ""
            resposta_agente = executar_agente(
                perfil=perfil_param,
                prazo_meses=prazo,
                valor=valor,
                mensagem_usuario=user_prompt
            )
            st.markdown(resposta_agente)
            
    st.session_state.messages.append({"role": "assistant", "content": resposta_agente})