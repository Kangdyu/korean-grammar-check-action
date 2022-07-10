from hanspell.constants import CheckResult

STYLES = {
    "error": "[bold red]",
    "warning": "[bold orange1]",
    CheckResult.PASSED: "[default]",
    CheckResult.WRONG_SPACING: "[green]",
    CheckResult.WRONG_SPELLING: "[red]",
    CheckResult.AMBIGUOUS: "[magenta]",
    CheckResult.STATISTICAL_CORRECTION: "[blue]"
}

RESULT_TYPE_STRING = {
    "error": "오류",
    "warning": "경고"
}

CAUSES = {
    CheckResult.WRONG_SPACING: "띄어쓰기",
    CheckResult.WRONG_SPELLING: "맞춤법",
    CheckResult.AMBIGUOUS: "표준어 의심",
    CheckResult.STATISTICAL_CORRECTION: "통계적 교정"
}
