import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE, BEFORE_DELETE
from utils import docker


class State(models.IntegerChoices):
    PENDING = 0, _('Pending')
    ACTIVE = 1, _('Active')


class Terminal(models.TextChoices):
    PYTHON = 'python', _('Python')
    JAVASCRIPT = 'javascript', _('Javascript')
    BASH = 'bash', _('Bash')
    SHELL = 'shell', _('Shell')
    CMD = 'cmd', _('CMD')


class Instance(LifecycleModelMixin, models.Model):
    """
    Model for sandbox instances
    """
    id = models.UUIDField(primary_key=True, db_index=True, unique=True, editable=False, default=uuid.uuid4)
    state = models.PositiveSmallIntegerField(choices=State.choices, default=State.PENDING)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    terminal_type = models.CharField(max_length=32, choices=Terminal.choices, default=Terminal.BASH)

    class Meta:
        default_permissions = []

    def __str__(self):
        return self.container_name

    @property
    def container_name(self) -> str:
        """
        Return Docker container name
        :return:
        """
        return f'sandbox-{self.id}'

    @property
    def docker_command(self) -> str:
        return self.terminal_type.value

    @property
    def socket_url(self) -> str:
        """
        This will return the local url socket for this instance
        :return:
        """
        return f'/ws/{self.container_name}'

    @hook(AFTER_CREATE)
    def after_create(self):
        """
        Create instance container on docker and activate instance
        """

        # TODO: Add to queue
        docker.Client.create_container(self.container_name, self.docker_command)
        self.state = State.ACTIVE
        self.save()

    @hook(BEFORE_DELETE)
    def before_delete(self):
        """
        Try to remove instance container from docker
        """
        # Delete instance from docker
        try:
            docker.Client.remove_container(self.container_name)
        except docker.Exceptions.NotFound:
            pass
