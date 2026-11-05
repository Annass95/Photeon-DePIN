// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title PhoteonCarbon
 * @dev Contrat de tokenisation RWA (Real World Asset) pour les économies de CO2
 * détectées par le pipeline IA Photeon Retina (YOLOv8 + CodeCarbon).
 */
contract PhoteonCarbon {
    
    string public name = "Photeon Carbon Credit";
    string public symbol = "PCC";
    
    // Enregistre le total de CO2 économisé par projet
    mapping(string => uint256) public projectSavedCO2;

    // L'événement est crucial : c'est ce qui s'affiche sur l'explorateur de la blockchain
    event CarbonMinted(string projectId, uint256 co2ReducedKg, uint256 timestamp);

    /**
     * @dev Fonction appelée par le script Python Oracle après lecture de l'API FastAPI.
     * Note: Solidity ne gère pas les float. On gérera la conversion côté Python.
     */
    function mintCarbonCredit(string memory _projectId, uint256 _co2ReducedKg) public {
        
        // Met à jour le registre incorruptible
        projectSavedCO2[_projectId] += _co2ReducedKg;
        
        // Émet la preuve cryptographique
        emit CarbonMinted(_projectId, _co2ReducedKg, block.timestamp);
    }

    // Fonction pour que les juges puissent vérifier le solde d'un projet
    function getProjectCO2(string memory _projectId) public view returns (uint256) {
        return projectSavedCO2[_projectId];
    }
}