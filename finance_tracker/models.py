from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        user = CustomUser.objects.filter(username=self.username).first()
        print(user)
        Balance.objects.get_or_create(user=self)
        UserProfile.objects.get_or_create(user=self)


class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('INCOME', 'income'),
        ('EXPENSE', 'expense'),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, verbose_name="Transaction")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    transacton_date = models.DateTimeField(auto_now=True, verbose_name="Transaction date")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey(CustomUser, related_name="transactions", on_delete=models.CASCADE, verbose_name="User")

    def save(self, *args, **kwargs):
        balance = Balance.objects.filter(user = self.user).first()
        if balance.amount >=self.amount or self.transaction_type == "INCOME":
            if self.transaction_type == 'EXPENSE':
                balance.amount -= self.amount
            else:
                balance.amount += self.amount
            balance.save()
            super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"Transaction type: {self.transaction_type}, User: {self.user}"
    
    class Meta:
        db_table = 'transaction'
        managed = True
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class UserProfile(models.Model):
    image = models.ImageField(upload_to='profiles/')
    user = models.OneToOneField(CustomUser, related_name="profile", on_delete=models.CASCADE, verbose_name="User")
    bio = models.TextField(null=True, blank=True, verbose_name="Bio")
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name="Phone number")
    address = models.CharField(max_length=30, null=True, blank=True, verbose_name="Address")

    def __str__(self):
        return f"User: {self.user}"
    
    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'
        

class Balance(models.Model):
    user = models.OneToOneField(CustomUser, related_name="balance", on_delete=models.CASCADE, verbose_name="User")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Amount")

    def __str__(self):
        return f"User: {self.user}"
    
    class Meta:
        db_table = 'balance'
        managed = True
        verbose_name = 'Balance'
        verbose_name_plural = 'Balances'
