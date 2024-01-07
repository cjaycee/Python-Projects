def merge(L1,L2):
    len1 = len(L1)
    len2 = len(L2)
    result = []
    i1 = 0
    i2 = 0
    while i1<len1 and i2<len2:
        if L1[i1]<L2[i2]:
            result.append(L1[i1])
            i1+=1
        else:
            result.append(L2[i2])   
            i2+=1
    if i1<len1:
        for i in range(i1,len1):
            result.append(L1[i])
    if i2<len2:
        for i in range(i2,len2):
            result.append(L2[i])
    return result

def mergesort(L):
    if len(L)<=1:
        return L
    else:
        half = len(L)//2
        L1 = mergesort(L[:half])
        L2 = mergesort(L[half:])
        return merge(L1,L2)

import random
list = random.sample(range(1, 1000000),100000)
print(mergesort(list))


        
