#!/usr/bin/env python3
"""Robust silent git push script.
- Stages, commits if needed, pushes
- Works from any location
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


def has_any_changes(cwd):
    # True if there are staged OR unstaged changes
    result = subprocess.run(['git', 'status', '--porcelain'], cwd=cwd, stdout=subprocess.PIPE, stderr=DEVNULL, text=True)
    return bool(result.stdout.strip())


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=repo_root)
        run(['git', 'fetch', '--all', '--prune'], cwd=repo_root)
        if has_any_changes(repo_root):
            run(['git', 'add', '-A'], cwd=repo_root)
            # Avoid failing when nothing to commit
            subprocess.run(['git', 'commit', '-m', 'chore: update'], cwd=repo_root, env=ENV, stdout=DEVNULL, stderr=DEVNULL)
        run(['git', 'push', 'origin', 'main'], cwd=repo_root)
    except subprocess.CalledProcessError:
        print('git_push: operation failed', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
