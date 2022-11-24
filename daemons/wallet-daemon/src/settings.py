import os


BASE_DIR = os.path.abspath(os.path.dirname(__name__))

CONFIG_DIR = os.path.join(BASE_DIR, 'config')

LOGS_DIR = os.path.join(CONFIG_DIR, 'logs')
BLOCKS_DIR = os.path.join(CONFIG_DIR, 'blocks')


INTERNAL_URI = os.getenv('INTERNAL_URI', 'http://127.0.0.1:8000')
INTERNAL_LOGIN = os.getenv('INTERNAL_LOGIN', 'daemon_wallet_login')
INTERNAL_PASSWORD = os.getenv('INTERNAL_PASSWORD', 'daemon_wallet_password')

TRON_GATE_URL = os.getenv('TRON_GATE_URL', 'https://api.shasta.trongrid.io/')
