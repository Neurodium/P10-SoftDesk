from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import MyAccountManager

# Create your models here.
class Users(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=30, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return str(self.email)


    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser



class Contributors(models.Model):
    #permission choices
    PERMISSION_CHOICES = (
        ('All Rights', 'All Rights'),
        ('Create and Read', 'Create and Read'),
    )

    #role choices
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Contributor', 'Contributor')
    )
    permission = models.CharField(max_length=80, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=80, choices=ROLE_CHOICES)

    user_id = models.ForeignKey('project.Users', on_delete=models.CASCADE, related_name='contributor_users')
    project_id = models.ForeignKey('project.Projects', on_delete=models.CASCADE, related_name='projects_contributed')

    class Meta:
        unique_together = ['user_id', 'project_id']

    def __str__(self):
        return self.user_id.email


class Projects(models.Model):
    #type choices
    TYPE_CHOICES = (
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    )

    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=80, choices=TYPE_CHOICES)

    author_user_id = models.ForeignKey('project.Users', on_delete=models.CASCADE, related_name='projects_users')

    def __str__(self):
        return self.title


class Issues(models.Model):
    #tag choices
    TAG_CHOICES = (
        ('BUG', 'BUG'),
        ('AMÉLIORATION', 'AMÉLIORATION'),
        ('TÂCHE', 'TÂCHE')
    )

    #priority choices
    PRIORITY_CHOICES = (
        ('FAIBLE', 'FAIBLE'),
        ('MOYENNE', 'MOYENNE'),
        ('ÉLEVÉE', 'ÉLEVÉE'),
    )

    #status choices
    STATUS_CHOICES = (
        ('Á faire', 'Á faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    )
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(max_length=255, choices=TAG_CHOICES)
    priority = models.CharField(max_length=80, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=80, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    project_id = models.ForeignKey('project.Projects', on_delete=models.CASCADE, related_name='projects_issues')
    author_user_id = models.ForeignKey('project.Users', on_delete=models.CASCADE, related_name='issues_author_users')
    assignee_user_id = models.ForeignKey('project.Users', on_delete=models.CASCADE, related_name='issues_assignee_users')

    def __str__(self):
        return self.title


class Comments(models.Model):
    description = models.CharField(max_length=2048, default='blank')
    created_time = models.DateTimeField(auto_now_add=True)

    author_user_id = models.ForeignKey('project.Users', on_delete=models.CASCADE, related_name='comment_author_users')
    issue_id = models.ForeignKey('project.Issues', on_delete=models.CASCADE, related_name='comment_issues')

    def __str__(self):
        return self.issue_id.title

    class Meta:
        ordering = ['id']

