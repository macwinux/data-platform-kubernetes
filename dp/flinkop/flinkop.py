import click
import utils.subprocess_com as utils
import utils.helm_const as h
import utils.constants as c
@click.group()
def flinkop():
    """
        Install flink operator command
    """

@flinkop.command(name='install')
@click.option('--version', '-v', type=str, default='1.8.0', help='Version of the flink operator that you want to deploy')
def install(version: str):
    """Install flink operator in kubernetes

    Args:
        v (str, optional): version that you want to install in kubernetes Defaults to '1.8.0'.
    
    """
    utils.create_ns(c.FLINK_OP_NS)
    utils.create_ns(c.FLINK_NS)
    utils.add_repo(c.FLINK_REPO, h.HELM_FLINK_REPO+version)
    utils.apply_cert_manager()
    utils.install_repo(c.FLINK_REPO, c.FLINK_REPO, c.FLINK_OP, c.FLINK_VALUES)

    
@flinkop.command(name="delete")
def delete():
    """Uninstall flink operator from kubernetes
    """
    utils.uninstall_repo(c.FLINK_REPO, c.FLINK_REPO)
    utils.delete_repo(c.FLINK_REPO)
    utils.delete_ns(c.FLINK_OP_NS)
    utils.delete_ns(c.FLINK_NS)

@flinkop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision(c.FLINK_OP_NS)