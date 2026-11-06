from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime

app = FastAPI(title="Photeon Retina - DePIN Oracle Node")

# --- NOUVEAU : Autorisation CORS pour le Front-end HTML ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Autorise n'importe quel fichier HTML local à lire l'API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de la donnée qui sera tokenisée sur la blockchain
class CarbonAsset(BaseModel):
    project_id: str
    energy_saved_kwh: float
    co2_reduced_kg: float
    verification_timestamp: str
    ai_confidence_score: float

@app.get("/api/v1/mint-data", response_model=CarbonAsset)
def get_carbon_data():
    """
    Simule la lecture du fichier emissions.csv généré par CodeCarbon après 
    le passage de YOLOv8. Expose la donnée pour le Smart Contract (T-REX).
    """
    # En production, ce code lit ton CSV. Pour la démo de ce soir, 
    # on génère des valeurs réalistes pour prouver le flux de données.
    energy = round(random.uniform(10.5, 25.0), 2)
    
    return CarbonAsset(
        project_id="PHOTEON_OPT_001",
        energy_saved_kwh=energy,
        co2_reduced_kg=round(energy * 0.4, 2), # Approximation de conversion
        verification_timestamp=datetime.now().isoformat(),
        ai_confidence_score=0.98
    )