import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE, BEFORE_DELETE
from utils import docker


class State(models.IntegerChoices):
    PENDING = 0, _('Pending')
    ACTIVE = 1, _('Active')


class Instance(LifecycleModelMixin, models.Model):
    """
    Model for sandbox instances
    """
    id = models.UUIDField(primary_key=True, db_index=True, unique=True, editable=False, default=uuid.uuid4)
    state = models.PositiveSmallIntegerField(choices=State.choices, default=State.PENDING)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        default_permissions = []

    def __str__(self):
        return self.container_name

    @property
    def container_name(self):
        return f'sandbox-{self.id}'

    @hook(AFTER_CREATE)
    def after_create(self):
        # Create instance on docker
        # TODO: Add to queue
        docker.Client.create_container(self.container_name)
        self.state = State.ACTIVE
        self.save()

    @hook(BEFORE_DELETE)
    def before_delete(self):
        # Delete instance from docker
        try:
            docker.Client.remove_container(self.container_name)
        except docker.exceptions.NotFound:
            pass
