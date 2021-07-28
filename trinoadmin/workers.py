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
Module for the presto worker`'s configuration.
Loads and validates the workers.json file and creates the files needed
to deploy on the presto cluster
"""

import copy
import logging
import urlparse

from fabric.api import env

import trinoadmin.util.fabricapi as util
from trinoadmin.node import Node
from trinoadmin.trino_conf import validate_presto_conf
from trinoadmin.util import constants
from trinoadmin.util.exception import ConfigurationError
from trinoadmin.util.local_config_util import get_workers_directory

_LOGGER = logging.getLogger(__name__)


class Worker(Node):
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
                          'config.properties': {'coordinator': 'false',
                                                'http-server.http.port':
                                                    '8080',
                                                'query.max-memory': '50GB',
                                                'query.max-memory-per-node':
                                                    '8GB'}
                          }

    def _get_conf_dir(self):
        return get_workers_directory()

    def default_config(self, filename):
        try:
            conf = copy.deepcopy(self.DEFAULT_PROPERTIES[filename])
        except KeyError:
            raise ConfigurationError('Invalid configuration file name: %s' %
                                     filename)
        if filename == 'config.properties':
            coordinator = util.get_coordinator_role()[0]
            conf['discovery.uri'] = 'http://%s:8080' % coordinator
        return conf

    @staticmethod
    def is_localhost(hostname):
        return hostname in ['localhost', '127.0.0.1', '::1']

    @staticmethod
    def validate(conf):
        validate_presto_conf(conf)
        if 'coordinator' not in conf['config.properties']:
            raise ConfigurationError('Must specify coordinator=false in '
                                     'worker\'s config.properties')
        if conf['config.properties']['coordinator'] != 'false':
            raise ConfigurationError('Coordinator must be false in the '
                                     'worker\'s config.properties')
        uri = urlparse.urlparse(conf['config.properties']['discovery.uri'])
        if Worker.is_localhost(uri.hostname) and len(env.roledefs['all']) > 1:
            raise ConfigurationError(
                'discovery.uri should not be localhost in a '
                'multi-node cluster, but found ' + urlparse.urlunparse(uri) +
                '.  You may have encountered this error by '
                'choosing a coordinator that is localhost and a worker that '
                'is not.  The default discovery-uri is '
                'http://<coordinator>:8080')
        return conf
