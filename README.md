# Korean Grammar Check Action

텍스트 파일에서 한국어 맞춤법이 잘못된 곳을 찾아 알려주는 Github Action

## 사용법

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
          check: "updated"
```

### 옵션 목록

| Input   | Description                                                  | Default Value  |
|---------|--------------------------------------------------------------|----------------|
| `token` | private 레포지토리를 fetch하거나 PR을 생성하기 위한 권한이 있는 토큰입니다.            | `GITHUB_TOKEN` |
| `path`  | 검사를 실행할 파일들이 있는 폴더 경로입니다. 하위 경로의 모든 md 파일을 검사합니다.            | `'.'`          |
| `check` | `all`: 레포지토리의 모든 md 파일을 검사합니다.<br>`updated`: 수정된 md 파일만 검사합니다. | `updated`      |

## 개발 환경 세팅

```bash
pip install -r requirements.txt
```
