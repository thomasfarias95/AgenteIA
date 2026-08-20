# 🏦 FinAssist - Agente de Recomendações de Investimento (Santander & DIO)

O **FinAssist** é um assistente virtual especialista em investimentos desenvolvido em Python utilizando a API do **Google Gemini** e o framework **Streamlit**. O projeto foi construído para o desafio de código do bootcamp de IA em parceria com o Santander na DIO.

O principal diferencial do FinAssist é a implementação de **Guardrails anti-alucinação com RAG (Retrieval-Augmented Generation)**: o agente não inventa dados, cotações ou rentabilidades. Todas as recomendações são rigorosamente ancoradas em uma base de conhecimento oficial.

---

## 📽️ Pitch da Solução (Apresentação do Projeto)

### O Problema
Muitos investidores iniciantes enfrentam dúvidas ao organizar suas finanças. Frequentemente encontram recomendações genéricas ou correm o risco de utilizar assistentes de IA que inventam taxas, promovem promessas irrealistas ou indicam produtos desalinhados com o perfil do investidor e com as regras do mercado financeiro.

### A Solução
O **FinAssist** atua como um conselheiro financeiro de primeira linha. A partir do perfil de risco (Conservador, Moderado ou Arrojado), do prazo do objetivo e do valor disponível, a IA analisa a base de ativos autorizada do banco e gera um plano personalizado e detalhado.

### Diferenciais de Segurança (Guardrails & Anti-Alucinação)
1. **Ancoragem em Dados Reais (RAG):** Respostas baseadas estritamente na base cadastrada (`data/mercado_financeiro.json`).
2. **Recusa Transparente:** Caso o usuário pergunte sobre criptomoedas, ações internacionais ou ativos fora do escopo, o FinAssist recusa educadamente a resposta, explicando que só opera com dados oficiais do catálogo.
3. **Perfil e Adequação:** Bloqueio automático de ativos de alto risco para investidores de perfil conservador.
4. **Isenção de Garantia:** O assistente reforça a volatilidade da renda variável sem prometer rentabilidade futura.

---

## 🛠️ Arquitetura e Tecnologias

- **Linguagem:** Python 3.10+
- **LLM / Engine de IA:** Google Gemini API (`gemini-3.6-flash`) via pacote oficial `google-genai`
- **Interface Web:** Streamlit
- **Gerenciamento de Ambiente:** `python-dotenv`
- **Testes & Avaliação:** Scripts automatizados para validação de escopo e *guardrails* (`tests/test_eval.py`)

---

## 📁 Estrutura do Projeto

```text
IA Agente/
├── data/
│   └── mercado_financeiro.json  # Base de conhecimento de ativos e regras
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Integração com a API Gemini
│   └── prompts.py               # Engenharia de prompt e System Prompt
├── tests/
│   └── test_eval.py             # Suíte de testes de segurança e alucinação
├── app.py                       # Interface do usuário com Streamlit
├── requirements.txt             # Dependências do projeto
├── .env.example                 # Modelo de variáveis de ambiente
└── README.md                    # Documentação do projeto
