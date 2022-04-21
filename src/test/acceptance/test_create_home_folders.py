from common_helper_process import execute_shell_command_get_return_code
from common_helper_files import get_dir_of_file

import os


SRC_DIR = os.path.join(get_dir_of_file(__file__), '../../')
MAINSCRIPT = os.path.join(SRC_DIR, 'create_home_folders.py')


def test_help():
    output, return_code = execute_shell_command_get_return_code('{} -h'.format(MAINSCRIPT), timeout=5)
    assert return_code == 0
    assert 'usage: create_home_folders.py' in output


def test_complete_run():
    output, return_code = execute_shell_command_get_return_code('{} -c test.cfg -d'.format(MAINSCRIPT), timeout=60)
    assert return_code == 0
    assert 'users need new rooms' in output
    assert 'oauth/revoke "HTTP/1.1 200 OK"' in output
