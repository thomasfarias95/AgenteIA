# 💡 FinAssist - Agente Virtual Financeiro de Investimentos

> **Projeto desenvolvido para o Bootcamp Santander DATA & IA (DIO)**

O **FinAssist** é um assistente virtual concebido para guiar pessoas físicas na escolha dos melhores produtos de investimento de acordo com seu perfil de risco, prazos e objetivos financeiros. O projeto foi desenhado focando em **segurança da informação, transparência e combate à alucinação de IA**, garantindo que todas as orientações sejam estritamente baseadas em dados reais e atualizados do mercado.

---

## 🎯 Objetivo e Público-Alvo

* **Objetivo:** Auxiliar usuários a tomar decisões financeiras informadas, recomendando produtos de investimento alinhados às suas necessidades sem inventar taxas ou rendimentos.
* **Público-Alvo:** Investidores iniciantes e intermediários que buscam clareza na alocação de seu patrimônio.
* **Persona do Assistente:** Um consultor educacional, didático, transparente e prudente.

---

## 🛑 Diretrizes Anti-Alucinação (Segurança da Informação)

Para garantir a confiabilidade exigida em serviços financeiros, o assistente opera sob regras estritas de *Guardrails*:
1. **Fato Acima de Tudo:** O agente responde exclusivamente com base na Base de Conhecimento fornecida ou em consultas a APIs de dados financeiros reais.
2. **Recusa Transparente:** Caso o usuário solicite informações ou produtos que não estejam na base (ex: taxas futuras não consolidadas ou ativos não mapeados), o assistente responderá formalmente que não possui dados suficientes.
3. **Sem Aconselhamento Cego:** O assistente não realiza garantias de rentabilidade para renda variável nem projeta ganhos sem citar as condições de mercado atuais.

---

## 🛠️ Arquitetura e Tecnologias

* **Linguagem Principal:** Python 3.10+
* **Orquestração de IA:** LangChain / Framework LLM (utilizando OpenAI GPT-4o ou Google Gemini)
* **Interface do Usuário (Front-End):** Streamlit (interface responsiva otimizada para Desktop e Mobile)
* **Base de Conhecimento:** Estrutura RAG (*Retrieval-Augmented Generation*) alimentada por dados em formato JSON/VectorDB contendo taxas oficiais do mercado (Selic, CDI, IPCA, regras de Renda Fixa e Renda Variável).

---

## 🚀 Estrutura do Repositório

```text
├── data/
│   └── mercado_financeiro.json   # Base de conhecimento com dados e regras
├── src/
│   ├── agent.py                   # Lógica de integração e cadeia RAG
│   └── prompts.py                 # System Prompts e diretrizes de comportamento
├── tests/
│   └── test_eval.py               # Casos de teste e matriz de avaliação
├── app.py                         # Aplicação Streamlit (Interface Web/Mobile)
├── README.md                      # Documentação do projeto
└── requirements.txt               # Dependências do projeto Python
