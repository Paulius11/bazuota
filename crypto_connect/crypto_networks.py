import json
import logging
import os
from decimal import Decimal
from enum import Enum
from os import path

import requests
from dotenv import dotenv_values
from eth_typing import ChecksumAddress
from web3 import Web3

ETHER = 10 ** 18
RUNNER_PATH = os.getcwd()
THIS_PATH = path.abspath(path.dirname(__file__))

file_network_path = path.join(THIS_PATH, ".network")
config_network = dotenv_values(file_network_path)
file_env_path = path.join(RUNNER_PATH, ".env")
config_private = dotenv_values(file_env_path)

if not os.path.exists(file_network_path): raise ValueError(f'.network file not found in {file_network_path}')
if not os.path.exists(file_env_path):
    logging.warning(f'.env file not found in working dir\n'
                 f'BSC_MAINNET_BLOCK_EXPLORER_API_KEY is recomended')

BSC_MAINNET = config_network.get("BSC_MAINNET")

BSC_MAINNET_CHAIN_ID = config_network.get("BSC_CHAIN_ID")
BSC_MAINNET_WBMB = config_network.get("PANKAKE_WBNB_MAINNET")
BSC_MAINNET_BUSD = config_network.get("PANKAKE_BUSD_ADDRESS")
BSC_MAINNET_FACTORY = config_network.get("PANKAKE_FACTORY_V2_MAINNET")
BSC_MAINNET_ROUTER = config_network.get("PANKAKE_ROUTER_V2_MAINNET")
# API
BSC_MAINNET_EXPLORER_API_URL = config_network.get("BSC_MAINNET_BLOCK_EXPLORER_API")
BSC_MAINNET_EXPLORER_API_KEY = config_private.get("BSC_MAINNET_BLOCK_EXPLORER_API_KEY")

BSC_TESTNET = config_network.get("BSC_TESTNET")
BSC_TESTNET_CHAIN_ID = config_network.get("BSC_CHAIN_ID_TEST")
BSC_TESTNET_WBMB = config_network.get("PANKAKESWAP_WBNB_TESTNET")
BSC_TESTNET_BUSD = config_network.get("PANKAKE_BUSD_ADDRESS_TEST")
BSC_TESTNET_FACTORY = config_network.get("PANKAKE_FACTORY_V2_TESTNET")
BSC_TESTNET_ROUTER = config_network.get("PANKAKE_ROUTER_V2_TESTNET")
# API
BSC_TESTNET_BLOCK_EXPLORER_API_URL = config_network.get("BSC_TESTNET_BLOCK_EXPLORER_API")
BSC_TESTNET_BLOCK_EXPLORER_API_KEY = config_private.get("BSC_TESTNET_BLOCK_EXPLORER_API_KEY")

NETWORKS = config_network

ABI_FACTORY = json.loads(
    '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

ABI_ROUTER = json.loads(
    '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')

ABI_TOKEN = json.loads(
    '[ { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "spender", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": false, "internalType": "uint256", "name": "value", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "_owner", "type": "address" }, { "internalType": "address", "name": "spender", "type": "address" } ], "name": "allowance", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "spender", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "approve", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "internalType": "address", "name": "account", "type": "address" } ], "name": "balanceOf", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "decimals", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getOwner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "name", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "symbol", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "totalSupply", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transfer", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "recipient", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" } ], "name": "transferFrom", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" } ]')

ABI_FACTORY_PAIR = json.loads(
    '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
)


class Network(Enum):
    BSC_MAINNET = 56
    BSC_TESTNET = 97


def check_address(contract_address):
    """Checks address"""
    return Web3.toChecksumAddress(contract_address)


class CryptoNetworkConnector:
    """
    Automatically connect to testnet or mainet
    """

    def __init__(self, network: Network, just_print=False):
        self.selected_network = network

        if network == Network.BSC_TESTNET:
            messege = "Running BSC testnet..."
            self.network = BSC_TESTNET
            self.wbnb: ChecksumAddress = check_address(BSC_TESTNET_WBMB)
            self.busd: ChecksumAddress = check_address(BSC_TESTNET_BUSD)
            self.factory_address: ChecksumAddress = check_address(BSC_TESTNET_FACTORY)
            self.router_address: ChecksumAddress = check_address(BSC_TESTNET_ROUTER)
            self.gas = '10'
            self.chain = int(BSC_TESTNET_CHAIN_ID)
            self.explorer_api_url = BSC_TESTNET_BLOCK_EXPLORER_API_URL
            self.explorer_url = "https://testnet.bscscan.com/"
            self.automate_market_maker = "https://pancake.kiemtienonline360.com/"
            print("Faucet  : https://testnet.binance.org/faucet-smart")

        if network == Network.BSC_MAINNET:
            messege = "Running BSC mainnet..."
            self.network = BSC_MAINNET
            self.wbnb: ChecksumAddress = check_address(BSC_MAINNET_WBMB)
            self.busd: ChecksumAddress = check_address(BSC_MAINNET_BUSD)
            self.factory_address: ChecksumAddress = check_address(BSC_MAINNET_FACTORY)
            self.router_address: ChecksumAddress = check_address(BSC_MAINNET_ROUTER)
            self.gas = '5'
            self.chain = int(BSC_MAINNET_CHAIN_ID)
            self.explorer_api_url = BSC_MAINNET_EXPLORER_API_URL
            self.explorer_api_key = BSC_MAINNET_EXPLORER_API_KEY
            self.explorer_url = "https://bscscan.com/"
            self.automate_market_maker = "https://pancakeswap.finance/"

        print(messege)
        print(f'Network  : {self.network}')
        print(f'WBNB     : {self.wbnb}')
        print(f'BUST     : {self.busd}')
        print(f'FACTORY  : {self.factory_address}')
        print(f'ROUTER   : {self.router_address}')
        print(f'GAS      : {self.gas}')
        print(f'CHAIN ID : {self.chain}')
        print(f'API      : {self.explorer_api_url}')
        print(f'EXPLORER : {self.explorer_url}')
        print(f'AMM      : {self.automate_market_maker}')
        if just_print: SystemExit
        self.web3 = self.init_web3()

    def get_web3(self):
        return self.web3

    def init_web3(self):
        self.web3 = Web3(Web3.HTTPProvider(self.network))
        print(f'Connected: {self.web3.isConnected()}')
        return self.web3

    def get_factory(self):
        "Get factory object"
        return self.web3.eth.contract(address=self.factory_address, abi=ABI_FACTORY)

    def get_router(self):
        "Get factory object"
        return self.web3.eth.contract(address=self.router_address, abi=ABI_ROUTER)

    def _get_pair_address(self, contract_address, base_currency: ChecksumAddress):
        pair_address = self.get_factory().functions.getPair(base_currency, check_address(contract_address)).call()
        pair_check = check_address(pair_address)
        return pair_address

    def __get_price(self, token, decimals, pair_contract, is_reversed, is_price_in_peg):
        peg_reserve = 0
        token_reserve = 0
        (reserve0, reserve1, blockTimestampLast) = pair_contract.functions.getReserves().call()

        if is_reversed:
            peg_reserve = reserve0
            token_reserve = reserve1
        else:
            peg_reserve = reserve1
            token_reserve = reserve0

        if token_reserve and peg_reserve:
            if is_price_in_peg:
                # CALCULATE PRICE BY TOKEN PER PEG
                price = (Decimal(token_reserve) / 10 ** decimals) / (Decimal(peg_reserve) / ETHER)
            else:
                # CALCULATE PRICE BY PEG PER TOKEN
                price = (Decimal(peg_reserve) / ETHER) / (Decimal(token_reserve) / 10 ** decimals)

            return price

        return Decimal('0')

    def get_price_in_dollars(self, custom_token, base_currency):
        """
        Get price in usdt
        :param custom_token: token you want to check
        :return: price in $
        """

        custom_token_checked = check_address(custom_token)

        pair = self._get_pair_address(contract_address=custom_token, base_currency=base_currency)
        if pair == '0x0000000000000000000000000000000000000000':
            return
        pair_contract = self.web3.eth.contract(address=pair, abi=ABI_FACTORY_PAIR)
        is_reversed = pair_contract.functions.token0().call().lower() == base_currency.lower()
        decimals, token_name, token_symbol = self.get_token_data(custom_token_checked)
        is_price_in_peg = False
        price = self.__get_price(custom_token_checked, decimals, pair_contract, is_reversed, is_price_in_peg)
        print(f'Token price: {price} {token_name} {token_symbol}')
        return price

    def get_token_data(self, custom_token_checked):
        "Get generic token data"
        decimals = self.web3.eth.contract(address=custom_token_checked, abi=ABI_TOKEN).functions.decimals().call()
        token_name = self.web3.eth.contract(address=custom_token_checked, abi=ABI_TOKEN).functions.name().call()
        token_symbol = self.web3.eth.contract(address=custom_token_checked, abi=ABI_TOKEN).functions.symbol().call()
        return decimals, token_name, token_symbol

    def get_abi_web(self, contract_address):
        """ Works in bsc mainet not testnet"""


        url = self.explorer_api_url + "/api?module=contract&action=getabi&address=" + contract_address

        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'Connection': "keep-alive",
            'Upgrade-Insecure-Requests': "1",
            'Sec-Fetch-Dest': "document",
            'Sec-Fetch-Mode': "navigate",
            'Sec-Fetch-Site': "none",
            'Sec-Fetch-User': "?1",
            'Cache-Control': "max-age=0",
        }

        response = requests.get(url, headers)
        if response.ok:
            response_json = response.json()
            abi_json = json.loads(response_json['result'])
            # result = json.dumps({"abi": abi_json}, indent=4, sort_keys=True)
            result = json.dumps({"abi": abi_json})
            open('.tmpABI', 'w').write(result),
            assert response_json.get("result"), "Can't receive remote ABI"
            return json.loads(response_json.get("result"))
        else:
            print(f"Bad response {response.status_code}")
            return False

    def get_bnb_price(self):
        try:
            if self.selected_network == Network.BSC_MAINNET:
                bnbPrice = requests.get(
                    self.explorer_api_url + "/api?module=stats&action=bnbprice&apikey=" + self.explorer_api_key)
                price = bnbPrice.json()['result']['ethusd']
                print(f"BNB: {price} USD")
            if self.selected_network == Network.BSC_TESTNET:
                print("Skipping BNB check....")
                return

        except TypeError:
            raise "Please add 'BSC_MAINNET_EXPLORER_API_KEY' api in .evn "
        return price

    def print_transaction_link(self, transaction_hash):
        base_url = "https://bscscan.com/"
        if self.selected_network == Network.BSC_TESTNET:
            base_url = "https://testnet.bscscan.com/"
        print(f'Transaction: {base_url}/tx/{transaction_hash}')

    def print_detected_transaction(self, address):
        base_url = "https://bscscan.com"
        if self.selected_network == Network.BSC_TESTNET:
            base_url = "https://testnet.bscscan.com"
        print(f'Created token: {base_url}/address/{address}')
        print(f'Token        : {base_url}/token/{address}')

    def print_charts(self, address):
        print(f'Charts       :  https://poocoin.app/tokens/{address}')


    def print_pair(self, pair_tx):
        base_url = "https://bscscan.com"
        if self.selected_network == Network.BSC_TESTNET:
            base_url = "https://testnet.bscscan.com"
        print(f'LP Pair: {base_url}/address/{pair_tx}')

    def print_verify_link(self, created_contract_address):
        base_url = "https://bscscan.com"
        if self.selected_network == Network.BSC_TESTNET:
            base_url = "https://testnet.bscscan.com"
        print(f'Verify@: {base_url}/verifyContract?a={created_contract_address}')


def main():
    network = Network.BSC_MAINNET
    bsc_testnet_address_random = "0x0ee1fb06ca68c4ef9f5350493d14bac6359ffd23"
    bsc_mainet_address_rubic = "0x8E3BCC334657560253B83f08331d85267316e08a"
    if network == Network.BSC_TESTNET:
        address = bsc_testnet_address_random
    if network == Network.BSC_MAINNET:
        address = bsc_mainet_address_rubic

    print(f"Quering: {address}")
    n = CryptoNetworkConnector(network)
    #n.get_bnb_price()
    # faktory = n.get_factory()
    # pari_address = n._get_pair_address(address, base_currency=n.wbnb)
    # price = n.get_price_in_dollars("0x6e0bef56b648b3eebae3808b8cbe7efe8755ad9c", base_currency=n.wbnb) #Mainet
    #price = n.get_price_in_dollars(address, base_currency=n.wbnb)  # Testnet
    a = n.get_abi_web(address)

    print("test")


if __name__ == "__main__":
    version = 1.0
    main()
