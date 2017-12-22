from rest_framework import serializers
from catalogManagement.models import Category, ValidFor
from datetime import datetime


class ValidForSerializer(serializers.Serializer):
    class Meta:
        model = ValidFor
        fields = ('startDateTime', 'endDateTime')

    def validate(self, data):
        print(data)


class CategorySerializer(serializers.Serializer):
    validFor_startDateTime = serializers.CharField(required=False)
    validFor_endDateTime = serializers.CharField(required=False)
    validFor = serializers.OrderedDict()
    href = serializers.CharField(max_length=200)
    version = serializers.CharField(max_length=200)
    lastUpdate = serializers.CharField(required=False)
    lifecycleStatus = serializers.CharField(max_length=10, required=False)
    parentId = serializers.CharField(max_length=200, required=False)
    isRoot = serializers.BooleanField()
    name = serializers.CharField()
    description = serializers.CharField(required=False)

    def check_dates(self, start, end):
        date_format = "%Y-%m-%dT%H:%M:%S"
        startTime = datetime.strptime(start, date_format)
        endTime = datetime.strptime(end, date_format)
        if startTime > endTime:
            raise serializers.ValidationError("finish must occur after start")
        return True

    def validate(self, attrs):
        print("initial data:")
        print(self.initial_data)
        attrs.update(self.initial_data['validFor'])

        print("pre-validation data:\n{}".format(attrs))
        if self.check_dates(attrs['startDateTime'], attrs['endDateTime']):
            return attrs

    def create(self, validated_data):
        print("Create from CategorySerializer: {}".format(validated_data))
        return Category.objects.create(validFor_startDateTime=validated_data.pop('startDateTime'),
                                       validFor_endDateTime=validated_data.pop('endDateTime'),
                                       **validated_data)