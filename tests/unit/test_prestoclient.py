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

import socket
from httplib import HTTPException, HTTPConnection

from fabric.operations import _AttributeString
from mock import patch, PropertyMock

from prestoadmin.prestoclient import URL_TIMEOUT_MS, PrestoClient
from prestoadmin.util.exception import InvalidArgumentError
from tests.base_test_case import BaseTestCase
from tests.unit.base_unit_case import PRESTO_CONFIG


@patch('prestoadmin.util.presto_config.PrestoConfig.coordinator_config',
       return_value=PRESTO_CONFIG)
class TestPrestoClient(BaseTestCase):
    def test_no_sql(self, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        self.assertRaisesRegexp(InvalidArgumentError,
                                "SQL query missing",
                                client.run_sql, "", )

    def test_no_server(self, mock_presto_config):
        client = PrestoClient("", 'any_user')
        self.assertRaisesRegexp(InvalidArgumentError,
                                "Server IP missing",
                                client.run_sql, "any_sql")

    def test_no_user(self, mock_presto_config):
        client = PrestoClient('any_host', "")
        self.assertRaisesRegexp(InvalidArgumentError,
                                "Username missing",
                                client.run_sql, "any_sql")

    @patch.object(PrestoClient, '_create_auth_headers', return_value={'X-Presto-Internal-Bearer': 'any_bearer'})
    @patch('prestoadmin.prestoclient.HTTPConnection')
    def test_default_request_called(self, mock_conn, mock_auth_header, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        headers = {"X-Presto-Catalog": "hive", "X-Presto-Schema": "default",
                   "X-Presto-Source": "presto-admin",
                   "X-Presto-Internal-Bearer": "any_bearer"}

        client.run_sql("any_sql")
        mock_conn.assert_called_with('any_host', 8080, False, URL_TIMEOUT_MS)
        mock_conn().request.assert_called_with("POST", "/v1/statement",
                                               "any_sql", headers)
        self.assertTrue(mock_conn().getresponse.called)

    @patch('prestoadmin.prestoclient.HTTPConnection')
    def test_connection_failed(self, mock_conn, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        client.run_sql("any_sql")

        self.assertTrue(mock_conn().close.called)
        self.assertFalse(client.run_sql("any_sql"))

    @patch('prestoadmin.prestoclient.HTTPConnection')
    def test_http_call_failed(self, mock_conn, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        mock_conn.side_effect = HTTPException("Error")
        self.assertFalse(client.run_sql("any_sql"))

        mock_conn.side_effect = socket.error("Error")
        self.assertFalse(client.run_sql("any_sql"))

    @patch.object(HTTPConnection, 'request')
    @patch.object(HTTPConnection, 'getresponse')
    def test_http_answer_valid(self, mock_response, mock_request, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        mock_response.return_value.read.return_value = '{}'
        type(mock_response.return_value).status = \
            PropertyMock(return_value=200)
        self.assertEquals(client.run_sql('any_sql'), [])

    @patch.object(HTTPConnection, 'request')
    @patch.object(HTTPConnection, 'getresponse')
    def test_http_answer_not_json(self, mock_response,
                                  mock_request, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        mock_response.return_value.read.return_value = 'NOT JSON!'
        type(mock_response.return_value).status =\
            PropertyMock(return_value=200)
        self.assertRaisesRegexp(ValueError, 'No JSON object could be decoded',
                                client.run_sql, 'any_sql')

    @patch('prestoadmin.prestoclient.HTTPConnection')
    @patch('prestoadmin.util.remote_config_util.sudo')
    def testrun_sql_get_port(self, sudo_mock, conn_mock, mock_presto_config):
        client = PrestoClient('any_host', 'any_user')
        client.rows = ['hello']
        client.next_uri = 'hello'
        client.response_from_server = {'hello': 'hello'}
        sudo_mock.return_value = _AttributeString('http-server.http.port=8080')
        sudo_mock.return_value.failed = False
        sudo_mock.return_value.return_code = 0
        client.run_sql('select * from nation')
        self.assertEqual(client.port, 8080)
        self.assertEqual(client.rows, [])
        self.assertEqual(client.next_uri, '')
        self.assertEqual(client.response_from_server, {})
