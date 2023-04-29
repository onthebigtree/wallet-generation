import os
import multiprocessing
from eth_account import Account

prefix = '0x000' #你想要的前缀
suffix = '000'  #你想要的后缀

def create_wallet():
    wallet = Account.create(os.urandom(32))
    return wallet

''' 
安全换速度的方法：十六进制值而不是随机生成值可能会稍微提高速度，使用时请注释掉上面的 create_wallet
def create_wallet():
    fixed_hex_value = bytes.fromhex("0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
    wallet = Account.create(fixed_hex_value)
    return wallet
'''

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

#        if counter % 10000 == 0:  #进度提醒，会影响速度
#            print(f"Process {multiprocessing.current_process().name} tried {counter} wallets.")

def worker():
    find_wallet_with_prefix_and_suffix(prefix, suffix)

if __name__ == '__main__':
    print("程序已开始运行。正在使用多进程查找指定前缀和后缀的以太坊钱包地址。请耐心等待。")

#进程数，默认为CPU核心数
    process_count = multiprocessing.cpu_count()
    processes = []

    for _ in range(process_count):
        p = multiprocessing.Process(target=worker)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
