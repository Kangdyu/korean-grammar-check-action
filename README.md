# Korean Grammar Check Action

마크다운 파일에서 한국어 맞춤법이 잘못된 곳을 찾아 알려주는 Github Action

## 사용 예시

```yml
name: Check Korean Grammar in Markdown Files

on: push

jobs:
  Check-Korean-Grammar:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Grammar Check
        uses: Kangdyu/korean-grammar-check-action@v1
        with:
          path: "blog/tech"
          check: "updated"
```

### 옵션 목록

| Input   | Description                                                    | Default Value  |
|---------|----------------------------------------------------------------|----------------|
| `path`  | 맞춤법 검사를 실행할 최상위 경로입니다. 하위 경로까지 모두 탐색합니다.              | `.` (root directory)          |
| `check` | `all`: `path` 하위의 모든 md 파일을 검사합니다.<br>`updated`: `path` 하위의 수정된 md 파일만 검사합니다. | `updated`      |
| `token` | GitHub API를 사용하기 위한 권한이 있는 토큰입니다.                              | `GITHUB_TOKEN` |

## 개발 환경 세팅

```bash
pip install -r requirements.txt
```
