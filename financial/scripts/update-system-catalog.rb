alter 'SYSTEM.CATALOG', {NAME => '0', KEEP_DELETED_CELLS => 'false'}
major_compact 'SYSTEM.CATALOG'
alter 'SYSTEM.CATALOG', {NAME => '0', KEEP_DELETED_CELLS => 'true'}
exit