"""Tests for the shared HTTPS session configuration."""

import os
import tempfile
import unittest
from unittest import mock

import main


class HttpSessionTests(unittest.TestCase):
    def test_session_uses_certifi_proxy_environment_and_limits(self):
        with (
            mock.patch.object(main.aiohttp, "TCPConnector") as connector,
            mock.patch.object(main.aiohttp, "ClientSession") as client_session,
        ):
            result = main._create_http_session(limit=12, limit_per_host=7)

        connector.assert_called_once()
        connector_kwargs = connector.call_args.kwargs
        self.assertEqual(connector_kwargs["limit"], 12)
        self.assertEqual(connector_kwargs["limit_per_host"], 7)
        self.assertEqual(connector_kwargs["ssl"].check_hostname, True)
        client_session.assert_called_once_with(
            connector=connector.return_value,
            trust_env=True,
        )
        self.assertIs(result, client_session.return_value)

    def test_custom_ca_bundle_is_added_to_ssl_context(self):
        with tempfile.NamedTemporaryFile(suffix=".pem", delete=False) as ca_file:
            ca_path = ca_file.name
        self.addCleanup(lambda: os.path.exists(ca_path) and os.remove(ca_path))

        with (
            mock.patch.dict(os.environ, {"EDOPRO_CA_BUNDLE": ca_path}, clear=False),
            mock.patch.object(main.aiohttp, "TCPConnector"),
            mock.patch.object(main.aiohttp, "ClientSession"),
            mock.patch.object(main.ssl.SSLContext, "load_verify_locations") as load_cas,
        ):
            main._create_http_session()

        load_cas.assert_any_call(cafile=ca_path)


if __name__ == "__main__":
    unittest.main()
