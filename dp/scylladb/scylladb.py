import click
import utils.subprocess_com as utils
import scylladb.argu as argu
import time
from pathlib import Path
from os import path
import yaml

@click.group()
def scylladb():
    """
        Install scyllaDB cluster command
    """

@scylladb.command(name='install')
@click.option('--nodes', '-n', default=1, help="Number of nodes for the scylladb cluster")
def install(nodes: int):
    """Install scylladb cluster in kubernetes
    
    Args: 
        nodes (int, optional): How many scylladb nodes will be deployed in Kubernetes. Default to 1.
    """
    utils.create_ns('scylla-operator')
    utils.create_ns('scylla')
    utils.add_repo('scylla', argu.HELM_REPO)
    utils.update_helm()
    utils.apply_cert_manager()
    utils.install_repo(namespace='scylla-operator', repo_name='scylla-operator', operator_name='scylla/scylla-operator')
    time.sleep(15)
    load_yaml(nodes)
    utils.install_repo(namespace='scylla', repo_name='scylla', operator_name='scylla/scylla', values_yaml='scylla-values.yaml')

@scylladb.command(name="delete")
def uninstall():
    """Uninstall scylladb cluster in kubernetes
    """
    utils.uninstall_repo(namespace='scylla', operator_name='scylla')
    utils.uninstall_repo(namespace='scylla-operator', operator_name='scylla-operator')
    utils.delete_repo(repo_name='scylla')
    utils.delete_ns('scylla')
    utils.delete_ns('scylla-operator')


@scylladb.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision('scylla-operator')

    
def load_yaml(nodes: int):
    absolute = str(Path(__file__).parent.parent)
    values_path = path.join(absolute, 'resources', 'scylla-values.yaml')
    with open(values_path) as f:
        doc = yaml.safe_load(f)
    doc['racks'] = [{
        'name': "us-east-1a",
        'scyllaConfig': 'scylla-config',
        'scyllaAgentConfig': 'scylla-agent-config',
        'members': nodes,
        'storage': {
          'capacity': '10Gi'
        },
        'resources': {
           'limits': {
             'cpu': 1,
             'memory': '4Gi'
           },
           'requests': {
             'cpu': 1,
             'memory': '4Gi'
           }
        }
    }]
    with open(values_path, 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)
        