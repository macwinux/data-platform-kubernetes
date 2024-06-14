import click
import utils.subprocess_com as utils
import utils.helm_const as h
import utils.constants as c

@click.group()
def sparkop():
    """
        Install spark operator command
    """

@sparkop.command(name='install')
def install():
    """Install spark operator in kubernetes
    """
    utils.create_ns(c.SPARK_NS_OP)
    utils.create_ns(c.SPARK_NS)
    utils.add_repo(c.SPARK_REPO, h.HELM_SPARK_REPO)
    """The spark operator chart helm points to an image that is not found in the kubeflow/spark-operator registry for now.
    So the version of the image in the resources/sparkop-values.yaml is modified with the correct version."""
    utils.install_repo(c.SPARK_NS_OP, c.SPARK_REPO, c.SPARK_OP, c.SPARK_VALUES)

@sparkop.command(name="delete")
def delete():
    """Uninstall spark operator from kubernetes
    """
    utils.uninstall_repo(c.SPARK_NS_OP, c.SPARK_REPO)
    utils.delete_repo(c.SPARK_REPO)
    utils.delete_ns(c.SPARK_NS_OP)
    utils.delete_ns(c.SPARK_NS)

@sparkop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision(c.SPARK_NS_OP)
    