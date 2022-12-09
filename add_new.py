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

    # Notebook or lab
    notebook_cmd = input('Use jupyter notebook (default, just press enter), or type "lab" to use jupyter lab instead.')
    if notebook_cmd in ['lab', 'Lab', '"Lab"', 'l']:
        notebook_cmd = 'jupyter lab'
    else:
        notebook_cmd = 'jupyter notebook'

    # Can use this to override passcode
    needs_password = input("Requires private key passcode (y/n): ").strip()

    # Get choice of alias name
    new_cmd = input("new command/alias name: ")

    # Generate alias as string
    alias = f'alias {new_cmd}="python {script_loc} --username={username} '
    alias += f'--hostname={hostname} --key_filename={key_filename} --needs_password={needs_password}'
    alias += f' --notebook_cmd={notebook_cmd}"'

    # Add to zshrc?
    add = input('Add to .zshrc? (y/n): ').strip()
    if add == 'y':
        os.system(f"echo '{alias}' >> ~/.zshrc")
        print('Either open a new terminal or run source ~/.zshrc to use your generated alias.')

    print('This is the generated alias:')
    print(alias)


if __name__ == '__main__':
    main()
