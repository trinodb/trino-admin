===========
Release 2.9
===========

Bug Fixes and Enhancements
--------------------------

* Update for RPM plugin directory location change and remove hard-coded
  plugin directory path.
* Deprecate JAVA8_HOME in favor of JAVA_HOME.
* Update to allow installing and managing Presto deployed on JDK 8.
* Add basic authentication to query endpoint request for
  `collect query_info` command.
