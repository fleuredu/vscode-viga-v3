#!/usr/bin/env python3
"""Silent git add/commit/push script.
- Stages all changes
- Commits only when there is something to commit
- Pushes to origin/main
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


def has_staged_changes(repo_root):
    # Returns True if there are staged changes
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=repo_root)
    return result.returncode == 1


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(repo_dir, '..'))
    try:
        run(['git', 'fetch', '--all'], cwd=repo_root)
        run(['git', 'add', '-A'], cwd=repo_root)
        if has_staged_changes(repo_root):
            run(['git', 'commit', '-m', 'chore: update'], cwd=repo_root)
        run(['git', 'push', 'origin', 'main'], cwd=repo_root)
    except subprocess.CalledProcessError:
        print('git_push: operation failed', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
