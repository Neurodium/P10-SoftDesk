from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer
from rest_framework import serializers


from project.models import Users, Projects, Issues, Contributors, Comments


class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginUserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['email', 'password']

class ProjectCreateSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type']


class ProjectContributor(Serializer):
    email = serializers.EmailField()


class UsersDetailsSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'email', 'last_name', 'first_name']


class ContributorsDetailsSerializer(ModelSerializer):
    user_id = UsersDetailsSerializer()

    class Meta:
        model = Contributors
        fields = ['project_id', 'user_id', 'role' ]


class IssuesDetailsSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = '__all__'


class IssueCreateSerializer(ModelSerializer):

    class Meta:
        model = Issues
        exclude = ['project_id', 'author_user_id', 'assignee_user_id']


class IssueModifySerializer(ModelSerializer):

    class Meta:
        model = Issues
        exclude = ['project_id', 'author_user_id']




