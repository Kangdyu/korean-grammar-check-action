# i-ppendix

## 소개

현재 성균관대학교의 아이캠퍼스를 이용하다보면 불편한 점이 많이 느껴진다. 아이캠퍼스의 기본화면인 대시보드 페이지에 수강중인 과목이 카드 형식으로 존재하기만 할 뿐, 그 이외에 별다른 정보를 제공하지 않기 때문이다. 오른쪽에 조그맣게 할 일이 나오기는 하지만, 마감일 순서가 아니라 등록된 순서로 정렬이 되어있을 뿐만 아니라 공지사항이나 참고영상이 혼재되어 있기 때문에 불편하기는 매한가지다. 따라서 우리는 다음과 같은 특징을 가진 새로운 웹 페이지를 개발하였다.

- 모든 과목의 아직 듣지 않은 수업과 과제를 마감일 순으로 정렬
- 마감일 기준 시간이 얼마나 남았는지 표시
- 정렬된 항목 클릭 시 해당 강의나 과제 페이지로 연결
- 온라인 수업 링크 등 매주 열람해야 하는 공지사항을 즐겨찾기에 등록
- 간단한 메모 기능

우리가 중요하다고 여기는 항목들을 빠르게 살펴보고, 원하는 페이지로 바로 이동할 수 있도록 안내하는 것이 전공책에 수록된 부록(appendix)과 유사하다고 생각하여 i-campus와 appendix의 합성어인 `i-ppendix`를 프로그램명으로 삼았다.

![ippendix](https://user-images.githubusercontent.com/43704761/169644217-d1c06335-f057-42ec-bd90-baebc20eb907.gif)

## 설치

1. 프로젝트 clone 후 패키지 dependency 설치 및 빌드 실행

```bash
npm install
npm run build
```

2. chrome://extensions 접속 및 개발자모드 실행

![image](https://user-images.githubusercontent.com/43704761/169644604-9cc4bc5c-c560-42a4-9555-624e77a078d3.png)

3. 압축해제된 확장프로그램을 로드합니다. 버튼 클릭

![image](https://user-images.githubusercontent.com/43704761/169644619-69d732ae-7001-4965-8ad1-aebc4e33690e.png)

4. `npm run build`로 생긴 build 폴더 선택 후 등록 확인

![image](https://user-images.githubusercontent.com/43704761/169644657-db22d45c-3458-4360-a725-25516db537f2.png)

5. 기존 아이캠퍼스 로그인한 후 대시보드 페이지가 열린 상태에서 i-ppendix 확장프로그램 아이콘 클릭하여 사용

## 개발

1. 코드 작성
2. `npm run build`
3. 대시보드 페이지 새로고침하여 확인
   - 확실하게 하기 위해서는 `chrome://extensions` 페이지에서 확장프로그램을 reload한 후 테스트

- **Code Overview**

```
Chrome Service Worker <----------------------------> Dashboard Page
   (background.js)          chrome message API         (React.js)
(under /src/chrome/*)    <---- sendMessage           (under /src/*)
(fetch data from API           sendResponse ---->   (rendering data)
     and refine)
```

- **Style Guideline**

  - 해당 프로젝트는 `prettier`를 사용하여 code formatting을 진행하고 있습니다. formatting 설정에 대해서는 `prettier.rc` 파일을 참고해주시고, push 전 formatting을 진행해주세요.
  - 변수명, 함수명에 대해서는 lowerCamelCase를 사용합니다.

## 기여

- 문제나 건의사항이 있을 시 이슈 탭에 이슈를 남겨주세요.
- 직접 구현한 기능에 대해서는 `dev` 브랜치에 Pull Request를 올려주세요.

## 사용 시 주의 사항

- 반드시 다른 세션에서 **기존 아이캠퍼스에 로그인한 후**에 확장 프로그램을 실행시켜야 한다.
- 만약 기존 아이캠퍼스에 로그인하였는데도 정상적으로 표시되지 안는다면 서버 문제일 수 있으니 잠시 기다렸다가 레포지토리를 재실행해본다.
- 기존 아이캠퍼스에서 강의 콘텐츠 탭에 올라오지 않고 과제 및 평가 탭에만 올라온 과제의 경우 가져오지 못한다.

## 라이센스

Licensed under the MIT license

## 개발

- 강대호
- 나호현
- 차동훈