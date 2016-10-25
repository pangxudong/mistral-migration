import paramiko
import os

from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result

class ValidateHostAction(NovaAction):

    def __init__(self, host, uuid, migrate):
        self._host = host
        self._uuid = uuid
        self._migrate = migrate

    def run(self):
        client = self._get_client()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self._host, 22)# make sure that ./ssh/authorized_keys is already set
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("virsh --version")
        remote_version = ssh_stdout.readline()

        local_version = os.popen("virsh --version").read()

        if (remote_version == local_version):
            return Result(data={"live_migrate":True, "migrate":self._migrate, "uuid":self._uuid})
        else:
            return Result(data={"live_migrate":False, "migrate":self._migrate, "uuid":self._uuid})
