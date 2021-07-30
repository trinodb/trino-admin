.. _java-installation-label:

===============
Installing Java
===============
Prerequisites: :ref:`trino-admin-installation-label` and :ref:`trino-admin-configuration-label`

A Java 11 runtime environment is a `requirement for running Trino
<https://trino.io/docs/current/installation/deployment.html#requirements>`_.

If a suitable 64-bit version of Java 11 is already installed on the nodes, you
can skip this step. Otherwise you have to install Java via RPM or a tarball.

``trino-admin`` can be used to install a Java RPM package on all nodes in the
cluster:

1. Download the JDK 11 RPM for Linux.

2. Copy the RPM to a location accessible by ``trino-admin``.

3. Run the following command to install Java:

.. code-block:: none

    $ ./trino-admin package install <local_path_to_java_rpm>

.. note::

  If installing Java on SLES, you need to specify the flag ``--nodeps`` for
  ``trino-admin package install``, so that the RPM is installed without
  checking or validating dependencies.
