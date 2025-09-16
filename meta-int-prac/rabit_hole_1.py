from typing import List

def getMaxVisitableWebpages(N: int, L: List[int]) -> int:
    state = [0] * (N+1) # 0=unvisited 1=visiting 2=done
    dp = [0] * (N+1)
    ans = 0

    for start in range(1, N + 1):
        print(start, ' ', L[start-1]) 

        stack = []  
        u = start 

        while True: 
            if state[u] == 0:
                state[u] = 1
                stack.append(u)
                u = L[u-1]
                continue 
            
            elif state[u] == 1:
                # cycle 
                cycle = []
                while True:
                    v = stack.pop()
                    cycle.append(v)
                    if u == v:
                        break 
                cycle_len = len(cycle)
                for v in cycle:
                    dp[v] = cycle_len 
                    state[v] = 2
                
                # back propagate 
                while stack:
                    v = stack.pop()
                    dp[v] = 1 + dp[L[v-1]]
                    state[v] = 2
                
                break 

            elif state[u] == 2:
                while stack:
                    v = stack.pop()
                    dp[v] = 1 + dp[L[v-1]]
                    state[v] = 2

                break  
            
        ans = max(ans, dp[start])

    return ans 

print('\n----\n')
print(getMaxVisitableWebpages(6, [2, 3, 4, 2, 6, 5]))
print('\n----\n')

b = 1

# eof 
