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

def results(request, bill_id):
    return HttpResponse("You're looking at the results of bill %s." % poll_id)

def vote(request, bill_id):
    return HttpResponse("You're voting on bill %s." % poll_id)

# Create your views here.
