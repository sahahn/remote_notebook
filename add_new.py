import os
from pathlib import Path


def main():

    # Get script loc
    cwd = os.getcwd()
    script_loc = os.path.join(cwd, 'dg_notebook.py')

    # Get basic info
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
        notebook_cmd = 'lab'
    else:
        notebook_cmd = 'notebook'

    # Can use this to override passcode
    needs_password = input("Requires private key passcode (y/n): ").strip().lower()
    if needs_password == 'y':
        needs_password = True
    else:
        needs_password = False

    # Get choice of alias name
    new_cmd = input("new command/alias name: ")

    # Generate alias as string
    cmd = f'python {script_loc} --username {username}'
    cmd += f' --hostname {hostname} --key_filename {key_filename} --needs_password {needs_password}'
    cmd += f' --notebook_cmd {notebook_cmd}'

    # Add to zshrc?
    add = input('Add to .zshrc? (y/n): ').strip()
    if add == 'y':
        alias = f'alias {new_cmd}="{cmd}"'
        os.system(f"echo '{alias}' >> ~/.zshrc")
        print('Either open a new terminal or run source ~/.zshrc to use your generated alias.')
        print('You can also go into ~/.zshrc and manually edit the command.')
        print('If everything worked you should now be able to start a remote notebook as:')
        print(new_cmd)

    else:
        print('This is your generated command for starting a remote notebook!')
        print(cmd)

if __name__ == '__main__':
    main()
