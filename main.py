import os
import threading
from eth_account import Account

# 创建钱包的函数，返回一个新钱包对象
def create_wallet():
    wallet = Account.create(os.urandom(32))
    return wallet

# 查找具有特定前缀和后缀的钱包地址的函数
def find_wallet_with_prefix_and_suffix(prefix, suffix, thread_name):
    counter = 0
    while True:
        counter += 1
        wallet = create_wallet()
        wallet_address = wallet.address

        if wallet_address.startswith(prefix) and wallet_address.endswith(suffix):
            with open('wallets.txt', 'a') as f:
                f.write(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()}\n")
                print(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()}")

        if counter % 10000 == 0:
            print(f"{thread_name} tried {counter} wallets.")

# 定义目标前缀和后缀、线程数
prefix = '0x00'
suffix = '00'

# 创建多线程
thread_count = 8
threads = []

for i in range(thread_count):
    t = threading.Thread(target=find_wallet_with_prefix_and_suffix, args=(prefix, suffix, f'Thread-{i + 1}'), name=f'Thread-{i + 1}')
    threads.append(t)
    t.start()
    print(i, '线程已启动')

# 等待所有线程完成
for t in threads:
    t.join()
