import os
import tempfile

sshCmdLine = ('sshpass -p {0} ssh -q -o UserKnownHostsFile={1} '
              '-o StrictHostKeyChecking=no {2}@{3} -p {4}')


def launch_shell(username, hostname, password, port=22):
    """
    Launches an ssh shell
    """
    if not username or not hostname or not password:
        return False

    with tempfile.NamedTemporaryFile() as tmpFile:
        os.system(sshCmdLine.format(password, tmpFile.name, username, hostname,
                                    port))
    return True


def do_cmd(username, hostname, password, command, port=22):
    """
    Runs a command via ssh
    """
    if not username or not hostname or not password or not command:
        return False

    with tempfile.NamedTemporaryFile() as tmpFile:
        os.system("{0} {1}".format(sshCmdLine.format(password, tmpFile.name,
                                                     username, hostname, port),
                                   command))
    return True
