import click
import utils.subprocess_com as utils
import utils.helm_const as h
import utils.constants as c

@click.group()
def miniop():
    """
        Install MinIO operator command
    """

@miniop.command(name='install')
def install():
    """Install MinIO operator in kubernetes
    """
    utils.create_ns(c.MINIO_NS)
    utils.add_repo(c.MINIO_REPO, h.HELM_MINIO_REPO)
    result = utils.install_repo(c.MINIO_REPO, c.MINIO_REPO, c.MINIO_OP)
    click.echo('-------------------------------------------')
    click.echo(f"{(result.stdout).decode()}")
    click.echo('-------------------------------------------')   

@miniop.command(name="delete")
def delete():
    """Uninstall MinIO operator from kubernetes
    """
    utils.uninstall_repo(c.MINIO_REPO, c.MINIO_REPO)
    utils.delete_repo(c.MINIO_REPO)
    utils.delete_ns(c.MINIO_NS)

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
@click.option('--namespace', '-n', default= 'minio-tenant', help='Namespace where MinIO tenant will be deployed')
def create_tenant(namespace: str):
    """Create a new tenenat using the MinIO operator

    Args:
        namespace (str, optional): namespace where MinIO tenant will be deployed
    """

    utils.create_ns(namespace)
    result=utils.install_repo(namespace, c.MINIO_T_REPO, c.MINIO_TENANT_OP, c.MINIO_T_REPO)
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

    utils.uninstall_repo(namespace, c.MINIO_T_REPO)
    #utils.delete_repo('minio-operator')
    utils.delete_ns(namespace)
    
@miniop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision(c.MINIO_NS)