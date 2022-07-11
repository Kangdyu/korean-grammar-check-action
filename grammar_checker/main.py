import sys
import os
import json
from wcmatch import glob
from git import Repo

from grammar import check_grammar


def parse_mode():
    _mode = 'ACTION'
    try:
        os.environ['GITHUB_ACTIONS']
    except KeyError:
        _mode = 'LOCAL'
    return _mode


def get_first_commit(_repo: Repo):
    _sha = None
    for commit in _repo.iter_commits(reverse=True):
        _sha = commit.hexsha
        break
    return _sha


def get_branch_files(_repo, branch_name):
    _repo.git.checkout(branch_name)
    _repo.git.execute(['git', 'fetch', '--unshallow'])
    print(f'checked out branch: {_repo.active_branch}')

    with open(github_event_path, 'r') as f:
        data = dict(json.load(f))

    before = data.get('before', get_first_commit(_repo))
    after = data.get('after')
    print(f'before commit SHA: {before}')
    print(f'after commit SHA: {after}')
    before_commit = _repo.commit(before)
    after_commit = _repo.commit(after)
    changed_files = set([item.b_path for item in before_commit.diff(after_commit)])

    return changed_files


def filter_path_prefix(_paths):
    result = []
    for p in _paths:
        if str(p).startswith('./'):
            p = p[2:]
        result.append(p)
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
                check_files = get_branch_files(repo, github_ref[11:])
            # case: PR
            elif github_ref.startswith('refs/pull/'):
                pass  # TODO
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
