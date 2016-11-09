### edit mistral/setup.cfg:
```
[entry_points]
...
mistral.actions =
    ...
    custom.filter_vm = filter_vm_action:FilterVmAction
    custom.cold_migrate = cold_migrate_vm_action:ColdMigrateVmAction
    custom.live_migrate = live_migrate_vm_action:LiveMigrateVmAction
    custom.validate_host = validate_host_action:ValidateHostAction
    custom.wait_vm = wait_vm_action:WaitVmAction
    custom.confirm_resize = confirm_resize_vm_action:ConfirmResizeVmAction
    custom.validate_flavor = validate_flavor_action:ValidateFlavorAction
```


### rebuild mistral & update db
```
$ sudo pip install -e .
$ mistral-db-manage --config-file etc/mistral.conf populate
```
