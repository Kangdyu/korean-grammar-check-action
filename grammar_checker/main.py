import sys
import os

from wcmatch import glob
import json
from grammar import check_grammar
from git import Repo


def parse_mode():
    _mode = 'ACTION'
    try:
        os.environ['GITHUB_ACTIONS']
    except KeyError:
        _mode = 'LOCAL'
    return _mode


def get_branch_files(branch_name):
    repo.git.checkout(branch_name)
    repo.remotes.origin.pull()

    with open(github_event_path, 'r') as f:
        data = json.load(f)

    before_commit = repo.commit(data['before'])
    after_commit = repo.commit(data['after'])
    changed_files = [item.b_path for item in before_commit.diff(after_commit)]

    return changed_files


if __name__ == '__main__':
    mode = parse_mode()
    repo = Repo()
    files = None

    # Config Git Security
    repo.git.execute(["git", "config", "--global", "--add", "safe.directory", "*"])

    # On GitHub Action
    if mode == 'ACTION':
        path = os.environ.get('INPUT_PATH', '.')
        check = os.environ.get('INPUT_CHECK', 'updated')
        github_ref = os.environ.get('GITHUB_REF')
        github_event_path = os.environ['GITHUB_EVENT_PATH']

        # Apply 'path'
        path_files = glob.glob(path + '/**/*.{md,MD}', flags=glob.GLOBSTAR | glob.BRACE)
        files = set(path_files)

        # Apply 'check'
        if check == 'all':
            pass
        elif check == 'updated':
            check_files = None

            # case: branch
            if github_ref.startswith('refs/heads/'):
                check_files = get_branch_files(github_ref[11:])

            # case: PR
            elif github_ref.startswith('refs/pull/'):
                pass  # TODO
            # case: tag
            elif github_ref.startswith('refs/tags/'):
                pass  # TODO

            if check_files:
                files = check_files - files
    # On Local
    else:
        files = set(sys.argv[1:])

    # Run Grammar Check
    if len(files) == 0:
        print("맞춤법 검사를 진행할 파일이 없습니다.")
        exit(0)

    print("다음 파일들에 대해 맞춤법 검사를 진행합니다.")
    print(files)
    print("=" * 50)

    check_grammar(files)
