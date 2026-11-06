import os
import requests
from dotenv import load_dotenv
from web3 import Web3

# 1. Charger les clés depuis le .env
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# 2. Connexion au réseau Whitechain
print("🔌 Connexion à l'infrastructure Whitechain...")
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
print(f"👤 Compte Oracle Node : {account.address}")

# 3. L'ABI (Le traducteur Python -> Solidity)
contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "_projectId", "type": "string"},
            {"internalType": "uint256", "name": "_co2ReducedKg", "type": "uint256"}
        ],
        "name": "mintCarbonCredit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def fetch_greenops_data():
    """Étape 1 : Lire les données de ton IA (YOLOv8 -> FastAPI)"""
    print("\n🔍 Recherche de nouvelles optimisations CO2 sur l'API Photeon...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/mint-data")
        return response.json()
    except Exception as e:
        print("❌ FastAPI hors ligne. Lance uvicorn d'abord !")
        return None

def send_rwa_transaction(project_id, co2_saved):
    """Étape 2 : Frapper le jeton sur la blockchain"""
    # Solidity n'aime pas les virgules, on arrondit à l'entier pour la démo
    co2_entier = int(co2_saved)
    print(f"\n🚀 Préparation RWA pour le projet {project_id} ({co2_entier} kg de CO2)...")
    
    try:
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Construction de la transaction avec les règles strictes de Whitechain
        tx = contract.functions.mintCarbonCredit(project_id, co2_entier).build_transaction({
            'chainId': 1874,
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        print("✍️ Signature cryptographique...")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

        print("📡 Déploiement sur le réseau Whitechain...")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"✅ SUCCÈS ! Transaction validée dans le bloc {receipt.blockNumber}")
        print(f"🔗 Preuve (Hash) : {w3.to_hex(tx_hash)}")
        
    except Exception as e:
        print(f"❌ Échec Web3 : {e}")

if __name__ == "__main__":
    print("=== 🌐 Démarrage de l'Oracle Photeon ===")
    api_data = fetch_greenops_data()
    
    if api_data:
        # On extrait les données de ton API et on les envoie à la blockchain
        send_rwa_transaction(api_data["project_id"], api_data["co2_reduced_kg"])