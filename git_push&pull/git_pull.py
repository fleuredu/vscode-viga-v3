#!/usr/bin/env python3
"""Verbose git pull script for VS Code.
- Prints each step and command duration
- Shows current branch, remote, ahead/behind, and uncommitted changes
- Debug flags: GIT_TRACE=1 and GIT_CURL_VERBOSE=1 when --debug
Usage:
    python git_pull.py [--debug]
"""
import os
import subprocess
import sys
import time

ENV = os.environ.copy()
ENV.setdefault('GIT_TERMINAL_PROMPT', '0')
ENV.setdefault('LC_ALL', 'C')
ENV.setdefault('LANG', 'C')

def run(cmd, cwd, capture=False, env=None):
    t0 = time.time()
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=(env or ENV),
        stdout=(subprocess.PIPE if capture else None),
        stderr=(subprocess.STDOUT if capture else None),
        text=True,
        check=False,
    )
    ms = int((time.time() - t0) * 1000)
    return proc.returncode, (proc.stdout if capture else ''), ms


def print_section(title):
    print("\n=== {0} ===".format(title))

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    debug = ('--debug' in sys.argv)
    env = ENV.copy()
    if debug:
        env['GIT_TRACE'] = '1'
        env['GIT_CURL_VERBOSE'] = '1'

    print_section('Repo')
    print('path:', repo_root)

    code, out, ms = run(['git', 'rev-parse', '--is-inside-work-tree'], repo_root, capture=True, env=env)
    print('rev-parse:', (out or '').strip(), '({0} ms)'.format(ms))
    if code != 0:
        print('Not a git repository.')
        sys.exit(1)

    print_section('Status')
    code, out, ms = run(['git', 'status', '-sb'], repo_root, capture=True, env=env)
    sys.stdout.write(out or '')
    if code != 0:
        sys.exit(code)

    print_section('Fetch --all --prune')
    code, out, ms = run(['git', 'fetch', '--all', '--prune'], repo_root, capture=True, env=env)
    print((out or '(no output)').strip(), '({0} ms)'.format(ms))
    if code != 0:
        sys.exit(code)

    # Stash if needed
    print_section('Stash (include untracked)')
    code, out, ms = run(['git', 'stash', '--include-untracked'], repo_root, capture=True, env=env)
    print((out or '(no changes stashed)').strip(), '({0} ms)'.format(ms))

    print_section('Pull --rebase origin main')
    code, out, ms = run(['git', 'pull', '--rebase', 'origin', 'main'], repo_root, capture=True, env=env)
    print((out or '(up to date)').strip(), '({0} ms)'.format(ms))
    if code != 0:
        print('Rebase encountered a problem. Resolve conflicts and run again.')
        sys.exit(code)

    code, out, _ = run(['git', 'stash', 'list'], repo_root, capture=True, env=env)
    if (out or '').strip():
        print_section('Stash pop')
        code, out, ms = run(['git', 'stash', 'pop'], repo_root, capture=True, env=env)
        print((out or '').strip(), '({0} ms)'.format(ms))

    print('\nDone.')

if __name__ == '__main__':
    main()
