=====================
Software requirements
=====================

**Operating systems**

* RedHat Linux version 6.x		
* CentOS (equivalent to above)

**Python**

* Python 2.6.x OR
* Python 2.7.x

**SSH configuration**

* Passwordless SSH from the node running ``presto-admin`` to the nodes where Presto will be installed OR
* Ability to SSH with a password from the node running ``presto-admin`` to the nodes where Presto will be installed

For more on SSH configuration, see :ref:`ssh-configuration-label`.

**Other configuration**

* Sudo privileges are required on both the node running ``presto-admin`` and
  the nodes where Presto is installed.
