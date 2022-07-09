import sys

from grammar import check_grammar

files = sys.argv[1:]

print("다음 파일들에 대해 맞춤법 검사를 진행합니다.")
print(files)
print("=" * 50)

check_grammar(files)