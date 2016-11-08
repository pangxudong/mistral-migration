from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result

class ConfirmResizeVmAction(NovaAction):

    def __init__(self, migrate, uuid):
        self._uuid = uuid
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            client.servers.confirm_resize(self._uuid)
