"""
Interface Web Interativa (Chat) para o Agente Virtual Financeiro FinAssist.
"""

import streamlit as st
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (chave GEMINI_API_KEY)
load_dotenv()

from src.agent import executar_agente

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
        min_value=0,
        max_value=360,
        value=0,
        step=1
    )
    
    valor = st.number_input(
        "Valor Disponível (R$)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        format="%.2f"
    )

    # Botão para enviar os dados da Sidebar diretamente para a conversa
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

# Processamento quando o usuário clica no botão da Sidebar
if btn_enviar_dados:
    prompt_simulado = f"Gostaria de uma recomendação para o meu perfil {perfil}, com prazo de {prazo} meses e valor de R$ {valor:,.2f}."
    
    # Exibe no chat a solicitação iniciada pela barra lateral
    st.session_state.messages.append({"role": "user", "content": prompt_simulado})
    with st.chat_message("user"):
        st.markdown(prompt_simulado)

    # Gera a resposta com o Gemini
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