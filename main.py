import requests

# API keys (replace with your own)
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

# Function to get real-time gas prices from Etherscan
def get_gas_prices():
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url).json()
    if response["status"] == "1":
        return {
            "low": int(response["result"]["SafeGasPrice"]),
            "average": int(response["result"]["ProposeGasPrice"]),
            "high": int(response["result"]["FastGasPrice"])
        }
    else:
        raise Exception("Failed to fetch gas prices")

# Function to get ETH price in USD
def get_eth_price():
    response = requests.get(COINGECKO_API_URL).json()
    return response["ethereum"]["usd"]

# Function to calculate transaction cost
def calculate_gas_fee(gas_price_gwei, gas_limit=21000):
    eth_price = get_eth_price()
    gas_fee_eth = (gas_price_gwei * gas_limit) / 1e9
    gas_fee_usd = gas_fee_eth * eth_price
    return gas_fee_eth, gas_fee_usd

if __name__ == "__main__":
    gas_prices = get_gas_prices()
    eth_price = get_eth_price()
    
    print(f"Ethereum Price: ${eth_price:.2f}")
    print("Gas Prices (Gwei):")
    print(f"  Low: {gas_prices['low']} Gwei")
    print(f"  Average: {gas_prices['average']} Gwei")
    print(f"  High: {gas_prices['high']} Gwei")
    
    for level in ["low", "average", "high"]:
        gas_fee_eth, gas_fee_usd = calculate_gas_fee(gas_prices[level])
        print(f"Estimated cost for {level} gas: {gas_fee_eth:.6f} ETH (${gas_fee_usd:.2f})")
