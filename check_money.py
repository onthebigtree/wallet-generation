import os
import threading
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
    return w3.fromWei(balance, 'ether')

def find_wallet_with_balance():
    counter = 0
    while True:
        counter += 1
        wallet = create_wallet()
        wallet_address = wallet.address
        eth_balance = check_balance(wallet_address)

        if eth_balance > 0:
            with open('rich_wallets.txt', 'a') as f:
                f.write(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()} Balance: {eth_balance} ETH\n")
                print(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()} Balance: {eth_balance} ETH")

        if counter % 1000 == 0:
            print(f"Thread {threading.current_thread().name} tried {counter} wallets.")

# 创建多线程
thread_count = 8
threads = []

for i in range(thread_count):
    t = threading.Thread(target=find_wallet_with_balance, name=f'Thread-{i + 1}')
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
