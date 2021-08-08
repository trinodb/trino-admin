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
This modules contains read-only constants used throughout
the presto admin project.
"""

import os
import sys

import trinoadmin

# Logging Config File Locations
LOGGING_CONFIG_FILE_NAME = 'trino-admin-logging.ini'
LOGGING_CONFIG_FILE_DIRECTORIES = [
    os.path.join(trinoadmin.main_dir, 'trinoadmin')
]

# Use the BRAND variable to define whether facebook's presto or trinodb's trino is being used at the time
# with the default value being the former.
# You can override the default by defining the environment variable PRESTO_TYPE.
# For example, PRESTO_TYPE=trino means use the latter
BRAND = os.environ.get('PRESTO_TYPE', 'trino').lower()
if BRAND == 'trinodb':
    BRAND = 'trino'
if BRAND not in ['trino', 'presto']:
    print >> sys.stderr, "PRESTO_TYPE only support trino and presto"
    BRAND = 'trino'

# local configuration
LOG_DIR_ENV_VARIABLE = 'PRESTO_ADMIN_LOG_DIR'
CONFIG_DIR_ENV_VARIABLE = 'PRESTO_ADMIN_CONFIG_DIR'
LOCAL_CONF_DIR = '.trinoadmin'
DEFAULT_LOCAL_CONF_DIR = os.path.join(os.path.expanduser('~'), LOCAL_CONF_DIR)
TOPOLOGY_CONFIG_FILE = 'config.json'
COORDINATOR_DIR_NAME = 'coordinator'
WORKERS_DIR_NAME = 'workers'
CATALOG_DIR_NAME = 'catalog'

# remote configuration
REMOTE_CONF_DIR = '/etc/' + BRAND
REMOTE_CATALOG_DIR = os.path.join(REMOTE_CONF_DIR, 'catalog')
REMOTE_PACKAGES_PATH = '/opt/trinoadmin/packages'
DEFAULT_PRESTO_SERVER_LOG_FILE = '/var/log/' + BRAND + '/server.log'
DEFAULT_PRESTO_LAUNCHER_LOG_FILE = '/var/log/' + BRAND + '/launcher.log'
REMOTE_PLUGIN_DIR = '/usr/lib/' + BRAND + '/plugin'
REMOTE_COPY_DIR = '/tmp'

# Presto configuration files
CONFIG_PROPERTIES = "config.properties"
LOG_PROPERTIES = "log.properties"
JVM_CONFIG = "jvm.config"
NODE_PROPERTIES = "node.properties"