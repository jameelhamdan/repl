import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE, AFTER_DELETE
import docker


class DockerClient:
    SANDBOX_DOCKER_IMAGE = settings.SANDBOX_DOCKER_IMAGE

    @classmethod
    def get_docker_client(cls) -> docker.DockerClient:
        return docker.from_env()

    @classmethod
    def create_container(cls, container_name):
        client = cls.get_docker_client()
        client.containers.run(cls.SANDBOX_DOCKER_IMAGE, name=container_name, detach=True)

    @classmethod
    def get_container(cls, container_name):
        client = cls.get_docker_client()
        return client.containers.get(container_name)

    @classmethod
    def remove_container(cls, container_name):
        container = cls.get_container(container_name)
        container.remove()


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
        DockerClient.create_container(self.container_name)
        self.state = State.ACTIVE
        self.save()

    @hook(AFTER_DELETE)
    def after_delete(self):
        # Delete instance from docker
        DockerClient.remove_container(self.container_name)
