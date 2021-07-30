.. _trino-admin-configuration-label:

========================
Configuring Trino Admin
========================
A Presto cluster consists of a coordinator node and one or more workers nodes.
A coordinator and worker may be located on the same node, meaning that you can
have a single-node installation of Presto, but having a dedicated node for the
coordinator is recommended for better performance, especially on larger
clusters.

In order to use ``trino-admin`` to manage software on a cluster of nodes,
you must specify a configuration for ``trino-admin``. This configuration
indicates the nodes on which to install as well as other credentials.

To set up a configuration, create a file ``~/.trinoadmin/config.json``
(or ``$PRESTO_ADMIN_CONFIG_DIR/config.json`` if you have the ``trino-admin``
config directory set using the environment variable) with the content below as
appropriate for your cluster setup. Replace the variables denoted with
brackets <> with actual values enclosed in double quotations. The user
specified by ``username`` must have sudo access, unless the username
is root, on all the Presto nodes, and ``trino-admin`` also must be
able to login to all of the nodes via SSH as that user (see
:ref:`ssh-configuration-label` for details on how to set that up). The
file should be owned by root with R/W permissions (i.e. 622).

.. NOTE::
   The sudo setup for a non-root user must have the ability to run /bin/bash
   as root. This can be a security issue. The IT organization should take the
   necessary steps to address this security hole and select an appropriate
   trino-admin user.

Configuration 
-------------

Use the following configuration as a template for clusters:

.. code-block:: none

    {
      "username": "<ssh_user_name>",
      "port": "<ssh_port>",
      "coordinator": "<host_name>",
      "workers": ["<host_name_1>", "<host_name_2>", ... "<host_name_n>"],
      "java_home":"<path/to/java/on/trino/nodes>"
    }

Do not use localhost as host_name for a multi-node cluster.
All of the properties are optional, and if left out the following defaults will
be used:

.. code-block:: none

    {
      "username": "root",
      "port": "22",
      "coordinator": "localhost",
      "workers": ["localhost"]
    }

Note that ``java_home`` is not set by default.  It only needs to be set if
Java is in a non-standard location on the Presto nodes.  The property is used
to tell the Presto RPM where to find Java.

.. NOTE::

    If you have installed the JDK, ``java_home`` should be set so refer to the
    ``jre`` subdirectory of the JDK.

You can also specify some but not all of the properties. For example, the
default configuration is for a single-node installation of Presto on the same
node that ``trino-admin`` is installed on. For a 6 node cluster with default
username and port, a sample ``config.json`` would be:

.. code-block:: none

    {
      "coordinator": "master",
      "workers": ["slave1","slave2","slave3","slave4","slave5"]
    }

You can specify a range of workers by including the number range in brackets
in the worker name.  For example:

.. code-block:: none

    "workers": ["worker[01-03]"]

is the same as

.. code-block:: none

    "workers": ["worker01", "worker02", "worker03"]

.. _sudo-password-spec:

Sudo password specification
---------------------------
Please note that if the username you specify is not root, and that user needs
to specify a sudo password, you do so in one of two ways. You can specify it on
the command line:

.. code-block:: none

    ./trino-admin <command> -p <password>

Alternatively, you can opt to use an interactive password prompt, which prompts
you for the initial value of your password before running any commands:

.. code-block:: none

    ./trino-admin <command> -I
    Initial value for env.password: <type your password here>

The sudo password for the user must be the same as the SSH password.
