import time
import paramiko
import getpass
import webbrowser
import fire
import typing
from sshtunnel import SSHTunnelForwarder


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
    return ssh


def _check_for_link(lines: str) -> str:

    # This is a bit hacky, but works fine
    for line in lines.split('\n'):
        line = line.strip()
        if '/?token=' in line:
            return line.split(' ')[-1]

    return ''

def _start_notebook(ssh, notebook_cmd):

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

    return notebook_link


def main(username: str,
         hostname: str,
         key_filename: str,
         needs_password: bool = False,
         notebook_cmd: str = 'notebook'):
    """Setup notebook on remote server, e.g., dgx2

    Args:
        username (str): Your username
        hostname (str): The address of the server
        key_filename (str): Location of your private key.
        needs_password (bool, optional): Does the private key require
            a passcode? By default, this is set to False, but if
            True, then will prompt user for a passcode.
        notebook_cmd (str, optional): By default 'notebook' and
            a jupyter notebook is launched. Can also provide
            'lab' to run jupyter lab instead.
    """

    print(type(needs_password))

    # Prompt for password if needed
    if needs_password:
        password = getpass.getpass('Private key password: ')
        if len(password) == 0:
            password = None
    else:
        password = None

    # Make sure input looks okay
    notebook_cmd = notebook_cmd.strip()
    if notebook_cmd not in {'notebook', 'lab'}:
        raise RuntimeError(f'Invalid notebook_cmd {notebook_cmd}')
    else:
        notebook_cmd = 'jupyter ' + notebook_cmd

    # Start connection to remote server which will run notebook
    ssh = _init_ssh_client(username, hostname, key_filename, password)
    print(f'Connected to {hostname} over SSH')

    # Run notebook
    notebook_link = _start_notebook(ssh, notebook_cmd)
    notebook_port = notebook_link.split(':')[-1].split('/')[0]
    print(f'Notebook running on remote host on port: {notebook_port}')

    # Start ssh tunnel forwarding, equiv of:
    # "ssh -L port:localhost:port username@hostname -i key_filename"
    forward_server = SSHTunnelForwarder(ssh_address_or_host=hostname,
                                        ssh_username=username,
                                        ssh_pkey=key_filename,
                                        ssh_private_key_password=password,
                                        remote_bind_address=('127.0.0.1', int(notebook_port)))
    forward_server.start()
    print('Started port forwarding connection')

    # Open notebook in browser
    local_link = notebook_link.replace(notebook_port, str(forward_server.local_bind_port))
    webbrowser.open(local_link, new=2)

    # Just keep running until user wants to quit
    try:
        close = 'keep going'
        while close == 'keep going':
            print('Press Enter to close connections')
            close = input('')
    except KeyboardInterrupt:
        pass

    # Close connections
    forward_server.stop()
    ssh.close()


if __name__ == '__main__':
    fire.Fire(main)
