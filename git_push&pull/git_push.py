#!/usr/bin/env python3
"""Verbose git push script for VS Code.
- Prints each step and what changed
- Auto commits only when needed, with diff summary
- Debug flags: GIT_TRACE=1 and GIT_CURL_VERBOSE=1 when --debug
Usage:
    python git_push.py [--debug] [--message "msg"]
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
    message = 'chore: update'
    if '--message' in sys.argv:
        i = sys.argv.index('--message')
        message = sys.argv[i+1] if i+1 < len(sys.argv) else message
    env = ENV.copy()
    if debug:
        env['GIT_TRACE'] = '1'
        env['GIT_CURL_VERBOSE'] = '1'

    print_section('Repo')
    print('path:', repo_root)

    # Status
    print_section('Status before')
    code, out, _ = run(['git', 'status', '-sb'], repo_root, capture=True, env=env)
    print(out, end='')

    # Fetch
    print_section('Fetch --all --prune')
    code, out, ms = run(['git', 'fetch', '--all', '--prune'], repo_root, capture=True, env=env)
    print(out or '(no output)', f'({int(ms)} ms)')

    # Add/Commit if needed
    code, out, _ = run(['git', 'status', '--porcelain'], repo_root, capture=True, env=env)
    if out.strip():
        print_section('Adding -A')
        code, out, ms = run(['git', 'add', '-A'], repo_root, capture=True, env=env)
        print(out or '(staged)', f'({int(ms)} ms)')
        print_section('Commit')
        code, out, ms = run(['git', 'commit', '-m', message], repo_root, capture=True, env=env)
        print(out, f'({int(ms)} ms)')
    else:
        print_section('No changes to commit')
        print('(clean working tree)')

    # Diff summary vs origin/main
    print_section('Diff vs origin/main')
    code, out, _ = run(['git', 'diff', '--stat', 'origin/main...HEAD'], repo_root, capture=True, env=env)
    print(out or '(no diff)')

    # Push
    print_section('Push origin main')
    code, out, ms = run(['git', 'push', 'origin', 'main'], repo_root, capture=True, env=env)
    print(out or '(done)', f'({int(ms)} ms)')
    if code != 0:
        sys.exit(code)

    print_section('Status after')
    code, out, _ = run(['git', 'status', '-sb'], repo_root, capture=True, env=env)
    print(out, end='')

    print('\nDone.')


if __name__ == '__main__':
    main()
