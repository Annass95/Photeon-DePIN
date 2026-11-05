import requests
import os
from web3 import Web3
from dotenv import load_dotenv

# Charge les variables de sécurité (clés privées) depuis un fichier .env caché
load_dotenv()

# 1. Connexion au réseau Blockchain (Le RPC)
# Demain, les sponsors te donneront l'URL exacte de leur réseau (Hedera, Whitechain...)
RPC_URL = "https://rpc.sepolia.org" 
web3 = Web3(Web3.HTTPProvider(RPC_URL))

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
CONTRACT_ADDRESS = "0x..." # Tu mettras l'adresse de ton contrat après l'avoir déployé demain

def fetch_greenops_data():
    """Étape 1 : Le script vient lire la vitrine de l'API (FastAPI)"""
    print("Recherche de nouvelles optimisations CO2 sur l'API locale...")
    response = requests.get("http://127.0.0.1:8000/api/v1/mint-data")
    return response.json()

def mint_on_blockchain(data):
    """Étape 2 : Le script signe cryptographiquement et envoie au Smart Contract"""
    project_id = data["project_id"]
    
    # ⚠️ CONVERSION OBLIGATOIRE : Solidity déteste les virgules. 
    # On multiplie par 100 pour n'avoir que des entiers (4.50 kg -> 450).
    co2_kg_entier = int(data["co2_reduced_kg"] * 100)

    print(f"Préparation de la transaction Blockchain pour le projet {project_id}...")
    print(f"Valeur convertie pour Solidity : {co2_kg_entier} unités.")
    
    if not PRIVATE_KEY:
        print("ATTENTION : Clé privée manquante. Test à blanc réussi. Fin de l'exécution.")
        return

    # --- La logique d'envoi Web3 (Commentée jusqu'au déploiement de demain) ---
    # contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI_DU_CONTRAT)
    # tx = contract.functions.mintCarbonCredit(project_id, co2_kg_entier).build_transaction({
    #     'from': WALLET_ADDRESS,
    #     'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS)
    # })
    # signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # print(f"Succès ! Transaction validée : {web3.to_hex(tx_hash)}")

if __name__ == "__main__":
    print("=== Démarrage de l'Oracle Photeon Web3 ===")
    api_data = fetch_greenops_data()
    print(f"Donnée API capturée : {api_data}")
    mint_on_blockchain(api_data)