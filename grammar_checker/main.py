import sys

from grammar import check_grammar

files = sys.argv[1:]

if len(files) == 0:
    print("맞춤법 검사를 진행할 파일이 없습니다.")
    exit(0)
    
print("다음 파일들에 대해 맞춤법 검사를 진행합니다.")
print(files)
print("=" * 50)

check_grammar(files)