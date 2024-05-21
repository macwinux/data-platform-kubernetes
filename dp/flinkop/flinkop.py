
import click
import utils.subprocess_com as utils
import flinkop.argu as argu
@click.group()
def flinkop():
    """
        Install flink operator command
    """

@flinkop.command(name='install')
@click.argument('v', type=str, required=False, default='1.8.0')
def install(v: str):
    """Install flink operator in kubernetes

    Args:
        v (str, optional): version that you want to install in kubernetes Defaults to '1.8.0'.
    
    """
    utils.create_ns('flink-operator')
    utils.create_ns('flink-jobs')
    utils.add_repo('flink-operator', argu.HELM_REPO+v)
    flink_op = 'flink-operator/flink-kubernetes-operator'
    utils.install_repo('flink-operator', 'flink-operator', flink_op, "flinkop-values.yaml")
    
@flinkop.command(name="delete")
def delete():
    """Uninstall flink operator from kubernetes
    """
    utils.uninstall_repo('flink-operator', 'flink-operator')
    utils.delete_repo('flink-operator')
    utils.delete_ns('flink-operator')
    utils.delete_ns('flink-jobs')
