.. _trino-server-installation-label:

============================
Installing the Trino server
============================

Prerequisites: :ref:`trino-admin-installation-label`,
:ref:`java-installation-label` and :ref:`trino-admin-configuration-label`

To install the Presto query engine on a cluster of nodes using ``trino-admin``:

1. Download ``trino-server-rpm-VERSION.ARCH.rpm``

2. Copy the RPM to a location accessible by ``trino-admin``.

3. Run the following command to install Presto:

.. code-block:: none

    $ ./trino-admin server install <local_path_to_rpm>

Presto! Presto is now installed on the coordinator and workers specified in
your ``~/.trinoadmin/config.json`` file.

The default port for Presto is 8080.  If that port is already in use on your
cluster, you will not be able to start Presto. In order to change the port
that Presto uses, proceed to :ref:`trino-port-configuration-label`.

There are additional configuration properties described at
:ref:`trino-configuration-label` that must be changed for optimal performance.
These configuration changes can be done either before or after starting the
Presto server and running queries for the first time, though all configuration
changes require a restart of the Presto servers.

4. Now, you are ready to start Presto:

.. code-block:: none

    $ ./trino-admin server start

This may take a few seconds, since the command doesn't exit until
``trino-admin`` verifies that Presto is fully up and ready to receive
queries.

