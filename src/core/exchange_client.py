import ccxt
from config.settings import config
from src.utils.logger import setup_logger

class ExchangeClient:
    """Cliente para interactuar con Binance Testnet"""
    
    def __init__(self):
        self.logger = setup_logger('ExchangeClient')
        
        # Obtener configuración de las llaves
        exchange_config = config.get_exchange_config()
        
        # Crear el cliente de Binance
        self.exchange = ccxt.binance({
            'apiKey': exchange_config['apiKey'],
            'secret': exchange_config['secret'],
            'enableRateLimit': exchange_config['enableRateLimit'],
            'options': exchange_config['options']
        })
        
        # Si estamos en modo testnet, activar el sandbox
        # CCXT automáticamente usará las URLs correctas de testnet
        if config.BINANCE_TESTNET:
            self.exchange.set_sandbox_mode(True)
            self.logger.info("🔬 Modo TESTNET activado (sin dinero real)")
        else:
            self.logger.warning("⚠️ Modo PRODUCCIÓN activado (¡CUIDADO! Dinero real)")
        
        self.logger.info("✅ Cliente de Binance inicializado correctamente")
    
    def check_connection(self):
        """Verifica la conexión con el exchange"""
        try:
            # load_markets() descarga la lista de monedas disponibles
            # Si funciona, la conexión está bien
            self.exchange.load_markets()
            self.logger.info("✅ Conexión exitosa con Binance")
            
            # Mostrar en qué entorno estamos
            if config.BINANCE_TESTNET:
                self.logger.info("📍 Conectado a BINANCE TESTNET (dinero de prueba)")
            else:
                self.logger.info("📍 Conectado a BINANCE PRODUCCIÓN (¡dinero real!)")
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Error de conexión: {e}")
            self.logger.error("   Verifica que tus API keys sean correctas")
            return False
    
    def get_balance(self, currency: str = 'USDT'):
        """Obtiene el balance de una moneda específica"""
        try:
            balance = self.exchange.fetch_balance()
            return balance['total'].get(currency, 0)
        except Exception as e:
            self.logger.error(f"Error obteniendo balance de {currency}: {e}")
            return 0
    
    def get_ticker(self, symbol: str = 'BTC/USDT'):
        """Obtiene el precio actual de un par"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'price': ticker.get('last',0),
                'bid': ticker.get('bid',0),
                'ask': ticker['ask'],
                'volume': ticker.get('volume',0)
            }
        except Exception as e:
            self.logger.error(f"Error obteniendo ticker de {symbol}: {e}")
            return None
    
    def create_order(self, symbol: str, side: str, amount: float, price: float = None):
        """
        Crea una orden de compra/venta
        
        Parámetros:
        - symbol: 'BTC/USDT', 'ETH/USDT', etc.
        - side: 'buy' (comprar) o 'sell' (vender)
        - amount: cantidad a comprar/vender
        - price: (opcional) precio límite, si no se da es orden de mercado
        """
        try:
            if price:
                # Orden LÍMITE: compra/vende SOLO a un precio específico
                self.logger.info(f"📊 Creando orden LÍMITE: {side} {amount} {symbol} a ${price}")
                order = self.exchange.create_limit_order(
                    symbol=symbol,
                    side=side,
                    amount=amount,
                    price=price
                )
            else:
                # Orden de MERCADO: compra/vende AL MEJOR PRECIO disponible
                self.logger.info(f"📊 Creando orden de MERCADO: {side} {amount} {symbol}")
                order = self.exchange.create_market_order(
                    symbol=symbol,
                    side=side,
                    amount=amount
                )
            
            self.logger.info(f"✅ Orden ejecutada exitosamente")
            self.logger.info(f"   ID: {order.get('id', 'N/A')}")
            self.logger.info(f"   Precio: {order.get('price', 'N/A')}")
            self.logger.info(f"   Cantidad: {order.get('amount', 'N/A')}")
            return order
            
        except Exception as e:
            self.logger.error(f"❌ Error creando orden: {e}")
            return None
    
    def get_open_orders(self, symbol: str = None):
        """Obtiene las órdenes abiertas (no ejecutadas)"""
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            self.logger.info(f"📋 Órdenes abiertas: {len(orders)}")
            return orders
        except Exception as e:
            self.logger.error(f"Error obteniendo órdenes abiertas: {e}")
            return []
    
    def cancel_order(self, order_id: str, symbol: str):
        """Cancela una orden específica"""
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            self.logger.info(f"✅ Orden {order_id} cancelada")
            return result
        except Exception as e:
            self.logger.error(f"❌ Error cancelando orden: {e}")
            return None
