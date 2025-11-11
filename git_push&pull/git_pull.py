#!/usr/bin/env python3
"""Silent git pull script.
- No logs written to files or console unless there is an error.
"""
import os
import subprocess
import sys

ENV = os.environ.copy()
ENV.setdefault('GIT_TERMINAL_PROMPT', '0')

DEVNULL = subprocess.DEVNULL


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, env=ENV, stdout=DEVNULL, stderr=DEVNULL, check=True)


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(repo_dir, '..'))
    try:
        run(['git', 'fetch', '--all'], cwd=repo_root)
        run(['git', 'pull', '--rebase', 'origin', 'main'], cwd=repo_root)
        print('git_pull: başarıyla güncellendi!')
    except subprocess.CalledProcessError:
        # On error, print minimal message to help debugging
        print('git_pull: operation failed', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
