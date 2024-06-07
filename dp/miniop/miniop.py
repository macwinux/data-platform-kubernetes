import click
import utils.subprocess_com as utils
import miniop.argu as argu

@click.group()
def miniop():
    """
        Install MinIO operator command
    """

@miniop.command(name='install')
def install():
    """Install MinIO operator in kubernetes
    """
    utils.create_ns('minio-operator')
    utils.add_repo('minio-operator', argu.HELM_REPO)
    minio_op = 'minio-operator/operator'
    result = utils.install_repo('minio-operator', 'operator', minio_op)
    click.echo('-------------------------------------------')
    click.echo(f"{(result.stdout).decode()}")
    click.echo('-------------------------------------------')   

@miniop.command(name="delete")
def delete():
    """Uninstall MinIO operator from kubernetes
    """
    utils.uninstall_repo('minio-operator', 'operator')
    utils.delete_repo('minio-operator')
    utils.delete_ns('minio-operator')

@miniop.command(name="get-jwt")
def get_jwt():
    """Get the MinIO Operator JSON Web Token (JWT) saved as a Kubernetes Secret for controlling access to the Operator Console.
    """
    command=["kubectl", "get", "secret", "console-sa-secret", "-o", "go-template='{{.data.token | base64decode}}'", "-n", "minio-operator"]
    result=utils.__run_subprocess(command)
    click.echo('-------------------------------------------')
    click.echo(f"JWT: {(result.stdout).decode()}")
    click.echo('-------------------------------------------')    


@miniop.command(name="create-tenant")
@click.option('--namespace', '-n', default= "minio-tenant", help='Namespace where MinIO tenant will be deployed')
def create_tenant(namespace: str):
    """Create a new tenenat using the MinIO operator

    Args:
        namespace (str, optional): namespace where MinIO tenant will be deployed
    """

    utils.create_ns(namespace)
    minio_tenant = 'minio-operator/tenant'
    result=utils.install_repo(namespace, 'tenant1', minio_tenant, "minio-tenant-values.yaml")
    click.echo('-------------------------------------------')
    click.echo(f"{(result.stdout).decode()}")
    click.echo('-------------------------------------------')   



@miniop.command(name="delete-tenant")
@click.option('--namespace', '-n', default='minio-tenant', help='Namespace where MinIO tenant will be deleted')
def delete_tenant(namespace: str):
    """Delte a tenant using the MinIO operator

    Args:
        namespace (str): namespace where MinIO tenant will be deployed
    """

    utils.uninstall_repo(namespace, 'tenant1')
    #utils.delete_repo('minio-operator')
    utils.delete_ns(namespace)