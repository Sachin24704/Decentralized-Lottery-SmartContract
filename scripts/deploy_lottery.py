# 0.0022
# 2200000000000000

from brownie import Lottery, accounts, config, network
from scripts.helpful_scripts import get_account, get_contract, fund_with_link
import time


def deploy_lottery() :
    account= get_account()
    lottery_obj= Lottery.deploy(get_contract("eth_usd_price_feed").address, #get_contract("inr_usd_price_feed").address,
    get_contract("vrf_coordinator").address,
    get_contract("link_token").address, config["networks"][network.show_active()]["fee"],
    config["networks"][network.show_active()]["keyhash"], {"from": account}, 
    publish_source =config["networks"][network.show_active()].get("verify", False) 
    )
    
    print("Deployed Lottery")
    return lottery_obj
    
def start():
    account=get_account()
    lottery_obj=Lottery[-1]
    tx=lottery_obj.StartLottery({"from": account})
    tx.wait(1)
    print("Lottery has started")

def Enter_lottery():
    account=get_account()
    lottery_obj=Lottery[-1]
    value= lottery_obj.getEntranceFee() + 100000000
    tx=lottery_obj.Enter({"from": account, "value": value} )
    tx.wait(1)
    print("Entered Lottery")

def end_lottery():
    account= get_account()
    lottery_obj=Lottery[-1]
    #fund the contract with link
    tx1=fund_with_link(lottery_obj.address)
    tx1.wait(1)
    tx=lottery_obj.StopLottery({"from": account})
    tx.wait(1)
    # the chainlink node will take time to return randomness
    time.sleep(180)
    Winner= lottery_obj.recentWinner()
    print(f"{Winner} is the new Winner !!")




def main():
    deploy_lottery()
    start()
    Enter_lottery()
    end_lottery()