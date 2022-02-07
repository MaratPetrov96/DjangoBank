from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,
                                primary_key=True)
    money = models.IntegerField(default=0)

class Transaction(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name='sended')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name='received')
    money = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=20,
                          choices=(('0','Gift'),('1','Borrow'),('2','Lend'),('3','Payment'))
                          ,blank=True)
