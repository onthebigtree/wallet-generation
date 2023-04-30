from web3 import Web3

INFURA_API_KEY = "YOUR_INFURA_API_KEY"
INFURA_URL = f'https://mainnet.infura.io/v3/{INFURA_API_KEY}' #这里是你的INFURA API KEY
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def get_balance(address):
    balance = w3.eth.getBalance(address)
    return w3.from_Wei(balance, 'ether')

def main():
    with open('check_balances_keys.txt', 'r') as file: #这里是你的私钥存放文件
        keys = file.readlines()
        keys = [key.strip() for key in keys]

    for key in keys:
        private_key = key
        account = w3.eth.account.privateKeyToAccount(private_key)
        address = account.address
        balance = get_balance(address)
        print(f'地址: {address} 余额: {balance} ETH')

if __name__ == '__main__':
    main()
