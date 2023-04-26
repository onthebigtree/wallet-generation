import os
import multiprocessing
from eth_account import Account

prefix1 = '0x0' #你想要的前缀
suffix1 = 'ac'  #你想要的后缀

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

def find_wallet_with_prefix_and_suffix(prefix, suffix):
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
            print(f"Process {multiprocessing.current_process().name} tried {counter} wallets.")

def worker():
    find_wallet_with_prefix_and_suffix(prefix1, suffix1)

if __name__ == '__main__':
    process_count = 8
    processes = []

    for _ in range(process_count):
        p = multiprocessing.Process(target=worker)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
