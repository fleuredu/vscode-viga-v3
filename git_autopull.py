#!/usr/bin/env python3
"""
Simple Git auto-pull script: pulls latest changes from remote.
Place in your repo and run manually (or schedule with Task Scheduler) to auto-pull changes.

Usage:
    python git_autopull.py --branch main --remote origin

Security: This script uses the local git configuration for authentication (SSH key or credential helper).
Do NOT embed plaintext credentials. If pull requires credentials, configure a credential helper or SSH key.
"""

import argparse
import logging
import os
import subprocess
import sys
import time

LOG_FILE = "git_autopull.log"

logger = logging.getLogger("git_autopull")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("[AUTOPULL] %(message)s"))
logger.addHandler(ch)

def run_cmd(cmd, cwd=None, check=False):
    logger.debug("Running: %s", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    logger.debug("Exit %s, stdout=%s, stderr=%s", proc.returncode, proc.stdout.strip(), proc.stderr.strip())
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
        logger.info("Pulling from %s/%s (attempt %d)", remote, branch, attempt)
        proc = run_cmd(["git", "pull", remote, branch], cwd=path)
        if proc.returncode == 0:
            logger.info("Pull successful.")
            return
        logger.warning("Pull failed (exit %s). stderr=%s", proc.returncode, proc.stderr.strip())
        if attempt >= max_retries:
            logger.error("Pull failed after %d attempts.", attempt)
            raise subprocess.CalledProcessError(proc.returncode, ["git", "pull", remote, branch], output=proc.stdout, stderr=proc.stderr)
        time.sleep(retry_delay)

def main():
    parser = argparse.ArgumentParser(description="Auto-pull git repo: pull latest changes from remote")
    parser.add_argument("--path", "-p", default='.', help="Repo path (default: current dir)")
    parser.add_argument("--remote", "-r", default="origin", help="Remote name (default: origin)")
    parser.add_argument("--branch", "-b", default=None, help="Branch to pull (default: current branch)")
    parser.add_argument("--retry", type=int, default=3, help="Pull retry count")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.path)
    logger.info("Repo path: %s", repo_path)
    logger.debug("Environment: %s", dict(os.environ))

    if not is_git_repo(repo_path):
        logger.error("Not a git repository: %s", repo_path)
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
        logger.exception("Command failed: %s", e)
        print(f"[AUTOPULL] ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unhandled exception")
        print(f"[AUTOPULL] ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
