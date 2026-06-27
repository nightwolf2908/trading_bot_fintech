# src/core/trading_engine.py - Versión con StateManager

"""
MOTOR DE TRADING con StateManager
Ahora el bot "recuerda" sus operaciones entre reinicios.
"""

import time
from src.core.exchange_client import ExchangeClient
from src.core.state_manager import StateManager  # 🔥 NUEVO
from src.strategies.simple_moving_average import SimpleMovingAverageStrategy
from src.utils.logger import setup_logger


class TradingEngine:
    """Motor principal de trading con persistencia de estado"""
    
    def __init__(self, symbol: str = 'BTC/USDT'):
        self.logger = setup_logger('TradingEngine')
        self.client = ExchangeClient()
        self.strategy = SimpleMovingAverageStrategy(
            short_window=20,
            long_window=50,
            risk_percentage=0.025  # 2.5%
        )
        self.symbol = symbol
        self.running = False
        
        # 🔥 NUEVO: Administrador de estado
        self.state_manager = StateManager('bot_state.json')
        
        # Verificar si hay posición abierta al iniciar
        if self.state_manager.has_open_position():
            pos = self.state_manager.get_position_info()
            self.logger.info(f"📊 Posición abierta detectada al iniciar:")
            self.logger.info(f"   {pos['amount']:.8f} {pos['symbol']} @ ${pos['entry_price']:,.2f}")
            self.logger.info(f"   Comprada en: {pos['timestamp']}")
        else:
            self.logger.info("✅ Sin posición abierta al iniciar")
        
        self.logger.info("✅ Motor de trading inicializado correctamente")
    
    def start(self):
        """Inicia el bot de trading"""
        
        self.logger.info("=" * 60)
        self.logger.info("🚀 INICIANDO BOT DE TRADING")
        self.logger.info("=" * 60)
        
        # Verificar conexión
        if not self.client.check_connection():
            self.logger.error("❌ No se pudo conectar a Binance")
            return
        
        self.running = True
        self.logger.info(f"▶️ Bot en estado: CORRIENDO")
        self.logger.info(f"📊 Monitoreando: {self.symbol}")
        
        # Mostrar resumen del estado
        summary = self.state_manager.get_summary()
        self.logger.info(f"📊 Estado del bot:")
        self.logger.info(f"   Trades totales: {summary['total_trades']}")
        self.logger.info(f"   Trades ganadores: {summary['winning_trades']}")
        self.logger.info(f"   Win rate: {summary['win_rate']}")
        self.logger.info(f"   Posición abierta: {'SÍ' if summary['open_position'] else 'NO'}")
        self.logger.info("-" * 60)
        
        iteration = 0
        
        while self.running:
            iteration += 1
            self.logger.info(f"\n🔄 Iteración #{iteration}")
            
            try:
                # 1. Obtener precio
                ticker = self.client.get_ticker(self.symbol)
                if not ticker or ticker.get('price', 0) == 0:
                    self.logger.warning("⚠️ No se pudo obtener precio válido")
                    time.sleep(10)
                    continue
                
                current_price = ticker['price']
                self.logger.info(f"💰 Precio actual: ${current_price:,.2f}")
                
                # 2. Actualizar estrategia
                self.strategy.add_price(current_price)
                
                # 3. Obtener balances
                usdt_balance = self.client.get_balance('USDT')
                btc_balance = self.client.get_balance('BTC')
                
                self.logger.info(f"💰 Balance USDT: ${usdt_balance:,.2f}")
                self.logger.info(f"💰 Balance BTC: {btc_balance:.8f}")
                
                # 4. Verificar posición abierta vs balance real
                # Si el StateManager dice que tenemos BTC pero el balance dice 0
                # significa que vendimos manualmente o hubo un error
                if self.state_manager.has_open_position():
                    pos = self.state_manager.get_position_info()
                    # Si el balance de BTC es menor que la posición registrada
                    if btc_balance < pos['amount'] * 0.99:  # 1% de margen por fees
                        self.logger.warning("⚠️ Balance de BTC no coincide con la posición registrada")
                        self.logger.warning("   Cerrando posición en el state manager...")
                        self.state_manager.close_position(current_price)
                
                # 5. Evaluar señales
                # 🔥 MODIFICADO: Solo comprar si NO hay posición abierta
                if not self.state_manager.has_open_position():
                    if self.strategy.should_buy(ticker):
                        self.logger.info("📈 ¡SEÑAL DE COMPRA DETECTADA!")
                        
                        position_size = self.strategy.calculate_position_size(
                            usdt_balance, 
                            current_price
                        )
                        
                        if position_size > 0 and usdt_balance > 0:
                            self.logger.info(f"💳 Comprando {position_size:.6f} BTC a ${current_price:,.2f}")
                            
                            order = self.client.create_order(
                                symbol=self.symbol,
                                side='buy',
                                amount=position_size
                            )
                            
                            if order:
                                self.logger.info("✅ ¡COMPRA EJECUTADA!")
                                # 🔥 NUEVO: Guardar la posición
                                self.state_manager.open_position(
                                    symbol=self.symbol,
                                    entry_price=current_price,
                                    amount=position_size
                                )
                            else:
                                self.logger.error("❌ Falló la ejecución de la compra")
                        else:
                            self.logger.warning("⚠️ No hay suficiente USDT para comprar")
                
                # 6. Evaluar señal de VENTA
                # 🔥 MODIFICADO: Solo vender si HAY posición abierta
                if self.state_manager.has_open_position():
                    if self.strategy.should_sell(ticker):
                        self.logger.info("📉 ¡SEÑAL DE VENTA DETECTADA!")
                        
                        pos = self.state_manager.get_position_info()
                        amount_to_sell = pos['amount']
                        
                        if btc_balance >= amount_to_sell:
                            self.logger.info(f"💳 Vendiendo {amount_to_sell:.8f} BTC a ${current_price:,.2f}")
                            
                            order = self.client.create_order(
                                symbol=self.symbol,
                                side='sell',
                                amount=amount_to_sell
                            )
                            
                            if order:
                                self.logger.info("✅ ¡VENTA EJECUTADA!")
                                # 🔥 NUEVO: Cerrar la posición
                                profit_loss = self.state_manager.close_position(current_price)
                                self.logger.info(f"💰 P&L: ${profit_loss:,.2f}")
                            else:
                                self.logger.error("❌ Falló la ejecución de la venta")
                        else:
                            self.logger.warning("⚠️ Balance BTC insuficiente para vender")
                            # Sincronizar estado con la realidad
                            if btc_balance < pos['amount'] * 0.99:
                                self.logger.warning("   Sincronizando estado con balance real...")
                                self.state_manager.close_position(current_price)
                else:
                    # Mostrar estado de la estrategia
                    self.logger.info("⏸️ Sin posición abierta, esperando señal de compra")
                
                # 7. Resumen
                self.logger.info("-" * 60)
                
                # Mostrar posición actual si existe
                if self.state_manager.has_open_position():
                    pos = self.state_manager.get_position_info()
                    unrealized_pnl = (current_price - pos['entry_price']) * pos['amount']
                    unrealized_pnl_pct = ((current_price - pos['entry_price']) / pos['entry_price']) * 100
                    self.logger.info(f"📊 POSICIÓN ABIERTA:")
                    self.logger.info(f"   Entrada: ${pos['entry_price']:,.2f}")
                    self.logger.info(f"   Actual: ${current_price:,.2f}")
                    self.logger.info(f"   P&L no realizado: ${unrealized_pnl:,.2f} ({unrealized_pnl_pct:+.2f}%)")
                else:
                    self.logger.info("📊 SIN POSICIÓN ABIERTA")
                
                self.logger.info("-" * 60)
                
                # 8. Esperar
                self.logger.info(f"⏳ Esperando 60 segundos...")
                time.sleep(60)
                
            except KeyboardInterrupt:
                self.logger.info("\n⏹️ Interrupción por usuario")
                self.stop()
                break
            except Exception as e:
                self.logger.error(f"❌ Error en ciclo principal: {e}")
                time.sleep(10)
    
    def stop(self):
        """Detiene el bot"""
        self.logger.info("=" * 60)
        self.logger.info("🛑 DETENIENDO EL BOT")
        self.running = False
        
        # Mostrar resumen final
        summary = self.state_manager.get_summary()
        self.logger.info(f"📊 RESUMEN FINAL:")
        self.logger.info(f"   Trades totales: {summary['total_trades']}")
        self.logger.info(f"   Win rate: {summary['win_rate']}")
        
        if self.state_manager.has_open_position():
            self.logger.info("⚠️ Hay una posición abierta al cerrar")
            pos = self.state_manager.get_position_info()
            self.logger.info(f"   {pos['amount']:.8f} {pos['symbol']} @ ${pos['entry_price']:,.2f}")
            self.logger.info("   La posición se mantendrá para la próxima ejecución")
        
        self.logger.info("✅ Bot detenido correctamente")
