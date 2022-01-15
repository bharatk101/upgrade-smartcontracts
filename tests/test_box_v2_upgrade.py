from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract, exceptions
from scripts.helpful_scripts import encode_fun_data, get_account, upgrade
import pytest


def test_proxy_upgrade():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encode_init_fun = encode_fun_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encode_init_fun, {
                                               "from": account, "gas_limit": 1000000})
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    assert proxy_box.retrive() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrive() == 1
