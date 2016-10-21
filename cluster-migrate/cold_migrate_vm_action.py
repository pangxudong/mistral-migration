from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result
import time

class ColdMigrateVmAction(NovaAction):

    def __init__(self, uuid, migrate, flavor_id):
        self._uuid = uuid
        self._flavor_id = flavor_id
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            client.servers.resize(self._uuid, flavor=self._flavor_id)
            time.sleep(10)
            client.servers.confirm_resize(self._uuid)
