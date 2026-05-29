# rtu-web

Web interface to remotely send and receive SMS via an Android phone running Termux over SSH. Uses Flask for the web UI and Paramiko for SSH connectivity.

## Stack

Python 3, Flask, Paramiko (SSH)

## Installation

```bash
pip install flask paramiko
```

## Usage

```bash
python app.py
```

Open `http://localhost:5000` to access the SMS interface. The app connects to a Termux Android device via SSH to execute `termux-sms-list` and `termux-sms-send`.

## API Endpoints

- `GET /messages` — List SMS messages
- `POST /send` — Send an SMS

## License

MIT
