# coding: utf-8

from committeeVotes.models import Bill, Meeting, Minister, Vote, VoteType
from rest_framework import serializers


class DynamicFieldsMixin(object):

    """
    A serializer mixin that takes an additional `fields` argument that controls
    which fields should be displayed.
    Usage::
        class MySerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
            class Meta:
                model = MyModel
    Copied from https://gist.github.com/dbrgn/4e6fc1fe5922598592d6
    """

    def __init__(self, *args, **kwargs):
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            fields = self.context['request'].QUERY_PARAMS.get('fields')
            if fields:
                fields = fields.split(',')
                # Drop any fields that are not specified in the `fields`
                # argument.
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class VoteSerializer(serializers.ModelSerializer):
    vote = serializers.StringRelatedField()
    minister = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ('vote', 'minister')


class VoteListSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return obj.minister


class MinisterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minister
        fields = ('id', 'name', 'photo_url', 'coop')


class VoteBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name')


class BillSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name', 'oknesset_url', 'passed')


class BillVoteSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):
    yay = serializers.SerializerMethodField()
    nay = serializers.SerializerMethodField()
    sustained = serializers.SerializerMethodField()
    others = serializers.SerializerMethodField()

    def get_votes(self, bill, voteTypeName):
        voteType = VoteType.objects.get(typeName=voteTypeName)
        votes = Vote.objects.select_related('minister').filter(vote=voteType, bill=bill)
        voted_ministers = []
        for v in votes:
            voted_ministers.append(v.minister.id)
        qs = Minister.objects.filter(id__in=voted_ministers)
        serializer = MinisterListSerializer(instance=qs, many=True)
        return serializer.data

    def get_other_ministers(self, bill):
        votes = Vote.objects.select_related('minister').filter(bill=bill)
        voted_ministers = []
        for v in votes:
            voted_ministers.append(v.minister.id)
        qs = Minister.objects.exclude(id__in=voted_ministers)
        serializer = MinisterListSerializer(instance=qs, many=True)
        return serializer.data

    def get_yay(self, bill):
        return self.get_votes(bill, u'בעד')

    def get_nay(self, bill):
        return self.get_votes(bill, u'נגד')

    def get_sustained(self, bill):
        return self.get_votes(bill, u'נמנע')

    def get_others(self, bill):
        return self.get_other_ministers(bill)

    class Meta:
        model = Bill
        fields = ('id', 'name', 'oknesset_url', 'passed', 'yay', 'nay', 'sustained', 'others')


class MinisterSerializer(MinisterListSerializer):

    class Meta(MinisterListSerializer.Meta):
        fields = MinisterListSerializer.Meta.fields + ('title',
                  'facebook', 'twitter', 'mail', 'phone', 'oknesset')


class MinisterVoteSerializer(serializers.ModelSerializer):
    bill = VoteBillSerializer()
    vote = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ('bill', 'vote')




class MeetingListSerializer(serializers.ModelSerializer):
    bill_count = serializers.IntegerField(
        source='proposed_bill_count',
        read_only=True
    )

    class Meta:
        model = Meeting
        fields = ('id', 'took_place', 'bill_count')


class MinisterInMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Minister
        fields = ('id', 'name', 'url')


class MeetingSerializer(serializers.ModelSerializer):
    proposed_bills = BillSerializer(many=True, read_only=True)
    voting_ministers = MinisterListSerializer(many=True, read_only=True)
    missing_ministers = MinisterListSerializer(many=True, read_only=True)
    non_voting_ministers = serializers.SerializerMethodField()

    def get_non_voting_ministers(self, meeting):
        voting_ministers = meeting.voting_ministers.all()
        voting_ids = voting_ministers.values_list('id', flat=True)
        missing_ministers = meeting.missing_ministers.all()
        missing_ids = missing_ministers.values_list('id', flat=True)
        qs = Minister.objects.exclude(id__in=voting_ids).exclude(id__in=missing_ids)
        serializer = MinisterListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Meeting


class MeetingBillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ('id', 'took_place')


class BillDetailSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)
    meeting = MeetingBillSerializer(many=True, read_only=True)

    class Meta:
        model = Bill


class MeetingDetailSerializer(serializers.HyperlinkedModelSerializer):
    proposed_bills = BillVoteSerializer(many=True, read_only=True)
    voting_ministers = MinisterListSerializer(many=True, read_only=True)
    missing_ministers = MinisterListSerializer(many=True, read_only=True)
    non_voting_ministers = serializers.SerializerMethodField()

    def get_non_voting_ministers(self, meeting):
        voting_ministers = meeting.voting_ministers.all()
        voting_ids = voting_ministers.values_list('id', flat=True)
        missing_ministers = meeting.missing_ministers.all()
        missing_ids = missing_ministers.values_list('id', flat=True)
        qs = Minister.objects.exclude(id__in=voting_ids).exclude(id__in=missing_ids)
        serializer = MinisterListSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Meeting
