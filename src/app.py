import streamlit as st
from src.agent import gerar_recomendacao

st.set_page_config(
    page_title="FinAssist - Assistente de Investimentos",
    page_icon="💡",
    layout="centered"
)

st.title("💡 FinAssist - Agente Financeiro")
st.caption("Protótipo de Inteligência Artificial para Recomendações de Investimento Baseadas em Dados Reais.")
st.markdown("---")

st.subheader("📋 Preencha seus dados de investimento")

col1, col2 = st.columns(2)

with col1:
    perfil = st.selectbox("Qual o seu perfil de investidor?", ["Conservador", "Moderado", "Arrojado"])
    valor = st.number_input("Valor disponível (R$):", min_value=100.0, value=1000.0, step=100.0)

with col2:
    prazo_opcao = st.selectbox(
        "Qual o prazo pretendido?",
        ["Curto Prazo (até 6 meses)", "Médio Prazo (1 a 3 anos)", "Longo Prazo (mais de 3 anos)"]
    )
    mapeamento_prazos = {
        "Curto Prazo (até 6 meses)": 6,
        "Médio Prazo (1 a 3 anos)": 24,
        "Longo Prazo (mais de 3 anos)": 60
    }
    prazo_meses = mapeamento_prazos[prazo_opcao]

duvida = st.text_input("Dúvida ou objetivo específico (opcional):", placeholder="Ex: Quero usar para reserva de emergência...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Obter Recomendação Personalizada", use_container_width=True):
    with st.spinner("Analisando perfil e consultando base oficial..."):
        resposta = gerar_recomendacao(perfil, prazo_meses, valor, duvida)
        
    st.markdown("### 📝 Recomendação do FinAssist")
    st.info(resposta)

st.markdown("---")
st.caption("🔒 *Orientações fundamentadas estritamente em base de dados estática e regras de alocação de risco.*")