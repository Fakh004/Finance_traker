from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class Transaction(models.Model):
    TRANSACTION_CHOICES = [('INCOME', 'Income'), ('EXPENSE', 'Expense')]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, verbose_name="Transaction type")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    transaction_date = models.DateTimeField(auto_now=True, verbose_name="Transaction date")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey('CustomUser', related_name="transactions", on_delete=models.CASCADE, verbose_name="User")

    def save(self, *args, **kwargs):
     balance, _ = Balance.objects.get_or_create(user=self.user)

     if self.pk:  
        old_tx = Transaction.objects.get(pk=self.pk)
        if old_tx.transaction_type == "EXPENSE":
            balance.amount += old_tx.amount
        else:
            balance.amount -= old_tx.amount

     if self.transaction_type == "EXPENSE":
        if balance.amount < self.amount:
            raise ValueError("Not enough balance for this expense")
        balance.amount -= self.amount
     else:
        balance.amount += self.amount

     balance.save()
     super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.transaction_type} | {self.amount} | {self.user}"

    class Meta:
        db_table = 'transaction'
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name="profile", on_delete=models.CASCADE, verbose_name="User")
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user}"

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'


class Balance(models.Model):
    user = models.OneToOneField(CustomUser, related_name="balance", on_delete=models.CASCADE, verbose_name="User")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Balance of {self.user}: {self.amount}"

    class Meta:
        db_table = 'balance'
        verbose_name = 'balance'
        verbose_name_plural = 'balances'
