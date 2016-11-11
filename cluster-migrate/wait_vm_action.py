from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result

class WaitVmAction(NovaAction):

    def __init__(self, uuid, migrate):
        self._uuid = uuid
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            # client.servers.findall(status="VERIFY_RESIZE")
            client.servers.find(id=self._uuid, status="VERIFY_RESIZE")
