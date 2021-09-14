import docker
import docker.errors
from docker.models.containers import Container
from django.conf import settings

__all__ = ['Client', 'Exceptions']

Exceptions = docker.errors


class Client:
    NETWORK = settings.DOCKER_NETWORK
    SANDBOX_IMAGE = settings.DOCKER_SANDBOX_IMAGE

    @classmethod
    def get_docker_client(cls) -> docker.DockerClient:
        return docker.from_env()

    @classmethod
    def create_container(cls, container_name: str, command: str) -> 'Container':
        client = cls.get_docker_client()
        client.containers.run(
            cls.SANDBOX_IMAGE,
            name=container_name,
            detach=True,
            network=cls.NETWORK,
            command=command
        )
        return cls.get_container(container_name)

    @classmethod
    def get_container(cls, container_name: str) -> 'Container':
        client = cls.get_docker_client()
        return client.containers.get(container_name)

    @classmethod
    def remove_container(cls, container_name: str, force: bool = True):
        container = cls.get_container(container_name)
        container.remove(force=force)
