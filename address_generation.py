import os
import multiprocessing
from eth_account import Account

def create_wallet():
    wallet = Account.create(os.urandom(32))
    return wallet

def find_wallet_with_prefix_and_suffix(prefix1, suffix1):
    counter = 0
    while True:
        counter += 1
        wallet = create_wallet()
        wallet_address = wallet.address

        if wallet_address.startswith(prefix1) and wallet_address.endswith(suffix1):
            with open('wallets.txt', 'a') as f:
                f.write(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()}\n")
                print(f"Wallet found: Address: {wallet_address} Private key: {wallet._private_key.hex()}")

def worker(prefix, suffix):
    find_wallet_with_prefix_and_suffix(prefix, suffix)

if __name__ == '__main__':
    prefix = input("请输入你想要的以太坊钱包地址前缀：")
    suffix = input("请输入你想要的以太坊钱包地址后缀：")

    print("程序已开始运行。正在使用多进程查找指定前缀和后缀的以太坊钱包地址。请耐心等待。")

    #进程数，默认为CPU核心数
    process_count = multiprocessing.cpu_count()
    processes = []

    for _ in range(process_count):
        p = multiprocessing.Process(target=worker, args=(prefix, suffix))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
