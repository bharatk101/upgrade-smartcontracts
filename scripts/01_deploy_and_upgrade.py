from scripts.helpful_scripts import get_account, encode_fun_data, upgrade
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, BoxV2


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account}, publish_source=True)
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    #  we dont have constructor but if requiree we can use initializer function
    # call a function and pass the value for ex box.store with 1 but first we have to encode it
    # pass that as a param(_data) in Proxy constructor
    # initializer = box.store, 1
    box_encoded_init_func = encode_fun_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_init_func, {
                                               "from": account, "gas_minit": 1000000}, publish_source=True)
    print(f"proxy deployed to {proxy}, now upgrade to V2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})

    # deploy upgraded contract
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    # upgrade proxy
    upgrade_tx = upgrade(account=account, proxy=proxy,
                         new_implementation_Add=box_v2.address, proxy_admin_contract=proxy_admin)
    upgrade_tx.wait(1)
    print("Procy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrive())
