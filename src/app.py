"""
Interface Web Interativa (Chat, Consolidador e Criptomoedas) para o Consultor Financeiro Joaquim.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from src.agent import executar_agente

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

st.set_page_config(page_title="Joaquim - Consultor Financeiro", page_icon="🧑‍💼", layout="centered")

st.title("🧑‍💼 Joaquim - Seu Consultor Financeiro")
st.caption("Planejamento personalizado, simulação, carteira e análise de criptoativos.")

# Inicialização de Session States
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Meu nome é Joaquim. Estou aqui para te ajudar a organizar suas finanças e planejar seus investimentos. Como posso te ajudar hoje?"}
    ]

if "exibir_grafico" not in st.session_state:
    st.session_state.exibir_grafico = False

if "carteira" not in st.session_state:
    st.session_state.carteira = pd.DataFrame([
        {"Classe": "Reserva de Emergência", "Valor (R$)": 0.0},
        {"Classe": "Renda Fixa (CDB/Tesouro)", "Valor (R$)": 0.0},
        {"Classe": "Ações Brasil", "Valor (R$)": 0.0},
        {"Classe": "Fundos Imobiliários (FIIs)", "Valor (R$)": 0.0},
        {"Classe": "Criptomoedas", "Valor (R$)": 0.0}
    ])

if "cripto_carteira" not in st.session_state:
    st.session_state.cripto_carteira = pd.DataFrame([
        {"Ativo": "Bitcoin (BTC)", "Valor (R$)": 0.0},
        {"Ativo": "Ethereum (ETH)", "Valor (R$)": 0.0},
        {"Ativo": "Solana (SOL)", "Valor (R$)": 0.0},
        {"Ativo": "Outras Altcoins", "Valor (R$)": 0.0}
    ])

# Barra Lateral (Sidebar)
with st.sidebar:
    st.header("⚙️ Simulação de Investimento")
    st.write("Preencha seus dados para conversarmos sobre seus objetivos:")
    
    perfil = st.selectbox("Perfil do Investidor", options=["Não especificado", "Conservador", "Moderado", "Arrojado"])
    prazo = st.number_input("Prazo Pretendido (meses)", min_value=0, max_value=360, value=0, step=1)
    valor = st.number_input("Aporte Inicial (R$)", min_value=0.0, value=0.0, step=50.0, format="%.2f")
    aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=0.0, step=50.0, format="%.2f")
    taxa_anual = st.number_input("Taxa Anual Estimada (%)", min_value=0.0, value=0.0, step=0.5, format="%.2f")
    
    btn_enviar_dados = st.button("📊 Enviar Simulação para o Joaquim", use_container_width=True)
    st.markdown("---")
    if st.button("🗑️ Limpar Conversa", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Olá! Meu nome é Joaquim. Como posso te ajudar a planejar seu futuro financeiro hoje?"}]
        st.session_state.exibir_grafico = False
        st.rerun()

# Trata envio pela Sidebar
if btn_enviar_dados:
    st.session_state.exibir_grafico = True
    prompt_sidebar = (
        f"Gostaria de uma orientação para o meu perfil {perfil}, planejando um prazo de {prazo} meses, "
        f"com aporte inicial de R$ {valor:,.2f} e aporte mensal de R$ {aporte_mensal:,.2f}."
    )
    st.session_state.messages.append({"role": "user", "content": prompt_sidebar})
    
    perfil_param = perfil if perfil != "Não especificado" else ""
    prompt_com_contexto = (
        f"{prompt_sidebar}\n\n"
        "[Instrução de tom: Responda de forma humana, empática e conversacional. "
        "Lembre-o gentilmente de consultar um especialista financeiro / planejador CFP® para acompanhamento detalhado.]"
    )
    resposta = executar_agente(perfil=perfil_param, prazo_meses=prazo, valor=valor, mensagem_usuario=prompt_com_contexto)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.rerun()

# Navegação por Abas
tab1, tab2, tab3 = st.tabs(["💬 Conversar com o Joaquim", "📊 Consolidador de Carteira", "🪙 Criptomoedas"])

# -------------------- ABA 1: CONSULTOR & SIMULADOR --------------------
with tab1:
    for msg in st.session_state.messages:
        avatar = "🧑‍💼" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if st.session_state.exibir_grafico and prazo > 0 and (valor > 0 or aporte_mensal > 0):
        st.markdown("---")
        st.subheader("📈 Projeção do Crescimento Patrimonial")
        df_chart = calcular_projecao(valor, aporte_mensal, taxa_anual, prazo)
        st.line_chart(df_chart, x="Mês", y=["Total Investido (R$)", "Saldo Estimado (R$)"], color=["#888888", "#29B6F6"])
        st.caption("⚠️ **Aviso:** Esta simulação é educacional. Em caso de dúvidas, consulte um especialista de investimentos.")

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        perfil_param = perfil if perfil != "Não especificado" else ""
        prompt_com_contexto = (
            f"{st.session_state.messages[-1]['content']}\n\n"
            "[Instrução de tom: Responda de forma humana, empática e conversacional. "
            "Lembre-o gentilmente de consultar um especialista financeiro / planejador CFP® para dúvidas complexas.]"
        )
        with st.chat_message("assistant", avatar="🧑‍💼"):
            with st.spinner("Joaquim está digitando..."):
                resposta = executar_agente(perfil=perfil_param, prazo_meses=prazo, valor=valor, mensagem_usuario=prompt_com_contexto)
                st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        st.rerun()

    if user_input := st.chat_input("Escreva sua mensagem para o Joaquim..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

# -------------------- ABA 2: CONSOLIDADOR DE CARTEIRA --------------------
with tab2:
    st.subheader("💼 Consolidador e Alocação de Ativos")
    st.write("Digite o valor que deseja aplicar em cada categoria:")

    col_cat, col_val = st.columns([2, 1])
    with col_cat:
        categoria_selecionada = st.selectbox(
            "Selecione a Classe de Ativo",
            options=["Reserva de Emergência", "Renda Fixa (CDB/Tesouro)", "Ações Brasil", "Fundos Imobiliários (FIIs)", "Criptomoedas"]
        )
    with col_val:
        valor_aporte = st.number_input("Valor a Aplicar (R$)", min_value=0.0, value=0.0, step=100.0, format="%.2f", key="input_carteira")

    if st.button("➕ Adicionar / Atualizar na Carteira", use_container_width=True):
        if valor_aporte >= 0:
            df = st.session_state.carteira
            if categoria_selecionada in df["Classe"].values:
                df.loc[df["Classe"] == categoria_selecionada, "Valor (R$)"] = valor_aporte
            else:
                novo_item = pd.DataFrame([{"Classe": categoria_selecionada, "Valor (R$)": valor_aporte}])
                st.session_state.carteira = pd.concat([df, novo_item], ignore_index=True)
            st.rerun()

    df_editado = st.data_editor(
        st.session_state.carteira,
        num_rows="dynamic",
        column_config={
            "Classe": st.column_config.TextColumn("Classe de Ativo"),
            "Valor (R$)": st.column_config.NumberColumn("Valor Total (R$)", min_value=0, format="R$ %.2f")
        },
        use_container_width=True
    )

    total_patrimonio = df_editado["Valor (R$)"].sum()
    st.metric("Patrimônio Total Consolidado", f"R$ {total_patrimonio:,.2f}")

    if total_patrimonio > 0:
        df_editado["Participação (%)"] = (df_editado["Valor (R$)"] / total_patrimonio) * 100
        st.markdown("### 📊 Distribuição da Carteira")
        st.bar_chart(df_editado, x="Classe", y="Participação (%)")

        if st.button("🧑‍💼 Pedir Análise da Carteira para o Joaquim", use_container_width=True):
            resumo_carteira = df_editado.to_string(index=False)
            prompt_carteira = (
                f"Joaquim, analise minha carteira com total acumulado de R$ {total_patrimonio:,.2f}:\n\n{resumo_carteira}\n\n"
                "Considere o valor total investido e o perfil selecionado. "
                "Forneça uma mensagem incentivadora e recomende consultar um especialista financeiro para estratégias avançadas."
            )
            
            with st.spinner("Joaquim está analisando sua alocação de ativos..."):
                resposta_carteira = executar_agente(perfil=perfil, mensagem_usuario=prompt_carteira)
                st.markdown("### 💡 Diagnóstico do Joaquim")
                st.info(resposta_carteira)

# -------------------- ABA 3: CRIPTOMOEDAS --------------------
with tab3:
    st.subheader("🪙 Gestão e Análise de Criptoativos")
    st.write("Digite o valor que deseja alocar em cada criptoativo:")

    col_cripto_nome, col_cripto_val = st.columns([2, 1])
    with col_cripto_nome:
        cripto_selecionada = st.selectbox(
            "Selecione o Criptoativo",
            options=["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)", "Outras Altcoins", "Stablecoins (USD/BRL)"]
        )
    with col_cripto_val:
        valor_cripto = st.number_input("Valor a Aplicar (R$)", min_value=0.0, value=0.0, step=50.0, format="%.2f", key="input_cripto")

    if st.button("➕ Adicionar / Atualizar Cripto", use_container_width=True):
        if valor_cripto >= 0:
            df_c = st.session_state.cripto_carteira
            if cripto_selecionada in df_c["Ativo"].values:
                df_c.loc[df_c["Ativo"] == cripto_selecionada, "Valor (R$)"] = valor_cripto
            else:
                novo_cripto = pd.DataFrame([{"Ativo": cripto_selecionada, "Valor (R$)": valor_cripto}])
                st.session_state.cripto_carteira = pd.concat([df_c, novo_cripto], ignore_index=True)
            st.rerun()

    df_cripto = st.data_editor(
        st.session_state.cripto_carteira,
        num_rows="dynamic",
        column_config={
            "Ativo": st.column_config.TextColumn("Criptoativo"),
            "Valor (R$)": st.column_config.NumberColumn("Valor Posicionado (R$)", min_value=0, format="R$ %.2f")
        },
        use_container_width=True
    )

    total_cripto = df_cripto["Valor (R$)"].sum()
    st.metric("Total Aplicado em Cripto", f"R$ {total_cripto:,.2f}")

    if total_cripto > 0:
        df_cripto["Participação (%)"] = (df_cripto["Valor (R$)"] / total_cripto) * 100
        st.markdown("### 📉 Distribuição do Portfólio Cripto")
        st.bar_chart(df_cripto, x="Ativo", y="Participação (%)")

    st.markdown("---")
    st.subheader("💡 Avaliação do Joaquim sobre Criptoativos")

    if st.button("🧑‍💼 Analisar Exposição em Criptomoedas", use_container_width=True):
        if total_cripto == 0:
            st.warning("Adicione valores na tabela acima antes de solicitar a análise.")
        else:
            resumo_cripto = df_cripto.to_string(index=False)
            prompt_cripto = (
                f"Joaquim, gostaria de uma análise sobre minha alocação atual em criptomoedas (total R$ {total_cripto:,.2f}):\n\n"
                f"{resumo_cripto}\n\n"
                f"Meu perfil de investidor selecionado é: {perfil}.\n"
                "Explique sobre gestão de risco, volatilidade e se a porcentagem está saudável para o meu perfil."
            )
            
            with st.spinner("Joaquim está analisando seu portfólio cripto..."):
                resposta_cripto = executar_agente(perfil=perfil, mensagem_usuario=prompt_cripto)
                st.info(resposta_cripto)