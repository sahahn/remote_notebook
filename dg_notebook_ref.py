import time
import paramiko
import os
import webbrowser
import fire
import typing


def _init_ssh_client(username: str, hostname: str,
                     key_filename: str,
                     password: typing.Optional[str]) -> paramiko.SSHClient:

    # Init ssh connection
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()

    # Connect
    ssh.connect(hostname=hostname,
                username=username,
                key_filename=key_filename,
                password=password)

    print(f'Connected to {hostname} over SSH')
    return ssh


def _check_for_link(lines: str) -> str:

    # This is a bit hacky, but works fine
    for line in lines.split('\n'):
        line = line.strip()
        if '/?token=' in line:
            return line.split(' ')[-1]

    return ''


def main(username: str, hostname: str,
         key_filename: str, password: str='',
         notebook_cmd: str='jupyter notebook'):
    """Setup notebook on remote server, e.g., dgx2

    Args:
        username (str): Your username
        hostname (str): The address of the server
        key_filename (str): Location of your private key.
        password (str, optional): This is the password
            if any used for your private key. Set to '' if
            no passcode set.
        notebook_cmd (str, optional): By default 'jupyter notebook' and
            a jupyter notebook is launched. Can also provide
            'jupyter lab' to run jupyter lab instead.
    """

    # Empty str password to None
    if len(password) == 0:
        password = None

    # Make sure input okay
    notebook_cmd = notebook_cmd.strip()
    if notebook_cmd not in {'jupyter notebook', 'jupyter lab'}:
        raise RuntimeError(f'Invalid notebook_cmd {notebook_cmd}')

    # Start connection to remote server which will run notebook
    ssh = _init_ssh_client(username, hostname, key_filename, password)

    # Start the notebook
    _, stdout, _ = ssh.exec_command(f'{notebook_cmd} --no-browser')

    notebook_link = None
    while stdout is not None:
        channel = stdout.channel
        channel.set_combine_stderr(True)
        exited = channel.exit_status_ready()
        while channel.recv_ready():
            lines = channel.recv(1024).decode('utf8')
            notebook_link = _check_for_link(lines)
            if len(notebook_link) > 0:
                stdout = None

        if exited:
            stdout = None

        time.sleep(.1)

    print('Setup notebook.')

    # Open in browser
    webbrowser.open(notebook_link, new=2)

    # Open port forwarding
    port = notebook_link.split(':')[-1].split('/')[0]
    os.system(f'ssh -L {port}:localhost:{port} {username}@{hostname} -i {key_filename}')


if __name__ == '__main__':
    fire.Fire(main)
