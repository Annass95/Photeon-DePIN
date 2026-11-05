# 🌍 Photeon Retina - DePIN Oracle Node

**Transforming Optical AI GreenOps into Real-World Assets (RWA) on the Blockchain.**

Photeon Retina is a Decentralized Physical Infrastructure Network (DePIN) project. It bridges the gap between heavy, localized AI computing (YOLOv8 + CodeCarbon) and the Web3 ecosystem.

## 🏗️ Architecture

This repository contains the **Oracle Node** and **Smart Contracts** connecting the physical AI pipeline to the blockchain:

1. **The Oracle API (`bridge_api.py`)**: A FastAPI micro-service that securely exposes the CO2 and energy savings calculated locally by the Photeon Retina AI pipeline.
2. **The Web3 Courier (`web3_oracle.py`)**: A Python automation script that fetches the GreenOps data from the local API, formats it for Solidity (handling float conversions), and signs the transaction.
3. **The RWA Smart Contract (`contracts/PhoteonCarbon.sol`)**: A Solidity contract acting as an immutable public ledger, minting verifiable Carbon Credit tokens based on the AI's metrics.

## 🚀 How to Run the Demo

### 1. Start the Oracle API
```bash
uvicorn bridge_api:app --reload