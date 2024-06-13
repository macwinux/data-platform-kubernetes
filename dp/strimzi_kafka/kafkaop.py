import click
import utils.subprocess_com as utils
import strimzi_kafka.argu as argu
from os import path
from pathlib import Path

@click.group()
def kafkaop():
    """
        Install spark operator command
    """

@kafkaop.command(name='install')
def install():
    """Install strimzi kafka operator in kubernetes
    """
    utils.create_ns('strimzi')
    utils.create_ns('kafka')
    utils.add_repo('strimzi', argu.HELM_REPO)
    kafka_op = 'strimzi/strimzi-kafka-operator'
    utils.install_repo('strimzi', 'strimzi', kafka_op, 'kafkaop-strimzi-values.yaml')


@kafkaop.command(name="delete")
def delete():
    """Uninstall strimzi kafka operator from kubernetes
    """
    utils.uninstall_repo('strimzi', 'strimzi')
    utils.delete_repo('strimzi')
    utils.delete_ns('strimzi')
    

@kafkaop.command(name="create-test-cluster")
@click.argument('kafka_yaml', type=str, required=True)
def create_test_cluster(kafka_yaml: str):
    """Deploy a test kafka cluster using strimzi kafka operator in kubernetes

    Args:
        namespace (str, optional): namespace where kafka test cluster will be deployed
    """
    utils.run_kubectl_apply(kafka_yaml,'kafka')

@kafkaop.command(name="delete-test-cluster")
@click.argument('kafka_yaml', type=str, required=True)
def delete_test_cluster(kafka_yaml: str):
    """Delete a test kafka cluster using strimzi kafka operator in kubernetes

    Args:
        namespace (str, optional): namespace where kafka test cluster will be deleted
    """
    utils.run_kubectl_delete(resource_yaml=kafka_yaml, namespace='kafka')
    utils.delete_ns('kafka')
    
@kafkaop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision('strimzi')
    