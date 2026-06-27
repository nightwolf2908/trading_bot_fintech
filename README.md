# 🤖 Trading Bot - Sistema de Comercio Algorítmico Cuantitativo
[![CI/CD Pipeline](https://github.com/nightwolf2908/trading_bot_fintech/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/nightwolf2908/trading_bot_fintech/actions/workflows/ci-cd.yml)
[![Docker Image](https://img.shields.io/badge/docker-ghcr.io-blue)](https://github.com/nightwolf2908/trading_bot_fintech/pkgs/container/trading-bot)

Un bot de trading algorítmico profesional que se conecta a Binance Testnet para operar con dinero de prueba. Diseñado con arquitectura modular, estrategias cuantitativas y despliegue automatizado.

## 🚀 Características

- ✅ **Conexión a Binance Testnet** - Opera con dinero de prueba sin riesgo
- ✅ **Estrategias Cuantitativas** - Media Móvil Simple (SMA) con gestión de riesgo
- ✅ **Arquitectura Modular** - Fácil de extender con nuevas estrategias
- ✅ **Persistencia de Estado** - Recuerda posiciones entre reinicios
- ✅ **Logging Profesional** - Registro detallado de todas las operaciones
- ✅ **Manejo de Errores** - Robusto ante fallos de red y API
- ✅ **Dockerizado** - Ejecución consistente en cualquier entorno
- ✅ **CI/CD Automatizado** - Pruebas y despliegue con GitHub Actions
- ✅ **Gestión de Riesgo** - Configuración de porcentaje de inversión

## 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| **Python 3.11** | Lenguaje principal |
| **CCXT** | Conexión a exchanges de criptomonedas |
| **Docker** | Contenerización y despliegue |
| **GitHub Actions** | CI/CD automatizado |
| **GitHub Secrets** | Gestión segura de credenciales |
| **python-dotenv** | Variables de entorno |

## 📦 Requisitos Previos

- Python 3.11 o superior
- Cuenta en Binance Testnet (gratuita)
- Docker (opcional, para contenerización)
- Git

## 🔧 Instalación

### Opción 1: Local (Desarrollo)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/trading-bot.git
cd trading-bot

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 5. Ejecutar pruebas
python test_strategy.py

# 6. Iniciar el bot
python main.py