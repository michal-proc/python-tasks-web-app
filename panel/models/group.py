from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from common import settings
from panel.enums.role import Role


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    join_code = models.CharField(max_length=20, unique=True, verbose_name=_("Join code"))
    join_code_for_instructor = models.CharField(max_length=20, unique=True, verbose_name=_("Join code for instructor"))
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name=_("Group creator")
    )
    image = models.ImageField(upload_to='media/group_images/', blank=True, null=True, verbose_name=_("Image"))

    def save(self, *args, **kwargs):
        if not self.join_code:
            self.join_code = str(uuid.uuid4())[:12]
        if not self.join_code_for_instructor:
            self.join_code_for_instructor = str(uuid.uuid4())[:12]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=Role.choices, verbose_name=_("Role"))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Joined at"))

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.group.name} - {self.role}"


class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group_messages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
