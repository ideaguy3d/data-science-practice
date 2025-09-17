from typing import List

def getMaxVisitableWebpages(N: int, L: List[int]) -> int:  
    ans = 0 
    state = [0] * (N+1)
    dp = [0] * (N+1)

    for start in range(1, N+1):
        if state[start] != 0:
            continue 

        u = start 
        stack = []

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
                
                # back prop
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

# --- Sample Tests ---
print('\n----\n')
print(getMaxVisitableWebpages(4, [4, 1, 2, 1]))    # 4
print(getMaxVisitableWebpages(5, [4, 3, 5, 1, 2])) # 3
print(getMaxVisitableWebpages(5, [2, 4, 2, 2, 3])) # 4
print(getMaxVisitableWebpages(6, [2, 3, 4, 2, 6, 5]))
print('\n----\n')

b = 1

# eof 
