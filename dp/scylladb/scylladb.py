import click
import utils.subprocess_com as utils
import utils.helm_const as h
import utils.constants as c
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
@click.option('--nodes', '-n', default=1, help='Number of nodes for the scylladb cluster')
def install(nodes: int):
    """Install scylladb cluster in kubernetes
    
    Args: 
        nodes (int, optional): How many scylladb nodes will be deployed in Kubernetes. Default to 1.
    """
    utils.create_ns(c.SCYLLA_NS_OP)
    utils.create_ns(c.SCYLLA_NS)
    utils.add_repo(c.SCYLLA_REPO, h.HELM_SCYLLA_REPO)
    utils.update_helm()
    utils.apply_cert_manager()
    utils.install_repo(namespace=c.SCYLLA_NS_OP, repo_name=c.SCYLLA_REPO, operator_name=c.SCYLLA_OP)
    time.sleep(15)
    load_yaml(nodes)
    utils.install_repo(namespace=c.SCYLLA_NS, repo_name=c.SCYLLA_REPO, operator_name=c.SCYLLA_SC_OP, values_yaml=c.SCYLLA_VALUES)

@scylladb.command(name="delete")
def uninstall():
    """Uninstall scylladb cluster in kubernetes
    """
    utils.uninstall_repo(namespace=c.SCYLLA_NS, operator_name=c.SCYLLA_REPO)
    utils.uninstall_repo(namespace=c.SCYLLA_NS_OP, operator_name=c.SCYLLA_REPO)
    utils.delete_repo(repo_name=c.SCYLLA_REPO)
    utils.delete_ns(c.SCYLLA_NS)
    utils.delete_ns(c.SCYLLA_NS_OP)


@scylladb.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision(c.SCYLLA_NS_OP)

    
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
        