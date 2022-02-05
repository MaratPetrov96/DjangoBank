from django.shortcuts import HttpResponse,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from .models import *

@login_required
def send_user_id(request):
    return HttpResponse(str(request.user.pk))

@login_required
def send_account(request):
    return HttpResponse(str(
        Account.objects.get(pk=request.user.pk).money
        ))

@login_required
def last_trans(request):
    dct = {f'{n}':i for n,i in enumerate(('Gift','Borrow','Lend','Payment'))}
    data = Transaction.objects.filter(receiver=request.user).last()
    if data.destination:
        return HttpResponse(f"{data.pk} {data.money} {dct[data.destination]}")
    return HttpResponse(f"{data.pk} {data.money}")

def transfer(request):
    receiver = User.objects.get(pk=request.POST['receiver'])
    sender = User.objects.get(pk=request.POST['sender'])
    summ = int(request.POST['sum'])
    new = Transaction(receiver=receiver,sender=sender,money=summ)
    try:
        new.destination = request.POST['destin']
    except:
        pass
    a = Account.objects.get(pk=receiver.pk)
    b = Account.objects.get(pk=sender.pk)
    a.money += summ
    a.save()
    b.money -= summ
    b.save()
    new.save()
    return HttpResponse('Перевод осуществлён')

def main(request):
    return render(request,'Login.html')

def Login(request): #аутентификация/authentication
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            login(request,user)
            return HttpResponse(username)
