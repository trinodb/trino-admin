.. _java-installation-label:

===============
Installing Java
===============
Prerequisites: :ref:`presto-admin-installation-label` and :ref:`presto-admin-configuration-label`

A Java 11 runtime is a `requirement <https://prestosql.io/docs/current/installation/deployment.html#requirements>`_ for Presto. If a suitable 64-bit version of JDK 11 is already installed on the cluster, you can skip this step.

There are two ways to install Java: via RPM and via tarball.  The RPM installation sets the default Java on your machine to be Java 11. If
it is acceptable to set the default Java to be Java 11, you can use ``presto-admin`` to install Java, otherwise you will need to install manually.

To install Java via RPM using ``presto-admin``:

1. Download the JDK 11 RPM for Linux.

2. Copy the RPM to a location accessible by ``presto-admin``.

3. Run the following command to install Java on each node in the Presto cluster:

.. code-block:: none

    $ ./presto-admin package install <local_path_to_java_rpm>


.. NOTE:: If installing Java on SLES, you will need to specify the flag ``--nodeps`` for ``presto-admin package install``, so that the RPM is installed without checking or validating dependencies.
