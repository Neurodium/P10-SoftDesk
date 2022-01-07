from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django.http import Http404

from .pagination import PaginationHandlerMixin
from .models import Users, Projects, Contributors, Issues, Comments
from project.serializers import CreateUserSerializer, \
    ProjectListSerializer, ProjectDetailSerializer, ProjectUpdateSerializer, ProjectCreateSerializer, \
    ProjectContributor, ContributorsDetailsSerializer, IssuesDetailsSerializer, IssueCreateSerializer, \
    IssueModifySerializer, CommentCreateSerializer, CommentsListSerializer, CommentDetailSerializer, \
    ContributorProjectList



# Create your views here.
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class CreateUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data['email']
        try:
            user = Users.objects.get(email=email)
        except BaseException as error:
            raise ValidationError({"400": f'{str(error)}'})

        if user.is_active:
            token = RefreshToken.for_user(user)
            response = {"email": email,
                        "token": str(token),
                        "access": str(token.access_token), }
            return Response(response, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"400": f'{user.last_name} {user.first_name} is not active'})


class UserProjectList(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = BasicPagination

    def get(self, request):
        contributor = Contributors.objects.filter(user_id=request.user)
        if not contributor:
            return Response("No Data")
        page = self.paginate_queryset(contributor)
        if page is not None:
            serializer = self.get_paginated_response(ContributorProjectList(page, many=True).data)
        else:
            serializer = ContributorProjectList(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        serializer = ProjectCreateSerializer(data=request.data)
        projects = Projects.objects.filter(title=data['title'])
        if not projects:
            if serializer.is_valid():
                serializer.save(author_user_id=request.user)
                project_saved = Projects.objects.get(title=data['title'])
                manager = Contributors(user_id=request.user,
                                        project_id=project_saved,
                                        permission='All Rights',
                                        role='Manager')
                manager.save()
                return Response(str(serializer.data), status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Project already created")


class ManageProject(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    pagination_class = BasicPagination

    def get_project(self, project_id):
        try:
            return Projects.objects.get(id=project_id)
        except Projects.DoesNotExist:
            raise Http404

    def get(self, request, project_id):
        project = self.get_project(project_id)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to view details of project {project.title}")
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        project = self.get_project(project_id)
        if request.user == project.author_user_id:
            data = request.data
            serializer = ProjectUpdateSerializer(project, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"You're not the author of the project {project.title}")

    def delete(self, request, project_id):
        project = self.get_project(project_id)
        if request.user == project.author_user_id:
            content = {"id": project_id,
                       "title": project.title}
            project.delete()
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        return Response(f"You're not the author of the project {project.title}")


class ManageProjectUsers(ManageProject):

    def get_user(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise Http404

    def get(self, request, project_id):
        project = self.get_project(project_id)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to view issues of project {project.title}")
        contributors = Contributors.objects.filter(project_id=project)
        page = self.paginate_queryset(contributors)
        if page is not None:
            serializer = self.get_paginated_response(ContributorsDetailsSerializer(page, many=True).data)
        else:
            serializer = ContributorsDetailsSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = self.get_project(project_id)
        if request.user == project.author_user_id:
            serializer = ProjectContributor(data=request.data)
            if serializer.is_valid():
                try:
                    user = Users.objects.get(email=serializer.data['email'])
                except Users.DoesNotExist:
                    raise Http404
                role = 'Contributor'
                permission = 'Create and Read'
                try:
                    Contributors.objects.get(user_id=user, project_id=project)
                except Contributors.DoesNotExist:
                    contributor = Contributors.objects.create(user_id=user,
                                                              project_id=project,
                                                              role=role,
                                                              permission=permission)
                    contributor.save
                    data = {"email": user.email,
                            "project": project.title,
                            "role": role,
                            "permission": permission}
                    return Response(data, status=status.HTTP_201_CREATED)
                return Response(f"User {user.last_name} {user.first_name} is already a contributor on project "
                                f"{project.title}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"You're not the author of the project {project.title}")

    def delete(self, request, project_id, user_id):
        project = self.get_project(project_id)
        if request.user == project.author_user_id:
            user = self.get_user(user_id)
            contributor = Contributors.objects.get(user_id=user, project_id=project)
            contributor.delete()
            return Response(f"User: {user.last_name} {user.first_name} has been removed from project {project.title}", status=status.HTTP_204_NO_CONTENT)
        return Response(f"You're not the author of the project {project.title}")


class ManageProjectIssues(ManageProject):

    def get_issue(self, issue_id):
        try:
            return Issues.objects.get(id=issue_id)
        except Issues.DoesNotExist:
            raise Http404

    def get(self, request, project_id):
        project = self.get_project(project_id)
        issues = Issues.objects.filter(project_id=project)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to view issues of project {project.title}")
        if not issues:
            return Response("No issues on this project")
        page = self.paginate_queryset(issues)
        if page is not None:
            serializer = self.get_paginated_response(IssuesDetailsSerializer(page, many=True).data)
        else:
            serializer = IssuesDetailsSerializer(issues)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = self.get_project(project_id)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to post issues in project {project.title}")
        serializer = IssueCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project, author_user_id=request.user, assignee_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id, issue_id):
        project = self.get_project(project_id)
        issue = self.get_issue(issue_id)
        if request.user == issue.author_user_id:
            data = request.data
            serializer = IssueModifySerializer(issue, data=data)
            if serializer.is_valid():
                serializer.save(project_id=project, author_user_id=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"You're not the author of the issue {project.title}")

    def delete(self, request, project_id, issue_id):
        issue = self.get_issue(issue_id)
        if request.user == issue.author_user_id:
            issue.delete()
            return Response(f"Issue: {issue.title} has been deleted")
        return Response(f"You're not the author of issue {issue.title}")


class ManageIssuesComments(ManageProjectIssues):

    def post(self, request, project_id, issue_id):
        project = self.get_project(project_id)
        issue = self.get_issue(issue_id)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to post comments in project {project.title}")
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user, issue_id=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id):
        project = self.get_project(project_id)
        issue = self.get_issue(issue_id)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to view comments in project {project.title}")
        comments = Comments.objects.filter(issue_id=issue)
        page = self.paginate_queryset(comments)
        serializer = self.get_paginated_response(CommentsListSerializer(page, many=True).data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageComments(ManageIssuesComments):

    def get_comment(self, comment_id):
        try:
            return Comments.objects.get(id=comment_id)
        except Comments.DoesNotExist:
            raise Http404

    def get(self, request, project_id, issue_id, comment_id):
        project = self.get_project(project_id)
        issue = self.get_issue(issue_id)
        comment = self.get_comment(comment_id)
        contributor = Contributors.objects.filter(user_id=request.user, project_id=project)
        if not contributor:
            return Response(f"You're not allowed to view this comment of project {project.title}")
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, project_id, issue_id, comment_id):
        issue = self.get_issue(issue_id)
        comment = self.get_comment(comment_id)
        if request.user == comment.author_user_id:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author_user_id=request.user, issue_id=issue)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(f"You're not the author of this comment")

    def delete(self, request, project_id, issue_id, comment_id):
        comment = self.get_comment(comment_id)
        if request.user == comment.author_user_id:
            comment.delete()
            return Response(f"Your comment: '{comment.description}' has been deleted")
        return Response(f"You're not the author of this comment")






















