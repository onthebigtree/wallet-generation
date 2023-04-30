import os
import multiprocessing
from eth_account import Account
from web3 import Web3

# 请确保输入您自己的Infura API密钥
infura_api_key = 'YOUR_INFURA_API_KEY'

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{infura_api_key}'))


def create_wallet():
    wallet = Account.create(os.urandom(32))
    return wallet


def check_balance(address):
    balance = w3.eth.get_balance(address)
    return w3.from_Wei(balance, 'ether')


def find_wallet_with_balance():
    counter = 0
    while True:
        counter += 1
        wallet = create_wallet()
        wallet_address = wallet.address
        eth_balance = check_balance(wallet_address)

        if eth_balance > 0:
            with open('rich_wallets.txt', 'a') as f:
                f.write(
                    f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()} Balance: {eth_balance} ETH\n")
                print(
                    f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()} Balance: {eth_balance} ETH")

        if counter % 1000 == 0:
            print(
                f"Process {multiprocessing.current_process().name} tried {counter} wallets.")


# 自动选择创建多进程
process_count = multiprocessing.cpu_count()
processes = []

if __name__ == "__main__":
    for i in range(process_count):
        p = multiprocessing.Process(target=find_wallet_with_balance,
                                    name=f'Process-{i + 1}')
        processes.append(p)
        p.start()

    # 等待所有进程完成
    for p in processes:
        p.join()
