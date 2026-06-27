"""
Módulo para guardar y cargar el estado del bot.
Permite que el bot "recuerde" sus operaciones entre reinicios.
"""

import json
import os
from datetime import datetime
from src.utils.logger import setup_logger


class StateManager:
    """
    Administra el estado del bot (posiciones abiertas, historial, etc.)
    Guarda la información en un archivo JSON para persistencia.
    """
    
    def __init__(self, state_file: str = "bot_state.json"):
        """
        Inicializa el administrador de estado.
        
        PARÁMETROS:
        - state_file: Nombre del archivo donde guardar el estado
        """
        self.logger = setup_logger('StateManager')
        self.state_file = state_file
        self.state = {
            'current_position': {
                'symbol': None,      # BTC/USDT
                'entry_price': 0,    # Precio al que compramos
                'amount': 0,         # Cantidad comprada
                'timestamp': None    # Cuándo compramos
            },
            'history': [],           # Historial de operaciones
            'balance_history': [],   # Historial de balances
            'last_update': None      # Última actualización
        }
        
        # Intentar cargar estado guardado
        self.load_state()
    
    def load_state(self):
        """
        Carga el estado desde el archivo JSON.
        Si no existe, crea uno nuevo.
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    loaded_state = json.load(f)
                    self.state.update(loaded_state)
                    self.logger.info(f"✅ Estado cargado desde {self.state_file}")
                    
                    # Mostrar posición actual si existe
                    if self.state['current_position']['symbol']:
                        pos = self.state['current_position']
                        self.logger.info(f"   📊 Posición abierta: {pos['amount']:.8f} {pos['symbol']}")
                        self.logger.info(f"   💰 Precio entrada: ${pos['entry_price']:,.2f}")
                return True
            except Exception as e:
                self.logger.warning(f"⚠️ Error cargando estado: {e}")
                self.logger.info("📝 Creando estado nuevo")
                return False
        else:
            self.logger.info("📝 No hay estado guardado, creando nuevo")
            return False
    
    def save_state(self):
        """
        Guarda el estado actual en el archivo JSON.
        """
        try:
            # Actualizar timestamp
            self.state['last_update'] = datetime.now().isoformat()
            
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            self.logger.debug(f"✅ Estado guardado en {self.state_file}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error guardando estado: {e}")
            return False
    
    def open_position(self, symbol: str, entry_price: float, amount: float):
        """
        Registra una nueva posición abierta (compra).
        
        PARÁMETROS:
        - symbol: Par operado (ej: 'BTC/USDT')
        - entry_price: Precio de compra
        - amount: Cantidad comprada
        """
        self.state['current_position'] = {
            'symbol': symbol,
            'entry_price': entry_price,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        
        # Registrar en el historial
        self.state['history'].append({
            'type': 'BUY',
            'symbol': symbol,
            'price': entry_price,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        })
        
        self.logger.info(f"📊 Posición abierta: {amount:.8f} {symbol} @ ${entry_price:,.2f}")
        self.save_state()
    
    def close_position(self, exit_price: float):
        """
        Cierra la posición actual (venta) y calcula ganancia/pérdida.
        
        PARÁMETROS:
        - exit_price: Precio de venta
        """
        position = self.state['current_position']
        
        if not position['symbol']:
            self.logger.warning("⚠️ No hay posición abierta para cerrar")
            return None
        
        # Calcular P&L
        entry_price = position['entry_price']
        amount = position['amount']
        profit_loss = (exit_price - entry_price) * amount
        profit_percentage = ((exit_price - entry_price) / entry_price) * 100
        
        # Registrar en el historial
        self.state['history'].append({
            'type': 'SELL',
            'symbol': position['symbol'],
            'entry_price': entry_price,
            'exit_price': exit_price,
            'amount': amount,
            'profit_loss': profit_loss,
            'profit_percentage': profit_percentage,
            'timestamp': datetime.now().isoformat()
        })
        
        self.logger.info(f"📊 Posición cerrada: {amount:.8f} {position['symbol']}")
        self.logger.info(f"   Precio entrada: ${entry_price:,.2f} → Salida: ${exit_price:,.2f}")
        self.logger.info(f"   P&L: ${profit_loss:,.2f} ({profit_percentage:+.2f}%)")
        
        # Limpiar posición actual
        self.state['current_position'] = {
            'symbol': None,
            'entry_price': 0,
            'amount': 0,
            'timestamp': None
        }
        
        self.save_state()
        return profit_loss
    
    def has_open_position(self) -> bool:
        """
        Verifica si hay una posición abierta.
        """
        return self.state['current_position']['symbol'] is not None
    
    def get_position_info(self) -> dict:
        """
        Devuelve información de la posición actual.
        """
        return self.state['current_position']
    
    def get_summary(self) -> dict:
        """
        Devuelve un resumen del estado del bot.
        """
        total_trades = len(self.state['history'])
        winning_trades = 0
        
        for trade in self.state['history']:
            if trade.get('profit_loss', 0) > 0:
                winning_trades += 1
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'open_position': self.has_open_position(),
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'win_rate': f"{win_rate:.1f}%",
            'last_update': self.state['last_update']
        }