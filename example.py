from tradePancake import Trade
from web3 import Web3
import time


w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org:443"))
if not w3.isConnected():
	print("[Error] Web3 connect failed! ")
	exit(0)

t = Trade(w3=w3, 
	tradeToken=' Contract which you want to trade .', 
	# withToken='0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56', # BUSD  ,default is WBNB
	walletAddr='Your Wallet Address',
	privateKey='Your Wallet private key')

print('\n\r')
print('-----------------------')

# buy token with WBNB amount . 
# t.buyToken(0.02, slippage=2)  # Caution: this amount is WBNB to sell.
t.buyToken(0.02)

time.sleep(20)

# sell token amount. 
t.sellToken(20)
# t.sellToken(20, slippage=2)

