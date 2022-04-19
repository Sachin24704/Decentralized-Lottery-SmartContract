from brownie import Lottery, network
import time, pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link
from scripts.deploy_lottery import deploy_lottery

def test_lottery():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS :
        pytest.skip()
    lottery_obj=deploy_lottery()
    account=get_account()
    lottery_obj.StartLottery({"from":account})
    lottery_obj.Enter({"from": account, "value" : lottery_obj.getEntranceFee()+100000000})
    lottery_obj.Enter({"from": account, "value" : lottery_obj.getEntranceFee()+100000000})
    fund_with_link(lottery_obj.address)
    lottery_obj.StopLottery({"from": account})
    time.sleep(180)
    assert lottery_obj.recentWinner() == account
    assert lottery_obj.balance() ==0
    
