import click
import utils.subprocess_com as utils
import sparkop.argu as argu
from os import path
from pathlib import Path

@click.group()
def sparkop():
    """
        Install spark operator command
    """

@sparkop.command(name='install')
def install():
    """Install spark operator in kubernetes
    """
    utils.create_ns('spark-operator')
    utils.create_ns('spark-jobs')
    utils.add_repo('spark-operator', argu.HELM_REPO)
    spark_op = 'spark-operator/spark-operator'
    """The spark operator chart helm points to an image that is not found in the kubeflow/spark-operator registry for now.
    So the version of the image in the resources/sparkop-values.yaml is modified with the correct version."""
    utils.install_repo('spark-operator', 'spark-operator', spark_op, 'sparkop-values.yaml')

@sparkop.command(name="delete")
def delete():
    """Uninstall spark operator from kubernetes
    """
    utils.uninstall_repo('spark-operator', 'spark-operator')
    utils.delete_repo('spark-operator')
    utils.delete_ns('spark-operator')
    utils.delete_ns('spark-jobs')