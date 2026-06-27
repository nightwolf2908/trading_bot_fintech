"""
ESTRATEGIA DE MEDIA MÓVIL SIMPLE (SMA)
Una de las estrategias más básicas y populares en trading.

¿CÓMO FUNCIONA?
1. Calcula dos medias móviles:
   - SMA Corta (ej: 20 períodos) → Reacciona rápido a cambios
   - SMA Larga (ej: 50 períodos) → Muestra la tendencia general

2. Señal de COMPRA:
   Cuando el precio CRUZA por encima de la SMA corta,
   y la SMA corta está por encima de la SMA larga.
   → Esto indica que la tendencia es ALCISTA

3. Señal de VENTA:
   Cuando el precio CRUZA por debajo de la SMA corta,
   y la SMA corta está por debajo de la SMA larga.
   → Esto indica que la tendencia es BAJISTA
"""

from src.strategies.base_strategy import BaseStrategy


class SimpleMovingAverageStrategy(BaseStrategy):
    """
    Estrategia basada en dos medias móviles simples (SMA).
    
    ATRIBUTOS:
    - short_window: Período de la SMA corta (defecto: 20)
    - long_window: Período de la SMA larga (defecto: 50)
    - prices: Lista de precios históricos
    - risk_percentage: Porcentaje del balance a invertir (defecto: 2.5%)
    """
    
    # ============================================
    # CONSTRUCTOR
    # ============================================
    def __init__(self, short_window: int = 20, long_window: int = 50, risk_percentage: float = 0.025):
        """
        Inicializa la estrategia SMA.
        
        PARÁMETROS:
        - short_window: Período para SMA corta (ej: 20 velas)
        - long_window: Período para SMA larga (ej: 50 velas)
        - risk_percentage: Porcentaje del balance a invertir (ej: 0.025 = 2.5%)
        
        EXPLICACIÓN DE LOS VALORES POR DEFECTO:
        - 20 períodos → Aprox 1 hora en velas de 3 minutos
        - 50 períodos → Aprox 2.5 horas en velas de 3 minutos
        - 2.5% de riesgo → Con $10,000 son $250 por operación
        - Estos son valores comunes en trading
        """
        
        # Llamar al constructor de la clase padre
        # Esto configura el logger y el nombre de la estrategia
        super().__init__('SMA')
        
        # Guardar los períodos configurados
        self.short_window = short_window
        self.long_window = long_window
        
        # 🔥 NUEVO: Porcentaje de riesgo (2.5%)
        self.risk_percentage = risk_percentage
        
        # Lista para almacenar precios históricos
        # Comienza vacía, se irá llenando con add_price()
        self.prices = []
        
        # Log de inicialización
        self.logger.info(f"📊 SMA configurada: corta={short_window}, larga={long_window}")
        self.logger.info(f"   Riesgo: {risk_percentage * 100}% por operación")
        self.logger.info(f"   Se necesitan al menos {long_window} precios para operar")
    
    
    # ============================================
    # MÉTODO PARA AGREGAR PRECIOS
    # ============================================
    def add_price(self, price: float):
        """
        Agrega un precio al histórico.
        
        ¿POR QUÉ ES IMPORTANTE?
        - La estrategia necesita precios históricos para calcular medias
        - Solo guardamos los últimos 'long_window' precios para ahorrar memoria
        
        PARÁMETROS:
        - price: El precio actual a agregar
        """
        
        # Agregar el nuevo precio al final de la lista
        self.prices.append(price)
        
        # Si la lista supera el tamaño necesario, eliminar el más viejo
        # Esto mantiene la memoria bajo control
        if len(self.prices) > self.long_window:
            oldest_price = self.prices.pop(0)
            self.logger.debug(f"🗑️ Eliminando precio antiguo: {oldest_price}")
        
        # Log cada 10 precios (para no saturar los logs)
        if len(self.prices) % 10 == 0:
            self.logger.debug(f"📊 Historial: {len(self.prices)} precios guardados")
    
    
    # ============================================
    # MÉTODO PARA CALCULAR MEDIA MÓVIL
    # ============================================
    def calculate_sma(self, window: int) -> float:
        """
        Calcula la Media Móvil Simple (SMA) para un período.
        
        ¿QUÉ ES LA MEDIA MÓVIL?
        Es el promedio de los últimos 'window' precios.
        
        FÓRMULA:
        SMA = (Precio_1 + Precio_2 + ... + Precio_n) / n
        
        EJEMPLO:
        Precios: [100, 102, 101, 103, 105]
        SMA(3) = (101 + 103 + 105) / 3 = 103
        
        PARÁMETROS:
        - window: Número de períodos a considerar
        
        RETORNA:
        - La media móvil calculada
        - 0 si no hay suficientes datos
        """
        
        # Verificar que tenemos suficientes datos
        if len(self.prices) < window:
            self.logger.debug(f"⚠️ Datos insuficientes: {len(self.prices)}/{window} necesarios")
            return 0
        
        # Tomar los últimos 'window' precios
        recent_prices = self.prices[-window:]
        
        # Calcular el promedio
        average = sum(recent_prices) / window
        
        self.logger.debug(f"📊 SMA({window}): ${average:,.2f} (basado en {len(recent_prices)} precios)")
        return average
    
    
    # ============================================
    # MÉTODO PARA DECIDIR SI COMPRAR
    # ============================================
    def should_buy(self, market_data: dict) -> bool:
        """
        Decide si es momento de COMPRAR.
        
        LÓGICA DE DECISIÓN:
        1. ¿Tenemos suficientes datos? (más que long_window)
        2. Calcular SMA corta y SMA larga
        3. Si precio > SMA_corta > SMA_larga → COMPRAR
        
        ¿POR QUÉ ESTA LÓGICA?
        - Precio > SMA_corta: El precio está subiendo rápido
        - SMA_corta > SMA_larga: La tendencia es alcista
        - Ambas condiciones juntas = fuerte señal de compra
        """
        
        # ---- PASO 1: Verificar datos suficientes ----
        if len(self.prices) < self.long_window:
            self.logger.debug(f"⏳ Esperando más datos... ({len(self.prices)}/{self.long_window})")
            return False
        
        # ---- PASO 2: Obtener precio actual ----
        current_price = market_data.get('price', 0)
        if current_price == 0:
            self.logger.warning("⚠️ Precio no disponible en market_data")
            return False
        
        # ---- PASO 3: Calcular medias móviles ----
        sma_short = self.calculate_sma(self.short_window)
        sma_long = self.calculate_sma(self.long_window)
        
        # Verificar que las medias se calcularon correctamente
        if sma_short == 0 or sma_long == 0:
            self.logger.warning("⚠️ No se pudieron calcular las medias")
            return False
        
        # ---- PASO 4: Evaluar condición de compra ----
        buy_signal = current_price > sma_short > sma_long
        
        if buy_signal:
            self.logger.info(f"📈 SEÑAL DE COMPRA DETECTADA")
            self.logger.info(f"   Precio: ${current_price:,.2f}")
            self.logger.info(f"   SMA({self.short_window}): ${sma_short:,.2f}")
            self.logger.info(f"   SMA({self.long_window}): ${sma_long:,.2f}")
            self.logger.info(f"   Condición: {current_price:,.2f} > {sma_short:,.2f} > {sma_long:,.2f} ✅")
        else:
            self.logger.debug(f"⏸️ Sin señal de compra")
            self.logger.debug(f"   Precio: {current_price:.2f} | SMA corta: {sma_short:.2f} | SMA larga: {sma_long:.2f}")
        
        return buy_signal
    
    
    # ============================================
    # MÉTODO PARA DECIDIR SI VENDER
    # ============================================
    def should_sell(self, market_data: dict) -> bool:
        """
        Decide si es momento de VENDER.
        
        LÓGICA DE DECISIÓN:
        1. ¿Tenemos suficientes datos? (más que long_window)
        2. Calcular SMA corta y SMA larga
        3. Si precio < SMA_corta < SMA_larga → VENDER
        
        ¿POR QUÉ ESTA LÓGICA?
        - Precio < SMA_corta: El precio está bajando rápido
        - SMA_corta < SMA_larga: La tendencia es bajista
        - Ambas condiciones juntas = fuerte señal de venta
        """
        
        # ---- PASO 1: Verificar datos suficientes ----
        if len(self.prices) < self.long_window:
            self.logger.debug(f"⏳ Esperando más datos... ({len(self.prices)}/{self.long_window})")
            return False
        
        # ---- PASO 2: Obtener precio actual ----
        current_price = market_data.get('price', 0)
        if current_price == 0:
            self.logger.warning("⚠️ Precio no disponible en market_data")
            return False
        
        # ---- PASO 3: Calcular medias móviles ----
        sma_short = self.calculate_sma(self.short_window)
        sma_long = self.calculate_sma(self.long_window)
        
        # Verificar que las medias se calcularon correctamente
        if sma_short == 0 or sma_long == 0:
            self.logger.warning("⚠️ No se pudieron calcular las medias")
            return False
        
        # ---- PASO 4: Evaluar condición de venta ----
        sell_signal = current_price < sma_short < sma_long
        
        if sell_signal:
            self.logger.info(f"📉 SEÑAL DE VENTA DETECTADA")
            self.logger.info(f"   Precio: ${current_price:,.2f}")
            self.logger.info(f"   SMA({self.short_window}): ${sma_short:,.2f}")
            self.logger.info(f"   SMA({self.long_window}): ${sma_long:,.2f}")
            self.logger.info(f"   Condición: {current_price:,.2f} < {sma_short:,.2f} < {sma_long:,.2f} ✅")
        else:
            self.logger.debug(f"⏸️ Sin señal de venta")
            self.logger.debug(f"   Precio: {current_price:.2f} | SMA corta: {sma_short:.2f} | SMA larga: {sma_long:.2f}")
        
        return sell_signal
    
    
    # ============================================
    # MÉTODO PARA CALCULAR TAMAÑO DE POSICIÓN
    # ============================================
    def calculate_position_size(self, balance: float, price: float) -> float:
        """
        Calcula cuánto comprar o vender.
        
        ESTRATEGIA DE GESTIÓN DE RIESGO:
        - Invertir máximo el 2.5% del balance en cada operación
        - Esto limita las pérdidas si la operación sale mal
        - Con $10,000 → $250 por operación
        
        FÓRMULA:
        Cantidad a comprar = (Balance * 2.5%) / Precio
        
        EJEMPLO:
        Balance: $10,000 USDT
        Precio BTC: $45,000
        2.5% de $10,000 = $250
        $250 / $45,000 = 0.0055 BTC
        
        PARÁMETROS:
        - balance: Dinero disponible en USDT
        - price: Precio actual del activo
        
        RETORNA:
        - Cantidad del activo a comprar/vender (en BTC, ETH, etc.)
        """
        
        # 🔥 NUEVO: Usar el porcentaje de riesgo configurado (2.5%)
        # Calcular cuánto dinero invertir
        investment_amount = balance * self.risk_percentage
        
        # Calcular cuántas unidades comprar
        position_size = investment_amount / price
        
        # Log de la operación
        self.logger.debug(f"📐 Cálculo de posición:")
        self.logger.debug(f"   Balance: ${balance:,.2f}")
        self.logger.debug(f"   Riesgo: {self.risk_percentage * 100}% → ${investment_amount:,.2f}")
        self.logger.debug(f"   Precio: ${price:,.2f}")
        self.logger.debug(f"   Cantidad: {position_size:.8f} unidades")
        
        return position_size
    
    
    # ============================================
    # MÉTODO PARA REINICIAR LA ESTRATEGIA
    # ============================================
    def reset(self):
        """
        Reinicia el estado de la estrategia.
        Útil para empezar de cero sin reiniciar todo el bot.
        
        QUE HACE:
        - Limpia el historial de precios
        - Reinicia el contador
        """
        self.logger.info(f"🔄 Reiniciando estrategia SMA")
        self.prices = []
        self.logger.info("✅ Historial de precios limpiado")
    
    
    # ============================================
    # MÉTODO PARA OBTENER PARÁMETROS
    # ============================================
    def get_parameters(self) -> dict:
        """
        Devuelve los parámetros actuales de la estrategia.
        Útil para monitoreo y configuración.
        
        RETORNA:
        - Diccionario con los parámetros
        """
        return {
            'short_window': self.short_window,
            'long_window': self.long_window,
            'risk_percentage': self.risk_percentage,
            'risk_percent': f"{self.risk_percentage * 100}%",
            'data_points': len(self.prices)
        }