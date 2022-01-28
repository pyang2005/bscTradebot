import time, sys
from web3 import Web3
from web3.middleware import geth_poa_middleware

address = '0x63Ec72008ac179E2CC1e652bDaCfE59772434085'       # Account need to monitor..... 
key     = 'Your Secret Key'  # private key of the address

gas          = 500000    # 设置 gas， 建议高出一般转账
gasPrice     = 10        # 设置 gasPrice ， 建议高出一般转账 
back_address = 'Backup address'  # Safe Account. 


def tt2time(timestamp):
    time_local = time.localtime(timestamp)                         #转换为localtime
    res        = time.strftime("%Y-%m-%d %H:%M:%S",time_local)     #转换为新的时间格式
    return res


def main(argv=None):

    w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org:443"))
    if not w3.isConnected():
        print("web3未连接")
        return

    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # 注入POA中间件

    prev_number = 0               # 上一个区块 
    while True:
        try:
            block = w3.eth.get_block('latest') 
            
            current_number = block['number']
            if current_number > prev_number:        # 此区块为新区块 立即处理。。。。。
                prev_number = current_number  
                print("[MSG]:", tt2time(time.time()), '---> Block Number: ', block['number'])

                # for tx in block['transactions']:      # 在区块中寻中和监控账号相关的 账号， from 为主。  
                #     res = w3.eth.getTransaction(tx)
                #     print(res['from'])                # 获取 from 的账号， 
                # # 该循环相当耗时， 需要使用多线程处理，看能否处理的过来， 一般一个区块1-3s， 但处理该过程需要100多秒。

                balance = w3.eth.get_balance(address)           # 获取 需拯救账号的 bnb余额 
                nonce = w3.eth.getTransactionCount(address)     # 获取 需拯救账号的 nonce 值
                # gasvalue  = w3.toWei(gasPrice, 'gwei') * gas          # 转还需要使用的gas， 用余额 减去， 即为需转账的余额 

                print("[MSG]: Your balance = {}, Nonce = {} .".format(w3.fromWei(balance,'ether'), nonce))

                if w3.fromWei(balance,'ether') > 0.0001 :     ## BNB 余额 大于 0 ， 立即转走！
                    tx = {
                        'nonce'     : nonce,
                        'to'        : back_address,
                        'value'     : balance - w3.toWei(gasPrice, 'gwei') * gas, 
                        'gas'       : gas,
                        'gasPrice'   : w3.toWei(gasPrice, 'gwei')
                    }

                    signed_tx = w3.eth.account.sign_transaction(tx, private_key=key)  # 转账签名 
                    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)     # 执行转账
                    print(w3.toHex(tx_hash))              # 打印执行的 tx Hash     
                    result = w3.eth.wait_for_transaction_receipt(w3.toHex(tx_hash), 20, poll_latency=1)
                    print("[MSG]: 转账成功！") if result["status"] else print("[MSG]: 转账失败！")
                else:
                    print("[MSG]: Balance is less than 0.0001 ...")
                    pass

                print("\n\r")
            else :                             # 没有新区块 不处理。
                time.sleep(1)
                pass

        except Exception as e:
            time.sleep(1)
            print("Error: {}".format(e))


if __name__ == '__main__':
    main()
