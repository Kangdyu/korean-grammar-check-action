from constants import STYLES, CAUSES, RESULT_TYPE_STRING
from hanspell import spell_checker
from hanspell.constants import CheckResult

from rich.text import Text
from rich.console import Console
from rich.theme import Theme
console = Console(theme=Theme(inherit=False), force_terminal=True)


def check_grammar(paths):
    for path in paths:
        console.print(f"[bold white]{path} 파일 맞춤법 검사[/]\n")
        print_fixed_grammar(path)
        print("=" * 50)


def print_fixed_grammar(path):
    f = open(path, "r")

    contents = []
    while True:
        line = f.readline()
        if not line:
            break

        contents.append(line.strip())

    results = spell_checker.check(contents)

    correction_count = {"errors": 0, "warnings": 0}
    for idx, result in enumerate(results):
        if result.errors == 0:
            continue

        result_type = ""
        corrected_line = ""
        causes = []
        for key, value in result.words:
            corrected_word = key

            if value == CheckResult.WRONG_SPELLING or value == CheckResult.WRONG_SPACING:
                result_type = "error"
                correction_count["errors"] += 1
                causes.append(f"{STYLES['error']}{CAUSES[value]}[/]")
            elif value == CheckResult.AMBIGUOUS or value == CheckResult.STATISTICAL_CORRECTION:
                result_type = "warning" if result_type != "error" else result_type
                correction_count["warnings"] += 1
                causes.append(f"{STYLES['warning']}{CAUSES[value]}[/]")

            corrected_word = f"{STYLES[value]}{corrected_word} [/]"
            corrected_line += corrected_word

        console.print(
            f"{STYLES[result_type]}{idx + 1}번째 줄에서 맞춤법 {RESULT_TYPE_STRING[result_type]}가 발생했습니다. [/]", end="(")
        console.print(*list(dict.fromkeys(causes)), sep=",", end=")\n")
        console.print(f"> [bold]원문[/]: {result.original}")
        console.print(f"> [bold]교정[/]: {corrected_line}\n")

    console.print(f"[white]{path} 파일 맞춤법 검사 결과[/]")
    console.print(
        f"오류: {correction_count['errors']}개, 경고: {correction_count['warnings']}개")

    f.close()
