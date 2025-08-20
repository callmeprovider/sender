# Wallet Balance Transfer Script

## Overview
This Python script automates the transfer of 99% of the native token balance (minus gas fees) from wallets listed in `private_keys.txt` to corresponding target addresses in `wallets.txt` across multiple EVM-compatible blockchain networks.

## Features
- **Supported Networks**: Transfers balances across Ethereum, BNB Smart Chain, Base, Arbitrum One, Avalanche C-Chain, Gnosis, Berachain, Sonic Mainnet, Linea, Scroll, Core Blockchain, Kava, and zkSync Era.
- **Randomized Wallet Processing**: Processes wallets in random order by default to support multi-account strategies (configurable in `config.py`).
- **Configurable Delays**: Random delays between wallets and transactions (default: 60-120 seconds) to avoid RPC rate limits.
- **Input Files**:
  - `private_keys.txt`: List of private keys (64 characters, no `0x` prefix).
  - `wallets.txt`: List of target addresses (42 characters, with `0x` prefix).
- **Configurable RPC Endpoints**: Network configurations (RPC URLs, chain IDs, etc.) are defined in `config.py` for easy customization.
- **Error Handling**: Validates private keys and addresses, logs invalid entries, and skips wallets with zero balance or insufficient funds.

## Requirements
- Python 3.7+
- Install dependencies:
  ```bash
  pip install web3
  ```

## Setup
1. **Prepare Input Files**:
   - `private_keys.txt`: One private key per line (e.g., `a1b2c3d4e5f6789a1b2c3d4e5f6789a1b2c3d4e5f6789a1b2c3d4e5f6789`).
   - `wallets.txt`: One target address per line (e.g., `0x54ad1f80b0bcb9946815adf4ae2090a7fdfb251f`). Ensure the number of addresses matches the number of private keys.
2. **Configure Settings**:
   - Edit `config.py` to customize:
     - `DELAYS`: Random delay ranges (in seconds) for `between_wallets` and `between_transactions`.
     - `NETWORKS`: RPC endpoints, chain IDs, gas settings, and native tokens.
     - `RANDOMIZE_WALLETS`: Set to `True` (default) to randomize wallet order or `False` for sequential processing.
3. **Place Files**: Ensure `main.py`, `config.py`, `private_keys.txt`, and `wallets.txt` are in the same directory.

## Usage
Run the script:
```bash
python3 main.py
```

The script will:
- Validate private keys and target addresses.
- Log warnings if the number of wallets differs from the expected 187.
- Process each wallet in random order (if enabled) across all configured networks.
- Transfer 99% of the balance (minus gas fees) to the corresponding target address.
- Log transaction hashes and statuses (success or failure).
- Apply random delays between transactions and wallets.

## Notes
- **Testing**: Test in testnets (e.g., Sepolia, Arbitrum Goerli) before using in mainnet.
- **RPC Endpoints**: Public RPCs may have rate limits. Replace with private endpoints (e.g., Infura, Alchemy) in `config.py` for production.
- **Address Validation**: Ensure all addresses in `wallets.txt` are valid (42 characters, `0x` prefix). Invalid addresses will be logged and skipped.
- **Dependencies Warning**: If you see a `pkg_resources` warning, ignore it or run:
  ```bash
  pip install "setuptools<81"
  ```

## Troubleshooting
- Check logs for invalid private keys or addresses.
- Verify that `private_keys.txt` and `wallets.txt` have the same number of entries.
- Ensure sufficient balance for gas fees in each wallet.
- If RPC connections fail, update `NETWORKS` in `config.py` with reliable endpoints.