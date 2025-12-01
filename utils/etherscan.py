import os
import requests
import json

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
if not ETHERSCAN_API_KEY:
    raise RuntimeError("No ETHERSCAN_API_KEY found in environment")

ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2"
ETHERSCAN_API_BASE_URL = f"{ETHERSCAN_BASE_URL}/api?apikey={ETHERSCAN_API_KEY}"


def get_gas_prices(chain_id: int) -> dict:
    url = f"{ETHERSCAN_API_BASE_URL}&chainid={chain_id}&module=gastracker&action=gasoracle"

    response = requests.get(url).json()
    if response.get("status") == "1" and response.get("message") == "OK":
        r = response["result"]
        return {
            "low": float(r["SafeGasPrice"]),
            "average": float(r["ProposeGasPrice"]),
            "high": float(r["FastGasPrice"]),
        }

    raise RuntimeError(f"Failed to fetch gas prices for chain id {chain_id}")


def get_native_token_price(chain_id: int) -> float:
    url = f"{ETHERSCAN_API_BASE_URL}&chainid={chain_id}&module=stats&action=ethprice"

    response = requests.get(url).json()
    if response.get("status") == "1" and response.get("message") == "OK":
        return float(response["result"]["ethusd"])

    raise RuntimeError(f"Failed to fetch native token price for chain id {chain_id}")


def calculate_gas_fee(chain_id: int, gas_price_gwei: float, gas_limit: int):
    eth_price = get_native_token_price(chain_id=chain_id)
    gas_fee_eth = (gas_price_gwei * gas_limit) / 1e9
    gas_fee_usd = gas_fee_eth * eth_price
    return gas_fee_eth, gas_fee_usd


def get_supported_chains_api():
    url = f"{ETHERSCAN_BASE_URL}/chainlist"

    response = requests.get(url).json()
    return response["result"]


def get_supported_chains(use_saved: bool = True):
    if use_saved:
        try:
            with open("chain_list.json", "r") as f:
                chain_list = json.load(f)
        except FileNotFoundError:
            return get_supported_chains_api()
        except Exception as e:
            raise e

        return chain_list

    return get_supported_chains_api()


def update_supported_chains():
    chain_list = get_supported_chains(use_saved=False)

    with open("chain_list.json", "w") as f:
        json.dump(chain_list, f)


def get_chain_name(chain_id: int) -> str:
    chain_id_str = str(chain_id)

    # First try using saved data
    try:
        chain_list = get_supported_chains(use_saved=True)
        for entry in chain_list:
            if str(entry.get("chainid")) == chain_id_str:
                return entry.get("chainname")
    except Exception:
        pass

    # Fallback: fetch live list
    try:
        chain_list = get_supported_chains(use_saved=False)
        for entry in chain_list:
            if str(entry.get("chainid")) == chain_id_str:
                return entry.get("chainname")
    except Exception:
        pass

    # Not found anywhere
    raise ValueError(f"Chain ID {chain_id} not found")
