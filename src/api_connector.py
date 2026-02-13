"""
Módulo para conectar e agregar dados de múltiplas APIs.

Suporta: Shopify, Google Sheets, Stripe, etc.
"""

import requests
import pandas as pd
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class APIConnector:
    """Conecta e busca dados de APIs externas."""
    
    def __init__(self, api_key: str, base_url: str):
        """Inicializa o conector de API."""
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_dados(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Busca dados de um endpoint da API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✓ Dados obtidos de: {endpoint}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao conectar API: {str(e)}")
            return None
    
    def post_dados(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """Envia dados para um endpoint da API."""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✓ Dados enviados para: {endpoint}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao enviar dados: {str(e)}")
            return None


class ShopifyConnector(APIConnector):
    """Conector específico para Shopify."""
    
    def __init__(self, shop_name: str, api_key: str):
        """Inicializa conector Shopify."""
        base_url = f"https://{shop_name}.myshopify.com/admin/api/2024-01"
        super( ).__init__(api_key, base_url)
    
    def obter_pedidos(self, status: str = "any") -> Optional[pd.DataFrame]:
        """Obtém pedidos da loja Shopify."""
        dados = self.get_dados("orders.json", {"status": status, "limit": 250})
        
        if dados and 'orders' in dados:
            df = pd.DataFrame(dados['orders'])
            logger.info(f"✓ {len(df)} pedidos obtidos do Shopify")
            return df
        
        return None
    
    def obter_produtos(self) -> Optional[pd.DataFrame]:
        """Obtém produtos da loja Shopify."""
        dados = self.get_dados("products.json", {"limit": 250})
        
        if dados and 'products' in dados:
            df = pd.DataFrame(dados['products'])
            logger.info(f"✓ {len(df)} produtos obtidos do Shopify")
            return df
        
        return None


class GoogleSheetsConnector:
    """Conector para Google Sheets."""
    
    def __init__(self, sheet_id: str, api_key: str):
        """Inicializa conector Google Sheets."""
        self.sheet_id = sheet_id
        self.api_key = api_key
        self.base_url = "https://sheets.googleapis.com/v4/spreadsheets"
    
    def obter_dados(self, range_name: str = "Sheet1" ) -> Optional[pd.DataFrame]:
        """Obtém dados de uma planilha Google Sheets."""
        try:
            url = f"{self.base_url}/{self.sheet_id}/values/{range_name}"
            params = {"key": self.api_key}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            dados = response.json()
            if 'values' in dados:
                df = pd.DataFrame(dados['values'][1:], columns=dados['values'][0])
                logger.info(f"✓ Dados obtidos do Google Sheets: {range_name}")
                return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao conectar Google Sheets: {str(e)}")
        
        return None
