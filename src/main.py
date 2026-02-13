"""
Pipeline principal do Growth Pro.

Orquestra: API → Agregação → Dashboards → Relatórios → Automações.
"""

import logging
import pandas as pd
from datetime import datetime
import os
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/growth_pro.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Importar módulos
from api_connector import ShopifyConnector, GoogleSheetsConnector
from data_aggregator import DataAggregator, KPICalculator
from dashboards import DashboardBuilder
from automations import N8NConnector, AutomationManager, SlackNotifier
from reports import ReportGenerator


class GrowthProPipeline:
    """Pipeline principal do Growth Pro."""
    
    def __init__(self):
        """Inicializa o pipeline."""
        logger.info("=" * 60)
        logger.info("🚀 INICIANDO GROWTH PRO PIPELINE")
        logger.info("=" * 60)
        
        self.agregador = DataAggregator()
        self.kpi_calc = KPICalculator()
        self.dashboard = DashboardBuilder()
        self.dados_finais = None
    
    def etapa_1_conectar_apis(self) -> None:
        """Etapa 1: Conectar a APIs e buscar dados."""
        logger.info("\n📡 ETAPA 1: Conectando a APIs...")
        
        # Exemplo: Shopify (você precisa adicionar suas credenciais no .env)
        # shopify = ShopifyConnector(os.getenv('SHOPIFY_SHOP'), os.getenv('SHOPIFY_API_KEY'))
        # pedidos = shopify.obter_pedidos()
        # self.agregador.adicionar_fonte('Shopify Pedidos', pedidos)
        
        logger.info("✓ Etapa 1 concluída")
    
    def etapa_2_agregar_dados(self) -> None:
        """Etapa 2: Agregar dados de múltiplas fontes."""
        logger.info("\n🔗 ETAPA 2: Agregando dados...")
        
        # Criar dados de exemplo para demonstração
        dados_exemplo = pd.DataFrame({
            'data': pd.date_range('2024-01-01', periods=100),
            'valor': [1000 + i * 50 for i in range(100)],
            'produto': ['Produto A', 'Produto B', 'Produto C'] * 33 + ['Produto A'],
            'categoria': ['Eletrônicos', 'Software', 'Serviços'] * 33 + ['Eletrônicos'],
            'cliente': ['Cliente ' + str(i % 10) for i in range(100)]
        })
        
        self.agregador.adicionar_fonte('Dados Exemplo', dados_exemplo)
        
        self.dados_finais = self.agregador.mesclar_dados()
        logger.info("✓ Etapa 2 concluída")
    
    def etapa_3_gerar_dashboards(self) -> None:
        """Etapa 3: Gerar dashboards."""
        logger.info("\n📊 ETAPA 3: Gerando dashboards...")
        
        if self.dados_finais is not None:
            self.dashboard.dashboard_vendas(self.dados_finais)
            self.dashboard.dashboard_performance(self.dados_finais)
            self.dashboard.dashboard_analise(self.dados_finais)
        
        logger.info("✓ Etapa 3 concluída")
    
    def etapa_4_calcular_kpis(self) -> None:
        """Etapa 4: Calcular KPIs."""
        logger.info("\n📈 ETAPA 4: Calculando KPIs...")
        
        if self.dados_finais is not None:
            receita_total = self.kpi_calc.calcular_receita_total(self.dados_finais, 'valor')
            ticket_medio = self.kpi_calc.calcular_ticket_medio(self.dados_finais, 'valor')
            
            logger.info(f"   Receita Total: R$ {receita_total:,.2f}")
            logger.info(f"   Ticket Médio: R$ {ticket_medio:,.2f}")
        
        logger.info("✓ Etapa 4 concluída")
    
    def etapa_5_gerar_relatorios(self) -> None:
        """Etapa 5: Gerar relatórios."""
        logger.info("\n📄 ETAPA 5: Gerando relatórios...")
        
        relatorio = ReportGenerator("Relatório Growth Pro", "Paulo Growth IA")
        
        if self.dados_finais is not None:
            receita_total = self.kpi_calc.calcular_receita_total(self.dados_finais, 'valor')
            ticket_medio = self.kpi_calc.calcular_ticket_medio(self.dados_finais, 'valor')
            
            relatorio.adicionar_secao(
                "Resumo Executivo",
                f"Receita Total: R$ {receita_total:,.2f} | Ticket Médio: R$ {ticket_medio:,.2f}"
            )
            relatorio.adicionar_tabela("Dados Agregados", self.dados_finais.head(20))
        
        relatorio.gerar_html()
        relatorio.gerar_excel()
        
        logger.info("✓ Etapa 5 concluída")
    
    def etapa_6_automacoes(self) -> None:
        """Etapa 6: Configurar automações."""
        logger.info("\n⚙️ ETAPA 6: Configurando automações...")
        
        # Exemplo de automação
        manager = AutomationManager()
        
        def acao_exemplo(dados):
            return {'status': 'sucesso', 'mensagem': 'Automação executada'}
        
        manager.registrar_automacao('relatorio_diario', 'schedule', acao_exemplo)
        
        logger.info("✓ Etapa 6 concluída")
    
    def executar(self) -> None:
        """Executa o pipeline completo."""
        try:
            self.etapa_1_conectar_apis()
            self.etapa_2_agregar_dados()
            self.etapa_3_gerar_dashboards()
            self.etapa_4_calcular_kpis()
            self.etapa_5_gerar_relatorios()
            self.etapa_6_automacoes()
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"\n❌ ERRO NO PIPELINE: {str(e)}")
            raise


if __name__ == "__main__":
    # Criar diretórios necessários
    os.makedirs('output', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Executar pipeline
    pipeline = GrowthProPipeline()
    pipeline.executar()
