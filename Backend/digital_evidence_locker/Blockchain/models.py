from django.db import models


class BlockchainTransaction(models.Model):
    transaction_hash = models.CharField(max_length=255, unique=True)
    block_number = models.BigIntegerField(null=True, blank=True)

    action = models.CharField(max_length=100)

    evidence_id = models.IntegerField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=50,
        default="Pending"
    )

    def __str__(self):
        return self.transaction_hash