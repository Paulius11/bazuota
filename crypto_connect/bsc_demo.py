from bazuota.crypto_connect import CryptoNetworkConnector

def main():
    n = CryptoNetworkConnector(testnet=False)
    # n.get_abi("0x2859e4544c4bb03966803b044a93563bd2d0dd4d")  # Mainnet
    n.get_bnb_price()
    # fak = n.get_factory()
    fak = n._get_pair_address("0x6e0bef56b648b3eebae3808b8cbe7efe8755ad9c", base_currency=n.wbnb)
    price = n.get_price_bnb("0x6e0bef56b648b3eebae3808b8cbe7efe8755ad9c", base_currency=n.wbnb)


if __name__ == "__main__":
    version = 1.0
    main()
