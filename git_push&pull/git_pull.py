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
        env=env or ENV,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        text=True,
        check=False,
    )
    dt = (time.time() - t0) * 1000
    if capture:
        return proc.returncode, proc.stdout, dt
    return proc.returncode, None, dt

def print_section(title):
    print(f"\n=== {title} ===")


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    debug = '--debug' in sys.argv
    env = ENV.copy()
    if debug:
        env['GIT_TRACE'] = '1'
        env['GIT_CURL_VERBOSE'] = '1'
    
    print_section('Repo')
    print('path:', repo_root)

    # Verify repo
    code, out, ms = run(['git', 'rev-parse', '--is-inside-work-tree'], repo_root, capture=True, env=env)
    print('rev-parse:', out.strip(), f'({int(ms)} ms)')
    if code != 0:
        print('Not a git repository.')
        sys.exit(1)

    # Status overview
    print_section('Status')
    code, out, ms = run(['git', 'status', '-sb'], repo_root, capture=True, env=env)
    print(out, end='')
    if code != 0:
        sys.exit(code)

    # Stash if needed
    print_section('Stash (include untracked)')
    code, out, ms = run(['git', 'stash', '--include-untracked'], repo_root, capture=True, env=env)
    print(out or '(no changes stashed)', f'({int(ms)} ms)')

    # Pull rebase
    print_section('Pull --rebase origin main')
    code, out, ms = run(['git', 'pull', '--rebase', 'origin', 'main'], repo_root, capture=True, env=env)
    print(out or '(up to date)', f'({int(ms)} ms)')
    if code != 0:
        print('Rebase encountered a problem. Resolve conflicts and run again.')
        sys.exit(code)

    # Stash pop if something was stashed
    code, out, _ = run(['git', 'stash', 'list'], repo_root, capture=True, env=env)
    if out.strip():
        print_section('Stash pop')
        code, out, ms = run(['git', 'stash', 'pop'], repo_root, capture=True, env=env)
        print(out, f'({int(ms)} ms)')

    print('\nDone.')


if __name__ == '__main__':
    main()
