import streamlit as st
from web3 import Web3
import json

st.set_page_config(page_title="GBT Network Bridge", layout="centered")

# === Embedded ABIs ===
BRIDGE_L1_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"}
        ],
        "name": "depositToL2",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

BRIDGE_L2_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "mintFromL1",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

wallet_connect_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Connect Wallet</title>
  <script src="https://cdn.jsdelivr.net/npm/web3@1.10.0/dist/web3.min.js"></script>
</head>
<body>
  <button onclick="connectWallet()">Connect MetaMask</button>
  <p id="wallet-address"></p>

  <script>
    async function connectWallet() {
      if (window.ethereum) {
        try {
          const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
          document.getElementById('wallet-address').innerText = 'Connected: ' + accounts[0];
        } catch (err) {
          console.error('User rejected connection:', err);
        }
      } else {
        alert('MetaMask not found!');
      }
    }
  </script>
</body>
</html>
"""

# === GBTNetwork UI ===
st.title("🌉 GBT Bridge (Layer 1 ⇄ Layer 2)")

st.subheader("🔌 RPC Connection")
rpc_url = st.text_input("GBT RPC URL", "http://localhost:8545")
bridge_l1_address = st.text_input("Bridge L1 Contract Address", "0xYourL1Address")
bridge_l2_address = st.text_input("Bridge L2 Contract Address", "0xYourL2Address")

connect = st.button("Connect to GBTNetwork")

if connect:
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            st.success("✅ Connected to GBTNetwork")
            bridge_l1 = w3.eth.contract(address=bridge_l1_address, abi=BRIDGE_L1_ABI)
            bridge_l2 = w3.eth.contract(address=bridge_l2_address, abi=BRIDGE_L2_ABI)
        else:
            st.error("❌ Failed to connect to RPC.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# === Bridge Operations ===
st.subheader("🔁 Bridge Operations")
wallet_address = st.text_input("Your Wallet Address", "")
amount = st.number_input("Amount (GBT)", min_value=0.0)

col1, col2 = st.columns(2)
with col1:
    if st.button("Deposit to Layer 2"):
        try:
            tx = bridge_l1.functions.depositToL2(wallet_address).build_transaction({
                'from': wallet_address,
                'value': w3.to_wei(amount, 'ether'),
                'gas': 2000000,
                'nonce': w3.eth.get_transaction_count(wallet_address)
            })
            st.success("✅ Transaction built. Sign it with MetaMask or wallet.")
            st.json(tx)
        except Exception as e:
            st.error(f"❌ Deposit failed: {str(e)}")

with col2:
    if st.button("Mint on Layer 2"):
        try:
            tx = bridge_l2.functions.mintFromL1(wallet_address, int(amount)).build_transaction({
                'from': wallet_address,
                'gas': 2000000,
                'nonce': w3.eth.get_transaction_count(wallet_address)
            })
            st.success("✅ Mint transaction built.")
            st.json(tx)
        except Exception as e:
            st.error(f"❌ Mint failed: {str(e)}")

# === WalletConnect HTML Preview ===
st.subheader("🧩 Wallet Connect Code")
with st.expander("Click to show HTML"):
    st.code(wallet_connect_html, language='html')

# === Footer ===
st.markdown("---")
st.markdown("🌐 **GBTNetwork Bridge App** — Layer 1 ⇄ Layer 2 Token Transporter (v1.0)")
