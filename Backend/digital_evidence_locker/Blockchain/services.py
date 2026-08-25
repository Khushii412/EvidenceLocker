from .contract import CONTRACT_ADDRESS, CONTRACT_ABI


def store_evidence_hash(evidence_hash):
    """
    Store evidence hash on the blockchain.
    """

    # Blockchain integration will be added here
    # after the smart contract is deployed.

    return {
        "success": False,
        "message": "Blockchain integration is not configured yet.",
        "evidence_hash": evidence_hash,
    }


def verify_evidence_hash(evidence_hash):
    """
    Verify evidence hash from the blockchain.
    """

    # Verification logic will be added here
    # after the smart contract is deployed.

    return {
        "success": False,
        "message": "Blockchain verification is not configured yet.",
        "evidence_hash": evidence_hash,
    }