"""
Módulo para agregar dados de múltiplas fontes.

Combina dados de APIs, CSVs e bancos de dados em um único DataFrame.
"""

import pandas as pd
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class DataAggregator:
    """Agrega dados de múltiplas fontes."""
    
    def __init__(self):
        """Inicializa o agregador."""
        self.dados = {}
    
    def adicionar_fonte(self, nome: str, df: pd.DataFrame) -> None:
        """Adiciona uma fonte de dados."""
        if df is not None and len(df) > 0:
            self.dados[nome] = df
            logger.info(f"✓ Fonte adicionada: {nome} ({len(df)} linhas)")
        else:
            logger.warning(f"⚠️ Fonte vazia: {nome}")
    
    def mesclar_dados(self, on: str = None, how: str = 'outer') -> Optional[pd.DataFrame]:
        """Mescla todas as fontes de dados."""
        if not self.dados:
            logger.error("✗ Nenhuma fonte de dados adicionada")
            return None
        
        dfs = list(self.dados.values())
        
        if len(dfs) == 1:
            resultado = dfs[0]
        else:
            resultado = dfs[0]
            for df in dfs[1:]:
                if on:
                    resultado = pd.merge(resultado, df, on=on, how=how)
                else:
                    resultado = pd.concat([resultado, df], ignore_index=True)
        
        logger.info(f"✓ Dados mesclados: {len(resultado)} linhas")
        return resultado
    
    def obter_resumo(self) -> dict:
        """Retorna resumo das fontes agregadas."""
        return {
            nome: {
                'linhas': len(df),
                'colunas': len(df.columns),
                'colunas_lista': df.columns.tolist()
            }
            for nome, df in self.dados.items()
        }


class KPICalculator:
    """Calcula KPIs a partir dos dados agregados."""
    
    @staticmethod
    def calcular_receita_total(df: pd.DataFrame, coluna_valor: str) -> float:
        """Calcula receita total."""
        return df[coluna_valor].sum()
    
    @staticmethod
    def calcular_ticket_medio(df: pd.DataFrame, coluna_valor: str) -> float:
        """Calcula ticket médio."""
        return df[coluna_valor].mean()
    
    @staticmethod
    def calcular_crescimento(df: pd.DataFrame, coluna_data: str, coluna_valor: str) -> dict:
        """Calcula crescimento mês a mês."""
        df[coluna_data] = pd.to_datetime(df[coluna_data])
        vendas_mes = df.groupby(df[coluna_data].dt.to_period('M'))[coluna_valor].sum()

        crescimento = vendas_mes.pct_change() * 100
        
        return {
            'vendas': vendas_mes.to_dict(),
            'crescimento': crescimento.to_dict()
        }
    
    @staticmethod
    def calcular_top_produtos(df: pd.DataFrame, coluna_produto: str, coluna_valor: str, top_n: int = 10) -> pd.DataFrame:
        """Retorna top N produtos por valor."""
        return df.groupby(coluna_produto)[coluna_valor].sum().nlargest(top_n)
