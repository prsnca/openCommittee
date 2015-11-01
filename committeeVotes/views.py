# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from committeeVotes.models import Bill, Minister, Vote, VoteType, Meeting
import json


def index(request):
    bills = Bill.objects.all().order_by('-id')[:10]
    last_meeting = Meeting.objects.all().order_by('-id')[0]
    votingMinisters = last_meeting.voting_ministers.all()
    votingIds = votingMinisters.values_list('id', flat=True)
    nonVotingMinisters = Minister.objects.exclude(id__in=votingIds)
    context = {'bills': bills,
               'last_meeting': last_meeting,
               'votingMinisters': votingMinisters,
               'nonVotingMinisters': nonVotingMinisters}
    return render(request, 'committeeVotes/index.html', context)

def search(request):
    ministerSearch = [dict([("url", reverse('minister', args=(minister.id,))),
                            ("name", minister.name),
                            ("type", "שר"),
                            ("tokens",[minister.name])]) for minister in Minister.objects.all()]
    billsSearch = [dict([("url", reverse('detail', args=(bill.id,))),
                         ("name", bill.name),
                         ("type", "הצעת חוק"),
                         ("tokens",[bill.name])]) for bill in Bill.objects.all()]
    searchResults = ministerSearch + billsSearch
    return HttpResponse(json.dumps(searchResults), content_type="application/json")


def searchBills(request):
    billsSearch = {'objects': [dict([("url", reverse('bill', args=(bill.id,))),
                         ("name",bill.name)]) for bill in Bill.objects.all()]}
    return HttpResponse(json.dumps(billsSearch), content_type="application/json")

def searchMinisters(request):
    ministerSearch = {'objects': [dict([("url", reverse('minister', args=(minister.id,))),
                            ("name",minister.name)]) for minister in Minister.objects.all()]}
    return HttpResponse(json.dumps(ministerSearch), content_type="application/json")

def bill(request, bill_id):
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
    return render(request, 'committeeVotes/bill.html', context)

def minister_details(request, minister_id):
    minister = get_object_or_404(Minister,pk=minister_id)
    votes = Vote.objects.filter(minister=minister).order_by('-id')
    context = {'minister': minister,
               'votes': votes}
    return render(request, 'committeeVotes/minister_detail.html', context)

def bills(request):
    bills = Bill.objects.all().order_by('-id')
    context = {'bills': bills}
    return render(request, 'committeeVotes/bills.html', context)

def ministers(request):
    ministers = Minister.objects.all()
    context = {'ministers': ministers}
    return render(request, 'committeeVotes/ministers.html', context)

def meetings(request):
    meetings = Meeting.objects.all().order_by('-id')
    context = {'meetings': meetings}
    return render(request, 'committeeVotes/meetings.html', context)

def about(request):
    return render(request, 'committeeVotes/about.html')

def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting,pk=meeting_id)
    bills = meeting.proposed_bills.all()
    votingMinisters = meeting.voting_ministers.all()
    votingIds = votingMinisters.values_list('id', flat=True)
    nonVotingMinisters = Minister.objects.exclude(id__in=votingIds)
    context = {'meeting': meeting,
               'bills': bills,
               'votingMinisters': votingMinisters,
               'nonVotingMinisters': nonVotingMinisters}
    return render(request, 'committeeVotes/meeting_detail.html', context)

