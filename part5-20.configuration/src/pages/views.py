from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account


@login_required
@csrf_exempt
def transferView(request):
	
	if request.method == 'POST':
		sender = request.user.id
		receiver = User.objects.get(username=request.GET.get('to'))
		amount = int(request.GET.get('amount'))

		if sender != receiver and amount > 0:
			acc1 = Account.objects.get(iban=sender)
			acc2 = Account.objects.get(iban=receiver)

			if acc1.balance >= amount:
				acc1.balance -= amount
				acc2.balance += amount

				acc1.save()
				acc2.save()


	
	return redirect('/')



@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
