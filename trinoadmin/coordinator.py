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
Module for the presto coordinator's configuration.
Loads and validates the coordinator.json file and creates the files needed
to deploy on the presto cluster
"""
import copy
import logging

from fabric.api import env

from trinoadmin.util import constants
from trinoadmin.node import Node
from trinoadmin.trino_conf import validate_presto_conf
from trinoadmin.util.exception import ConfigurationError
from trinoadmin.util.local_config_util import get_coordinator_directory

_LOGGER = logging.getLogger(__name__)


class Coordinator(Node):
    DEFAULT_PROPERTIES = {'node.properties':
                          {'node.environment': constants.BRAND,
                           'node.data-dir': '/var/lib/{}/data'.format(constants.BRAND),
                           'node.launcher-log-file':
                               '/var/log/{}/launcher.log'.format(constants.BRAND),
                           'node.server-log-file':
                               '/var/log/{}/server.log'.format(constants.BRAND),
                           'catalog.config-dir': '/etc/{}/catalog'.format(constants.BRAND),
                           'plugin.dir': '/usr/lib/{}/lib/plugin'.format(constants.BRAND)},
                          'jvm.config': ['-server',
                                         '-Xmx16G',
                                         '-XX:-UseBiasedLocking',
                                         '-XX:+UseG1GC',
                                         '-XX:G1HeapRegionSize=32M',
                                         '-XX:+ExplicitGCInvokesConcurrent',
                                         '-XX:+ExitOnOutOfMemoryError',
                                         '-XX:+UseGCOverheadLimit',
                                         '-XX:+HeapDumpOnOutOfMemoryError',
                                         '-XX:ReservedCodeCacheSize=512M',
                                         '-Djdk.attach.allowAttachSelf=true',
                                         '-Djdk.nio.maxCachedBufferSize=2000000',
                                         '-DHADOOP_USER_NAME=hive',  # not Presto default
                                         ],
                          'config.properties': {
                              'coordinator': 'true',
                              'discovery-server.enabled': 'true',
                              'http-server.http.port': '8080',
                              'node-scheduler.include-coordinator': 'false',
                              'query.max-memory': '50GB',
                              'query.max-memory-per-node': '8GB'}
                          }

    def _get_conf_dir(self):
        return get_coordinator_directory()

    def default_config(self, filename):
        try:
            conf = copy.deepcopy(self.DEFAULT_PROPERTIES[filename])
        except KeyError:
            raise ConfigurationError('Invalid configuration file name: %s' %
                                     filename)
        if filename == 'config.properties':
            coordinator = env.roledefs['coordinator'][0]
            workers = env.roledefs['worker']
            if coordinator in workers:
                conf['node-scheduler.include-coordinator'] = 'true'
            conf['discovery.uri'] = 'http://%s:8080' % coordinator
        return conf

    @staticmethod
    def validate(conf):
        validate_presto_conf(conf)
        if 'coordinator' not in conf['config.properties']:
            raise ConfigurationError('Must specify coordinator=true in '
                                     'coordinator\'s config.properties')
        if conf['config.properties']['coordinator'] != 'true':
            raise ConfigurationError('Coordinator cannot be false in the '
                                     'coordinator\'s config.properties.')
        return conf
