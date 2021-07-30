.. _presto-cli-installation-label:

============================
Running Trino/Presto queries
============================

The Presto CLI provides a terminal-based interactive shell for running queries.
The CLI is a self-executing JAR file, which means it acts like a normal UNIX
executable.

To run a query via the Presto CLI:

1. Download the ``trino-cli`` and copy it to the location you want to run it
   from. This location may be any node that has network access to the
   coordinator.

2. Rename the artifact to ``trino`` and make it executable, substituting
   your version of Presto for "version":

.. code-block:: none

    $ mv trino-cli-<version>-executable.jar presto
    $ chmod +x presto

.. NOTE::
    Presto must run with at least Java 11, so if another version is default on
    your cluster, you will need to explicitly specify the Java 11 executable.
    For example, ``<path_to_java_11_executable> -jar trino``. It may be
    helpful to add an alias for the Presto CLI:
    ``alias trino='<path_to_java_11_executable> -jar <path_to_presto>'``.

3. By default, ``trino-admin`` configures a TPC-H catalog, which generates
   TPC-H data on-the-fly. Using this catalog, issue the following commands to
   run your first Presto query:

.. code-block:: none

    $ ./trino --catalog tpch --schema tiny
    $ select count(*) from lineitem;

The above command assumes that you installed the Presto CLI on the coordinator,
and that the Presto server is on port 8080. If either of these are not the
case, then specify the server location in the command:

.. code-block:: none

    $ ./trino --server <host_name>:<port_number> --catalog tpch --schema tiny

