from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class LiveMigrateVmAction(NovaAction):

    def __init__(self, uuid, host, migrate, live_migrate, block_migration, disk_over_commit):
        self._uuid = uuid
        self._host = host
        self._migrate = migrate
        self._live_migrate = live_migrate
        self._block_migration = block_migration
        self._disk_over_commit = disk_over_commit

    def run(self):
        client = self._get_client()

        if (self._migrate and self._live_migrate):
            client.servers.live_migrate(self._uuid, host=self._host, block_migration=self._block_migration, disk_over_commit=self._disk_over_commit)
