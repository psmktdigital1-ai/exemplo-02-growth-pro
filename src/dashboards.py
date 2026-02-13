"""
Módulo para criar múltiplos dashboards profissionais.

Cria 3 dashboards: Vendas, Performance, Análise Detalhada.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logger = logging.getLogger(__name__)


class DashboardBuilder:
    """Cria dashboards profissionais com Plotly."""
    
    @staticmethod
    def dashboard_vendas(df: pd.DataFrame, arquivo_saida: str = 'output/dashboard_vendas.html') -> None:
        """Cria dashboard de vendas."""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Receita por Mês",
                "Top 5 Produtos",
                "Distribuição de Valores",
                "Crescimento Acumulado"
            )
        )
        
        # Gráfico 1: Receita por Mês
        if 'mes' in df.columns:
            vendas_mes = df.groupby('mes')['valor'].sum()
        else:
            vendas_mes = df.groupby(df['data'].dt.to_period('M'))['valor'].sum()
        
        fig.add_trace(
            go.Scatter(x=list(range(len(vendas_mes))), y=vendas_mes.values, mode='lines+markers', name='Receita'),
            row=1, col=1
        )
        
        # Gráfico 2: Top 5 Produtos
        if 'produto' in df.columns:
            top_produtos = df.groupby('produto')['valor'].sum().nlargest(5)
            fig.add_trace(
                go.Bar(x=top_produtos.index, y=top_produtos.values, name='Top Produtos'),
                row=1, col=2
            )
        
        # Gráfico 3: Distribuição de Valores
        fig.add_trace(
            go.Box(y=df['valor'], name='Distribuição'),
            row=2, col=1
        )
        
        # Gráfico 4: Crescimento Acumulado
        vendas_acumulado = df['valor'].cumsum()
        fig.add_trace(
            go.Scatter(y=vendas_acumulado.values, mode='lines', name='Acumulado', fill='tozeroy'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Dashboard de Vendas", template='plotly_dark')
        fig.write_html(arquivo_saida)
        logger.info(f"✓ Dashboard de vendas salvo: {arquivo_saida}")
    
    @staticmethod
    def dashboard_performance(df: pd.DataFrame, arquivo_saida: str = 'output/dashboard_performance.html') -> None:
        """Cria dashboard de performance."""
        
        fig = go.Figure()
        
        # Gráfico de performance
        if 'categoria' in df.columns:
            performance = df.groupby('categoria')['valor'].agg(['sum', 'count', 'mean'])
            
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=("Receita por Categoria", "Quantidade de Transações", "Ticket Médio")
            )
            
            fig.add_trace(go.Bar(x=performance.index, y=performance['sum'], name='Receita'), row=1, col=1)
            fig.add_trace(go.Bar(x=performance.index, y=performance['count'], name='Transações'), row=1, col=2)
            fig.add_trace(go.Bar(x=performance.index, y=performance['mean'], name='Ticket Médio'), row=1, col=3)
        
        fig.update_layout(height=500, title_text="Dashboard de Performance", template='plotly_dark')
        fig.write_html(arquivo_saida)
        logger.info(f"✓ Dashboard de performance salvo: {arquivo_saida}")
    
    @staticmethod
    def dashboard_analise(df: pd.DataFrame, arquivo_saida: str = 'output/dashboard_analise.html') -> None:
        """Cria dashboard de análise detalhada."""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Tendência Temporal", "Correlação", "Distribuição", "Ranking")
        )
        
        # Gráfico 1: Tendência
        if 'data' in df.columns:
            df['data'] = pd.to_datetime(df['data'])
            tendencia = df.groupby(df['data'].dt.date)['valor'].sum()
            fig.add_trace(go.Scatter(x=tendencia.index, y=tendencia.values, mode='lines', name='Tendência'), row=1, col=1)
        
        # Gráfico 2: Histograma
        fig.add_trace(go.Histogram(x=df['valor'], name='Distribuição'), row=1, col=2)
        
        # Gráfico 3: Scatter
        if len(df) > 0:
            fig.add_trace(go.Scatter(y=df['valor'].values, mode='markers', name='Valores'), row=2, col=1)
        
        # Gráfico 4: Ranking
        if 'cliente' in df.columns:
            top_clientes = df.groupby('cliente')['valor'].sum().nlargest(10)
            fig.add_trace(go.Bar(x=top_clientes.values, y=top_clientes.index, orientation='h', name='Top Clientes'), row=2, col=2)
        
        fig.update_layout(height=800, title_text="Dashboard de Análise Detalhada", template='plotly_dark')
        fig.write_html(arquivo_saida)
        logger.info(f"✓ Dashboard de análise salvo: {arquivo_saida}")
