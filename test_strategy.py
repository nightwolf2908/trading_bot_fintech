#!/usr/bin/env python3
"""
Prueba de la estrategia SMA SIN conexión a Binance
Usa datos simulados para verificar que la lógica funciona

Esto es útil para:
1. Verificar que la estrategia funciona correctamente
2. Entender cómo toma decisiones
3. Hacer pruebas sin riesgo de perder dinero
"""

import time
import sys
from src.strategies.simple_moving_average import SimpleMovingAverageStrategy
from src.utils.logger import setup_logger


def generar_precios_simulados():
    """
    Genera una serie de precios simulados para probar la estrategia.
    
    Simula un mercado que:
    1. Sube lentamente (tendencia alcista)
    2. Sube más rápido (tendencia alcista fuerte)
    3. Baja (tendencia bajista)
    4. Sube fuerte (recuperación)
    
    RETORNA:
    - Lista de precios simulados
    """
    
    precios = []
    precio_base = 45000  # Precio inicial de BTC
    
    # Fase 1: Subida lenta (30 precios)
    for i in range(30):
        precio_base += 50  # Sube $50 cada paso
        precios.append(precio_base)
    
    # Fase 2: Subida más rápida (20 precios)
    for i in range(20):
        precio_base += 200  # Sube $200 cada paso
        precios.append(precio_base)
    
    # Fase 3: Bajada (30 precios)
    for i in range(30):
        precio_base -= 150  # Baja $150 cada paso
        precios.append(precio_base)
    
    # Fase 4: Subida fuerte (20 precios)
    for i in range(20):
        precio_base += 300  # Sube $300 cada paso
        precios.append(precio_base)
    
    return precios


def probar_estrategia():
    """
    Prueba la estrategia SMA con datos simulados.
    Muestra en tiempo real cómo toma decisiones.
    """
    
    logger = setup_logger('TestStrategy')
    
    print("\n" + "=" * 70)
    print("🧪 PRUEBA DE ESTRATEGIA SMA (SIN BINANCE)")
    print("=" * 70)
    print("📊 Simulando datos de mercado...")
    print("⏱️  Presiona Ctrl+C para detener")
    print("=" * 70 + "\n")
    
    # ---- PASO 1: Crear la estrategia ----
    logger.info("🔧 Creando estrategia SMA...")
    strategy = SimpleMovingAverageStrategy(
        short_window=10,  # SMA corta (10 períodos)
        long_window=20    # SMA larga (20 períodos)
    )
    logger.info(f"✅ Estrategia creada: SMA corta={strategy.short_window}, larga={strategy.long_window}")
    logger.info(f"   Se necesitan {strategy.long_window} precios para empezar a operar")
    print("-" * 70)
    
    # ---- PASO 2: Generar precios simulados ----
    logger.info("📊 Generando precios simulados...")
    precios_simulados = generar_precios_simulados()
    logger.info(f"✅ {len(precios_simulados)} precios generados")
    
    # Mostrar rango de precios
    logger.info(f"   Precio mínimo: ${min(precios_simulados):,.2f}")
    logger.info(f"   Precio máximo: ${max(precios_simulados):,.2f}")
    print("-" * 70)
    
    # ---- PASO 3: Procesar cada precio ----
    logger.info("🔄 Procesando precios...\n")
    
    # Contadores para el resumen
    total_buy_signals = 0
    total_sell_signals = 0
    last_buy_price = 0
    last_sell_price = 0
    
    for i, precio in enumerate(precios_simulados, 1):
        # Agregar precio a la estrategia
        strategy.add_price(precio)
        
        # Crear datos de mercado simulados
        market_data = {
            'price': precio,
            'bid': precio - 10,
            'ask': precio + 10,
            'volume': 1000
        }
        
        # Mostrar estado actual (cada 5 pasos)
        if i % 5 == 0 or i <= 5:
            logger.info(f"📊 Paso {i}: Precio = ${precio:,.2f}")
            
            # Mostrar medias si hay suficientes datos
            if len(strategy.prices) >= strategy.long_window:
                sma_short = strategy.calculate_sma(strategy.short_window)
                sma_long = strategy.calculate_sma(strategy.long_window)
                logger.info(f"   SMA({strategy.short_window}): ${sma_short:,.2f}")
                logger.info(f"   SMA({strategy.long_window}): ${sma_long:,.2f}")
        
        # Verificar señales
        buy_signal = strategy.should_buy(market_data)
        sell_signal = strategy.should_sell(market_data)
        
        # Mostrar señales detectadas
        if buy_signal:
            total_buy_signals += 1
            last_buy_price = precio
            print(f"\n{'=' * 70}")
            logger.info(f"📈 ¡SEÑAL DE COMPRA DETECTADA en paso {i}!")
            logger.info(f"   Precio: ${precio:,.2f}")
            
            # Calcular tamaño de posición
            balance_simulado = 10000  # $10,000 USDT
            position_size = strategy.calculate_position_size(balance_simulado, precio)
            logger.info(f"   Invertir: {position_size:.6f} BTC (${balance_simulado * 0.025:,.2f})")
            print(f"{'=' * 70}\n")
            
        elif sell_signal:
            total_sell_signals += 1
            last_sell_price = precio
            print(f"\n{'=' * 70}")
            logger.info(f"📉 ¡SEÑAL DE VENTA DETECTADA en paso {i}!")
            logger.info(f"   Precio: ${precio:,.2f}")
            
            # Calcular ganancia estimada
            if last_buy_price > 0:
                profit_percentage = ((precio - last_buy_price) / last_buy_price) * 100
                logger.info(f"   Ganancia estimada: {profit_percentage:.2f}%")
            print(f"{'=' * 70}\n")
        
        # Pequeña pausa para ver el progreso
        time.sleep(0.05)  # 50ms para no ir demasiado rápido
    
    # ---- PASO 4: Resumen final ----
    print("\n" + "=" * 70)
    logger.info("📊 RESUMEN DE LA PRUEBA")
    print("=" * 70)
    
    logger.info(f"📈 Total de precios procesados: {len(precios_simulados)}")
    logger.info(f"📊 Precio inicial: ${precios_simulados[0]:,.2f}")
    logger.info(f"📊 Precio final: ${precios_simulados[-1]:,.2f}")
    logger.info(f"📈 Cambio total: ${precios_simulados[-1] - precios_simulados[0]:,.2f}")
    
    # Mostrar estadísticas de señales
    logger.info(f"\n📊 SEÑALES DETECTADAS:")
    logger.info(f"   📈 Compras: {total_buy_signals}")
    logger.info(f"   📉 Ventas: {total_sell_signals}")
    
    if total_buy_signals > 0 or total_sell_signals > 0:
        logger.info(f"\n📊 ÚLTIMAS SEÑALES:")
        if last_buy_price > 0:
            logger.info(f"   Última compra: ${last_buy_price:,.2f}")
        if last_sell_price > 0:
            logger.info(f"   Última venta: ${last_sell_price:,.2f}")
    
    # Mostrar última SMA
    if len(strategy.prices) >= strategy.long_window:
        sma_short_final = strategy.calculate_sma(strategy.short_window)
        sma_long_final = strategy.calculate_sma(strategy.long_window)
        logger.info(f"\n📈 MEDIAS FINALES:")
        logger.info(f"   SMA({strategy.short_window}): ${sma_short_final:,.2f}")
        logger.info(f"   SMA({strategy.long_window}): ${sma_long_final:,.2f}")
        
        # Interpretación final
        last_price = precios_simulados[-1]
        if last_price > sma_short_final > sma_long_final:
            logger.info("   📈 Tendencia: ALCISTA (señal de compra)")
        elif last_price < sma_short_final < sma_long_final:
            logger.info("   📉 Tendencia: BAJISTA (señal de venta)")
        else:
            logger.info("   ⏸️ Tendencia: NEUTRAL (sin señal clara)")
    
    logger.info("\n✅ Prueba completada exitosamente")
    print("=" * 70 + "\n")


# ============================================
# EJECUTAR PRUEBA
# ============================================
if __name__ == "__main__":
    try:
        # Si se pasa el argumento --quick, ejecutar versión rápida
        if len(sys.argv) > 1 and sys.argv[1] == "--quick":
            print("⚡ Modo rápido: solo verificando sintaxis...")
            from src.strategies.simple_moving_average import SimpleMovingAverageStrategy
            strategy = SimpleMovingAverageStrategy(short_window=5, long_window=10)
            for i in range(20, 40):
                strategy.add_price(i)
            assert len(strategy.prices) == 20
            print("✅ Estrategia funciona correctamente")
        else:
            probar_estrategia()
    except KeyboardInterrupt:
        print("\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("📋 Detalles del error:")
        import traceback
        traceback.print_exc()