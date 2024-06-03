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
    utils.install_repo('minio-operator', 'operator', minio_op)

@miniop.command(name="delete")
def delete():
    """Uninstall MinIO operator from kubernetes
    """
    utils.uninstall_repo('minio-operator', 'operator')
    utils.delete_repo('minio-operator')
    utils.delete_ns('minio-operator')