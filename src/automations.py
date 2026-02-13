"""
Módulo para integração com N8N e automações.

Gerencia workflows, triggers e ações automatizadas.
"""

import requests
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class N8NConnector:
    """Conecta e gerencia workflows N8N."""
    
    def __init__(self, n8n_url: str, api_key: str):
        """Inicializa conector N8N."""
        self.n8n_url = n8n_url
        self.api_key = api_key
        self.headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
    
    def listar_workflows(self) -> Optional[List[Dict]]:
        """Lista todos os workflows."""
        try:
            url = f"{self.n8n_url}/workflows"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✓ {len(response.json())} workflows encontrados")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao listar workflows: {str(e)}")
            return None
    
    def executar_workflow(self, workflow_id: str, dados: Dict = None) -> Optional[Dict]:
        """Executa um workflow."""
        try:
            url = f"{self.n8n_url}/workflows/{workflow_id}/execute"
            payload = {'data': dados or {}}
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            logger.info(f"✓ Workflow {workflow_id} executado com sucesso")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao executar workflow: {str(e)}")
            return None


class AutomationManager:
    """Gerencia automações e triggers."""
    
    def __init__(self):
        """Inicializa gerenciador de automações."""
        self.automacoes = {}
    
    def registrar_automacao(self, nome: str, trigger: str, acao: callable) -> None:
        """Registra uma automação."""
        self.automacoes[nome] = {
            'trigger': trigger,
            'acao': acao,
            'criada_em': datetime.now().isoformat()
        }
        logger.info(f"✓ Automação registrada: {nome}")
    
    def executar_automacao(self, nome: str, dados: Dict = None) -> Optional[Dict]:
        """Executa uma automação registrada."""
        if nome not in self.automacoes:
            logger.error(f"✗ Automação não encontrada: {nome}")
            return None
        
        try:
            automacao = self.automacoes[nome]
            resultado = automacao['acao'](dados or {})
            logger.info(f"✓ Automação executada: {nome}")
            return resultado
        
        except Exception as e:
            logger.error(f"✗ Erro ao executar automação: {str(e)}")
            return None
    
    def listar_automacoes(self) -> Dict:
        """Lista todas as automações registradas."""
        return {
            nome: {
                'trigger': auto['trigger'],
                'criada_em': auto['criada_em']
            }
            for nome, auto in self.automacoes.items()
        }


class SlackNotifier:
    """Envia notificações para Slack."""
    
    def __init__(self, webhook_url: str):
        """Inicializa notificador Slack."""
        self.webhook_url = webhook_url
    
    def enviar_mensagem(self, texto: str, canal: str = None) -> bool:
        """Envia mensagem para Slack."""
        try:
            payload = {
                'text': texto,
                'channel': canal or '#automacoes'
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"✓ Mensagem enviada para Slack")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao enviar para Slack: {str(e)}")
            return False
    
    def enviar_alerta(self, titulo: str, descricao: str, severidade: str = 'warning') -> bool:
        """Envia alerta formatado para Slack."""
        cores = {
            'info': '#36a64f',
            'warning': '#ff9900',
            'error': '#ff0000'
        }
        
        payload = {
            'attachments': [{
                'color': cores.get(severidade, '#36a64f'),
                'title': titulo,
                'text': descricao,
                'ts': int(datetime.now().timestamp())
            }]
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"✓ Alerta enviado para Slack")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Erro ao enviar alerta: {str(e)}")
            return False
