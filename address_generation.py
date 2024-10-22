import os
import multiprocessing
from eth_account import Account
import time
import secrets
import math
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519

def create_eth_wallet():
    private_key = secrets.token_bytes(32)
    return Account.from_key(private_key)

def create_sui_wallet():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes_raw()
    address = hashlib.blake2b(public_key_bytes, digest_size=32).hexdigest()
    return (address, private_key.private_bytes_raw().hex())

def find_eth_wallet_with_prefix_and_suffix(prefix, suffix, queue, counter, batch_size=1000):
    while True:
        wallets = [create_eth_wallet() for _ in range(batch_size)]
        with counter.get_lock():
            counter.value += batch_size
        for wallet in wallets:
            if wallet.address[2:].startswith(prefix) and wallet.address.endswith(suffix):
                queue.put((wallet.address, wallet._private_key.hex()))
                return

def find_sui_wallet_with_prefix_and_suffix(prefix, suffix, queue, counter, batch_size=1000):
    while True:
        wallets = [create_sui_wallet() for _ in range(batch_size)]
        with counter.get_lock():
            counter.value += batch_size
        for address, private_key in wallets:
            if address.startswith(prefix) and address.endswith(suffix):
                queue.put((address, private_key))
                return

def worker(wallet_type, prefix, suffix, queue, counter):
    try:
        if wallet_type == "ETH":
            find_eth_wallet_with_prefix_and_suffix(prefix, suffix, queue, counter)
        elif wallet_type == "SUI":
            find_sui_wallet_with_prefix_and_suffix(prefix, suffix, queue, counter)
    except Exception as e:
        print(f"Worker error: {e}")

def calculate_search_space(prefix, suffix):
    return 16 ** (len(prefix) + len(suffix))

def estimate_time(expected_attempts, attempts, elapsed_time):
    attempts_per_second = attempts / elapsed_time if elapsed_time > 0 else 0
    if attempts_per_second == 0:
        return float('inf')
    
    remaining_attempts = max(0, expected_attempts - attempts)
    estimated_time = remaining_attempts / attempts_per_second
    
    return estimated_time

def format_time(seconds):
    if math.isinf(seconds):
        return "无法估计"
    if seconds < 60:
        return f"{seconds:.2f} 秒"
    elif seconds < 3600:
        return f"{seconds/60:.2f} 分钟"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} 小时"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} 天"
    else:
        return f"{seconds/31536000:.2f} 年"

def main():
    wallet_type = input("请选择要生成的钱包类型 (ETH/SUI): ").upper()
    while wallet_type not in ["ETH", "SUI"]:
        wallet_type = input("无效的选择。请输入 ETH 或 SUI: ").upper()

    prefix = input("请输入你想要的钱包地址前缀（不包括'0x'）：")
    suffix = input("请输入你想要的钱包地址后缀：")

    expected_attempts = calculate_search_space(prefix, suffix)
    print(f"程序已开始运行。预期需要尝试次数：{expected_attempts}")
    print(f"正在使用多进程查找指定前缀和后缀的{wallet_type}钱包地址。请耐心等待。")

    process_count = multiprocessing.cpu_count()
    queue = multiprocessing.Queue()
    counter = multiprocessing.Value('i', 0)
    processes = []

    start_time = time.time()
    for _ in range(process_count):
        p = multiprocessing.Process(target=worker, args=(wallet_type, prefix, suffix, queue, counter))
        processes.append(p)
        p.start()

    try:
        while queue.empty():
            time.sleep(1)  # Update every second
            elapsed_time = time.time() - start_time
            estimated_time = estimate_time(expected_attempts, counter.value, elapsed_time)
            formatted_time = format_time(estimated_time)
            print(f"\r已尝试 {counter.value} 次，当前速度：{counter.value/elapsed_time:.2f} 次/秒，预计还需 {formatted_time}", end='', flush=True)
    except KeyboardInterrupt:
        print("\n程序已被用户终止。")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        return

    result = queue.get()
    
    for p in processes:
        p.terminate()

    for p in processes:
        p.join()

    end_time = time.time()
    total_time = end_time - start_time
    
    address, private_key = result
    print(f"\n找到匹配的{wallet_type}钱包地址！")
    print(f"地址: {address}")
    print(f"私钥: {private_key}")
    print(f"用时: {format_time(total_time)}")
    print(f"总尝试次数: {counter.value}")

    with open('wallets.txt', 'a') as f:
        f.write(f"{wallet_type} Wallet found: Address: {address} Private key: {private_key}\n")

if __name__ == '__main__':
    main()
