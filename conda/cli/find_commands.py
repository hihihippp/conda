from __future__ import print_function, division, absolute_import

import re
import os
import sys
import subprocess
from os.path import isdir, isfile, join



if sys.platform == 'win32':
    dir_paths = [join(sys.prefix, 'Scripts')]
else:
    dir_paths = [join(sys.prefix, 'bin')]

dir_paths.extend(os.environ['PATH'].split(os.pathsep))


def find_executable(cmd):
    executable = 'conda-%s' % cmd
    for dir_path in dir_paths:
        if sys.platform == 'win32':
            for ext in  '.exe', '.bat':
                path = join(dir_path, executable + ext)
                if isfile(path):
                    return path
        else:
            path = join(dir_path, executable)
            if isfile(path):
                return path
    return None


def find_commands():
    if sys.platform == 'win32':
        pat = re.compile(r'conda-(\w+)\.(exe|bat)$')
    else:
        pat = re.compile(r'conda-(\w+)$')

    res = set()
    for dir_path in dir_paths:
        if not isdir(dir_path):
            continue
        for fn in os.listdir(dir_path):
            m = pat.match(fn)
            if m:
                res.add(m.group(1))
    return sorted(res)


def filter_descr(cmd):
    args = [find_executable(cmd), '--help']
    try:
        output = subprocess.check_output(args)
    except subprocess.CalledProcessError:
        print('failed: %s' % (' '.join(args)))
        return
    try:
        descr = output.decode('utf-8').split('\n\n')[1]
    except IndexError:
        descr = '<could not extract description>'
    print('    %-12s %s' % (cmd, descr))


def help():
    print("\nexternal commands:")
    for cmd in find_commands():
        filter_descr(cmd)


if __name__ == '__main__':
    help()
