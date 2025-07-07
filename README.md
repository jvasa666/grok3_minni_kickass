# OraculumX Command Center: Golden Minni AI Integration

![OraculumX Logo - Placeholder](https://via.placeholder.com/150x50?text=OraculumX)
*(Consider replacing this with an actual logo or a relevant screenshot of your Streamlit app)*

## Project Overview

The **OraculumX Command Center** is a sophisticated, AI-driven platform designed to provide real-time crypto market signals and advanced financial insights. It integrates the cutting-edge **Golden Minni AI** as its backend, handling secure wallet operations, risk assessment, compliance checks, and more.

This application features a Streamlit-based user interface for intuitive interaction and a robust payment gateway that unlocks premium AI signals upon successful ETH payment.

## Features

* **AI-Driven Crypto Signals:** Leverage Golden Minni's advanced algorithms (including Grok-3) for short-term, mid-term, and long-term market predictions.
* **Premium Access Model:** Unlock exclusive signals and features via a simple Ethereum (ETH) payment.
* **Secure Payment Gateway:** Utilizes hardcoded, secure wallet addresses for receiving payments.
* **Real-time ETH Balance Monitoring:** Automatically detects incoming payments and activates premium access.
* **Golden Minni Backend Operations Dashboard:** Gain transparency into the status, latest operations, and alerts from core AI layers (Wallet, Transfer, Risk, Compliance, Consensus, Self-Defense AI).
* **Simulated AI Actions:** Ability to trigger simulated backend actions (e.g., transfers, risk assessments) for monitoring and demonstration purposes.
* **Sleek User Interface:** A dark-themed, professional dashboard built with Streamlit.

## Installation & Setup

To get the OraculumX Command Center up and running, follow these steps:

1.  **Clone the Repository (or download the script):**
    If you have a Git repository:
    ```bash
    git clone [your-repository-url]
    cd [your-repository-name]
    ```
    If you just have the `grok3_minni_kickass.py` file, navigate to its directory.

2.  **Create a Virtual Environment (Recommended):**
    This helps manage dependencies and avoids conflicts with other Python projects.
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install streamlit qrcode Pillow requests web3 cryptography
    ```
    *(Note: Ensure `requests` is installed, which you confirmed you need.)*

4.  **Configure API Keys and Settings:**

    * **Etherscan API Key:**
        Obtain a free API key from [Etherscan](https://etherscan.io/apis).
        **Crucially, set this as an environment variable.** For example, on Windows (in PowerShell):
        ```powershell
        $env:ETHERSCAN_API_KEY="YOUR_ETHERSCAN_API_KEY"
        # Or in Command Prompt:
        set ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY
        ```
        On macOS/Linux:
        ```bash
        export ETHERSCAN_API_KEY="YOUR_ETHERSCAN_API_KEY"
        ```
        *It's best practice to set this in your system's environment variables or in a `.env` file loaded by a library like `python-dotenv` for production, rather than hardcoding.*

    * **Infura Project ID:**
        Sign up for an Infura account ([infura.io](https://infura.io/)) and create a new project to get your Project ID.
        **You MUST replace `"YOUR_INFURA_PROJECT_ID"`** in the `grok3_minni_kickass.py` file (around line 43 or 76, look for `INFURA_PROJECT_ID = "YOUR_INFURA_PROJECT_ID"`) with your actual Infura Project ID. This is necessary for Golden Minni to connect to the Ethereum Sepolia testnet.

## Usage

1.  **Launch the OraculumX Command Center:**
    Make sure your virtual environment is active (if you created one) and navigate to the directory containing `grok3_minni_kickass.py`.
    ```bash
    streamlit run grok3_minni_kickass.py
    ```
    This will open the application in your default web browser.

2.  **Gain Premium Access:**
    * Navigate to the "Access & Payment" tab.
    * Send at least `0.001 ETH` to the displayed Ethereum wallet address (`0x5036dbcEEfae0a7429e64467222e1E259819c7C7` or your updated address if you changed it).
    * The system will automatically detect the payment within approximately 30 seconds (or on manual refresh), and the "Dashboard" tab will display unlocked premium signals.

3.  **Monitor Golden Minni:**
    * Visit the "Golden Minni Backend Operations" tab to see the real-time status, latest actions, and any alerts from the AI layers.
    * You can also use the "Simulate Golden Minni Transfer" button to trigger a dummy transaction request within the AI backend for observation.

## Project Structure (Conceptual)

.
├── grok3_minni_kickass.py    # Main Streamlit application and integrated AI logic
├── README.md                 # This file
├── requirements.txt          # (Optional, but recommended) Lists all Python dependencies
└── venv/                     # Python virtual environment (created by python -m venv venv)


*(You might want to create a `requirements.txt` file by running `pip freeze > requirements.txt` after installing all dependencies. This makes it easier for others to install everything with `pip install -r requirements.txt`)*

## Contributing

*(Optional section - if you plan for others to contribute)*
We welcome contributions! If you have ideas for improvements or new features, please open an issue or submit a pull request.

## License

*(Optional section - state your project's license)*
This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT). *(Or choose another license)*

## Contact

For any questions or support, please contact [Your Name/Email/GitHub Profile].
