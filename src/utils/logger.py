"""
Módulo de logging (registro de eventos)
Configura el sistema de bitácoras para toda la aplicación
"""

import logging
import sys
from datetime import datetime

def setup_logger(name: str, level: str = "INFO"):
    """
    Configura y devuelve un logger con formato profesional
    
    PARÁMETROS:
    - name: Nombre del logger (ej: 'ExchangeClient', 'TradingEngine')
    - level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    RETORNA:
    - Logger configurado listo para usar
    
    EJEMPLO:
        logger = setup_logger('MiBot', 'DEBUG')
        logger.info("Bot iniciado")
        logger.error("Error crítico")
    """
    
    # 1. Crear el logger con el nombre dado
    logger = logging.getLogger(name)
    
    # 2. Establecer el nivel mínimo (ignora mensajes menos graves)
    #    Si level = INFO, ignora DEBUG (solo muestra INFO, WARNING, ERROR)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 3. Crear un "handler" para enviar mensajes a la consola (pantalla)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Muestra todos los niveles
    
    # 4. Definir el FORMATO de cada mensaje
    #    %(asctime)s  → Fecha y hora
    #    %(name)s     → Nombre del logger
    #    %(levelname)s → Nivel (INFO, ERROR, etc.)
    #    %(message)s  → El mensaje en sí
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # Formato de fecha: 2026-06-26 15:30:45
    )
    console_handler.setFormatter(formatter)
    
    # 5. Agregar el handler al logger
    logger.addHandler(console_handler)
    
    # 6. Devolver el logger configurado
    return logger


def setup_file_logger(name: str, filename: str = "trading_bot.log", level: str = "INFO"):
    """
    Versión del logger que también GUARDA en un archivo
    
    PARÁMETROS:
    - name: Nombre del logger
    - filename: Nombre del archivo donde guardar los logs
    - level: Nivel de logging
    
    EJEMPLO:
        logger = setup_file_logger('MiBot', 'logs/bot.log')
        logger.info("Este mensaje se ve en consola Y se guarda en archivo")
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Handler para CONSOLA (pantalla)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Handler para ARCHIVO (disco duro)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    
    # Formato para ambos handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Agregar ambos handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# ===== FUNCIÓN PARA PROBAR EL LOGGER =====
if __name__ == "__main__":
    """Prueba rápida del logger"""
    
    print("=" * 60)
    print("🧪 PRUEBA DEL LOGGER")
    print("=" * 60 + "\n")
    
    # Crear un logger de prueba
    logger = setup_logger('Prueba', 'DEBUG')
    
    # Probar todos los niveles
    logger.debug("🔍 Esto es DEBUG (solo para desarrollo)")
    logger.info("ℹ️ Esto es INFO (información normal)")
    logger.warning("⚠️ Esto es WARNING (algo extraño)")
    logger.error("❌ Esto es ERROR (algo falló)")
    logger.critical("💀 Esto es CRITICAL (error grave)")
    
    print("\n" + "=" * 60)
    print("✅ Prueba completada")
    print("=" * 60)