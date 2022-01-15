from scripts.helpful_scripts import encode_fun_data, get_account
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract

def test_proxy_deligates_calls():
    account = get_account()
    box = Box.deploy({"from":account})
    proxy_admin = ProxyAdmin.deploy({"from":account})
    box_encoded_init_func = encode_fun_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_init_func, {"from":account, "gas_limit":1000000})
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrive()==0
    proxy_box.store(1,{"from":account})
    assert proxy_box.retrive() == 1
