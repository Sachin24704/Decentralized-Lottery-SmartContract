from unicodedata import decimal
from brownie import network, accounts, config, Contract, MockV3Aggregator, VRFCoordinatorMock, LinkToken


FORKED_LOCAL_ENVIRONMENT =["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS =["development", "ganache-local"]

def get_account(index = None, id= None) :
    #testnet
    #local network
    #forcked network
    if index:
        return accounts[index]
    if id :
        return accounts[id]
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENT):
        return accounts[0]
    else :
        return accounts.add(config["wallets"]["from_key"])


contract_to_mock ={"eth_usd_price_feed" : MockV3Aggregator , #"inr_usd_price_feed"  : MockV3Aggregator, 
"vrf_coordinator": VRFCoordinatorMock, "link_token" : LinkToken}

# grab contract address from config if defined otherwise deploy mocks 
def get_contract(contract_name):
    contract_type=contract_to_mock[contract_name]
    if network.show_active()  in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        
        if(len(contract_type) <=0) :
           deploy_mocks()
        if(contract_name == "eth_usd_price_feed" ):
            contract=contract_type[0]
        else:
            contract= contract_type[-1] 
        return contract
        
    else :
        contract_address= config["networks"][network.show_active()][contract_name]
        contract=Contract.from_abi(contract_type._name , contract_address , contract_type.abi)
        return contract

DECIMALS = 8
INITIAL_VALUE = 250000000000
INITIAL_VALUE2= 1310000

def deploy_mocks(decimals=DECIMALS, initial_value= INITIAL_VALUE, initial_value2= INITIAL_VALUE2):
    account= get_account()
    MockV3Aggregator.deploy(decimals , initial_value, {"from": account})
    #MockV3Aggregator.deploy(decimals, initial_value2,{"from": account})
    link_token_obj= LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token_obj.address,{"from": account})

    print("deployed")

def fund_with_link(contract_address, account= None, link_token=None , fee= 300000000000000000)  :#0.1 link
    account= account if account else get_account()
    link_token= link_token if link_token else get_contract("link_token") # link_token_obj
    tx=link_token.transfer(contract_address, fee, {"from" : account})
    tx.wait(1)
    return tx
