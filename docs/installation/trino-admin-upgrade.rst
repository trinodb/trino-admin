======================
Upgrading Trino Admin
======================

Upgrading to a newer version of ``trino-admin`` requires deleting the old
installation and then installing the new version.  After you've deleted the
``trinoadmin`` directory, install the newer version of ``trino-admin``
by following the instructions in the installation section
(see :ref:`trino-admin-installation-label`).

For ``trino-admin`` versions earlier than 2.0, the configuration files are
located at ``/etc/opt/trinoadmin``.  To upgrade to a newer version and
continue to use these configuration files, make sure you copy them to the
new configuration directory at ``~/.trinoadmin`` (or
``$PRESTO_ADMIN_CONFIG_DIR``). The connector configuration directory
located at ``/etc/opt/trinoadmin/connectors`` must be renamed to
``/etc/opt/trinoadmin/catalog``, before copying to ``~/.trinoadmin``.

For ``trino-admin`` versions 2.0 and later, the configuration files
located in ``~/.trinoadmin`` will remain intact and continue to be used
by the newer version of ``trino-admin``.
