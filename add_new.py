import os
from pathlib import Path


def main():

    # Get script loc
    cwd = os.getcwd()
    script_loc = os.path.join(cwd, 'dg_notebook.py')

    username = input("username: ")
    hostname = input("server ip: ")

    # Get right path
    key_filename = input("private key loc: ")
    if '~' in key_filename:
        key_filename = os.path.expanduser(key_filename)
    key_filename = os.path.abspath(key_filename)

    password = input("private key passcode (empty for none): ")
    new_cmd = input("command name: ")

    # Generate alias as string
    alias = f'alias {new_cmd}="python {script_loc} --username={username} '
    alias += f'--hostname={hostname} --key_filename={key_filename} --password={password}"'

    add = input('Add to .zshrc? (y/n): ').strip()
    if add == 'y':
        os.system(f"echo '{alias}' >> ~/.zshrc")

    print(alias)

if __name__ == '__main__':
    main()
