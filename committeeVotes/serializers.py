from committeeVotes.models import Bill, Meeting, Minister
from rest_framework import serializers


class BillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bill
        fields = ('name', 'oknesset_url', 'passed')


class MinisterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Minister
        fields = ('name', 'title')