from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from committeeVotes.models import Bill, Minister, Vote

def index(request):
    bills = Bill.objects.all()
    ministers = Minister.objects.all()
    context = {'bills': bills,
               'ministers' : ministers}
    return render(request, 'committeeVotes/index.html', context)

def detail(request, bill_id):
    bill = get_object_or_404(Bill,pk=bill_id)
    votes = Vote.objects.filter(bill=bill)
    context = {'bill': bill,
               'votes' : votes}
    return render(request, 'committeeVotes/detail.html', context)

def minister_details(request, minister_id):
    minister = get_object_or_404(Minister,pk=minister_id)
    votes = Vote.objects.filter(minister=minister)
    context = {'minister': minister,
               'votes' : votes}
    return render(request, 'committeeVotes/minister_detail.html', context)
