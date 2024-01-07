import random
answer = random.randint(1,100)
user_1 = int(input("What is your guess,player 1?"))
user_2 = int(input("What is your guess, player 2?"))
import math
diff1 = int(math.fabs(user_1 - answer))
diff2 = int(math.fabs(user_2 - answer))
if diff1<diff2:
    print("player 1 is the winner!")
elif diff2<diff1:
    print("player 2 is the winner!")   
else:
    print("It's a tie!") 