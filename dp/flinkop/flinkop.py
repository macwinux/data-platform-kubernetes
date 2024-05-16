
import click
import utils.subprocess_com as utils

@click.group()
def flinkop():
    """
        Install flink operator command
    """

@flinkop.command(name='install')
@click.argument('v', type=str, required=False)
def install(v: str='1.8.0'):
    """install flink operator for kubernetes

    Args:
        v (str, optional): version that you want to install in kubernetes Defaults to '1.8.0'.
    
    """
    
    utils.create_ns('flink-operator')
    #utils.create_ns('flink-jobs')
    #utils.add_repo('flink-operator',argu.HELM_REPO+v)
    #flink_op = f'flink-kubernetes-operator-{v}/flink-kubernetes-operator'
    #utils.install_repo('flink-operator', flink_op)