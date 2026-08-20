# 💡 FinAssist - Agente Inteligente de Recomendações de Investimento

O **FinAssist** é um assistente virtual especialista em orientar investimentos e planejamento financeiro, desenvolvido em Python utilizando a API do **Google Gemini** e o framework **Streamlit**. O projeto foi construído como parte do bootcamp de Inteligência Artificial da DIO.

O grande diferencial do FinAssist é a sua arquitetura baseada em **Guardrails Anti-Alucinação com RAG (Retrieval-Augmented Generation)** e **Manejo Dinâmico de Risco**: a IA não inventa ativos nem promete rentabilidades milagrosas, adaptando-se com segurança a qualquer combinação de perfil, prazo ou valor.

---

## 🎯 Diferenciais e Funcionalidades

- **Ancoragem em Dados Reais (RAG):** Recomendações baseadas estritamente em um catálogo estático e oficial (`data/mercado_financeiro.json`).
- **Flexibilidade Dinâmica:** Aceita qualquer combinação de parâmetros (ex: perfil Arrojado para curto prazo de 6 meses) gerando estratégias divididas entre liquidez e risco.
- **Proteção Anti-Alucinação:** Se o usuário solicitar ativos fora da base (como Criptomoedas ou Ações Internacionais), a IA recusa a resposta de forma transparente.
- **Linguagem Isenta e Educacional:** Foco em educação financeira sem propaganda de instituições específicas ou garantias indevidas sobre renda variável.

---

## 🛠️ Arquitetura e Tecnologias

- **Linguagem:** Python 3.10+
- **LLM / Engine de IA:** Google Gemini API (`gemini-3.6-flash`) via SDK `google-genai`
- **Interface Web:** Streamlit
- **Gerenciamento de Ambiente:** `python-dotenv`
- **Testes & Avaliação:** Scripts automatizados de validação (`tests/test_eval.py`)

---

## 📁 Estrutura do Projeto

```text
IA Agente/
├── data/
│   └── mercado_financeiro.json  # Base de conhecimento estática de ativos
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Lógica da IA e resolução dinâmica de caminhos
│   └── prompts.py               # Engenharia de prompt neutra e guardrails
├── tests/
│   └── test_eval.py             # Suíte de testes automatizados de segurança
├── app.py                       # Interface interativa no Streamlit
├── requirements.txt             # Dependências do projeto
└── README.md                    # Documentação oficial
