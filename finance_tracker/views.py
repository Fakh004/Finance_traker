from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transaction, Balance, UserProfile
from decimal import Decimal
from django.utils import timezone
from decimal import InvalidOperation

def user_required(request):
    if not request.user.is_authenticated:
        return HttpResponse("Login required")
    return None

def transaction_list(request):
    auth = user_required(request)
    if auth:
        return auth

    transactions = Transaction.objects.filter(user=request.user)

    amount = request.GET.get("amount")
    if amount:
        try:
            amount = Decimal(amount)
            transactions = transactions.filter(amount=amount)
        except:
            pass

    search_desc = request.GET.get("search")
    if search_desc:
        transactions = transactions.filter(description__icontains=search_desc)

    today = timezone.now().date()
    if request.GET.get("today_only") == "1":
        transactions = transactions.filter(transaction_date__date=today)

    return render(request, "transaction_list.html", {"transactions": transactions})


def add_transaction(request):
    auth = user_required(request)
    if auth:
        return auth

    if request.method == "GET":
        return render(request, "create.html")

    user_balance, _ = Balance.objects.get_or_create(user=request.user)

    try:
        amount = Decimal(request.POST.get("amount"))
    except:
        return HttpResponse("Invalid amount")

    transaction_type = request.POST.get("transaction_type")
    description = request.POST.get("description")

    if transaction_type == "EXPENSE" and user_balance.amount < amount:
        return HttpResponse("Not enough balance for this expense")

    tx = Transaction.objects.create(
        transaction_type=transaction_type,
        amount=amount,
        description=description,
        user=request.user
    )

    if transaction_type == "EXPENSE":
        user_balance.amount -= amount
    else:
        user_balance.amount += amount
    user_balance.save()

    return redirect("get_transaction")



def transaction_detail(request, pk):
    auth = user_required(request)
    if auth:
        return auth

    tx = Transaction.objects.filter(id=pk, user=request.user).first()
    if not tx:
        return HttpResponse("Not found")

    return render(request, "transaction_detail.html", {"transaction": tx})



def transaction_edit(request, pk):
    tx = Transaction.objects.filter(id=pk, user=request.user).first()
    if not tx:
        return HttpResponse("Transaction not found")

    if request.method == "GET":
        return render(request, "create.html", {"transaction": tx})

    try:
        new_amount = Decimal(request.POST.get("amount"))
        new_type = request.POST.get("transaction_type", "").upper()
    except:
        return HttpResponse("Invalid data")

    description = request.POST.get("description", "")
    
    tx.amount = new_amount
    tx.transaction_type = new_type
    tx.description = description

    try:
        tx.save()  
    except ValueError as e:
        return HttpResponse(str(e))

    return redirect("get_transaction")






def delete_transaction(request, pk):
    auth = user_required(request)
    if auth:
        return auth

    tx = Transaction.objects.filter(id=pk, user=request.user).first()
    if not tx:
        return HttpResponse("Not found")

    if request.method == "GET":
        return render(request, "confirm_delete.html", {"transaction": tx})

    balance, _ = Balance.objects.get_or_create(user=request.user)

    if tx.transaction_type.upper() == 'EXPENSE':
        balance.amount += tx.amount
    elif tx.transaction_type.upper() == 'INCOME':
        balance.amount -= tx.amount
    balance.save()

    tx.delete()
    return redirect("get_transaction")




def get_transaction(request):
    auth = user_required(request)
    if auth:
        return auth

    balance, _ = Balance.objects.get_or_create(user=request.user)

    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

    amount = request.GET.get("amount")
    if amount:
        try:
            amount = Decimal(amount)
            transactions = transactions.filter(amount=amount)
        except:
            pass

    search_desc = request.GET.get("search")
    if search_desc:
        transactions = transactions.filter(description__icontains=search_desc)

    if request.GET.get("today_only") == "1":
        today = timezone.now().date()
        transactions = transactions.filter(transaction_date__date=today)

    return render(request,'home.html',
        {
            'user': request.user,
            'balance': balance,
            'transactions': transactions,
            'request': request, 
        }
    )


def profile_view(request):
    auth = user_required(request)
    if auth:
        return auth
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"user": request.user, "profile": profile})


def edit_profile(request):
    auth = user_required(request)
    if auth:
        return auth

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "GET":
        return render(request, "edit_profile.html", {"profile": profile})

    profile.bio = request.POST.get("bio", profile.bio)
    profile.phone_number = request.POST.get("phone_number", profile.phone_number)
    profile.address = request.POST.get("address", profile.address)

    if 'image' in request.FILES:
        profile.image = request.FILES['image']

    profile.save()

    return redirect("profile")
