import sys
import os
import json
from wcmatch import glob
from git import Repo
from github import Github

from grammar import check_grammar


def parse_mode():
    _mode = 'ACTION'
    try:
        os.environ['GITHUB_ACTIONS']
    except KeyError:
        _mode = 'LOCAL'
    return _mode


def get_first_commit(_repo: Repo):
    for commit in _repo.iter_commits(reverse=True):
        return commit


def get_parent_latest_commit(_repo: Repo, _after):
    after_commit = _repo.commit(_after)
    if after_commit.parents:
        before_commit = after_commit.parents[0]
    else:
        before_commit = get_first_commit(_repo)
    return before_commit


def check_sha_zero(_sha: str):
    if _sha.isdigit() and int(_sha) == 0:
        return True
    return False


def filter_path_prefix(_paths):
    result = []
    for p in _paths:
        if str(p).startswith('./'):
            p = p[2:]
        result.append(p)
    return result


def get_branch_files(_repo, branch_name):
    _repo.git.checkout(branch_name)
    _repo.git.execute(['git', 'fetch', '--unshallow'])
    print(f'checked out branch: {_repo.active_branch}')

    with open(github_event_path, 'r') as f:
        data = dict(json.load(f))

    before = data.get('before', '0')
    after = data.get('after')

    # Check before SHA if zero
    if check_sha_zero(before):
        before = get_parent_latest_commit(repo, after).hexsha

    print(f'before commit SHA: {before}')
    print(f'after commit SHA: {after}')

    before_commit = _repo.commit(before)
    after_commit = _repo.commit(after)

    changed_files = set([item.b_path for item in before_commit.diff(after_commit)])

    return changed_files


def get_pr_files(_g, _github_repository, _pr_number):
    pr_files = _g.get_repo(_github_repository).get_pull(_pr_number).get_files()
    result = set()
    for file in pr_files:
        if file.status != 'removed':
            result.add(file.filename)
    return result


if __name__ == '__main__':
    mode = parse_mode()
    repo = None
    files = None

    # On GitHub Action
    if mode == 'ACTION':
        token = os.environ['INPUT_TOKEN']
        path = os.environ.get('INPUT_PATH', '.')
        check = os.environ.get('INPUT_CHECK', 'updated')
        github_ref = os.environ.get('GITHUB_REF')
        github_event_path = os.environ['GITHUB_EVENT_PATH']
        github_repository = os.environ['GITHUB_REPOSITORY']

        # Setup git repository instance
        repo = Repo()

        # Config Git Security
        repo.git.execute(["git", "config", "--global", "--add", "safe.directory", "*"])

        # Apply 'path'
        path_files = glob.glob(path + '/**/*.{md,MD}', flags=glob.GLOBSTAR | glob.BRACE)
        path_files = filter_path_prefix(path_files)
        files = set(path_files)

        # Apply 'check'
        if check == 'all':
            pass
        elif check == 'updated':
            check_files = None

            # case: branch
            if github_ref.startswith('refs/heads/'):
                branch_name = github_ref[11:]
                check_files = get_branch_files(repo, branch_name)
            # case: PR
            elif github_ref.startswith('refs/pull/'):
                pr_number = github_ref[10:len(github_ref) - 6]
                g = Github(token)
                check_files = get_pr_files(g, github_repository, pr_number)
            # case: tag
            elif github_ref.startswith('refs/tags/'):
                pass  # TODO

            if check_files:
                files = files & check_files
    # On Local
    else:
        repo = Repo()
        files = set(sys.argv[1:])

    # Run Grammar Check
    if len(files) == 0:
        print("맞춤법 검사를 진행할 파일이 없습니다.")
        exit(0)

    print("다음 파일들에 대해 맞춤법 검사를 진행합니다.")
    print(files)
    print("=" * 50)

    check_grammar(files)
