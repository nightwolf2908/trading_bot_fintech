#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Binance Testnet
"""

import sys
from src.core.exchange_client import ExchangeClient
from src.utils.logger import setup_logger


def main():
    logger = setup_logger('Test')
    
    print("\n" + "=" * 60)
    print("🔬 PRUEBA DE CONEXIÓN CON BINANCE TESTNET")
    print("=" * 60 + "\n")
    
    # 1. Crear el cliente
    logger.info("Creando cliente...")
    client = ExchangeClient()
    
    # 2. Verificar conexión
    logger.info("Verificando conexión...")
    if not client.check_connection():
        logger.error("❌ No se pudo conectar. Verifica tus API keys.")
        return
    
    # 3. Obtener balance de USDT
    logger.info("Obteniendo balance de USDT...")
    balance_usdt = client.get_balance('USDT')
    print(f"💰 Balance USDT: ${balance_usdt:,.2f}")
    
    # 4. Obtener balance de BTC
    logger.info("Obteniendo balance de BTC...")
    balance_btc = client.get_balance('BTC')
    print(f"💰 Balance BTC: {balance_btc:.8f}")
    
    # 5. Obtener precio de BTC/USDT
    logger.info("Obteniendo precio de BTC/USDT...")
    ticker = client.get_ticker('BTC/USDT')
    if ticker:
        print(f"📊 BTC/USDT:")
        print(f"   Precio actual: ${ticker['price']:,.2f}")
        print(f"   Mejor compra (bid): ${ticker['bid']:,.2f}")
        print(f"   Mejor venta (ask): ${ticker['ask']:,.2f}")
        print(f"   Volumen 24h: {ticker['volume']:,.2f}")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)