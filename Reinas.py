from itertools import permutations
from time import time

def test():
    N=11
    cols = range(N)
    sol=0
    for combo in permutations(cols):                      
        if N==len(set(combo[i]+i for i in cols))==len(set(combo[i]-i for i in cols)):
            sol += 1
            print('Solution '+str(sol)+': '+str(combo)+'\n')  
            print("\n".join(' o ' * i + ' ♛ ' + ' o ' * (N-i-1) for i in combo) + "\n\n\n\n")

start_time = time()
test()
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)

