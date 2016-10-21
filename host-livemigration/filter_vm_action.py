"""
FilterVmAction - custom action.

Simple action for filtering VM on the presence of metadata/extra spec
"live_migrate" flag
"""
from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class FilterVmException(Exception):
    pass


class FilterVmAction(NovaAction):
    """
    Filter and return VMs whith the flag 'live_migrate' either on vm metadtata
    or flavor extra spec.
    """

    def __init__(self, metadata, flavor, uuid):
        """init."""
        self._metadata = metadata
        self._flavor = flavor
        self._uuid = uuid

    def run(self):
        """Entry point for the action execution."""
        client = self._get_client()
        metadata = self._metadata

        if str(metadata.get('live_migrate')).upper() == 'TRUE':
            return Result(data={'live_migrate': True, 'uuid': self._uuid})
        elif str(metadata.get('live_migrate')).upper() == 'FALSE':
            return Result(data={'live_migrate': False, 'uuid': self._uuid})

        # Ether is no metadata for vm - check flavor.
        try:
            # Maybe this should be done in different action
            # only once per whole workflow.
            # In case there is ~100 VMs to live_migrate, there will be
            # the same amount of calls to nova API.
            flavor = filter(
                lambda f: f.id == self._flavor,
                client.flavors.list()
            )[0]
        except IndexError:
            raise FilterVmException('Flavor not found')

        live_migrate = flavor.get_keys().get('live_migrate:live_migrate')

        if str(live_migrate).upper() == 'TRUE':
            return Result(data={'live_migrate': True, 'uuid': self._uuid})

        return Result(data={'live_migrate': False, 'uuid': self._uuid})
