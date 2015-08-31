from committeeVotes.models import Bill, Meeting, Minister
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


class BillSerializer(DynamicFieldsMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name', 'oknesset_url', 'passed')

class MinisterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minister
        fields = ('id', 'name', 'photo_url', 'coop')

class MinisterSerializer(MinisterListSerializer):

    class Meta(MinisterListSerializer.Meta):
        fields = MinisterListSerializer.Meta.fields + ('title',
                  'facebook', 'twitter', 'mail', 'phone', 'oknesset')


class MeetingListSerializer(serializers.ModelSerializer):
    bill_count = serializers.IntegerField(
        source='proposed_bill_count',
        read_only=True
    )

    class Meta:
        model = Meeting
        fields = ('id', 'took_place', 'bill_count')


class BillInMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'name')


class MeetingSerializer(serializers.ModelSerializer):
    proposed_bills = BillInMeetingSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
