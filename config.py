import random

# Налаштування затримок (у секундах)
DELAYS = {
    'between_wallets': [60, 120],  # Затримка між гаманцями
    'between_transactions': [60, 120]  # Затримка між транзакціями на одному гаманці
}

# Налаштування рандомізації гаманців
RANDOMIZE_WALLETS = True  # True - увімкнути рандомізацію, False - вимкнути

# Конфігурація мереж (RPC-ендпоінти та параметри)
NETWORKS = {
    'Ethereum': {
        'rpc': 'https://rpc.ankr.com/eth',
        'chain_id': 1,
        'native_token': 'ETH',
        'gas_limit': 21000,
        'gas_price_buffer': 1.5
    },
    'BNB Smart Chain': {
        'rpc': 'https://bsc-dataseed.binance.org/',
        'chain_id': 56,
        'native_token': 'BNB',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2
    },
    'Base': {
        'rpc': 'https://mainnet.base.org',
        'chain_id': 8453,
        'native_token': 'ETH',
        'gas_limit': 21000,
        'gas_price_buffer': 1.5
    },
    'Arbitrum One': {
        'rpc': 'https://arb1.arbitrum.io/rpc',
        'chain_id': 42161,
        'native_token': 'ETH',
        'gas_limit': 21000,
        'gas_price_buffer': 1.5
    },
    'Avalanche C-Chain': {
        'rpc': 'https://api.avax.network/ext/bc/C/rpc',
        'chain_id': 43114,
        'native_token': 'AVAX',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2
    },
    'Gnosis': {
        'rpc': 'https://rpc.gnosischain.com',
        'chain_id': 100,
        'native_token': 'xDAI',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2,
        'poa': True
    },
    'Berachain': {
        'rpc': 'https://rpc.berachain.com',
        'chain_id': 80094,
        'native_token': 'BERA',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2
    },
    'Sonic Mainnet': {
        'rpc': 'https://rpc.sonic.omniflix.network',
        'chain_id': 146,
        'native_token': 'S',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2
    },
    'Linea': {
        'rpc': 'https://rpc.linea.build',
        'chain_id': 59144,
        'native_token': 'ETH',
        'gas_limit': 21000,
        'gas_price_buffer': 1.5
    },
    'Scroll': {
        'rpc': 'https://rpc.scroll.io',
        'chain_id': 534352,
        'native_token': 'ETH',
        'gas_limit': 21000,
        'gas_price_buffer': 1.5
    },
    'Core Blockchain': {
        'rpc': 'https://rpc.coredao.org',
        'chain_id': 1116,
        'native_token': 'CORE',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2
    },
    'Kava': {
        'rpc': 'https://evm.kava.io',
        'chain_id': 2222,
        'native_token': 'KAVA',
        'gas_limit': 21000,
        'gas_price_buffer': 1.2
    },
    'zkSync Era': {
        'rpc': 'https://mainnet.era.zksync.io',
        'chain_id': 324,
        'native_token': 'ETH',
        'gas_limit': 21000,
        'gas_price_buffer': 1.5
    }
}

# Функція для отримання випадкової затримки в заданому діапазоні
def get_random_delay(delay_range):
    return random.uniform(delay_range[0], delay_range[1])