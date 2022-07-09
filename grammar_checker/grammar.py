from hanspell import spell_checker
from hanspell.constants import CheckResult

from rich.console import Console
from rich.theme import Theme
console = Console(theme=Theme(inherit=False), force_terminal=True)

def check_grammar(paths):
    for path in paths:
        console.print(f"[bold orange1]{path} 파일 맞춤법 검사[/]\n")
        print_fixed_grammar(path)
        print("=" * 50)


def print_fixed_grammar(path):
    f = open(path, "r")

    contents = []
    while True:
        line = f.readline()
        if not line: break

        contents.append(line.strip())

    results = spell_checker.check(contents)

    error_count = 0
    for idx, result in enumerate(results):
        if result.errors == 0:
            continue

        error_count += result.errors

        corrected_line = ""
        for key, value in result.words.items():
            corrected_word = key

            if value == CheckResult.AMBIGUOUS:
                corrected_word = f"[magenta]{corrected_word}[/] "
            elif value == CheckResult.WRONG_SPELLING:
                corrected_word = f"[red]{corrected_word}[/] "
            elif value == CheckResult.WRONG_SPACING:
                corrected_word = f"[green]{corrected_word}[/] "
            else:
                corrected_word = f"{corrected_word} "
            corrected_line += corrected_word
            
        console.print(f"[bold red]{idx + 1}번째 줄에서 맞춤법 오류가 발생했습니다.[/]")
        console.print(f"[bold]원문[/]: {result.original}")
        console.print(f"[bold]교정[/]: {corrected_line}\n")

    console.print(f"맞춤법 오류: {error_count}개")

    f.close()
