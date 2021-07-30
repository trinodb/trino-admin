.. _trino-admin-installation-label:

=======================
Installing Trino Admin
=======================

Prerequisites:

 *  `Python 2.7 <https://www.python.org/downloads>`_.
 *  If you are using the online installer then make sure you've installed the
    Python development package for your system. For RedHat/Centos that package is
    ``python2-devel`` and for Debian/Ubuntu it is ``python-dev``.

Trino Admin is packaged as an offline installer --
``trinoadmin-<version>-offline.tar.gz`` -- and as an online
installer -- ``trinoadmin-<version>-online.tar.gz``.

The offline installer includes all of the dependencies for
``trino-admin``, so it can be used on a cluster without an outside
network connection. The offline installer is currently only supported
on RedHat Linux 6.x or CentOS equivalent.

The online installer downloads all of the dependencies when you run
``./install-trinoadmin.sh``. You must use the online installer for
installation of Presto on Amazon EMR and for use on any operating
system not listed above. If you are using trino-admin on an
unsupported operating system, there may be operating system
dependencies beyond the installation process, and trino-admin may not
work.

To install ``trino-admin``:

1. Download an offline installer from
`releases page <https://github.com/wgzhao/trino-admin/releases>`_.

2. Copy the installer ``trinoadmin-<version>-offline.tar.gz`` to the
location where you want ``trino-admin`` to run.
Note that ``trino-admin`` does not have to be on the same node(s)
where Presto will run, though it does need to have SSH access to all
of the nodes in the cluster.

.. NOTE::
     For Amazon EMR, use the online installer instead of the offline installer.

3.  Extract and run the installation script from within the ``trinoadmin``
directory.

.. code-block:: none

    $ tar xvf trinoadmin-<version>-offline.tar.gz
    $ cd trinoadmin
    $ ./install-trinoadmin.sh

The installation script will create a ``trino-admin-install`` directory and an
executable ``trino-admin`` script. By default, the ``trino-admin`` config and
log directory locations are configured to be ``~/.trinoadmin`` and
``~/.trinoadmin/log``, respectively. This can be changed by modifying the
environment variables, PRESTO_ADMIN_CONFIG_DIR and PRESTO_ADMIN_LOG_DIR.
The installation script will also create the directories pointed to by
PRESTO_ADMIN_CONFIG_DIR and PRESTO_ADMIN_LOG_DIR. If those directories
already exist, the installation script will not erase their contents.

4.  Verify that ``trino-admin`` was installed properly by running the following
command:

.. code-block:: none

    $ ./trino-admin --help

Please note that you should only run one ``trino-admin`` command on your
cluster at a time.

