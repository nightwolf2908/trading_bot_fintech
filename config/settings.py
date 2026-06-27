import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """Configuración central de la aplicación"""
    
    # ===== LLAVES DE API (las tomamos del .env) =====
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
    
    # ===== MODO DE PRUEBA (True = testnet, False = real) =====
    BINANCE_TESTNET = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
    
    # ===== NIVEL DE REGISTRO (INFO, DEBUG, ERROR) =====
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    def get_exchange_config(self):
        """
        Devuelve la configuración para CCXT
        CCXT ya sabe las URLs, solo necesita las llaves
        """
        return {
            'apiKey': self.BINANCE_API_KEY,
            'secret': self.BINANCE_SECRET_KEY,
            'enableRateLimit': True,  # Evita que nos baneen por muchas peticiones
            'options': {
                'defaultType': 'spot'  # Operamos en el mercado spot (compra/venta normal)
            }
        }

# Crear una instancia de la configuración para usarla en otros archivos
config = Config()
