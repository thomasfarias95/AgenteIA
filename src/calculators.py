# src/calculators.py
import pandas as pd

def calcular_projecao(valor_inicial: float, aporte_mensal: float, taxa_anual_pct: float, anos: int) -> pd.DataFrame:
    """Calcula a evolução patrimonial mês a mês com base em juros compostos."""
    taxa_mensal = (1 + taxa_anual_pct / 100) ** (1/12) - 1
    meses = anos * 12
    
    saldo = valor_inicial
    dados = []
    
    for mes in range(1, meses + 1):
        rendimento = saldo * taxa_mensal
        saldo += rendimento + aporte_mensal
        total_investido = valor_inicial + (aporte_mensal * mes)
        
        dados.append({
            "Mês": mes,
            "Total Investido": round(total_investido, 2),
            "Saldo Estimado": round(saldo, 2)
        })
        
    return pd.DataFrame(dados)