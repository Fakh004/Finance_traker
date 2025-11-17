from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction, CustomUser, Balance
from decimal import Decimal


def transaction_list(request):
    transactions = request.objets.all()
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    if transactions:
        transactions = Transaction.filter(amount__icontains=transactions)
    # from_salary = request.GET.get('from_salary', None)
    return render(request, "transaction_list.html", {"transactions": transactions})

def add_transaction(request):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    if request.method == "GET":
        return render(request, "create.html")
    Transaction.objects.create(
        transaction_type=request.POST.get("transaction_type"),
        amount=Decimal(request.POST.get("amount")),
        description=request.POST.get("description"),
        user=request.user
    )
    return redirect("get_transaction")

def transaction_detail(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    tx = Transaction.objects.filter(id=pk, user=request.user).first()
    if not tx:
        return HttpResponse("Not found")
    return render(request, "transaction_detail.html", {"transaction": tx})

def update_transaction(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    tx = Transaction.objects.filter(id=pk, user=request.user).first()
    if not tx:
        return HttpResponse("Not found")
    if request.method == "GET":
        return render(request, "create.html", {"transaction": tx})
    
    old_type = tx.transaction_type
    old_amount = tx.amount
    
    new_type = request.POST.get("transaction_type", tx.transaction_type)
    new_amount = Decimal(request.POST.get("amount", tx.amount))
    tx.transaction_type = new_type
    tx.amount = new_amount
    tx.description = request.POST.get("description", tx.description)
    
    balance = Balance.objects.filter(user=request.user).first()
    if balance:
        if old_type == 'EXPENSE':
            balance.amount += old_amount
        else:
            balance.amount -= old_amount
        
        if new_type == 'EXPENSE':
            balance.amount -= new_amount
        else:
            balance.amount += new_amount
        
        balance.save()
    
    tx.save()
    return redirect("transaction_detail", pk=tx.id)


def get_transaction(request):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    return render(request, 'home.html', {
        'user': request.user,
        'balance': request.user.balance,
        'transactions': request.user.transactions.all()
    })


def delete_transaction(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    tx = Transaction.objects.filter(id=pk, user=request.user).first()
    if not tx:
        return HttpResponse("Not found")
    if request.method == "GET":
        return render(request, "confirm_delete.html", {"transaction": tx})
    
    balance = Balance.objects.filter(user=request.user).first()
    if balance:
        if tx.transaction_type == 'EXPENSE':
            balance.amount += tx.amount
        else:
            balance.amount -= tx.amount
        balance.save()
    
    tx.delete()
    return redirect("get_transaction")

def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    return render(request, "profile.html", {"user": request.user, "profile": request.user.profile})

def edite_profile(request):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    if request.method == "GET":
        return render(request, "edit_profile.html", {"profile": request.user.profile})
    
    profile = request.user.profile
    profile.bio = request.POST.get("bio", profile.bio)
    profile.phone_number = request.POST.get("phone_number", profile.phone_number)
    profile.address = request.POST.get("address", profile.address)
    
    if 'image' in request.FILES:
        profile.image = request.FILES['image']
    
    profile.save()
    return redirect("profile")