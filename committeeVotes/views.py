from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from committeeVotes.models import Bill, Minister, Vote, VoteType

def index(request):
    bills = Bill.objects.all()[:10]
    ministers = Minister.objects.all()
    context = {'bills': bills,
               'ministers': ministers}
    return render(request, 'committeeVotes/index.html', context)

def detail(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    votes = Vote.objects.select_related('minister').filter(bill=bill)
    vote_types = VoteType.objects.all().order_by('id')
    votes_by_type = {}
    for vt in vote_types:
        votes_by_type[vt.typeName] = votes.filter(vote=vt)
    voted_ministers = []
    for v in votes:
        voted_ministers.append(v.minister.id)
    non_voting_ministers = Minister.objects.exclude(id__in=voted_ministers)
    context = {'bill': bill,
               'votes_by_type': sorted(votes_by_type.iteritems()),
               'unknown_ministers': non_voting_ministers}
    return render(request, 'committeeVotes/detail.html', context)

def minister_details(request, minister_id):
    minister = get_object_or_404(Minister,pk=minister_id)
    votes = Vote.objects.filter(minister=minister)
    context = {'minister': minister,
               'votes': votes}
    return render(request, 'committeeVotes/minister_detail.html', context)

def bills(request):
    bills = Bill.objects.all()
    context = {'bills': bills}
    return render(request, 'committeeVotes/bills.html', context)

def ministers(request):
    ministers = Minister.objects.all()
    context = {'ministers': ministers}
    return render(request, 'committeeVotes/ministers.html', context)

