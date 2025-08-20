from web3 import Web3
import asyncio
from web3.middleware import geth_poa_middleware
import random
from config import DELAYS, get_random_delay, NETWORKS, RANDOMIZE_WALLETS

# Читання файлів
def read_private_keys():
    private_keys = []
    invalid_lines = []
    with open('private_keys.txt', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                invalid_lines.append((i, "порожній рядок"))
                continue
            try:
                # Перевіряємо, чи приватний ключ валідний
                Web3.to_bytes(hexstr=line)
                private_keys.append(line)
            except ValueError:
                invalid_lines.append((i, f"невалідний ключ: {line[:10]}..."))
    if invalid_lines:
        print(f"Знайдено невалідні або порожні рядки в private_keys.txt: {invalid_lines}")
    if not private_keys:
        print("Помилка: Не знайдено жодного валідного приватного ключа в private_keys.txt")
    return private_keys

def read_wallets():
    wallets = []
    invalid_lines = []
    with open('wallets.txt', 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                invalid_lines.append((i, "порожній рядок"))
                continue
            try:
                # Приводимо до checksum-формату
                address = Web3.to_checksum_address(line)
                wallets.append(address)
            except ValueError:
                invalid_lines.append((i, f"невалідна адреса: {line[:10]}..."))
    if invalid_lines:
        print(f"Знайдено невалідні або порожні рядки в wallets.txt: {invalid_lines}")
    if not wallets:
        print("Помилка: Не знайдено жодної валідної адреси в wallets.txt")
    return wallets

# Перевірка валідності адреси
def is_valid_address(w3, address):
    try:
        return w3.is_address(address)
    except:
        return False

# Отримання балансу
def get_balance(w3, address):
    try:
        return w3.eth.get_balance(address)
    except Exception as e:
        print(f"Помилка при отриманні балансу для {address}: {str(e)}")
        return 0

# Відправка транзакції
async def send_transaction(w3, private_key, from_address, to_address, amount, network_config):
    try:
        gas_price = int(w3.eth.gas_price * network_config['gas_price_buffer'])
        gas_limit = network_config['gas_limit']
        nonce = w3.eth.get_transaction_count(from_address)

        # Формуємо транзакцію
        tx = {
            'nonce': nonce,
            'to': Web3.to_checksum_address(to_address),  # Переконаємося, що адреса в checksum-форматі
            'value': int(amount),  # Переконаємося, що value є цілим числом
            'gas': gas_limit,
            'gasPrice': gas_price,
            'chainId': network_config['chain_id']
        }

        # Підписуємо та відправляємо
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Транзакція відправлена: {tx_hash.hex()} для гаманця {from_address} в мережі {network_config['native_token']} на адресу {to_address}")

        # Чекаємо підтвердження
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            print(f"Транзакція успішна: {tx_hash.hex()}")
        else:
            print(f"Транзакція не вдалася: {tx_hash.hex()}")
    except Exception as e:
        print(f"Помилка при відправці транзакції з {from_address} на {to_address}: {str(e)}")

# Основна функція для обробки одного гаманця
async def process_wallet(w3, private_key, main_wallet, network_config, wallet_index):
    try:
        account = w3.eth.account.from_key(private_key)
        from_address = account.address

        if not is_valid_address(w3, from_address):
            print(f"Невалідна адреса джерела (гаманець #{wallet_index + 1}): {from_address}")
            return

        if not is_valid_address(w3, main_wallet):
            print(f"Невалідна цільова адреса (гаманець #{wallet_index + 1}): {main_wallet}")
            return

        balance = get_balance(w3, from_address)
        if balance <= 0:
            print(f"Гаманець #{wallet_index + 1} {from_address} має нульовий баланс у {network_config['native_token']}")
            return

        # Оцінюємо комісію
        gas_price = int(w3.eth.gas_price * network_config['gas_price_buffer'])
        gas_limit = network_config['gas_limit']
        gas_fee = gas_price * gas_limit

        # Відправляємо 99% балансу, якщо вистачає на комісію
        amount_to_send = int(balance * 0.99) - gas_fee
        if amount_to_send <= 0:
            print(f"Недостатньо коштів для транзакції з {from_address} (гаманець #{wallet_index + 1}) після врахування комісії")
            return

        # Перевірка, що amount_to_send є додатнім цілим числом
        if amount_to_send <= 0:
            print(f"Некоректна сума для відправки з {from_address} (гаманець #{wallet_index + 1}): {amount_to_send}")
            return

        # Відправляємо транзакцію
        await send_transaction(w3, private_key, from_address, main_wallet, amount_to_send, network_config)
        # Випадкова затримка між транзакціями
        delay = get_random_delay(DELAYS['between_transactions'])
        print(f"Затримка між транзакціями: {delay:.2f} секунд")
        await asyncio.sleep(delay)

    except Exception as e:
        print(f"Помилка при обробці гаманця #{wallet_index + 1} {from_address}: {str(e)}")

# Обробка однієї мережі
async def process_network(network_name, network_config, wallet_pairs):
    print(f"\nОбробка мережі {network_name}...")
    w3 = Web3(Web3.HTTPProvider(network_config['rpc']))

    # Додаємо POA middleware для мереж, що його потребують (наприклад, Gnosis)
    if network_config.get('poa'):
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    if not w3.is_connected():
        print(f"Не вдалося підключитися до мережі {network_name}")
        return

    # Обробка всіх гаманців
    for index, (private_key, main_wallet) in enumerate(wallet_pairs):
        await process_wallet(w3, private_key, main_wallet, network_config, index)
        # Випадкова затримка між гаманцями
        delay = get_random_delay(DELAYS['between_wallets'])
        print(f"Затримка між гаманцями: {delay:.2f} секунд")
        await asyncio.sleep(delay)

# Головна функція
async def main():
    private_keys = read_private_keys()
    wallets = read_wallets()

    if len(private_keys) != len(wallets):
        print(f"Помилка: Кількість гаманців ({len(private_keys)}) не відповідає кількості цільових адрес ({len(wallets)})")
        return

    if len(private_keys) != 187:
        print(f"Попередження: Знайдено {len(private_keys)} гаманців замість 187")

    # Створюємо пари (приватний ключ, цільова адреса)
    wallet_pairs = list(zip(private_keys, wallets))
    # Рандомізуємо, якщо увімкнено
    if RANDOMIZE_WALLETS:
        random.shuffle(wallet_pairs)
        print("Рандомізація гаманців увімкнена")
    else:
        print("Рандомізація гаманців вимкнена")

    # Обробляємо кожну мережу
    for network_name, network_config in NETWORKS.items():
        await process_network(network_name, network_config, wallet_pairs)

if __name__ == "__main__":
    asyncio.run(main())