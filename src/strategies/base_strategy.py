"""
ESTRATEGIA BASE
Define el "contrato" que todas las estrategias deben cumplir.
Cualquier estrategia que crees DEBE tener estos métodos.
"""

from abc import ABC, abstractmethod
from src.utils.logger import setup_logger


class BaseStrategy(ABC):
    """
    Clase base abstracta para todas las estrategias de trading.
    
    ¿Qué significa "abstracta"?
    - No se puede crear un objeto directamente de esta clase
    - Solo sirve como plantilla para otras clases
    - OBLIGA a las clases hijas a implementar ciertos métodos
    
    ¿Por qué hacer esto?
    - Garantiza que TODAS las estrategias tengan la misma estructura
    - El Trading Engine puede usar CUALQUIER estrategia sin importar
      cómo funciona internamente
    - Es más fácil añadir nuevas estrategias en el futuro
    """
    
    def __init__(self, name: str):
        """
        Constructor de la estrategia base.
        
        PARÁMETROS:
        - name: Nombre de la estrategia (ej: 'SMA', 'RSI', 'MACD')
        
        QUE HACE:
        - Crea un logger con el nombre de la estrategia
        - Guarda el nombre para referencia
        """
        self.logger = setup_logger(f'Strategy_{name}')
        self.name = name
        self.logger.info(f"📊 Estrategia '{name}' inicializada")
    
    # ============================================
    # MÉTODOS ABSTRACTOS (OBLIGATORIOS)
    # ============================================
    # Estos métodos DEBEN ser implementados por cualquier
    # clase que herede de BaseStrategy
    # ============================================
    
    @abstractmethod
    def should_buy(self, market_data: dict) -> bool:
        """
        Determina si se debe COMPRAR.
        
        PARÁMETROS:
        - market_data: Diccionario con datos del mercado
          Ej: {'price': 45000, 'bid': 44950, 'ask': 45050, 'volume': 1000}
        
        RETORNA:
        - True: Si hay señal de compra
        - False: Si no hay señal de compra
        
        EJEMPLO DE IMPLEMENTACIÓN:
            def should_buy(self, market_data):
                if market_data['price'] > 50000:
                    return True
                return False
        """
        pass  # ← Esto no hace nada, la clase hija lo implementa
    
    @abstractmethod
    def should_sell(self, market_data: dict) -> bool:
        """
        Determina si se debe VENDER.
        
        PARÁMETROS:
        - market_data: Diccionario con datos del mercado
        
        RETORNA:
        - True: Si hay señal de venta
        - False: Si no hay señal de venta
        
        EJEMPLO DE IMPLEMENTACIÓN:
            def should_sell(self, market_data):
                if market_data['price'] < 40000:
                    return True
                return False
        """
        pass
    
    @abstractmethod
    def calculate_position_size(self, balance: float, price: float) -> float:
        """
        Calcula el TAMAÑO DE LA POSICIÓN (cuánto comprar/vender).
        
        PARÁMETROS:
        - balance: El dinero disponible en USDT
        - price: El precio actual del activo
        
        RETORNA:
        - La cantidad de BTC a comprar/vender (en unidades, no en dinero)
        
        EJEMPLO:
            balance = 10000 (USDT)
            price = 45000 (precio de BTC)
            Si queremos invertir 10%:
            → 10000 * 0.10 = 1000 USDT
            → 1000 / 45000 = 0.0222 BTC
        
        EJEMPLO DE IMPLEMENTACIÓN:
            def calculate_position_size(self, balance, price):
                # Invertir 10% del balance
                return balance * 0.10 / price
        """
        pass
    
    # ============================================
    # MÉTODOS OPCIONALES (con implementación por defecto)
    # ============================================
    # Estos métodos pueden ser sobreescritos por las clases hijas
    # si necesitan comportamiento personalizado
    # ============================================
    
    def get_info(self) -> dict:
        """
        Devuelve información sobre la estrategia.
        Útil para logs y monitoreo.
        
        RETORNA:
        - Diccionario con información de la estrategia
        """
        return {
            'name': self.name,
            'type': self.__class__.__name__,  # Nombre de la clase
            'parameters': self.get_parameters() if hasattr(self, 'get_parameters') else {}
        }
    
    def reset(self):
        """
        Reinicia el estado de la estrategia.
        Útil para empezar de cero sin reiniciar todo el bot.
        
        Por defecto no hace nada, pero las clases hijas pueden
        sobrescribirlo si necesitan reiniciar su estado interno.
        """
        self.logger.info(f"🔄 Reiniciando estrategia '{self.name}'")
        pass
