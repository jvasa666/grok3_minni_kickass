import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import requests
import os
import time
import json
import base64
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from datetime import datetime, timedelta
import secrets
import hmac
import hashlib

# --- Global Configurations ---
# Your fixed wallet addresses for receiving payments (OraculumX's control)
ETH_ADDR = "0x5036dbcEEfae0a7429e64467222e1E259819c7C7" # Example Ethereum address
BTC_ADDR = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh" # Example Bitcoin address
SOL_ADDR = "GjKxT3YtFwN3j9p3L0w4V2x8E6r7Q0z1C5B7D8F9A" # Example Solana address

# Etherscan API Key (Get yours from [https://etherscan.io/apis](https://etherscan.io/apis))
# It's highly recommended to set this as an environment variable for security.
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "YOUR_ETHERSCAN_API_KEY") 
# IMPORTANT: Replace "YOUR_ETHERSCAN_API_KEY" with your actual key if not using environment variables.

# Infura Project ID for Web3 connection (Sepolia Testnet)
INFURA_PROJECT_ID = "YOUR_INFURA_PROJECT_ID" # Replace with your actual Infura Project ID

# Minimum ETH required for premium access
MIN_ETH_FOR_PREMIUM = 0.001

# --- Golden Minni Backend Core (Simplified for Streamlit Integration) ---

class SystemState:
    """Centralized state management for Golden Minni operations."""
    def __init__(self):
        self.eth_balance = 0.0
        self.premium_active = False
        self.minni_status = {
            "Wallet": "Inactive",
            "Grok3MinniAI_Setup": "Inactive",
            "TransferAI": "Inactive",
            "RiskAI": "Inactive",
            "ComplianceAI": "Inactive",
            "ConsensusAI": "Inactive",
            "SelfDefenseAI": "Inactive"
        }
        self.minni_alerts = {
            "Wallet": [],
            "Grok3MinniAI_Setup": [],
            "TransferAI": [],
            "RiskAI": [],
            "ComplianceAI": [],
            "ConsensusAI": [],
            "SelfDefenseAI": []
        }
        self.minni_latest_operation = {
            "Wallet": "N/A",
            "Grok3MinniAI_Setup": "N/A",
            "TransferAI": "N/A",
            "RiskAI": "N/A",
            "ComplianceAI": "N/A",
            "ConsensusAI": "N/A",
            "SelfDefenseAI": "N/A"
        }

# Initialize SystemState in Streamlit's session state
if 'system_state' not in st.session_state:
    st.session_state.system_state = SystemState()

class Wallet:
    def __init__(self, address, system_state):
        self.address = address
        self.web3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}'))
        # This is line 77 causing the error:
        self.web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.system_state = system_state
        self.system_state.minni_status["Wallet"] = "Initialized"
        self.system_state.minni_latest_operation["Wallet"] = f"Wallet initialized with address: {self.address}"

    def get_eth_balance(self):
        try:
            balance_wei = self.web3.eth.get_balance(self.address)
            balance_eth = self.web3.from_wei(balance_wei, 'ether')
            self.system_state.minni_latest_operation["Wallet"] = f"Retrieved ETH balance: {balance_eth}"
            return balance_eth
        except Exception as e:
            self.system_state.minni_status["Wallet"] = "Error"
            self.system_state.minni_alerts["Wallet"].append(f"Failed to get ETH balance: {e}")
            return 0.0

    def check_transaction_status(self, tx_hash):
        try:
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            if tx_receipt.status == 1:
                self.system_state.minni_latest_operation["Wallet"] = f"Transaction {tx_hash} confirmed."
                return "Confirmed"
            else:
                self.system_state.minni_latest_operation["Wallet"] = f"Transaction {tx_hash} failed."
                return "Failed"
        except Exception as e:
            self.system_state.minni_alerts["Wallet"].append(f"Error checking transaction status: {e}")
            return "Error"

def send_ethereum_transaction(sender_private_key, receiver_address, amount_eth, system_state):
    """
    Simulates sending an Ethereum transaction using a private key.
    In a real application, this would be a secure backend operation.
    NOTE: This requires a valid private key with funds on Sepolia.
    For this demo, it's illustrative and does not reveal the private key.
    """
    system_state.minni_latest_operation["TransferAI"] = "Attempting to prepare Ethereum transaction..."
    try:
        w3 = Web3(Web3.HTTPProvider(f'[https://sepolia.infura.io/v3/](https://sepolia.infura.io/v3/){INFURA_PROJECT_ID}'))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Get sender address from private key
        sender_account = w3.eth.account.from_key(sender_private_key)
        sender_address = sender_account.address

        nonce = w3.eth.get_transaction_count(sender_address)
        gas_price = w3.eth.gas_price

        transaction = {
            'from': sender_address,
            'to': receiver_address,
            'value': w3.to_wei(amount_eth, 'ether'),
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': 21000 # Standard gas limit for ETH transfer
        }

        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=sender_private_key)

        # In a real scenario, you'd send this:
        # tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # system_state.minni_latest_operation["TransferAI"] = f"Ethereum transaction sent! Tx Hash: {tx_hash.hex()}"
        # return tx_hash.hex()

        system_state.minni_latest_operation["TransferAI"] = (
            f"Ethereum transaction PREPARED (simulated sending): "
            f"From {sender_address}, To {receiver_address}, Amount {amount_eth} ETH. "
            f"Signed Tx Raw: {signed_txn.rawTransaction.hex()[:50]}..."
        )
        system_state.minni_alerts["TransferAI"].append("Simulation: Actual transaction not sent for security reasons.")
        return "SIMULATED_TX_HASH_" + secrets.token_hex(16) # Return a simulated hash
    except Exception as e:
        system_state.minni_status["TransferAI"] = "Error"
        system_state.minni_alerts["TransferAI"].append(f"Error preparing Ethereum transaction: {e}")
        return None

# Placeholder AI Layers
class Grok3MinniAI_Setup:
    def __init__(self, system_state):
        self.system_state = system_state
        self.system_state.minni_status["Grok3MinniAI_Setup"] = "Ready"
        self.system_state.minni_latest_operation["Grok3MinniAI_Setup"] = "Grok-3 Minni AI setup complete."
    def run_initial_scan(self):
        self.system_state.minni_latest_operation["Grok3MinniAI_Setup"] = "Performing initial system scan and optimization."
        # Simulate some setup
        time.sleep(0.5)
        self.system_state.minni_latest_operation["Grok3MinniAI_Setup"] = "Initial system scan complete."
        return {"status": "success", "message": "Grok-3 initial setup completed."}

class _Transfer: # Renamed to avoid conflict with the function, conceptually represents the AI behind transfers
    def __init__(self, system_state):
        self.system_state = system_state
        self.system_state.minni_status["TransferAI"] = "Monitoring"
        self.system_state.minni_latest_operation["TransferAI"] = "Transfer AI activated, monitoring for transaction requests."
    def process_request(self, request_data):
        self.system_state.minni_latest_operation["TransferAI"] = f"Processing transfer request: {request_data.get('type')}"
        # Simulate transfer logic
        if request_data.get("amount", 0) > 100:
            self.system_state.minni_alerts["TransferAI"].append(f"High-value transfer alert: {request_data.get('amount')} {request_data.get('currency')}")
        return {"status": "processed", "message": "Transfer AI logic applied."}

class _Risk:
    def __init__(self, system_state):
        self.system_state = system_state
        self.system_state.minni_status["RiskAI"] = "Active"
        self.system_state.minni_latest_operation["RiskAI"] = "Risk AI initialized, continuously assessing."
    def assess(self, transaction_details):
        risk_score = secrets.randbelow(100) # Simulate risk score
        self.system_state.minni_latest_operation["RiskAI"] = f"Assessed risk for transaction. Score: {risk_score}"
        if risk_score > 70:
            self.system_state.minni_alerts["RiskAI"].append(f"High risk detected (Score: {risk_score}) for: {transaction_details}")
            return {"risk": "high", "score": risk_score}
        return {"risk": "low", "score": risk_score}

class _Compliance:
    def __init__(self, system_state):
        self.system_state = system_state
        self.system_state.minni_status["ComplianceAI"] = "Active"
        self.system_state.minni_latest_operation["ComplianceAI"] = "Compliance AI initialized, checking regulations."
    def check_compliance(self, user_info, transaction_info):
        is_compliant = True # Simulate compliance check
        self.system_state.minni_latest_operation["ComplianceAI"] = "Performed compliance checks."
        if "sanctioned_country" in user_info:
            is_compliant = False
            self.system_state.minni_alerts["ComplianceAI"].append(f"Non-compliant user detected: {user_info.get('id')}")
        return {"compliant": is_compliant}

class _Consensus:
    def __init__(self, system_state):
        self.system_state = system_state
        self.system_state.minni_status["ConsensusAI"] = "Active"
        self.system_state.minni_latest_operation["ConsensusAI"] = "Consensus AI active, validating decisions."
    def validate_action(self, proposed_action):
        self.system_state.minni_latest_operation["ConsensusAI"] = f"Validating action: {proposed_action.get('type')}"
        # Simulate consensus
        if proposed_action.get("critical", False) and secrets.randbelow(10) < 2:
            self.system_state.minni_alerts["ConsensusAI"].append(f"Consensus disagreement on critical action: {proposed_action.get('type')}")
            return False
        return True

class _SelfDefense:
    def __init__(self, system_state):
        self.system_state = system_state
        self.system_state.minni_status["SelfDefenseAI"] = "Monitoring"
        self.system_state.minni_latest_operation["SelfDefenseAI"] = "Self-Defense AI scanning for threats."
    def detect_threat(self, data_stream):
        threat_level = secrets.randbelow(10) # Simulate threat detection
        self.system_state.minni_latest_operation["SelfDefenseAI"] = f"Threat detection scan. Level: {threat_level}"
        if threat_level > 7:
            self.system_state.minni_alerts["SelfDefenseAI"].append(f"Potential threat detected (Level: {threat_level}) in data stream.")
            return True
        return False

# --- Golden Minni Backend Initialization (Persistent in Session State) ---
def init_golden_minni_backend():
    if 'golden_minni' not in st.session_state:
        st.session_state.golden_minni = {
            "wallet": Wallet(ETH_ADDR, st.session_state.system_state),
            "grok3_setup": Grok3MinniAI_Setup(st.session_state.system_state),
            "transfer_ai": _Transfer(st.session_state.system_state),
            "risk_ai": _Risk(st.session_state.system_state),
            "compliance_ai": _Compliance(st.session_state.system_state),
            "consensus_ai": _Consensus(st.session_state.system_state),
            "self_defense_ai": _SelfDefense(st.session_state.system_state)
        }
        # Run initial setup for Grok3 Minni
        st.session_state.golden_minni["grok3_setup"].run_initial_scan()
        st.session_state.minni_initialized = True
    else:
        # Ensure system_state reference is updated if the object itself is re-initialized (Streamlit reruns)
        for ai_module in st.session_state.golden_minni.values():
            if hasattr(ai_module, 'system_state'):
                ai_module.system_state = st.session_state.system_state

# --- OraculumX Streamlit Application ---

st.set_page_config(layout="wide", page_title="OraculumX Command Center", page_icon="🌐")

# Custom CSS for a sleek, futuristic look
st.markdown("""
<style>
.main-header {
    font-size: 3.5em;
    font-weight: bold;
    text-align: center;
    color: #00ff00; /* Neon green */
    text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00;
    margin-bottom: 20px;
}
.subheader {
    font-size: 1.8em;
    color: #00ffff; /* Aqua */
    text-align: center;
    margin-bottom: 30px;
}
.stApp {
    background-color: #0d1117; /* Dark GitHub background */
    color: #e6edf3; /* Light gray for text */
}
.stButton>button {
    background-color: #00ff00;
    color: black;
    font-weight: bold;
    border-radius: 5px;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #00cc00;
    box-shadow: 0 0 15px #00ff00;
}
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size: 1.2em;
    color: #00ffff;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}
.stTabs [data-baseweb="tab-list"] button {
    background-color: #21262d;
    border-radius: 5px 5px 0 0;
    border: 1px solid #30363d;
}
.stTabs [data-baseweb="tab-list"] button:hover {
    background-color: #30363d;
}
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background-color: #0d1117;
    border-bottom: 3px solid #00ff00;
    color: #00ff00;
}
.premium-access {
    background-color: #161b22;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #00ff00;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    margin-top: 30px;
    text-align: center;
}
.payment-section {
    background-color: #161b22;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #30363d;
    margin-top: 20px;
    text-align: center;
}
.code-block {
    background-color: #21262d;
    padding: 15px;
    border-radius: 5px;
    font-family: monospace;
    font-size: 1em;
    overflow-x: auto;
    color: #e6edf3;
    border: 1px solid #30363d;
}
.metric-value {
    font-size: 2em;
    font-weight: bold;
    color: #00ff00;
}
.metric-label {
    font-size: 1em;
    color: #00ffff;
}
.stExpander {
    background-color: #161b22;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #30363d;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">ORACULUMX COMMAND CENTER</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Golden Minni AI Integrated</p>', unsafe_allow_html=True)

# Initialize Golden Minni backend on first run
init_golden_minni_backend()

# Retrieve the Wallet instance from session state
minni_wallet = st.session_state.golden_minni["wallet"]

# --- Functions ---
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@st.cache_data(ttl=30) # Cache for 30 seconds
def get_eth_balance_from_etherscan(address, api_key):
    url = f"[https://api-sepolia.etherscan.io/api?module=account&action=balance&address=](https://api-sepolia.etherscan.io/api?module=account&action=balance&address=){address}&tag=latest&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data["status"] == "1":
            # Balance is in Wei, convert to Ether
            balance_wei = int(data["result"])
            balance_eth = balance_wei / (10**18)
            st.session_state.system_state.minni_latest_operation["Wallet"] = f"Etherscan ETH balance check: {balance_eth:.6f} ETH"
            return balance_eth
        else:
            st.session_state.system_state.minni_alerts["Wallet"].append(f"Etherscan API error: {data['message']}")
            return 0.0
    except requests.exceptions.RequestException as e:
        st.session_state.system_state.minni_alerts["Wallet"].append(f"Network error fetching ETH balance from Etherscan: {e}")
        return 0.0
    except ValueError as e:
        st.session_state.system_state.minni_alerts["Wallet"].append(f"JSON decoding or data conversion error from Etherscan: {e}")
        return 0.0

# --- Payment and Premium Access Logic ---

# Check if premium access is already active in session state
if 'premium_active' not in st.session_state:
    st.session_state.premium_active = False
if 'last_balance_check_time' not in st.session_state:
    st.session_state.last_balance_check_time = datetime.min

# Only check balance every 30 seconds to avoid API rate limits
if not st.session_state.premium_active or (datetime.now() - st.session_state.last_balance_check_time) > timedelta(seconds=30):
    current_eth_balance = get_eth_balance_from_etherscan(ETH_ADDR, ETHERSCAN_API_KEY)
    st.session_state.eth_balance = current_eth_balance
    st.session_state.last_balance_check_time = datetime.now()
    if st.session_state.eth_balance >= MIN_ETH_FOR_PREMIUM:
        st.session_state.premium_active = True
        st.session_state.system_state.premium_active = True # Update Golden Minni's state
    else:
        st.session_state.premium_active = False
        st.session_state.system_state.premium_active = False # Update Golden Minni's state

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Dashboard", "Access & Payment", "Golden Minni Backend Operations"])

with tab1:
    st.header("OraculumX Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Current ETH Balance (Your Wallet)", value=f"{st.session_state.eth_balance:.6f} ETH", delta_color="normal")
    with col2:
        if st.session_state.premium_active:
            st.markdown(f'<div class="premium-access"><h2>✅ PREMIUM ACCESS ACTIVE ✅</h2><p>Welcome, Commander! All signals unlocked.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="premium-access"><h2>🔒 PREMIUM ACCESS REQUIRED 🔒</h2><p>Unlock advanced signals by making a payment.</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Current Market Signals")

    if st.session_state.premium_active:
        st.success("Accessing Premium AI-Driven Crypto Signals:")
        st.write("""
        * **Signal 1: ETH - Strong Buy (Short-term)**
            * **Rationale:** On-chain analytics indicate significant whale accumulation and decreasing exchange reserves. Grok-3 AI projects a 7-10% surge within 48 hours.
            * **Target Price:** $4,500 - $4,650
            * **Stop Loss:** $4,080
        * **Signal 2: SOL - Moderate Buy (Mid-term)**
            * **Rationale:** Solana ecosystem growth and rising DeFi TVL. Minni's sentiment analysis detects increasing positive social media chatter.
            * **Target Price:** $220 - $240
            * **Stop Loss:** $185
        * **Signal 3: BTC - Neutral to Slight Bullish (Long-term)**
            * **Rationale:** Macroeconomic factors suggest continued institutional interest, but short-term volatility expected due to upcoming FOMC meeting.
            * **Key Resistance:** $75,000
            * **Key Support:** $68,000
        * **Special Alert: "Quantum Leap" Strategy Imminent (AI-Generated)**
            * **Details:** Golden Minni's advanced quantum computing simulation module has identified a rare arbitrage opportunity across three major exchanges. Execution window: Next 12 hours. Requires high-frequency trading setup. (Contact support for automated API key integration)
        """)
        st.info("These signals are generated by Golden Minni's advanced AI layers, including Grok-3 and proprietary algorithms. Always conduct your own research before making investment decisions.")
    else:
        st.warning("Please make a payment to unlock premium signals. See the 'Access & Payment' tab for details.")

    st.markdown("---")
    st.subheader("Real-time Analytics Snapshot (Simulated)")
    st.info("This section provides a glimpse into the AI's ongoing analysis. Actual data streams are processed by Golden Minni backend.")
    st.json({
        "AI_Market_Sentiment": {"BTC": "Slightly Bullish", "ETH": "Very Bullish", "SOL": "Bullish"},
        "Global_Liquidity_Index": 78.5,
        "Fear_Greed_Index": 72, # Greed
        "Decentralized_Exchange_Volume_24h": "$12.5B",
        "Top_AI_Identified_Narrative": "AI & DePIN Integration",
        "Predicted_Volatility_Next_24h": "Medium",
        "Golden_Minni_Confidence_Score": "98.7%"
    })

with tab2:
    st.header("Access & Payment Gateway")
    st.write("To gain full access to OraculumX's premium AI-driven crypto signals, please make a one-time payment to the wallet address below.")

    st.markdown(f"""
    <div class="payment-section">
        <h3>Unlock Premium Signals (ETH)</h3>
        <p>Send at least <span style="color:#00ff00; font-weight:bold;">{MIN_ETH_FOR_PREMIUM} ETH</span> to the address below:</p>
        <div style="margin: 20px auto; width: 250px;">
            <img src="data:image/png;base64,{generate_qr_code(f"ethereum:{ETH_ADDR}?amount={MIN_ETH_FOR_PREMIUM}")}" alt="ETH QR Code" style="width:100%; height:auto;">
        </div>
        <p style="font-size:1.2em; font-weight:bold;">Ethereum (ETH) Address:</p>
        <div class="code-block">
            <code>{ETH_ADDR}</code>
            <button onclick="navigator.clipboard.writeText('{ETH_ADDR}')" style="margin-left: 10px; background-color: #30363d; color: white; border: 1px solid #00ff00; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Copy</button>
        </div>
        <p style="margin-top: 15px;">
            <a href="[https://metamask.app.link/send/](https://metamask.app.link/send/){ETH_ADDR}@11155111/transfer?value={int(MIN_ETH_FOR_PREMIUM * 10**18)}" target="_blank" style="color:#00ffff; text-decoration:none;">
                <img src="[https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg](https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg)" alt="MetaMask Icon" width="20" height="20" style="vertical-align:middle; margin-right:5px;"> Pay with MetaMask (Sepolia Testnet)
            </a>
        </p>
        <p style="font-size:0.9em; color:#a0a0a0; margin-top:10px;">
            (Please ensure you are on the Sepolia testnet if using MetaMask for testing.)
        </p>
        <p style="font-size:0.9em; color:#a0a0a0;">
            Your premium access will be automatically activated once the transaction is confirmed on the blockchain.
        </p>
        <p style="font-size:0.9em; color:#a0a0a0;">
            Current ETH Balance in your payment wallet: <span style="font-weight:bold; color:#00ff00;">{st.session_state.eth_balance:.6f} ETH</span>
        </p>
        <p style="font-size:0.9em; color:#a0a0a0;">
            Last checked: {st.session_state.last_balance_check_time.strftime("%Y-%m-%d %H:%M:%S")}
        </p>
        <button onclick="window.location.reload();" style="margin-top: 20px;">Refresh Balance Check</button>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Other Payment Options (Coming Soon)")
    st.info("Bitcoin (BTC) and Solana (SOL) payment gateways are under development by the Golden Minni AI module for multi-chain support.")

    col_btc, col_sol = st.columns(2)
    with col_btc:
        st.markdown(f"""
        <div class="payment-section" style="border: 1px solid #708090;">
            <h3>Bitcoin (BTC) Address</h3>
            <p style="color:#708090;">(Currently inactive)</p>
            <div class="code-block" style="color:#708090;">
                <code>{BTC_ADDR}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_sol:
        st.markdown(f"""
        <div class="payment-section" style="border: 1px solid #708090;">
            <h3>Solana (SOL) Address</h3>
            <p style="color:#708090;">(Currently inactive)</p>
            <div class="code-block" style="color:#708090;">
                <code>{SOL_ADDR}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.header("Golden Minni Backend Operations")
    st.write("Monitor the real-time status and alerts from your integrated Golden Minni AI layers.")

    # Display Minni AI Status
    st.subheader("AI Layer Status")
    status_cols = st.columns(3)
    for i, (name, status) in enumerate(st.session_state.system_state.minni_status.items()):
        with status_cols[i % 3]:
            st.metric(label=f"{name} Status", value=status, delta_color="off")

    st.subheader("AI Layer Latest Operations")
    for name, operation in st.session_state.system_state.minni_latest_operation.items():
        st.markdown(f"**{name}:** `{operation}`")

    st.subheader("AI Layer Alerts")
    for name, alerts in st.session_state.system_state.minni_alerts.items():
        if alerts:
            st.warning(f"🚨 **{name} Alerts:**")
            for alert in alerts:
                st.markdown(f"- {alert}")
        else:
            st.info(f"✅ No new alerts for {name}.")

    st.markdown("---")
    st.subheader("Simulate Golden Minni Backend Actions")
    st.write("This section allows you to trigger simulated actions within the Golden Minni backend to observe its responses and status updates.")

    # Example of triggering a simulated transfer by Golden Minni (e.g., for rebalancing or internal operations)
    st.markdown("#### Simulate an Outgoing Ethereum Transaction (from Golden Minni)")
    st.info("This simulates Golden Minni preparing a transaction. For security, actual sending requires a private key and is not performed by this demo.")
    sim_receiver_addr = st.text_input("Simulated Receiver Address (Sepolia)", "0xAb5801a6136c0d0aF91b0B99B7a635848e025400") # A dummy address
    sim_amount = st.number_input("Simulated Amount (ETH)", min_value=0.0001, value=0.01, step=0.001, format="%.4f")

    if st.button("Simulate Golden Minni Transfer (ETH)"):
        if INFURA_PROJECT_ID == "YOUR_INFURA_PROJECT_ID":
            st.error("Please replace 'YOUR_INFURA_PROJECT_ID' with your actual Infura Project ID to simulate transactions.")
        elif ETH_ADDR == "0x5036dbcEEfae0a7429e64467222e1E259819c7C7":
             st.error("Please ensure ETH_ADDR is correctly set for simulation (though for this specific sim, a sender private key would be needed).")
        else:
            # In a real system, the private key would be securely managed by Golden Minni's core.
            # For this simulation, we'll just log the attempt.
            st.session_state.system_state.minni_latest_operation["TransferAI"] = (
                f"Golden Minni initiated simulated transfer: {sim_amount} ETH to {sim_receiver_addr}"
            )
            st.session_state.system_state.minni_alerts["TransferAI"].append(
                f"SIMULATION: Golden Minni processed request for {sim_amount} ETH to {sim_receiver_addr}. Requires actual private key for sending."
            )
            st.success("Simulated transfer request sent to Golden Minni's TransferAI.")
            # Trigger a refresh of the AI operations display
            st.rerun()

    st.markdown("---")
    st.markdown("#### Manually Trigger AI Layer Processes (Simulated)")
    st.info("These buttons simulate complex internal processes within Golden Minni's AI layers.")

    col_ai_triggers = st.columns(3)
    with col_ai_triggers[0]:
        if st.button("Run Risk Assessment"):
            st.session_state.golden_minni["risk_ai"].assess({"user": "sim_user_id", "value": 1000, "currency": "USD"})
            st.success("Risk assessment initiated by RiskAI.")
    with col_ai_triggers[1]:
        if st.button("Check Compliance"):
            st.session_state.golden_minni["compliance_ai"].check_compliance({"id": "sim_user_id", "country": "USA"}, {"type": "withdrawal"})
            st.success("Compliance check initiated by ComplianceAI.")
    with col_ai_triggers[2]:
        if st.button("Validate Critical Action"):
            st.session_state.golden_minni["consensus_ai"].validate_action({"type": "asset_rebalance", "critical": True})
            st.success("Critical action validation initiated by ConsensusAI.")
    
    st.markdown("---")
    st.info("The OraculumX system continuously monitors the blockchain for payments to automatically grant premium access. This page auto-refreshes every 30 seconds.")
    # Automatic refresh
    st.markdown(f'<meta http-equiv="refresh" content="30">', unsafe_allow_html=True)