# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from committeeVotes.models import Bill, Minister, Vote, VoteType, Meeting
from committeeVotes.serializers import MinisterVoteSerializer, BillSerializer, BillVoteSerializer, BillDetailSerializer, MinisterSerializer, MinisterListSerializer, MeetingSerializer, MeetingDetailSerializer, MeetingListSerializer, MeetingDetailSerializer
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from committeeVotes.serializers import BillSerializer, MinisterSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
import json

def index(request):
    bills = Bill.objects.all().order_by('-id')[:10]
    last_meeting = Meeting.objects.all().order_by('-id')[0]
    votingMinisters = last_meeting.voting_ministers.all()
    votingIds = votingMinisters.values_list('id', flat=True)
    missingMinisters = last_meeting.missing_ministers.all()
    missingIds = missingMinisters.values_list('id', flat=True)
    nonVotingMinisters = Minister.objects.exclude(id__in=votingIds).exclude(id__in=missingIds)
    context = {'bills': bills,
               'last_meeting': last_meeting,
               'votingMinisters': votingMinisters,
               'missingMinisters': missingMinisters,
               'nonVotingMinisters': nonVotingMinisters}
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

def last_meeting(request):
    last_meeting = Meeting.objects.latest('took_place')
    serializer = MeetingDetailSerializer(last_meeting, context={'request': request})
    return HttpResponse(json.dumps(serializer.data), content_type="application/json")


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
    meeting = votes[0].meeting if len(votes) > 0 else None
    votes_by_type = {}
    for vt in vote_types:
        votes_by_type[vt.typeName] = votes.filter(vote=vt)
    voted_ministers = []
    for v in votes:
        voted_ministers.append(v.minister.id)
    non_voting_ministers = Minister.objects.exclude(id__in=voted_ministers)
    context = {'bill': bill,
               'votes_by_type': sorted(votes_by_type.iteritems()),
               'unknown_ministers': non_voting_ministers,
               'meeting': meeting}
    return render(request, 'committeeVotes/bill.html', context)


def minister_details(request, minister_id):
    minister = get_object_or_404(Minister,pk=minister_id)
    all_votes = Vote.objects.filter(minister=minister).order_by('-id')
    paginator = Paginator(all_votes, 12)
    page = request.GET.get('page')
    try:
        votes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        votes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        votes = paginator.page(paginator.num_pages)

    context = {'minister': minister,
               'votes': votes}
    return render(request, 'committeeVotes/minister_detail.html', context)


def bills(request):
    bills = Bill.objects.all().order_by('-id')
    context = {'bills': bills}
    return render(request, 'committeeVotes/bills.html', context)


class BillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bill.objects.all()
    def get_serializer_class(self):
        if self.action == 'list':
            return BillSerializer
        if self.action == 'retrieve':
            return BillVoteSerializer
        return None


def ministers(request):
    ministers = Minister.objects.all()
    context = {'ministers': ministers}
    return render(request, 'committeeVotes/ministers.html', context)


class MinisterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Minister.objects.all()
    def get_serializer_class(self):
        if self.action == 'list':
            return MinisterListSerializer
        if self.action == 'retrieve':
            return MinisterSerializer
        return None

    @detail_route()
    def votes(self, request, pk):
        minister = self.get_object()
        votes = minister.votes.all()
        page = self.paginate_queryset(votes)
        if page is not None:
            serializer = MinisterVoteSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = MinisterVoteSerializer(votes, many=True, context={'request': request})
        return Response(serializer.data)




def meetings(request):
    meetings = Meeting.objects.all().order_by('-id')
    context = {'meetings': meetings}
    return render(request, 'committeeVotes/meetings.html', context)


class MeetingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meeting.objects.order_by('-took_place').annotate(
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
    votingMinisters = meeting.voting_ministers.all()
    votingIds = votingMinisters.values_list('id', flat=True)
    missingMinisters = meeting.missing_ministers.all()
    missingIds = missingMinisters.values_list('id', flat=True)
    nonVotingMinisters = Minister.objects.exclude(id__in=votingIds).exclude(id__in=missingIds)
    context = {'meeting': meeting,
               'bills': bills,
               'votingMinisters': votingMinisters,
               'missingMinisters': missingMinisters,
               'nonVotingMinisters': nonVotingMinisters}
    return render(request, 'committeeVotes/meeting_detail.html', context)
