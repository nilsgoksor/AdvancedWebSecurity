def findValueOfX(cardNumber, indexOfX):
    """Find value of X"""
    # IF X IS THE CHECKSUM
    if(indexOfX == 15):
        sum = 0
        # FOR EACH DIGIT IN THE CARDNUMBER
        for i in range(14,-1,-1):
            # EVERY OTHER NUMBER IS MULTIPLIED WITH 1 OR 2, AND ADDED TO SUM
            if(i%2==0):
                nbr = int(cardNumber[i])*2
                if(nbr > 9):
                    sum += 1 + (nbr-10)
                else:
                    sum +=nbr
            else:
                sum +=int(cardNumber[i])
        # FINDS THE VALUE OF X BY CHECKING WHICH NUMBER THAT GIVES A SUM % 10 = 0
        for y in range(0,10):
            if((sum + y) % 10 == 0):  
                return str(y)
    
    # X IS A CARDNUMBER
    else:
        sum = 0
        # FOR EACH DIGIT IN THE CARDNUMBER
        for i in range(15,-1,-1):
            if(i != indexOfX):
                # EVERY OTHER NUMBER IS MULTIPLIED WITH 1 OR 2, AND ADDED TO SUM
                if(i%2==0):
                    nbr = int(cardNumber[i])*2
                    if(nbr > 9):
                        sum += 1 + (nbr-10)
                    else:
                        sum +=nbr
                else:
                    sum +=int(cardNumber[i])
        
        if(indexOfX%2==0):
            multiplier=2
        else:
            multiplier=1
        
        # FINDS THE VALUE OF X BY CHECKING WHICH NUMBER THAT GIVES A SUM % 10 = 0
        for i in range(0,10):
            y = i * multiplier
            if(y>9):
                y = 1 + (y-10)
            if((sum + y) % 10 == 0):  
                return str(i)
               
# Converts cardlist.txt cardnumbers to a list
with open("cardlist.txt") as f:
    allCardNumbers = f.read().splitlines()
answer = ""

# For each unknown cardnumber, find X wiht lynh algorithm
for cardNumber in allCardNumbers:
    indexOfX = cardNumber.find('X')
    valueOfX = findValueOfX(cardNumber, indexOfX)
    answer = answer + str(valueOfX)

print('Answer:', answer)
