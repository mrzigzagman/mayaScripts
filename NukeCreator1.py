import subprocess
import os
import os.path

nuke = os.path.join(os.path.dirname(__file__), "NukeCreator2.py")


def main():
    print 'Start!'

    command = 'nuke -t -- %s &' % nuke
    try:
        process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print line,
        print 'tried1'
        err = process.stderr.read()
        if err:
            raise Exception(err)
    finally:
        print 'finally'


    print 'End!'
