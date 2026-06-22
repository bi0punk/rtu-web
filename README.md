# rtu-web

Web interface to remotely send and receive SMS via an Android phone running Termux over SSH. Uses Flask for the web UI and Paramiko for SSH connectivity.

**Security:** Input sanitization via `shlex.quote()` prevents command injection. SSH uses `RejectPolicy` for host key verification.

## Stack

Python 3, Flask, Paramiko (SSH)

## Installation

```bash
pip install flask paramiko
```

## Configuration

Edit the variables in `app.py` or set environment variables:

| Variable | Description |
|---|---|
| `HOST` | Android phone IP |
| `USER` | Termux SSH username |
| `PASSWORD` | Termux SSH password |

## Usage

```bash
python app.py
```

Open `http://localhost:5000` to access the SMS interface.

## API Endpoints

- `GET /messages` — List SMS messages via `termux-sms-list`
- `POST /send` — Send an SMS (number validated, text sanitized)

## Security

- **Command injection:** Phone number is validated with regex `^\d{7,15}$`; text is escaped via `shlex.quote()`
- **SSH:** Host key verification uses `RejectPolicy` (rejects unknown hosts)
- Run behind a reverse proxy with HTTPS in production

## License

MIT
