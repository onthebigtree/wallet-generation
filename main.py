import os
import threading
from eth_account import Account

def create_wallet():
    wallet = Account.create(os.urandom(32))
    return wallet

def find_wallet_with_prefix(prefix):
    counter = 0
    while True:
        counter += 1
        wallet = create_wallet()
        wallet_address = wallet.address

        if wallet_address.startswith(prefix):
            with open('wallets.txt', 'a') as f:
                f.write(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()}\n")
                print(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()}")
        if counter % 1000 == 0:
            print(f"Thread {threading.current_thread().name} tried {counter} wallets.")

# 调用函数
prefix = '0x00'

# 创建多线程
thread_count = 3
threads = []

for i in range(thread_count):
    t = threading.Thread(target=find_wallet_with_prefix, args=(prefix,), name=f'Thread-{i + 1}')
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()
