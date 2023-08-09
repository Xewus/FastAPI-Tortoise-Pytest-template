from time import sleep

import docker
from docker.models.containers import Container


class Docker:
    def __init__(
        self,
        postgres_user: str,
        postgres_password: str,
        postgres_port: str | int,
        postgres_db: str,
        postgres_name: str = "postgres_test",
    ) -> None:
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.postgres_port = postgres_port
        self.postgres_db = postgres_db
        self.postgres_name = postgres_name
        self.containers: list[Container] = []
        self.client = docker.from_env()

        for _ in range(5):
            if self.client.ping():
                break
            sleep(1)
        else:
            raise ConnectionError("no connection to docker")

        for container in self.client.containers.list():
            container: Container
            if container.name == postgres_name:
                container.stop()
                container.wait()

    async def __aenter__(self) -> None:
        self.run_all()

    async def __aexit__(self, *_) -> None:
        self.stop_all()
        ...

    def _check_running_container(self, container: Container) -> None:
        """Make sure the container status is running.
        Time limit for checking is near `1.5 sec`.

        #### Args:
        - container (Container):
            Container for checking.

        #### Raises:
        - ConnectionError:
            Time limit for checking is out.
        """
        for _ in range(5):
            if container.status == "running":
                break
            sleep(0.3)
            container.reload()
        else:
            raise ConnectionError(f"{container.name} is not running")
        return None

    def _check_running_containers(self) -> None:
        """Check the status of all containers."""
        for container in self.containers:
            self._check_running_container(container)
        return None

    def _run_postgres(self) -> None:
        """Run container with `Postgres` database."""
        postgres: Container = self.client.containers.create(
            image="postgres:14-alpine",
            name=self.postgres_name,
            environment={
                "POSTGRES_USER": self.postgres_user,
                "POSTGRES_PASSWORD": self.postgres_password,
                "POSTGRES_DB": self.postgres_db,
            },
            ports={5432: self.postgres_port},
            auto_remove=True,
            detach=True,
        )
        assert postgres.status == "created"
        postgres.start()
        self.containers.append(postgres)
        return None

    def stop_all(self) -> None:
        """Stop all containers associated with the `Doker` instance."""
        for container in self.containers:
            container.stop()
            # container.wait()
        return None

    def run_all(self) -> None:
        """Run all containers associated with the `Doker` instance."""
        self.stop_all()
        self._run_postgres()
        self._check_running_containers()
        return None
