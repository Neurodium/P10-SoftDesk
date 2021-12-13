"""softdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



from project.views import CreateUser, LoginUser, UserProjectList, ManageProject, ManageProjectUsers, \
    ManageProjectIssues

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', CreateUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('projects/', UserProjectList.as_view()),
    path('projects/<project_id>/', ManageProject.as_view()),
    path('projects/<project_id>/users/', ManageProjectUsers.as_view()),
    path('projects/<project_id>/users/<user_id>/', ManageProjectUsers.as_view()),
    path('projects/<project_id>/issues/', ManageProjectIssues.as_view()),
    path('projects/<project_id>/issues/<issue_id>/', ManageProjectIssues.as_view()),

]
