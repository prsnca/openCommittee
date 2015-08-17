# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from committeeVotes.models import Bill, Minister, Vote, VoteType, Meeting
from committeeVotes.serializers import BillSerializer, MinisterSerializer,MinisterListSerializer, MeetingSerializer,MeetingListSerializer
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
import json


def index(request):
    bills = Bill.objects.all().order_by('-id')[:10]
    ministers = Minister.objects.all().order_by('id')
    context = {'bills': bills,
               'ministers': ministers}
    return render(request, 'committeeVotes/index.html', context)


def search(request):
    ministerSearch = [dict([("url", reverse('minister', args=(minister.id,))),
                            ("name", minister.name),
                            ("type", "שר"),
                            ("tokens", [minister.name])]) for minister in Minister.objects.all()]
    billsSearch = [dict([("url", reverse('detail', args=(bill.id,))),
                         ("name", bill.name),
                         ("type", "הצעת חוק"),
                         ("tokens", [bill.name])]) for bill in Bill.objects.all()]
    searchResults = ministerSearch + billsSearch
    return HttpResponse(json.dumps(searchResults), content_type="application/json")


def searchBills(request):
    billsSearch = {'objects': [dict([("url", reverse('bill', args=(bill.id,))),
                                     ("name", bill.name)]) for bill in Bill.objects.all()]}
    return HttpResponse(json.dumps(billsSearch), content_type="application/json")


def searchMinisters(request):
    ministerSearch = {'objects': [dict([("url", reverse('minister', args=(minister.id,))),
                                        ("name", minister.name)]) for minister in Minister.objects.all()]}
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
    minister = get_object_or_404(Minister, pk=minister_id)
    votes = Vote.objects.filter(minister=minister).order_by('-id')
    context = {'minister': minister,
               'votes': votes}
    return render(request, 'committeeVotes/minister_detail.html', context)


def bills(request):
    bills = Bill.objects.all().order_by('-id')
    context = {'bills': bills}
    return render(request, 'committeeVotes/bills.html', context)


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


def ministers(request):
    ministers = Minister.objects.all()
    context = {'ministers': ministers}
    return render(request, 'committeeVotes/ministers.html', context)


class MinisterViewSet(viewsets.ModelViewSet):
    queryset = Minister.objects.all()
    def get_serializer_class(self):
        print "serializer_class"
        if self.action == 'list':
            print "MinisterList"
            return MinisterListSerializer
        if self.action == 'retrieve':
            return MinisterSerializer
        return None    

def meetings(request):
    meetings = Meeting.objects.all().order_by('-id')
    context = {'meetings': meetings}
    return render(request, 'committeeVotes/meetings.html', context)


class MeetingsViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.annotate(
        proposed_bill_count=Count('proposed_bills')).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MeetingListSerializer
        if self.action == 'retrieve':
            return MeetingSerializer
        return None


def about(request):
    return render(request, 'committeeVotes/about.html')


def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    bills = meeting.proposed_bills.all()
    context = {'meeting': meeting,
               'bills': bills}
    return render(request, 'committeeVotes/meeting_detail.html', context)
