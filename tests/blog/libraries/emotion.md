<!--
Created at: 2022-02-02T12:12:15
Author: 강대호 (Kangdyu)
-->

# emotion (css-in-js 라이브러리)
  - 개요
    - 클래스명 중복 걱정할 필요 없음
    - 자동으로 critical CSS를 뽑아줌
      - critical CSS: 맨 처음 보게 되는 화면의 CSS
    - auto vendor prefix
      - -webkit, -moz 등등 vendor prefix를 자동으로 붙여줌
  - 사용 예시
    - 프로젝트 세팅
      - 패키지 설치
        ```bash
        npm i @emotion/react @emotion/styled
        ```
      - `tsconfig.json`
        - `compilerOptions` 에 `"jsxImportSource": "@emotion/react"` 추가
        ```tsx
        {
        	"compilerOptions": {
        		"jsxImportSource": "@emotion/react",
        		... other options
        	},
        	...
        }
        ```
        - TypeScript에서 element들에 css prop의 type을 inject하기 위함
      - `next.config.js`
        ```tsx
        const nextConfig = {
          reactStrictMode: true,
          // 아래 부분 추가
          compiler: {
            emotion: true,
          },
        };
        ```
    - 추가된 스타일 문법
      - nested selector
        - 일반적인 CSS
        ```css
        .container {
          width: 100%;
        }
        .container p {
          color: dodgerblue;
        }
        .container p span {
          font-weight: bold;
        }
        .container p blockquote {
          margin-left: 16px;
        }
        ```
        - nested selector
        ```css
        const containerStyle = css`
        	width: 100%;
        	p {
        		color: dodgerblue;
        		span {
        			font-weight: bold;
        		}
        		blockquote {
        			margin-left: 16px;
        		}
        	}
        `;
        ```
      - `&`
        - 일반적인 CSS
        ```css
        .button {
          background-color: red;
        }
        .button:hover {
          background-color: blue;
        }
        .button:not(:last-child) {
          margin-right: 16px;
        }
        ```
        - `&` 사용
        ```css
        const buttonStyle = css`
        	background-color: red;
        	&:hover {
        		background-color: blue;
        	}
        	&:not(:last-child) {
        		margin-right: 16px;
        	}
        `;
        ```
      - 또 뭐 있나
    - tagged template literal 방식, object 방식
      - tagged template literal
        - **css 문법과 동일하게 사용 가능**
        - 자동 완성 등의 기능을 사용할 수 없음
          - `vscode-styled-components` extension을 설치하여 해소 가능
      ```tsx
      const Text = styled.p`
        font-size: 24px;
      `;

      const textStyle = css`
        font-size: 24px;
      `;
      ```
      - object
        - **TypeScript**를 통해 자동 완성 사용 가능 및 type safe한 작업 가능
      ```tsx
      const Text = styled.p({
        fontSize: "24px",
      });

      const textStyle = css({
        fontSize: "24px",
      });
      ```
      - 개인 취향껏 사용하면 될듯?
    - styled component (@emotion/styled)
      - 기본적인 사용법
        ```jsx
        // tagged template literal 사용
        const Title = styled.h1`
          font-weight: bold;
          font-size: 32px;
          color: dodgerblue;
        `;

        function SomeComponent() {
          return <Title>이것은 스타일이 들어간 제목입니다</Title>;
        }
        ```
      - prop 사용
        ```tsx
        const Text = styled.span<{ strong?: boolean }>`
        	color: #444;
        	font-weight: ${(props) => (props.strong ? "bold" : "normal")};
          font-size: ${({ strong }) => (strong ? "24px" : "18px")};
        `

        // 위처럼 동일한 prop을 사용하는 css property가 여러개일 시 다음과 같이 사용할 수도 있음
        const Text = styled.p<{ strong?: boolean }>`
          ${({ strong }) => css`
        		color: #444;
            font-weight: ${strong ? "bold" : "normal"};
            font-size: ${strong ? "24px" : "18px"};
          `}
        `;

        // 객체 문법. 편한대로 사용하면 될듯
        const Text = styled.p<{ strong?: boolean }>(
        	{
        		// 여기에는 props를 사용 안하는 스타일들
        		color: "#444"
        	},
        	(({ strong }) => ({
        		fontWeight: strong ? "bold" : "normal",
        		fontSize: strong ? "24px" : "18px"
        	})
        );

        // Text 사용
        function SomeComponent() {
        	return (
        		<div>
        			<Text>Normal Text</Text>
        			<Text strong>Strong Text</Text>
        		</div>
        	);
        }
        ```
      - 컴포넌트 스타일링
        - emotion component
        ```tsx
        const Button = styled.button`
          border: none;
          outline: none;
          cursor: pointer;
          overflow: hidden;
          padding: 8px 16px;
        `;

        // 위의 스타일들 + 추가할 스타일 (상속 느낌)
        // override도 가능
        const ExtendedButton = styled(Button)`
          border: 1px solid black;
          border-radius: 8px;
          background-color: dodgerblue;
        `;
        ```
        - React component
        ```tsx
        interface Props extends HTMLAttributes<HTMLDivElement> {}

        function Container({ children, ...props }: Props) {
          return (
            <div {...props}>
              <nav>Nav</nav>
              {children}
            </div>
          );
        }
        ```
        ```tsx
        const AboutContainer = styled(Container)`
          max-width: 400px;
          width: 100%;
          margin: 0 auto;
        `;

        function AboutPage() {
          return <AboutContainer>about</AboutContainer>;
        }
        ```
          <aside>
          ⚠️ 스타일링 할 대상이 `className` 을 prop으로 받아야만 가능함
          
          </aside>
          
          ```tsx
          interface Props {
          	children: ReactNode;
          }
          
          function Container({ children }: Props) {
          	**/* 이 경우 최상위인 div가 className을 받고 있지 않기 때문에 위의 예시처럼 사용 불가
          	 * Props interface에 className: string 을 더해주어 div의 prop으로 넘겨주거나,
          	 * className을 가지고 있는 HTMLAttributes<HTMLDivElement> 타입을 extend하여 넘겨주면 된다
          	 */**
          	return (
          		<div>
          			<nav>Nav</nav>
          			{children}
          		</div>
          	);
          }
          ```

      - 다른 emotion component를 selector로 사용하기
        - `@emotion/babel-plugin` 을 사용해야하는데 next.js가 최근 babel 대신 swc를 사용하도록 바뀌면서 swc의 플러그인을 찾아야하는듯
        - 좀 더 알아보고 내용 추가 예정
        ```tsx
        const Paragraph = styled.p`
          font-size: 18px;
        `;

        const Article = styled.article`
          ${Paragraph} {
            font-size: 20px;
            margin-left: 16px;
          }
        `;
        ```
    - css prop (@emotion/react)
      - 기본적인 사용법
        ```jsx
        // 객체 사용
        <button css={{ width: "100%" }}>버튼</button>

        // @emotion/react의 css 함수 사용
        <button css={css`width: 100%`}>버튼</button>

        // 변수로도 저장 가능
        const flexCenterStyle = css`
        	display: flex;
        	justify-content: center;
        	align-itmes: center;
        `;
        <div css={flexCenterStyle}>center</div>
        ```
    - composition
      ```tsx
      const buttonBaseStyle = css`
        border: none;
        outline: none;
        cursor: pointer;
      `;

      const primaryButtonStyle = css`
        ${buttonBaseStyle};
        background-color: dodgerblue;
      `;

      // styled 에도 사용 가능
      const PrimaryButton = styled.button`
        ${buttonBaseStyle};
        background-color: dodgerblue;
      `;
      ```
      ```tsx
      const baseStyle = css`
      	background-color: green;
      `;
      const dangerStyle = css`
      	background-color: red;
      	color: white;
      `;

      function Component() {
      	return (
      		<div>
      			{/* 배열의 뒤에 들어간 것이 앞의 것을 덮어 씌우므로, 결과가 다르다 */}
      			<p css={[dangerStyle, baseStyle]}>danger -> base</p>
      			<p css={[baseStyle, dangerStyle]}>base -> danger</p>
      		</div>
      	)
      }
      ```
    - Global Style
      - styles/globalStyles.ts
      ```tsx
      import { css } from "@emotion/react";

      export const globalStyles = css`
        html,
        body {
          padding: 0;
          margin: 0;
          font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
            Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
        }

        a {
          color: inherit;
          text-decoration: none;
        }

        * {
          box-sizing: border-box;
        }
      `;
      ```
      - \_app.tsx
      ```tsx
      import { Global } from "@emotion/react";
      import type { AppProps } from "next/app";
      import { globalStyles } from "styles/globalStyles";

      function MyApp({ Component, pageProps }: AppProps) {
        return (
          <>
            <Global styles={globalStyles} />
            <Component {...pageProps} />
          </>
        );
      }

      export default MyApp;
      ```
    - Theme
      - emotion.d.ts
      ```tsx
      import "@emotion/react";

      declare module "@emotion/react" {
        // 프로젝트 전역으로 사용할 테마 관련 아무거나 넣으면 됨
        export interface Theme {
          color: {
            primary: string;
            secondary: string;
            white: string;
          };
          padding: {
            container: string;
            button: string;
          };
        }
      }
      ```
      - theme.ts
      ```tsx
      import { Theme } from "@emotion/react";

      // emotion.d.ts 파일에서 정의한 테마 인터페이스대로 구현하면 됨
      export const theme: Theme = {
        color: {
          primary: "#1363DF",
          secondary: "#47B5FF",
          white: "#eee",
        },
        padding: {
          container: "0 16px",
          button: "12px 16px",
        },
      };
      ```
      - \_app.tsx
      ```tsx
      import { Global, ThemeProvider } from "@emotion/react";
      import type { AppProps } from "next/app";
      import { globalStyles } from "styles/globalStyles";
      import { theme } from "styles/theme";

      function MyApp({ Component, pageProps }: AppProps) {
        // ThemeProvider로 감싸주기
        return (
          <ThemeProvider theme={theme}>
            <Global styles={globalStyles} />
            <Component {...pageProps} />
          </ThemeProvider>
        );
      }

      export default MyApp;
      ```
      - 테마 사용
      ```tsx
      import styled from "@emotion/styled";

      const Button = styled.button`
        background-color: ${(props) => props.theme.color.secondary};
        color: ${({ theme }) => theme.color.white};
        padding: ${({ theme }) => theme.padding.button};
      `;

      function IndexPage() {
        return <Button>button</Button>;
      }

      export default IndexPage;
      ```