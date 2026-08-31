from .contract import w3, contract, ACCOUNT


def store_evidence_hash(evidence_hash):
    """
    Store an evidence hash on the Ethereum Sepolia blockchain.
    """

    try:
        # Make sure the hash is in bytes32 format
        if isinstance(evidence_hash, str):
            evidence_hash = bytes.fromhex(evidence_hash.replace("0x", ""))

        # Get next transaction nonce
        nonce = w3.eth.get_transaction_count(ACCOUNT.address)

        # Build transaction
        transaction = contract.functions.storeEvidence(
            evidence_hash
        ).build_transaction({
            "from": ACCOUNT.address,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
        })

        # Sign transaction with backend wallet
        signed_transaction = ACCOUNT.sign_transaction(transaction)

        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(
            signed_transaction.raw_transaction
        )

        # Wait until blockchain confirms it
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "success": True,
            "transaction_hash": tx_hash.hex(),
            "block_number": receipt.blockNumber,
            "evidence_hash": evidence_hash.hex(),
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "evidence_hash": (
                evidence_hash.hex()
                if isinstance(evidence_hash, bytes)
                else evidence_hash
            ),
        }


def verify_evidence_hash(evidence_hash):
    """
    Verify an evidence hash from the blockchain.
    """

    try:
        if isinstance(evidence_hash, str):
            evidence_hash = bytes.fromhex(
                evidence_hash.replace("0x", "")
            )

        result = contract.functions.verifyEvidence(
            evidence_hash
        ).call()

        return {
            "success": True,
            "exists": result[0],
            "timestamp": result[1],
            "uploaded_by": result[2],
            "evidence_hash": evidence_hash.hex(),
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "evidence_hash": (
                evidence_hash.hex()
                if isinstance(evidence_hash, bytes)
                else evidence_hash
            ),
        }