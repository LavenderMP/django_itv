from django.db import models
import uuid

class Ticket(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    def __str__(self):
        return str(self.token)
