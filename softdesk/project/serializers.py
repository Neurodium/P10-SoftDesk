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


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email']


class ProjectCreateSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type']


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title']


class ContributorProjectList(ModelSerializer):
    project_id = SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ['project_id']

    def get_project_id(self, obj):
        queryset = Projects.objects.get(title=obj.project_id.title)
        serializer = ProjectListSerializer(queryset)
        return serializer.data


class ProjectDetailSerializer(ModelSerializer):
    author_user_id = SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def get_author_user_id(self, obj):
        queryset = Users.objects.get(email=obj.author_user_id)
        serializer = UserDetailSerializer(queryset)
        return serializer.data


class ProjectUpdateSerializer(ModelSerializer):

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

    author_user_id = SerializerMethodField()
    assignee_user_id = SerializerMethodField()
    project_id = SerializerMethodField()

    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'status', 'created_time', 'author_user_id', 'assignee_user_id', 'project_id']

    def get_author_user_id(self, obj):
        queryset = Users.objects.get(email=obj.author_user_id)
        serializer = UserDetailSerializer(queryset)
        return serializer.data

    def get_assignee_user_id(self, obj):
        queryset = Users.objects.get(email=obj.assignee_user_id)
        serializer = UserDetailSerializer(queryset)
        return serializer.data

    def get_project_id(self, obj):
        queryset = Projects.objects.get(id=obj.project_id.id)
        serializer = ProjectDetailSerializer(queryset)
        return serializer.data


class IssueCreateSerializer(ModelSerializer):

    class Meta:
        model = Issues
        exclude = ['project_id', 'author_user_id', 'assignee_user_id']


class IssueModifySerializer(ModelSerializer):
    assignee_user_id = serializers.EmailField(max_length=60)

    class Meta:
        model = Issues
        exclude = ['project_id', 'author_user_id']


class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['description']


class CommentsListSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'description']

class CommentDetailSerializer(ModelSerializer):

    author_user_id = SerializerMethodField()
    issue_id = SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'description', 'created_time', 'issue_id', 'author_user_id']

    def get_author_user_id(self, obj):
        queryset = Users.objects.get(email=obj.author_user_id)
        serializer = UserDetailSerializer(queryset)
        return serializer.data

    def get_issue_id(self, obj):
        queryset = Issues.objects.get(id=obj.issue_id.id)
        serializer = IssuesDetailsSerializer(queryset)
        return serializer.data



