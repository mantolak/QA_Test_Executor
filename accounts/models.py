from django.db import models
from django.contrib.auth.models import User
from mirage import fields

class Accounts(models.Model):
    #token = models.CharField(max_length=100)
    token = fields.EncryptedTextField(max_length=100, default='testtoken')
    gh_token = fields.EncryptedTextField(max_length=100, default='testtoken')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
