"""
FilterVmAction - custom action.

Simple action for filtering VM on the presence of metadata/extra spec
"cluster_id" flag
"""
from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class FilterVmException(Exception):
    pass


class FilterVmAction(NovaAction):
    """
    Filter and return VMs whith the flag 'cluster_id' either on vm metadtata
    or flavor extra spec.
    """

    def __init__(self, metadata, flavor, uuid, cluster_id):
        """init."""
        self._metadata = metadata
        self._flavor = flavor
        self._uuid = uuid
        self._cluster_id = cluster_id

    def run(self):
        """Entry point for the action execution."""
        client = self._get_client()
        metadata = self._metadata

        if str(metadata.get('cluster_id')) == str(self._cluster_id):
            return Result(data={'live_migrate': True, 'uuid': self._uuid})

        # Ether is no metadata for vm - check flavor.
        try:
            # Maybe this should be done in different action
            # only once per whole workflow.
            # In case there is ~100 VMs to cluster_id, there will be
            # the same amount of calls to nova API.
            flavor = filter(
                lambda f: f.id == self._flavor,
                client.flavors.list()
            )[0]
        except IndexError:
            raise FilterVmException('Flavor not found')

        cluster_id = flavor.get_keys().get('cluster_id:cluster_id')

        if str(cluster_id) == str(self._cluster_id):
            return Result(data={'live_migrate': True, 'uuid': self._uuid})

        return Result(data={'live_migrate': False, 'uuid': self._uuid})
