#!/usr/bin/env python3
"""
Simple Git auto-update script: stages changes, commits and pushes to remote.
Place in your repo and run manually (or schedule with Task Scheduler) to auto-push changes.

Usage:
    python git_autoupdate.py --message "Auto-update" --branch master

Security: This script uses the local git configuration for authentication (SSH key or credential helper).
Do NOT embed plaintext credentials. If push requires credentials, configure a credential helper or SSH key.
"""

import argparse
import logging
import os
import subprocess
import sys
import time

# --- logging: file (detailed) + console (summary) ---
LOG_FILE = "git_autoupdate.log"

logger = logging.getLogger("git_autoupdate")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("[AUTOGIT] %(message)s"))
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


def has_changes(path: str) -> bool:
    p = run_cmd(["git", "status", "--porcelain"], cwd=path)
    return bool(p.stdout.strip())


def git_add_all(path: str) -> None:
    run_cmd(["git", "add", "-A"], cwd=path, check=True)


def git_commit(path: str, message: str, author: str = None) -> bool:
    cmd = ["git", "commit", "-m", message]
    if author:
        # author format: "Name <email>"
        cmd = ["git", "-c", f"user.name={author.split('<')[0].strip()}", "commit", "-m", message]
    proc = run_cmd(cmd, cwd=path)
    # git commit returns 0 on success, 1 when there are no changes to commit (older git), or 128 on error
    if proc.returncode == 0:
        logger.info("Committed: %s", message)
        return True
    else:
        # inspect stdout/stderr for "nothing to commit"
        out = (proc.stdout + proc.stderr).lower()
        if "nothing to commit" in out or "no changes added to commit" in out:
            logger.info("No changes to commit.")
            return False
        else:
            logger.error("Commit failed: %s", proc.stderr.strip())
            raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)


def git_push(path: str, remote: str, branch: str, max_retries: int = 3, retry_delay: int = 3) -> None:
    attempt = 0
    while True:
        attempt += 1
        logger.info("Pushing to %s/%s (attempt %d)", remote, branch, attempt)
        proc = run_cmd(["git", "push", remote, branch], cwd=path)
        if proc.returncode == 0:
            logger.info("Push successful.")
            return
        logger.warning("Push failed (exit %s). stderr=%s", proc.returncode, proc.stderr.strip())
        if attempt >= max_retries:
            logger.error("Push failed after %d attempts.", attempt)
            raise subprocess.CalledProcessError(proc.returncode, ["git", "push", remote, branch], output=proc.stdout, stderr=proc.stderr)
        time.sleep(retry_delay)


def main():
    parser = argparse.ArgumentParser(description="Auto-update git repo: add, commit and push")
    parser.add_argument("--path", "-p", default='.', help="Repo path (default: current dir)")
    parser.add_argument("--message", "-m", default=None, help="Commit message (default: Auto-update: <timestamp>)")
    parser.add_argument("--remote", "-r", default="origin", help="Remote name (default: origin)")
    parser.add_argument("--branch", "-b", default=None, help="Branch to push (default: current branch)")
    parser.add_argument("--no-push", action="store_true", help="Only stage and commit, do not push")
    parser.add_argument("--author", default=None, help='Commit author in form "Name <email>"')
    parser.add_argument("--retry", type=int, default=3, help="Push retry count")
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
        branch = p.stdout.strip() if p.returncode == 0 else "master"
    else:
        branch = args.branch

    # default commit message
    if not args.message:
        args.message = f"Auto-update: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        # stage
        git_add_all(repo_path)

        # check changes
        if not has_changes(repo_path):
            logger.info("No changes detected. Nothing to do.")
            print("[AUTOGIT] No changes to commit.")
            return

        # commit
        committed = git_commit(repo_path, args.message, author=args.author)
        if not committed:
            print("[AUTOGIT] Nothing to commit after staging.")
            return

        # push unless disabled
        if not args.no_push:
            git_push(repo_path, args.remote, branch, max_retries=args.retry)
        else:
            logger.info("Skipping push (--no-push set)")

        print("[AUTOGIT] Update complete.")
    except subprocess.CalledProcessError as e:
        logger.exception("Command failed: %s", e)
        print(f"[AUTOGIT] ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unhandled exception")
        print(f"[AUTOGIT] ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
