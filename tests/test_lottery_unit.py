# 0.0022
# 2200000000000000

from brownie import Lottery, accounts, config, network, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account, get_contract
from scripts.deploy_lottery import deploy_lottery, start 
from web3 import Web3
import pytest


def test_getEntranceFee():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery_obj= deploy_lottery()
    #Act
    Entrance_fee= lottery_obj.getEntranceFee()
    #Assert
    assert Entrance_fee == Web3.toWei(0.00262 ,"ether")



def test_cant_enter_unless_started():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / Assert
    with pytest.raises(AttributeError):
        lottery.Enter({"from": get_account(), "value": lottery.getEntranceFee()+100000000})

def test_start():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery_obj= deploy_lottery()
    account=get_account()
    lottery_obj.StartLottery({"from": account})
    assert lottery_obj.lottery_state() == 0

def test_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery_obj= deploy_lottery()
    account=get_account()
    lottery_obj.StartLottery({"from": account})
    lottery_obj.Enter({"from": account, "value" : lottery_obj.getEntranceFee()+1000000})
    assert lottery_obj.players(0) == account

def test_stop():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery_obj= deploy_lottery()
    account=get_account()
    lottery_obj.StartLottery({"from": account})
    lottery_obj.Enter({"from": account, "value" : lottery_obj.getEntranceFee()+100000000})
    fund_with_link(lottery_obj.address)
    lottery_obj.StopLottery({"from" : account})
    assert lottery_obj.lottery_state() == 2

def test_calculating_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery_obj=deploy_lottery()
    account=get_account()
    lottery_obj.StartLottery({"from":account})
    lottery_obj.Enter({"from": account, "value" : lottery_obj.getEntranceFee()+100000000})
    lottery_obj.Enter({"from": get_account(index=1), "value" : lottery_obj.getEntranceFee()+100000000})
    lottery_obj.Enter({"from": get_account(index=2), "value" : lottery_obj.getEntranceFee()+100000000})
    fund_with_link(lottery_obj.address)
    initial_balance= account.balance()
    contract_balance= lottery_obj.balance()
    tx=lottery_obj.StopLottery({"from" : account})
    STATIC_ABC= 777
    request_id=tx.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(request_id,STATIC_ABC, lottery_obj.address)
    
    assert lottery_obj.recentWinner() == account
    assert account.balance() == initial_balance+ contract_balance
    assert lottery_obj.balance() ==0


    

        
    