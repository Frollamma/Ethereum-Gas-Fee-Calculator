import os
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
if not ETHERSCAN_API_KEY:
    raise RuntimeError("No ETHERSCAN_API_KEY found in environment")

ETHERSCAN_BASE_PATH = (
    f"https://api.etherscan.io/v2/api?chainid=1&apikey={ETHERSCAN_API_KEY}"
)


def get_gas_prices() -> dict:
    url = f"{ETHERSCAN_BASE_PATH}&module=gastracker&action=gasoracle"

    response = requests.get(url).json()
    if response.get("status") == "1" and response.get("message") == "OK":
        r = response["result"]
        return {
            "low": float(r["SafeGasPrice"]),
            "average": float(r["ProposeGasPrice"]),
            "high": float(r["FastGasPrice"]),
        }

    raise RuntimeError("Failed to fetch gas prices")


def get_eth_price() -> float:
    url = f"{ETHERSCAN_BASE_PATH}&module=stats&action=ethprice"

    response = requests.get(url).json()
    if response.get("status") == "1" and response.get("message") == "OK":
        return float(response["result"]["ethusd"])

    raise RuntimeError("Failed to fetch gas prices")


def calculate_gas_fee(gas_price_gwei: float, gas_limit: int):
    eth_price = get_eth_price()
    gas_fee_eth = (gas_price_gwei * gas_limit) / 1e9
    gas_fee_usd = gas_fee_eth * eth_price
    return gas_fee_eth, gas_fee_usd


def cli():
    parser = argparse.ArgumentParser(description="Ethereum gas fee calculator")
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

    if not ETHERSCAN_API_KEY:
        raise EnvironmentError("ETHERSCAN_API_KEY missing in .env")

    gas_prices = get_gas_prices()
    eth_price = get_eth_price()

    print(f"Ethereum Price: ${eth_price:.2f}")
    print("\nGas Prices (Gwei):")
    print(f"  Low: {gas_prices['low']}")
    print(f"  Average: {gas_prices['average']}")
    print(f"  High: {gas_prices['high']}")

    print(f"\nGas costs in ETH and USD for {args.gas_limit} gas")

    levels = [args.level] if args.level else ["low", "average", "high"]

    for level in levels:
        fee_eth, fee_usd = calculate_gas_fee(gas_prices[level], args.gas_limit)
        print(f"{level.capitalize()} gas cost: {fee_eth:.6f} ETH (${fee_usd:.4f})")


if __name__ == "__main__":
    cli()
