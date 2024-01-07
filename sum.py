def sum(n):
    if n == 1:
        return n
    return sum(n-1)+n
 

print(sum(100))

def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1)+fib(n-2)

print(fib(7))

