from dotenv import load_dotenv
import argparse

load_dotenv()
from utils import etherscan


chain_list = etherscan.get_supported_chains()


def cli():
    parser = argparse.ArgumentParser(description="EVM gas fee calculator")
    parser.add_argument(
        "--chain-id",
        type=int,
        default=1,
        help="Chain id supported by Etherscan: https://docs.etherscan.io/supported-chains (default: 1)",
    )
    parser.add_argument(
        "--gas-limit",
        type=int,
        default=21000,
        help="Gas limit to use in cost calculation (default: 21000)",
    )
    parser.add_argument(
        "--level",
        type=str,
        choices=["low", "average", "high"],
        default=None,
        help="Show only one gas level instead of all",
    )

    args = parser.parse_args()

    gas_prices = etherscan.get_gas_prices(chain_id=args.chain_id)
    eth_price = etherscan.get_native_token_price(chain_id=args.chain_id)

    chain_name = etherscan.get_chain_name(chain_id=args.chain_id)
    print(f"{chain_name} Native Token Price: ${eth_price:.2f}")
    print("\nGas Prices (Gwei):")
    print(f"  Low: {gas_prices['low']}")
    print(f"  Average: {gas_prices['average']}")
    print(f"  High: {gas_prices['high']}")

    print(f"\nGas costs in ETH and USD for {args.gas_limit} gas")

    levels = [args.level] if args.level else ["low", "average", "high"]

    for level in levels:
        fee_eth, fee_usd = etherscan.calculate_gas_fee(
            chain_id=args.chain_id,
            gas_price_gwei=gas_prices[level],
            gas_limit=args.gas_limit,
        )
        print(f"{level.capitalize()} gas cost: {fee_eth:.8f} ETH (${fee_usd:.4f})")


if __name__ == "__main__":
    cli()
