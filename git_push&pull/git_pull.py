#!/usr/bin/env python3
"""
Simple Git auto-pull script: pulls latest changes from remote.
Place in your repo and run manually (or schedule with Task Scheduler) to auto-pull changes.
Usage:
    python git_pull.py --branch main --remote origin
"""

import argparse
import os
import subprocess
import sys
import time

def run_cmd(cmd, cwd=None, check=False):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)
    return proc

def is_git_repo(path: str) -> bool:
    p = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=path)
    return p.returncode == 0 and p.stdout.strip() == "true"

def git_pull(path: str, remote: str, branch: str, max_retries: int = 3, retry_delay: int = 3) -> None:
    attempt = 0
    while True:
        attempt += 1
        print(f"[AUTOPULL] Fetching from {remote} (attempt {attempt})")
        proc_fetch = run_cmd(["git", "fetch", "--prune", remote], cwd=path)
        if proc_fetch.returncode != 0:
            print(f"[AUTOPULL] Fetch failed (exit {proc_fetch.returncode}). stderr={proc_fetch.stderr.strip()}")
            if attempt >= max_retries:
                print(f"[AUTOPULL] Fetch failed after {attempt} attempts.")
                raise subprocess.CalledProcessError(proc_fetch.returncode, ["git", "fetch", "--prune", remote], output=proc_fetch.stdout, stderr=proc_fetch.stderr)
            time.sleep(retry_delay)
            continue
        print(f"[AUTOPULL] Resetting local branch to {remote}/{branch}")
        proc_reset = run_cmd(["git", "reset", "--hard", f"{remote}/{branch}"], cwd=path)
        if proc_reset.returncode == 0:
            print("[AUTOPULL] Reset successful. Local repo is now identical to remote.")
            return
        print(f"[AUTOPULL] Reset failed (exit {proc_reset.returncode}). stderr={proc_reset.stderr.strip()}")
        if attempt >= max_retries:
            print(f"[AUTOPULL] Reset failed after {attempt} attempts.")
            raise subprocess.CalledProcessError(proc_reset.returncode, ["git", "reset", "--hard", f"{remote}/{branch}"], output=proc_reset.stdout, stderr=proc_reset.stderr)
        time.sleep(retry_delay)

def main():
    parser = argparse.ArgumentParser(description="Auto-pull git repo: pull latest changes from remote")
    parser.add_argument("--path", "-p", default='.', help="Repo path (default: current dir)")
    parser.add_argument("--remote", "-r", default="origin", help="Remote name (default: origin)")
    parser.add_argument("--branch", "-b", default=None, help="Branch to pull (default: current branch)")
    parser.add_argument("--retry", type=int, default=3, help="Pull retry count")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.path)
    print(f"[AUTOPULL] Repo path: {repo_path}")

    if not is_git_repo(repo_path):
        print(f"[AUTOPULL] Not a git repository: {repo_path}")
        sys.exit(2)

    # determine branch if not provided
    if not args.branch:
        p = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path)
        branch = p.stdout.strip() if p.returncode == 0 else "main"
    else:
        branch = args.branch

    try:
        git_pull(repo_path, args.remote, branch, max_retries=args.retry)
        print("[AUTOPULL] Pull complete.")
    except subprocess.CalledProcessError as e:
        print(f"[AUTOPULL] ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[AUTOPULL] ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
