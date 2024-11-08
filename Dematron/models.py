from django.db import models
from Base.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.

class DemateAccountType(models.TextChoices):
    ANGELONE = 'aone', _('AngelOne') 

class DemateAccount(BaseModel):
    name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=DemateAccountType.choices, default=DemateAccountType.ANGELONE)
    brokerConfig = models.JSONField()

    class Meta:
        verbose_name = _('Demate Account')
        verbose_name_plural = _('Demate Accounts')
    
    def __str__(self):
        return self.name

