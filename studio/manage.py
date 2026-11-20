#!/usr/bin/env python3
import os
import sys

from django.core.management import execute_from_command_line


if __name__ == "__main__":
    settings_module = "central.test_settings" if sys.argv[1:2] == ["test"] else "central.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    execute_from_command_line(sys.argv)
