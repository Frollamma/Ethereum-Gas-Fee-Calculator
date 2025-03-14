# Ethereum Gas Fee Calculator

Ethereum Gas Fee Calculator is a simple Python script that fetches real-time gas prices and estimates the transaction cost in USD. It utilizes the Etherscan API for gas prices and the CoinGecko API for ETH price conversion.

## Features
- Fetches real-time gas prices (Low, Average, High)
- Calculates transaction cost for standard transfers
- Converts ETH gas fees to USD
- CLI-based for easy usage

## Installation   
1. Clone the repository:   
   ```bash 
   git clone https://github.com/yourusername/ethereum-gas-calculator.git
   cd ethereum-gas-calculator
   ```   
2. Install dependencies:  
   ```bash   
   pip install requests 
   ```

## Usage
1. Get your free API key from [Etherscan](https://etherscan.io/apis)
2. Replace `YOUR_ETHERSCAN_API_KEY` in the script with your key
3. Run the script:
   ```bash
   python ethereum_gas_calculator.py
   ```

## Example Output
```
Ethereum Price: $3,200.50
Gas Prices (Gwei):
  Low: 25 Gwei
  Average: 30 Gwei
  High: 45 Gwei
Estimated cost for low gas: 0.000525 ETH ($1.68)
Estimated cost for average gas: 0.000630 ETH ($2.02)
Estimated cost for high gas: 0.000945 ETH ($3.03)
```

## License
This project is licensed under the MIT License.

