<!--
Created at: 2022-02-02T12:12:12
Author: 강대호 (Kangdyu)
-->

# SWR

<aside>
⚠️ 현재 2.0.0 버전이 베타로 나왔기에 조만간 기본적인 사용법이 약간 바뀔 수 있음 (현재 1.3.0)

</aside>

- 개요
    - 비동기 작업인 data fetching에 특화된 라이브러리. 외부에서 받아오는 dynamic한 데이터를 전역 상태로 손쉽게 사용할 수 있게 해준다.
    - 데이터를 prop drilling 없이 사용하고자 하는 컴포넌트에서 hook으로 정보를 바로 받아올 수 있음
        - `useSWR()`
    - caching, revalidating 지원
    - Theme이나 기타 전역 상태 관리를 위해서는 Context API 등 다른 전역 상태 관리 도구와 사용해야함
- 사용 예시
    - 기본 사용법
        
        ```tsx
        /* utils/fetcher.ts */
        
        // axios 사용 시
        export function fetcher(url: string) {
            return axios.get(url).then((res) => res.data);
        }
        
        // 기본 fetch 함수 사용 시
        export function fetcher(url: string) {
            return fetch(url).then((res) => res.json());
        }
        ```
        
        ```tsx
        /* pages/users.tsx */
        function UsersPage() {
            const { data, error } = useSWR<User[]>("/api/users", fetcher);
        
            if (error) return <div>error</div>;
            if (!data) return <div>loading</div>;
            return (data.map(...))
        }
        
        export default UsersPage;
        ```
        
    - Custom Hook
        
        ```tsx
        /* hooks/useUser.ts */
        export function useUser(id: number) {
            return useSWR<User>(`/api/users/${id}`, fetcher);
        }
        ```
        
        ```tsx
        function ComponentA({ id }: { id: number }) {
            const { data: user } = useUser(id);
            ...
        }
        
        function ComponentB() {
            const { data: user } = useUser(5);
            ...
        }
        ```
        
    - 옵션
        
        ```tsx
        useSWR(key, fetcher, **options**)
        ```
        
        - `revalidateIfStale` : stale data 존재 시 자동 갱신 (default: true)
        - `revalidateOnMount` : 컴포넌트가 마운트되었을 때 자동 갱신 여부
        - `revalidateOnFocus` : 페이지에 다시 포커스할 때 갱신 여부 (default: true)
        - `revalidateOnReconnect` : 네트워크 재연결 시 자동 갱신 (default: true)
        - `refreshInterval` :  설정한 시간마다 자동 갱신 (default: 0 - 비활성화)
        - 기타 많은 옵션:
        
        [API 옵션 - SWR](https://swr.vercel.app/ko/docs/options)
        
        - 자동 갱신 비활성화
            
            ```tsx
            import useSWRImmutable from 'swr/immutable'
            
            // useSWR과 동일한 인터페이스
            useSWRImmutable(key, fetcher, options);
            
            // 다음 option들을 가진 useSWR과 동일한 역할을 함
            useSWR(key, fetcher, {
                revalidateIfStale: false,
                revalidateOnFoucs: false,
                revalidateOnReconnect: false
            });
            ```
            
        - 전역 옵션 설정
            
            ```tsx
            <SWRConfig value={options}>
                <Component/>
            </SWRConfig>
            ```
            
            - 동일한 fetcher를 사용, 3초마다 데이터를 자동 갱신하는 전역 설정
            
            ```tsx
            import useSWR, { SWRConfig } from 'swr'
            
            function Dashboard () {
                const { data: events } = useSWR('/api/events')
                const { data: projects } = useSWR('/api/projects')
                const { data: user } = useSWR('/api/user', { refreshInterval: 0 }) // 오버라이드
            
                // ...
            }
            
            function App () {
                return (
                <SWRConfig 
                    value={{
                    refreshInterval: 3000,
                    fetcher: (resource, init) => fetch(resource, init).then(res => res.json())
                    }}
                >
                    <Dashboard />
                </SWRConfig>
                )
            }
            ```
            
    - 에러 처리
        - `fetcher` 에서 에러가 발생 시 `useSWR` hook의 error로 반환됨
        
        ```tsx
        const { data, **error** } = useSWR<User>('/api/user', fetcher);
        ```
        
        - error의 타입도 `useSWR` hook의 제네릭으로 넘겨줄 수 있음
            - default: `any`
            - 상세하게 에러 처리를 해야할 때 필요
        
        ```tsx
        // typeof error: AxiosError
        const { data, error } = useSWR<User, AxiosError>(...);
        ```
        
        - fetcher가 더 많은 정보를 반환하도록 커스터마이징 할 수도 있음
            - 아래 예시는 참고용으로만 볼 것
        
        ```tsx
        export interface CustomError extends Error {
            statusCode?: number;
        }
        
        export async function fetcher(url: string) {
            try {
            const res = await axios.get(url);
            return res.data;
            } catch (e) {
            const error: CustomError = new Error();
        
            if (axios.isAxiosError(e)) {
                error.message = e.message;
                if (e.response) {
                error.statusCode = e.response.status;
                }
            } else {
                error.message = "Unknown Error";
            }
        
            throw error;
            }
        }
        ```
        
    - 공식 문서
    
    [데이터 가져오기를 위한 React Hooks - SWR](https://swr.vercel.app/ko)
