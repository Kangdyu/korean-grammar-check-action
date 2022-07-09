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
```

### input 옵션 목록

| Input   | Description | Default Value |
| ------- | ----------- | ------------- |
| `check` | `all`: 레포지토리의 모든 md파일을 검사합니다.<br>`updated`: 수정된 md파일만 검사합니다. | `updated` |

## 개발 환경 세팅

```bash
pip install -r requirements.txt
```
