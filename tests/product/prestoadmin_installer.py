# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module for installing prestoadmin on a cluster.
"""

import errno
import fnmatch
import os
import shutil
import tempfile
import subprocess

import prestoadmin
from tests.base_installer import BaseInstaller
from tests.configurable_cluster import ConfigurableCluster
from tests.product.config_dir_utils import get_install_directory
from tests.product.constants import LOCAL_RESOURCES_DIR, _BASE_IMAGE_NAME, BASE_IMAGE_TAG


class PrestoadminInstaller(BaseInstaller):
    def __init__(self, testcase):
        self.testcase = testcase

    @staticmethod
    def get_dependencies():
        return []

    def install(self, cluster=None, dist_dir=None):
        # Passing in a cluster supports the installation tests. We need to be
        # able to try an installation against an unsupported OS, and for that
        # testcase, we create a cluster that is local to the testcase and then
        # run the install on it. We can't replace self.cluster with the local
        # cluster in the test, because that would prevent the test's "regular"
        # cluster from getting torn down.
        if not cluster:
            cluster = self.testcase.cluster

        if not dist_dir:
            dist_dir = self._build_dist_if_necessary(cluster)
        self._copy_dist_to_host(cluster, dist_dir, cluster.master)
        with open(LOCAL_RESOURCES_DIR + "/install-admin.sh", 'r') as file_obj:
            script = file_obj.read()

        script = script.format(mount_dir=cluster.mount_dir)
        cluster.run_script_on_host(script, cluster.master, tty=False)

    @staticmethod
    def assert_installed(testcase, msg=None):
        cluster = testcase.cluster
        cluster.exec_cmd_on_host(cluster.master, 'test -x %s' % get_install_directory())

    def get_keywords(self):
        return {}

    def _build_dist_if_necessary(self, cluster, unique=False):
        if (not os.path.isdir(cluster.get_dist_dir(unique)) or
                not fnmatch.filter(
                    os.listdir(cluster.get_dist_dir(unique)),
                    'prestoadmin-*.tar.gz')):
            self._build_installer_in_docker(cluster, unique=unique)
        return cluster.get_dist_dir(unique)

    def _build_installer_in_docker(self, cluster, online_installer=None,
                                   unique=False):
        if online_installer is None:
            pa_test_online_installer = os.environ.get('PA_TEST_ONLINE_INSTALLER')
            online_installer = pa_test_online_installer is not None

        if isinstance(cluster, ConfigurableCluster):
            online_installer = True

        temp_dir = os.path.join(tempfile.mkdtemp(), "presto-admin")

        try:
            shutil.copytree(
                prestoadmin.main_dir,
                temp_dir,
                ignore=shutil.ignore_patterns('tmp', '.git', 'presto*.rpm')
            )

            cmd = [prestoadmin.main_dir + "/bin/build-artifacts-in-docker.sh",
                   "--root_dir", temp_dir,
                   "--base_image_name", _BASE_IMAGE_NAME,
                   "--base_image_tag", BASE_IMAGE_TAG,
                   "--online-dist" if online_installer else "--offline-dist"]
            subprocess.check_call(cmd)

            try:
                os.makedirs(cluster.get_dist_dir(unique))
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
            installer_file = fnmatch.filter(
                os.listdir(os.path.join(temp_dir, "dist")),
                'prestoadmin-*.tar.gz')[0]
            shutil.copy(
                os.path.join(os.path.join(temp_dir, "dist"), installer_file),
                cluster.get_dist_dir(unique))
        finally:
            shutil.rmtree(os.path.abspath(os.path.join(temp_dir, os.pardir)), ignore_errors=True)

    @staticmethod
    def _copy_dist_to_host(cluster, local_dist_dir, dest_host):
        for dist_file in os.listdir(local_dist_dir):
            if fnmatch.fnmatch(dist_file, "prestoadmin-*.tar.gz"):
                cluster.copy_to_host(
                    os.path.join(local_dist_dir, dist_file),
                    dest_host)
