# rtu-web

Web interface to remotely send and receive SMS via an Android phone running Termux over SSH. Uses Flask for the web UI and Paramiko for SSH connectivity.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![CI](https://github.com/bi0punk/rtu-web/actions/workflows/ci.yml/badge.svg)](https://github.com/bi0punk/rtu-web/actions/workflows/ci.yml)

## Tabla de Contenidos

- [Características](#características)
- [Stack](#stack)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tests](#tests)
- [Configuración](#configuración)
- [API](#api)
- [CI](#ci)
- [Seguridad](#seguridad)
- [Limitaciones / Roadmap](#limitaciones--roadmap)
- [Licencia](#licencia)

## Características

- Listado de mensajes SMS via `termux-sms-list`
- Envío de SMS con validación de número y sanitización de texto
- Conexión SSH a Android con Termux
- Validación de número con regex (`^\d{7,15}$`)
- Protección contra command injection con `shlex.quote()`

## Stack

- Python 3.11+, Flask, Paramiko (SSH)

## Arquitectura

```
rtu-web/
├── app.py
├── templates/
│   └── index.html
├── tests/
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Requisitos

- Python 3.11+
- Android con Termux y `termux-sms-send` / `termux-sms-list`
- SSH habilitado en Termux

## Instalación

```bash
git clone https://github.com/bi0punk/rtu-web.git
cd rtu-web
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Configurar credenciales SSH en .env
cp .env.example .env
# Editar HOST, USER, PASSWORD

python app.py
```

Abrir `http://localhost:5000` para acceder a la interfaz SMS.

## Tests

```bash
pip install pytest ruff
pytest -q
ruff check .
```

## Configuración

Variables de entorno (ver `.env.example`):

| Variable   | Descripción                        |
|------------|------------------------------------|
| `HOST`     | IP del teléfono Android            |
| `USER`     | Usuario SSH de Termux              |
| `PASSWORD` | Contraseña SSH de Termux           |

## API

| Método | Endpoint      | Descripción                             |
|--------|---------------|-----------------------------------------|
| GET    | `/messages`   | Lista SMS via `termux-sms-list`         |
| POST   | `/send`       | Envía SMS (number validado, texto sanitizado) |

## CI

GitHub Actions ejecuta ruff lint + pytest en cada push y PR.

## Seguridad

- **Command injection:** Número validado con regex `^\d{7,15}$`; texto escapado via `shlex.quote()`
- **SSH:** Host key verification usa `RejectPolicy` (rechaza hosts desconocidos)
- Ejecutar detrás de reverse proxy con HTTPS en producción

## Limitaciones / Roadmap

- [ ] Soporte para MMS
- [ ] Historial de mensajes enviados
- [ ] Contactos desde la agenda del teléfono
- [ ] WebSockets para notificaciones en tiempo real

## Licencia

MIT
