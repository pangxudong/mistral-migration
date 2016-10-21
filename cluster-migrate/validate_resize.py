from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result

class ValidateMigrateVmAction(NovaAction):

    def __init__(self, uuid, new_flavor, flavor_id):
        self._uuid = uuid
        self._flavor_id = flavor_id
        self._new_flavor = new_flavor

    def run(self):
        client = self._get_client()
        if(self._new_flavor == self._flavor_id):
            return Result(data={'SUCCESS': True})
        else:
            return Result(data={'SUCCESS': False})
