import os
import tempfile

sshCmdLine = 'sshpass -p {0} ssh -o UserKnownHostsFile={1} -o StrictHostKeyCheck=no {2}@{3} -o {4}'

def launch_shell (username, hostname, password, port = 22):
    """
    Launches an ssh shell
    """
    if not username or not hostname or not password:
        return False
    tmpFile = tempfile.mktemp()
    os.system(sshCmdLine.format(password, tmpFile, username, hostname, port))
    os.remove(tmpFile)

    return True

def do_cmd (username, hostname, password, command, port = 22):
    """
    Runs a command via ssh
    """
    if not username or not hostname or not password or not command:
        return False
    tmpFile = tempfile.mktemp()
    os.system("{0} {1}".format(sshCmdLine.format(password, tmpFile, username, hostname, port), command))
    os.remove(tmpFile)
