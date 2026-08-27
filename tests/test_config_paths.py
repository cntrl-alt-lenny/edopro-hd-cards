import json
import os
import tempfile
import unittest
from unittest import mock

import config as config_module
from config import Config


class ConfigPathTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.test_root = self.temp_dir.name
        self.original_cwd = os.getcwd()
        os.chdir(self.test_root)
        self.addCleanup(os.chdir, self.original_cwd)

    def test_default_config_uses_script_directory_when_running_from_source(self):
        script_dir = os.path.join(self.test_root, "source-build")
        os.makedirs(script_dir, exist_ok=True)
        fake_config_py = os.path.join(script_dir, "config.py")

        with mock.patch.object(config_module, "__file__", fake_config_py):
            cfg = Config([])

        expected = os.path.join(script_dir, config_module.CONFIG_FILENAME)
        self.assertEqual(cfg.config_path, expected)

    def test_default_config_uses_user_data_directory_when_frozen(self):
        frozen_dir = os.path.join(self.test_root, "frozen-build")
        os.makedirs(frozen_dir, exist_ok=True)
        fake_executable = os.path.join(frozen_dir, "EDOPro-HD-Sync.exe")

        with (
            mock.patch.object(config_module.sys, "executable", fake_executable),
            mock.patch.object(config_module.sys, "frozen", True, create=True),
            mock.patch.object(
                config_module, "user_data_dir", return_value=os.path.join(self.test_root, "state")
            ),
        ):
            cfg = Config([])

        expected = os.path.join(self.test_root, "state", config_module.CONFIG_FILENAME)
        self.assertEqual(cfg.config_path, expected)

    def test_user_data_dir_uses_windows_local_app_data(self):
        with (
            mock.patch.object(config_module.sys, "platform", "win32"),
            mock.patch.dict(
                config_module.os.environ,
                {"LOCALAPPDATA": os.path.join(self.test_root, "Local"), "APPDATA": ""},
                clear=True,
            ),
        ):
            self.assertEqual(
                config_module.user_data_dir(),
                os.path.join(self.test_root, "Local", config_module.APP_DATA_NAME),
            )

    def test_user_data_dir_uses_macos_application_support(self):
        with mock.patch.object(config_module.sys, "platform", "darwin"):
            self.assertEqual(
                config_module.user_data_dir(),
                os.path.join(
                    os.path.expanduser("~"),
                    "Library",
                    "Application Support",
                    config_module.APP_DATA_NAME,
                ),
            )

    def test_user_data_dir_uses_xdg_config_on_linux(self):
        xdg_dir = os.path.join(self.test_root, "xdg")
        with (
            mock.patch.object(config_module.sys, "platform", "linux"),
            mock.patch.dict(config_module.os.environ, {"XDG_CONFIG_HOME": xdg_dir}, clear=True),
        ):
            self.assertEqual(
                config_module.user_data_dir(),
                os.path.join(xdg_dir, config_module.APP_DATA_NAME),
            )

    def test_default_config_loads_existing_file_from_script_directory(self):
        script_dir = os.path.join(self.test_root, "source-build")
        os.makedirs(script_dir, exist_ok=True)
        local_config = os.path.join(script_dir, config_module.CONFIG_FILENAME)
        with open(local_config, "w", encoding="utf-8") as file_obj:
            json.dump({"concurrency": 7}, file_obj)

        with mock.patch.object(config_module, "__file__", os.path.join(script_dir, "config.py")):
            cfg = Config([])

        self.assertEqual(cfg.config_path, local_config)
        self.assertEqual(cfg.concurrency, 7)

    def test_saving_edopro_path_creates_config_in_user_data_directory(self):
        frozen_dir = os.path.join(self.test_root, "frozen-build")
        os.makedirs(frozen_dir, exist_ok=True)
        fake_executable = os.path.join(frozen_dir, "EDOPro-HD-Sync.exe")
        edopro_path = os.path.join(self.test_root, "ProjectIgnis")
        os.makedirs(edopro_path, exist_ok=True)

        with (
            mock.patch.object(config_module.sys, "executable", fake_executable),
            mock.patch.object(config_module.sys, "frozen", True, create=True),
            mock.patch.object(
                config_module, "user_data_dir", return_value=os.path.join(self.test_root, "state")
            ),
        ):
            cfg = Config([])
            saved = cfg.set_edopro_path(edopro_path, save=True)

        self.assertTrue(saved)
        self.assertEqual(
            cfg.config_path,
            os.path.join(self.test_root, "state", config_module.CONFIG_FILENAME),
        )
        self.assertTrue(os.path.exists(cfg.config_path))
        with open(cfg.config_path, encoding="utf-8") as file_obj:
            saved_config = json.load(file_obj)
        self.assertEqual(saved_config["edopro_path"], os.path.abspath(edopro_path))
        self.assertFalse(os.path.exists(cfg.config_path + ".part"))

    def test_save_report_can_be_loaded_from_config_file(self):
        config_path = os.path.join(self.test_root, "config.json")
        with open(config_path, "w", encoding="utf-8") as file_obj:
            json.dump({"save_report": True}, file_obj)

        cfg = Config(["--config", config_path])

        self.assertTrue(cfg.save_report)

    def test_save_report_can_be_enabled_from_cli(self):
        cfg = Config(["--config", os.path.join(self.test_root, "config.json"), "--save-report"])

        self.assertTrue(cfg.save_report)

    def test_manual_map_file_uses_config_directory(self):
        config_path = os.path.join(self.test_root, "nested", "config.json")

        cfg = Config(["--config", config_path])

        self.assertEqual(
            cfg.manual_map_file,
            os.path.join(self.test_root, "nested", "manual_map.json"),
        )

    def test_packaged_build_defaults_to_parent_edopro_folder_when_no_config_exists(self):
        edopro_root = os.path.join(self.test_root, "ProjectIgnis")
        tool_dir = os.path.join(edopro_root, "EDOPro HD Sync Windows")
        os.makedirs(tool_dir, exist_ok=True)
        open(os.path.join(edopro_root, "EDOPro.exe"), "wb").close()
        fake_executable = os.path.join(tool_dir, "EDOPro-HD-Sync.exe")

        with (
            mock.patch.object(config_module.sys, "executable", fake_executable),
            mock.patch.object(config_module.sys, "frozen", True, create=True),
            mock.patch.object(
                config_module, "user_data_dir", return_value=os.path.join(self.test_root, "state")
            ),
        ):
            cfg = Config([])

        self.assertEqual(cfg.edopro_path, os.path.abspath(edopro_root))

    def test_mac_app_runtime_checks_folder_containing_the_app(self):
        game_root = os.path.join(self.test_root, "Tools")
        app_dir = os.path.join(game_root, "EDOPro HD Sync.app", "Contents", "MacOS")
        os.makedirs(app_dir, exist_ok=True)
        os.makedirs(os.path.join(game_root, "expansions"), exist_ok=True)
        open(os.path.join(game_root, "expansions", "cards.cdb"), "wb").close()

        with mock.patch.object(config_module.sys, "platform", "darwin"):
            found = config_module._detect_packaged_edopro_path(
                os.path.join(app_dir, "EDOPro-HD-Sync")
            )

        self.assertEqual(found, os.path.abspath(game_root))

    def test_legacy_packaged_config_is_migrated(self):
        frozen_dir = os.path.join(self.test_root, "frozen-build")
        os.makedirs(frozen_dir, exist_ok=True)
        fake_executable = os.path.join(frozen_dir, "EDOPro-HD-Sync.exe")
        legacy_path = os.path.join(frozen_dir, config_module.CONFIG_FILENAME)
        with open(legacy_path, "w", encoding="utf-8") as file_obj:
            json.dump({"concurrency": 9}, file_obj)

        with (
            mock.patch.object(config_module.sys, "executable", fake_executable),
            mock.patch.object(config_module.sys, "frozen", True, create=True),
            mock.patch.object(
                config_module, "user_data_dir", return_value=os.path.join(self.test_root, "state")
            ),
        ):
            cfg = Config([])

        self.assertEqual(cfg.concurrency, 9)
        self.assertTrue(os.path.exists(cfg.config_path))

    def test_legacy_packaged_manual_map_remains_available(self):
        frozen_dir = os.path.join(self.test_root, "frozen-build")
        os.makedirs(frozen_dir, exist_ok=True)
        fake_executable = os.path.join(frozen_dir, "EDOPro-HD-Sync.exe")
        legacy_map = os.path.join(frozen_dir, "manual_map.json")
        with open(legacy_map, "w", encoding="utf-8") as file_obj:
            file_obj.write("{}")

        with (
            mock.patch.object(config_module.sys, "executable", fake_executable),
            mock.patch.object(config_module.sys, "frozen", True, create=True),
            mock.patch.object(
                config_module, "user_data_dir", return_value=os.path.join(self.test_root, "state")
            ),
        ):
            cfg = Config([])

        self.assertEqual(cfg.manual_map_file, legacy_map)

    def test_health_check_can_be_enabled_from_cli(self):
        cfg = Config(["--config", os.path.join(self.test_root, "config.json"), "--health-check"])

        self.assertTrue(cfg.health_check)

    def test_edopro_path_flag_overrides_config_file(self):
        config_path = os.path.join(self.test_root, "config.json")
        with open(config_path, "w", encoding="utf-8") as file_obj:
            json.dump({"edopro_path": os.path.join(self.test_root, "from-config")}, file_obj)
        cli_path = os.path.join(self.test_root, "from-flag")

        cfg = Config(["--config", config_path, "--edopro-path", cli_path])

        self.assertEqual(cfg.edopro_path, os.path.abspath(cli_path))
        self.assertEqual(cfg.pics_path, os.path.join(os.path.abspath(cli_path), "pics"))

    def test_force_defaults_to_false_even_when_frozen(self):
        frozen_dir = os.path.join(self.test_root, "frozen-build")
        os.makedirs(frozen_dir, exist_ok=True)
        fake_executable = os.path.join(frozen_dir, "EDOPro-HD-Sync.exe")

        with (
            mock.patch.object(config_module.sys, "executable", fake_executable),
            mock.patch.object(config_module.sys, "frozen", True, create=True),
            mock.patch.object(
                config_module, "user_data_dir", return_value=os.path.join(self.test_root, "state")
            ),
        ):
            cfg = Config([])

        self.assertFalse(cfg.force)

    def test_force_flag_enables_full_refresh(self):
        cfg = Config(["--config", os.path.join(self.test_root, "config.json"), "--force"])

        self.assertTrue(cfg.force)


if __name__ == "__main__":
    unittest.main()
