import json

from rest_framework import serializers

from django.contrib.auth import get_user_model

from message_coding.apps.coding import models as coding_models
from message_coding.apps.project import models as project_models
from message_coding.apps.dataset import models as dataset_models


# http://stackoverflow.com/questions/24852555/how-to-exclude-parent-when-serializer-is-nested-when-using-django-rest-framework
class ExclusiveModelSerializer(serializers.ModelSerializer):
    """
    A HyperlinkedModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        # Instantiate the superclass normally
        super(ExclusiveModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude:
            # Drop fields that are specified in the `exclude` argument.
            excluded = set(exclude)
            for field_name in excluded:
                try:
                    self.fields.pop(field_name)
                except KeyError:
                    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'is_staff', 'projects',
                  'projects_owned', 'tasks_owned', 'tasks_assigned')

class OrderedListSerializer(serializers.ListSerializer):

    # def to_representation(self, data):
    #     """
    #     List of object instances -> List of dicts of primitive datatypes.
    #     """
    #     # Dealing with nested relationships, data can be a Manager,
    #     # so, first get a queryset from the Manager if needed
    #     iterable = data.all() if isinstance(data, (models.Manager, query.QuerySet)) else data
    #     return [
    #         self.child.to_representation(item) for item in iterable
    #     ]

    def update(self, instances, validated_data):
        # Maps for id->instance and id->data item.
        instance_map = {instance.pk: instance for instance in instances}

        # Perform creations and updates.
        return_instances = []
        id_set = set()
        for item in validated_data:
            instance = instance_map.get(item['id'], None)
            if instance is None:
                return_instances.append(self.child.create(item))
            else:
                return_instances.append(self.child.update(instance, item))
                id_set.add(instance.pk)

        # Perform deletions.
        for id, instance in instance_map.items():
            if id not in id_set:
                instance.delete()

        return return_instances


class CodeSerializer(ExclusiveModelSerializer):
    class Meta:
        model = coding_models.Code
        fields = ('id', 'name', 'description', 'code_group',)
        list_serializer_class = OrderedListSerializer


class CodeGroupSerializer(ExclusiveModelSerializer):

    class Meta:
        model = coding_models.CodeGroup
        fields = ('id', 'name', 'description', 'codes', 'scheme',)
        list_serializer_class = OrderedListSerializer

    codes = CodeSerializer(many=True)


# Serializers define the API representation.
class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = coding_models.Scheme
        fields = ('id', 'name', 'description',
                  'created_at', 'owner', 'project', 'code_groups', )
        read_only_fields = ('created_at', 'owner', )

    code_groups = CodeGroupSerializer(many=True)

class DatasetSerializer(serializers.ModelSerializer):
    min_time = serializers.DateTimeField()
    max_time = serializers.DateTimeField()
    class Meta:
        model = dataset_models.Dataset
        fields = ('id', 'name', 'description', 'slug', 'created_at',
                  'owner', 'projects', 'min_time', 'max_time')
        read_only_fields = ('created_at',)


class TypedBlobField(serializers.Field):
    """
    This field translates binary descriptions in the database for the REST api.
    It uses a second field on the model, the 'type' field,
    to determine how to encode and decode the blob field.
    """

    def __init__(self,
                 type_field='type',
                 default_type='json',
                 **kwargs):
        self.type_field = type_field
        self.default_type = default_type
        self.value_type = default_type

        super(TypedBlobField, self).__init__(**kwargs)

    def to_representation(self, value):
        if self.value_type == 'json':
            return json.loads(value)
        else:
            return value

    def to_internal_value(self, data):
        if self.value_type == 'json':
            return json.dumps(data)
        else:
            return data

    def get_value(self, dictionary):
        self.value_type = dictionary.get(self.type_field, self.default_type)
        return super(TypedBlobField, self).get_value(dictionary)

    def get_attribute(self, instance):
        self.value_type = getattr(instance, self.type_field, self.default_type)
        return super(TypedBlobField, self).get_attribute(instance)


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = dataset_models.Selection
        fields = ('id', 'created_at', 'owner', 'dataset', 'type', 'selection', 'size')
        read_only_fields = ('created_at', 'owner', 'size',)

    selection = TypedBlobField(type_field='type', default_type='json')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = dataset_models.Message
        fields = ('id', 'sender', 'time', 'text', 'dataset')


class TaskSerializer(serializers.ModelSerializer):
    selection = SelectionSerializer()

    class Meta:
        model = project_models.Task
        fields = ('id', 'name', 'description', 'selection',
                  'created_at', 'owner', 'project', 'scheme', 'assigned_coders')
        read_only_fields = ('created_at', 'owner',)


    def create(self, validated_data):
        # Create the nested selection
        selection_data = validated_data.pop('selection')
        if 'owner' not in selection_data:
            selection_data['owner'] = validated_data['owner']

        selection = dataset_models.Selection.objects.create(**selection_data)
        validated_data['selection'] = selection
        return super(TaskSerializer, self).create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Project
        fields = ('id', 'name', 'description',
                  'slug', 'created_at', 'owner', 'members',
                  'tasks', 'schemes', 'datasets')
        read_only_fields = ('created_at', 'owner',)


class CodeInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.CodeInstance
        fields = ('id', 'created_at',
                  'owner', 'task',
                  'message', 'code',)
        read_only_fields = ('created_at', 'owner',)
