"""
Script de Execução Principal
Inicia o sistema Visual Inspector AI
"""

import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Função principal"""
    try:
        logger.info("=" * 60)
        logger.info("🚀 VISUAL INSPECTOR AI - Sistema de Inspeção Inteligente")
        logger.info("=" * 60)
        logger.info("")
        
        from web.app import app
        
        host = '0.0.0.0'
        port = 5050
        debug = True
        
        logger.info(f"📡 Servidor iniciando...")
        logger.info(f"   URL: http://{host}:{port}")
        logger.info(f"   Modo Debug: {debug}")
        logger.info("")
        logger.info("🛑 Pressione Ctrl+C para parar")
        logger.info("")
        
        app.run(host=host, port=port, debug=debug, use_reloader=False)
        
    except KeyboardInterrupt:
        logger.info("")
        logger.info("🛑 Encerrando sistema...")
        logger.info("✅ Sistema encerrado com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}", exc_info=True)
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())