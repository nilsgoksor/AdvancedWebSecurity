
def calculatePolynomSum(polynom, x):
    sum = 0
    for i in range(0,len(polynom)):
        if i == 0:
            sum += polynom[i]
        else: 
            sum += polynom[i]*(x**i)
    return sum

def calculateDeactivationCode(treshHoldScheme):
    deactivationCode = 0
    for i in range(len(treshHoldScheme)):
        product = 1
        for j in range(len(treshHoldScheme)):
            if i != j:
                input_i = treshHoldScheme[i][0]
                input_j = treshHoldScheme[j][0]
                product *= -input_j/(input_j-input_i)
        deactivationCode+=treshHoldScheme[i][1]*product
    return round(abs(deactivationCode))


# INPUT DATA
# our polynom
test1 = False
realTest = True
if test1:
    privatePolynom = [13, 8, 11, 1, 5]

    treshHoldScheme = []
    treshHoldScheme.append([1, 75+75+54+52+77+54+43 + calculatePolynomSum(privatePolynom,1)])

    # Add to treshHoldScheme.
    treshHoldScheme.append([2, 2782])
    treshHoldScheme.append([4, 30822])
    treshHoldScheme.append([5, 70960])
    treshHoldScheme.append([7, 256422])
if realTest:
    privatePolynom = [16,4,14]

    # Calculate own sum, given we are user 1
    treshHoldScheme = []
    treshHoldScheme.append([1, 45+57+30+39 + calculatePolynomSum(privatePolynom,1)])
 
    # Add to treshHoldScheme.
    treshHoldScheme.append([2, 471])
    treshHoldScheme.append([4, 1381])

deactivationCode =  calculateDeactivationCode(treshHoldScheme)
print("deactivationCode code:", deactivationCode)