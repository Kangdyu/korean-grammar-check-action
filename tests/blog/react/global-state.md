<!--
Created at: 2022-02-02T12:12:15
Author: 강대호 (Kangdyu)
-->

# 리액트 전역 상태 관리
## Context API (built-in)
  - 개요
    - 리액트에서 제공하는 기본적인 전역 상태관리 API
    - re-rendering 최적화 이슈가 있음
      - Context로 관리하는 것이 객체인 경우, 객체의 property 중 하나만 바뀌더라도 객체가 새로 생성되기 때문에, 구독하고 있는 모든 컴포넌트가 해당 property와 관련이 없더라도 re-render 되어버림
      - 따라서 자주 변경되는 데이터를 관리해야하는 경우 적합하지 않음
  - 사용 예시
    - Counter 예시
      - CounterProvider.tsx
      ```tsx
      import { createContext, ReactNode, useContext, useState } from "react";

      interface CounterContextValue {
        count: number;
        plus: (amount: number) => void;
        minus: (amount: number) => void;
      }

      const CounterContext = createContext<CounterContextValue | null>(null);

      interface Props {
        children: ReactNode;
      }

      export function CounterProvider({ children }: Props) {
        const [count, setCount] = useState(0);

        return (
          <CounterContext.Provider
            value={{
              count,
              plus: (amount: number) => setCount(count + amount),
              minus: (amount: number) => setCount(count - amount),
            }}
          >
            {children}
          </CounterContext.Provider>
        );
      }

      // CounterContext를 보다 편하게 사용하기 위해 만든 커스텀 훅. 안 만들어도 됨
      export function useCounter() {
        const context = useContext(CounterContext);

        if (context == null) {
          throw new Error("Counter Context 안에서 사용해주세요");
        }

        return context;
      }
      ```
      - Counter.tsx - CounterContext를 구독하여 카운트를 표시하고 조정하는 컴포넌트
      ```tsx
      import { useCounter } from "components/CounterProvider";

      function Counter() {
        const { count, plus, minus } = useCounter();

        return (
          <div>
            <button onClick={() => minus(1)}>-1</button>
            <span>{count}</span>
            <button onClick={() => plus(1)}>+1</button>
          </div>
        );
      }

      export default Counter;
      ```
      - UserList.tsx - CounterContext를 구독하여 카운트에 따라 리스트 표시 개수를 조절
      ```tsx
      import useUsers from "hooks/useUsers";
      import { useCounter } from "components/CounterProvider";

      function UserList() {
        const { data: users } = useUsers(); // SWR hook
        const { count } = useCounter();

        return (
          <ul>
            {users?.data.slice(0, count).map((user) => (
              <li key={user.id}>{user.name}</li>
            ))}
          </ul>
        );
      }

      export default UserList;
      ```
      - index.tsx - Counter를 공유해야하는 컴포넌트를 Provider로 감싸줌
      ```tsx
      import Counter from "components/Counter";
      import { CounterProvider } from "components/CounterProvider";
      import UserList from "components/UserList";

      function IndexPage() {
        /* _app.tsx에 Provider로 감싸서 앱 전역으로 적용해 줄 수도,
         * 아래처럼 필요한 컴포넌트에만 감싸서 적용해 줄 수도 있음
         */
        return (
          <CounterProvider>
            <Counter />
            <UserList />
          </CounterProvider>
        );
      }

      export default IndexPage;
      ```

## 전역 상태 관리에 대한 고찰

- 주로 전역 상태로 관리되는 것
  - 외부(서버)에서 받아오는 데이터
  - 다크모드, 라이트모드 등의 theme
  - 다국어 처리 (i18n)
- 외부(서버)에서 받아오는 데이터
  - SWR, react-query 등의 라이브러리로 손쉽게 caching, revalidating하며 관리 가능
- Theme, i18n
  - Theme의 경우 emotion, styled-components 에서 제공하는 `<ThemeProvider>` 로 처리 가능
  - 리액트의 Context API로 관리 가능
- 상태 관리 라이브러리의 필요성
  - Context API의 경우, 위에서 적었듯이 복잡하고 동적인 데이터를 다루는 데에는 re-rendering 이슈로 인해 적합하지 않을 수 있음
  - 하지만 전역으로 관리하는 상태의 특징을 보면,
    - 상태가 변경될 시 application 전반적으로 re-rendering이 발생해야만 함
    - 자주 바뀌는 데이터가 아님
    ⇒ 따라서, Context API가 아닌 다른 라이브러리를 사용한다고 해서 크게 달라지는게 없음
  - 이 외에는 두 개 이상의 컴포넌트에서 상태를 공유해야하는 경우일 것 (ex. Dropdown)
    - 컴포넌트를 Context Provider로 묶어주어 해결 가능
    - 일반적으로 `상태 공유가 필요하다 = 한 쪽에서 상태가 변하면 그에 맞게 따라서 변해야 한다` 이므로 Context API의 re-rendering 이슈와 크게 관련이 없을 것이라 생각
    - 컴포넌트 설계에 대해 많은 시간을 들여 고민해보도록 하자 ~~(학생일 때 안하면 하기 힘듬)~~
  - 그럼에도 필요한 케이스가 충분히 있을 수 있다
    - 이 때 사용을 고려해보도록 하자
