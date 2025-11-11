#!/usr/bin/env python3
"""Robust silent git pull script.
- Works from any location
- Avoids terminal prompts
- Silent unless error occurs
"""
import os
import subprocess
import sys

ENV = os.environ.copy()
ENV.setdefault('GIT_TERMINAL_PROMPT', '0')
ENV.setdefault('LC_ALL', 'C')
ENV.setdefault('LANG', 'C')

DEVNULL = subprocess.DEVNULL


def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, env=ENV, stdout=DEVNULL, stderr=DEVNULL, check=True)


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=repo_root)
        run(['git', 'fetch', '--all', '--prune'], cwd=repo_root)
        run(['git', 'pull', '--rebase', 'origin', 'main'], cwd=repo_root)
    except subprocess.CalledProcessError:
        print('git_pull: operation failed', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
