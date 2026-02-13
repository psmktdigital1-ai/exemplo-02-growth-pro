"""
Módulo para gerar relatórios automatizados.

Cria relatórios em PDF, Excel e HTML.
"""

import pandas as pd
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Gera relatórios profissionais."""
    
    def __init__(self, titulo: str, empresa: str = "Paulo Growth IA"):
        """Inicializa gerador de relatórios."""
        self.titulo = titulo
        self.empresa = empresa
        self.data_geracao = datetime.now()
        self.secoes = []
    
    def adicionar_secao(self, titulo: str, conteudo: str) -> None:
        """Adiciona uma seção ao relatório."""
        self.secoes.append({
            'titulo': titulo,
            'conteudo': conteudo
        })
        logger.info(f"✓ Seção adicionada: {titulo}")
    
    def adicionar_tabela(self, titulo: str, df: pd.DataFrame) -> None:
        """Adiciona uma tabela ao relatório."""
        self.secoes.append({
            'titulo': titulo,
            'tipo': 'tabela',
            'dados': df
        })
        logger.info(f"✓ Tabela adicionada: {titulo}")
    
    def gerar_html(self, arquivo_saida: str = 'output/relatorio.html') -> bool:
        """Gera relatório em HTML."""
        try:
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{self.titulo}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                    .header {{ background-color: #1a1a1a; color: white; padding: 20px; border-radius: 5px; }}
                    .header h1 {{ margin: 0; }}
                    .header p {{ margin: 5px 0; font-size: 12px; }}
                    .secao {{ background-color: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    .secao h2 {{ color: #1a1a1a; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                    th {{ background-color: #007bff; color: white; padding: 10px; text-align: left; }}
                    td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                    tr:hover {{ background-color: #f9f9f9; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{self.titulo}</h1>
                    <p>Empresa: {self.empresa}</p>
                    <p>Gerado em: {self.data_geracao.strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            """
            
            for secao in self.secoes:
                html += f"<div class='secao'><h2>{secao['titulo']}</h2>"
                
                if secao.get('tipo') == 'tabela':
                    html += secao['dados'].to_html(classes='tabela')
                else:
                    html += f"<p>{secao['conteudo']}</p>"
                
                html += "</div>"
            
            html += """
            </body>
            </html>
            """
            
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write(html)
            
            logger.info(f"✓ Relatório HTML gerado: {arquivo_saida}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Erro ao gerar HTML: {str(e)}")
            return False
    
    def gerar_excel(self, arquivo_saida: str = 'output/relatorio.xlsx') -> bool:
        """Gera relatório em Excel."""
        try:
            with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
                # Aba de resumo
                resumo_data = {
                    'Métrica': ['Título', 'Empresa', 'Data de Geração'],
                    'Valor': [self.titulo, self.empresa, self.data_geracao.strftime('%d/%m/%Y %H:%M:%S')]
                }
                pd.DataFrame(resumo_data).to_excel(writer, sheet_name='Resumo', index=False)
                
                # Abas com as seções
                for i, secao in enumerate(self.secoes):
                    if secao.get('tipo') == 'tabela':
                        secao['dados'].to_excel(writer, sheet_name=secao['titulo'][:31], index=False)
            
            logger.info(f"✓ Relatório Excel gerado: {arquivo_saida}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Erro ao gerar Excel: {str(e)}")
            return False
