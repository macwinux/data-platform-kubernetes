from unittest import TestCase, mock, main
from .subprocess_com import create_ns, add_repo, install_repo, delete_ns, delete_repo, uninstall_repo
from subprocess import CompletedProcess
from pathlib import Path

class TestCreateNs(TestCase):
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_create_ns(self, mock_run):
        expected = CompletedProcess(args = "", returncode=0, stdout="Created namespace in kubernetes")
        mock_run.return_value = expected
        response = create_ns(namespace="flink-operator")
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected.stdout)


    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_failed_create_ns(self, mock_run):
        err_msg = "Error creating namespace"
        with self.assertRaises(SystemError):
            expected = CompletedProcess(args = "", returncode=1, stderr=err_msg)
            mock_run.return_value = expected
            create_ns(namespace="flink-operator")
    
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_ns_already_exists(self, mock_run):
        err_msg = "Error (AlreadyExists): namespace flink-operator already exits"
        expected = CompletedProcess(args = "", returncode=1, stderr=err_msg)
        mock_run.return_value = expected
        response = create_ns(namespace="flink-operator")
        self.assertEqual(response.returncode, 1)

class TestDeleteNs(TestCase):
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_delete_ns(self, mock_run):
        expected = CompletedProcess(args = "", returncode=0, stdout="Deleted namespace in kubernetes")
        mock_run.return_value = expected
        response = delete_ns(namespace="flink-operator")
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected.stdout)
    
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_failed_delete_ns(self, mock_run):
        err_msg = "Error creating the namespace"
        with self.assertRaises(SystemError):
            expected = CompletedProcess(args = "", returncode=1, stderr=err_msg)
            mock_run.return_value = expected
            delete_ns(namespace="flink-operator")

    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_ns_not_exits(self, mock_run):
        err_msg = "Error (NotFound): namespace flink-operator not found"
        expected = CompletedProcess(args = "", returncode=1, stderr=err_msg)
        mock_run.return_value = expected
        response = delete_ns(namespace="flink-operator")
        self.assertEqual(response.returncode, 1)

class TestAddRepo(TestCase):
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_add_repo(self, mock_run):
        expected = CompletedProcess(args="", returncode=0, stdout="Repo created")
        mock_run.return_value = expected
        response = add_repo("flink-operator-repo", "https://repo.com")
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected.stdout)
        
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_filed_add_repo(self, mock_run):
        with self.assertRaises(SystemError):
          expected = CompletedProcess(args = "", returncode=1, stderr="Failed adding a repo in Helm")
          mock_run.return_value = expected
          add_repo("flink-operator-repo", "https://repo.com")
      
class TestDeleteRepo(TestCase):
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_delete_repo(self, mock_run):
        expected = CompletedProcess(args="", returncode=0, stdout="Repo deleted")
        mock_run.return_value = expected
        response = delete_repo("flink-operator-repo")
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected.stdout)
        
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_filed_add_repo(self, mock_run):
        with self.assertRaises(SystemError):
          expected = CompletedProcess(args = "", returncode=1, stderr="Failed deleting a repo in Helm")
          mock_run.return_value = expected
          delete_repo("flink-operator-repo")
      
class TestInstallRepo(TestCase):
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_install_repo(self, mock_run):
        expected = CompletedProcess(args="", returncode=0, stdout="Repo installed")
        mock_run.return_value = expected
        response = install_repo("flink-operator-repo", "flink-op-1.8.0", "flink-op-1.8.0", "flink-values.yaml")
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected.stdout)
        
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_filed_install_repo(self, mock_run):
        with self.assertRaises(SystemError):
          expected = CompletedProcess(args = "", returncode=1, stderr="Failed installing a repo in Helm")
          mock_run.return_value = expected
          install_repo("flink-operator", "flink-operator-repo", "flink-op-1.8.0", "flink-values.yaml")

class TestUninstallRepo(TestCase):
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_uninstall_repo(self, mock_run):
        expected = CompletedProcess(args="", returncode=0, stdout="Repo uninstalled")
        mock_run.return_value = expected
        response = uninstall_repo("flink-operator", "flink-operator")
        self.assertEqual(response.returncode, 0)
        self.assertEqual(response.stdout, expected.stdout)
        
    @mock.patch("dp.utils.subprocess_com.__run_subprocess")
    def test_filed_install_repo(self, mock_run):
        with self.assertRaises(SystemError):
          expected = CompletedProcess(args = "", returncode=1, stderr="Failed uninstalling a repo in Helm")
          mock_run.return_value = expected
          uninstall_repo("flink-operator", "flink-operator")
        

if __name__ == '__main__':
    main()