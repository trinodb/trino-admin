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
from StringIO import StringIO

from trinoadmin.util.presto_config import PrestoConfig
from tests.unit.base_unit_case import BaseUnitCase


class TestPrestoConfig(BaseUnitCase):
    realworld = """
coordinator=true
discovery-server.enabled=true
discovery.uri=http://localhost:8285
http-server.http.port=8285
node-scheduler.include-coordinator=true
query.max-memory-per-node=8GB
query.max-memory=50GB
http-server.https.port=8444
http-server.https.enabled=true
http-server.https.keystore.path=/tmp/mykeystore.jks
http-server.https.keystore.key=testldap
internal-communication.shared-secret=internal-secret
    """

    def _get_presto_config(self, config, node_config):
        config_file = StringIO(config)
        return PrestoConfig.from_file(config_file, StringIO(node_config))

    def _assert_use_https(self, expected, config, node_config):
        presto_config = self._get_presto_config(config, node_config)
        self.assertEqual(presto_config.use_https(), expected)

    def test_use_https(self):
        self._assert_use_https(False, "", "")
        self._assert_use_https(False, "http-server.http.enabled=true", "")
        self._assert_use_https(False, "http-server.https.enabled=true", "")

        self._assert_use_https(False, """
http-server.http.enabled=true
http-server.https.enabled=true")
        """, "")

        self._assert_use_https(True, """
http-server.http.enabled=false
http-server.https.enabled=true
        """, "")

        self._assert_use_https(False, self.realworld, "")

    def test_get_node_environment(self):
        presto_config = self._get_presto_config("", "node.environment=presto")
        self.assertEqual("presto", presto_config.get_node_environment())
