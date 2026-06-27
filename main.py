#!/usr/bin/env python3
"""
Sistema de Comercio Algorítmico Cuantitativo (Trading Bot)
Punto de entrada principal del bot

Cómo usar:
1. Asegúrate de tener tu .env con las API keys
2. Ejecuta: python main.py
3. Para detener: Presiona Ctrl+C
"""

import sys
import time
from src.core.trading_engine import TradingEngine
from src.utils.logger import setup_logger


def main():
    """
    Función principal que inicia el bot de trading.
    
    FLUJO:
    1. Configura el logger
    2. Crea el motor de trading
    3. Inicia el bot (entra en loop infinito)
    4. Maneja interrupciones (Ctrl+C) y errores
    """
    
    # ---- PASO 1: Configurar logger ----
    logger = setup_logger('Main')
    
    # ---- PASO 2: Mostrar banner de inicio ----
    print("\n" + "=" * 70)
    print("🚀 SISTEMA DE COMERCIO ALGORÍTMICO CUANTITATIVO")
    print("=" * 70)
    print("📊 Trading Bot - Binance Testnet")
    print("⚠️  Usando DINERO DE PRUEBA (sin riesgo)")
    print("=" * 70 + "\n")
    
    logger.info("🔧 Iniciando aplicación...")
    
    # ---- PASO 3: Crear el motor de trading ----
    try:
        # Puedes cambiar el símbolo aquí si quieres
        # Ejemplos: 'BTC/USDT', 'ETH/USDT', 'BNB/USDT'
        SYMBOL = 'BTC/USDT'
        
        logger.info(f"📊 Creando motor de trading para {SYMBOL}...")
        engine = TradingEngine(symbol=SYMBOL)
        logger.info("✅ Motor creado exitosamente")
        
        # ---- PASO 4: Iniciar el bot ----
        logger.info("🚀 Iniciando bot...")
        logger.info("⏹️  Presiona Ctrl+C para detener")
        logger.info("-" * 70)
        
        # Esto entra en un loop infinito hasta que el usuario detenga
        engine.start()
        
    except KeyboardInterrupt:
        # ---- PASO 5: Detener por Ctrl+C ----
        logger.info("\n" + "=" * 70)
        logger.info("⏹️ Interrupción detectada (Ctrl+C)")
        logger.info("🛑 Deteniendo el bot de forma ordenada...")
        
        # Si el motor existe, llamar a stop()
        if 'engine' in locals():
            engine.stop()
        
        logger.info("✅ Bot detenido correctamente")
        logger.info("👋 ¡Hasta luego!")
        sys.exit(0)
        
    except Exception as e:
        # ---- PASO 6: Manejar errores inesperados ----
        logger.error(f"❌ Error fatal: {e}")
        logger.error(f"   Tipo: {type(e).__name__}")
        
        # Mostrar más detalles del error
        import traceback
        logger.error("📋 Detalles del error:")
        logger.error(traceback.format_exc())
        
        logger.info("🛑 Deteniendo el bot debido a error crítico...")
        
        # Intentar detener el motor si existe
        if 'engine' in locals():
            try:
                engine.stop()
            except:
                pass
        
        sys.exit(1)
    
    finally:
        # ---- PASO 7: Limpieza final ----
        logger.info("=" * 70)
        logger.info("🏁 Programa finalizado")
        logger.info("=" * 70)


# ============================================
# PUNTO DE ENTRADA
# ============================================
if __name__ == "__main__":
    """
    Esta condición verifica si el archivo se está ejecutando
    directamente (no importado como módulo).
    
    Si ejecutas: python main.py → Esto se ejecuta
    Si importas: import main → Esto NO se ejecuta
    """
    main()