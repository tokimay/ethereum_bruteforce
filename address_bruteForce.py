
# This file is part of https://github.com/tokimay/ethereum_bruteforce
# Copyright (C) 2016 https://github.com/tokimay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# This software is licensed under GPLv3. If you use or modify this project,
# you must include a reference to the original repository: https://github.com/tokimay/ethereum_bruteforce

import secrets
import web3
from sha3 import keccak_256
from coincurve import PublicKey
from web3 import Web3

balance = 0
addLst = []
fileCounter = 1
temCounter = 0

while balance == 0:
    private_key = keccak_256(secrets.token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]
    print('private_key:', private_key.hex())
    print('public_key: ', public_key.hex())
  
    address_cksm = Web3.to_checksum_address(addr.hex())
    print('eth check sum addr: ', address_cksm)
  
    w3 = web3.Web3(web3.HTTPProvider('https://nodes.mewapi.io/rpc/eth'))
    balance = w3.eth.get_balance(address_cksm)
    print('balance: ', balance)
  
    addLst.append({'Address': str(addr.hex()),
                   'public_key': str(public_key.hex()),
                   'private_key': str(private_key.hex())})
  
    if len(addLst) >= 1000:
        temCounter = len(addLst) + temCounter
        if temCounter >= 100000:
            fileCounter = fileCounter + 1
            temCounter = 0
        with open('Address_list_' + str(fileCounter) + '.txt', 'a') as fp:
            for ad in addLst:
                fp.write(f"{ad}\n")
        addLst.clear()

    if balance > 0:
        file = open('ETH_None_Zero_balance.txt', 'a')
        file.write('private_key:\n')
        file.write(str(private_key.hex()) + '\n')

        file.write('public_key:\n')
        file.write(str(public_key.hex()) + '\n')

        file.write('addr.hex():\n')
        file.write(str(addr.hex()) + '\n')

        file.write('address_cksm:\n')
        file.write(str(address_cksm) + '\n')

        file.write('balance:\n')
        file.write(str(balance))

        file.close()

