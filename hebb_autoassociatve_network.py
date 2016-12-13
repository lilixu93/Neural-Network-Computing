"""
Neural Network Computing Project
Lili Xu
"""
import numpy as np
# import pattern vectors form digit image file
f = open("/Users/lilixu/TenDigitPatterns.txt")
raw_d = []
for line in f:
    vector = []
    for ch in line:
        if ch == '#':
            vector.append(1)
        if ch == ' ':
            vector.append(-1)
    while len(vector) < 35:
        vector.append(-1)
    raw_d.append(vector)

# input vectors
s = np.matrix(raw_d)


# bipolar transfer function
def bipolar(x, theta=0):
    if x > theta:
        return 1
    elif x < theta:
        return -1
    else:
        return 0
bp = np.vectorize(bipolar)


# result output function, turn the trained vectors to digit image representation
def output(a):
    i = 0
    for _ in range(7):
        s = ''
        for j in range(i,i+5):
            p = ' ' if a[0, j] == -1 else '#'
            s += p
        print s
        i += 5


# get combinations of 1-10
def subsets(nums):
    result = []
    helper(result, [], nums, 0)
    return result


def helper(result, subset, nums, pos):
    if len(subset) >= 5: # by previous manual test, combination 1-5 is valid
        result.append(subset[:])
    for i in range(pos, len(nums)):
        helper(result, subset+[nums[i]], nums, i+1)

# Hebb Rule on all combinations
patterns, maxn = [], 0
for subset in subsets(range(10)):
    w = sum(np.dot(s[i].transpose(), s[i]) for i in subset)
    cd = []
    for i in range(10):
        if np.array_equal(bp(np.dot(s[i], w)), s[i]):
            cd.append(i)
    if len(cd) >= maxn:
        if subset == cd:
            patterns.append(cd)
            maxn = len(cd)
print patterns
'''
1.
We can store and recall maxinum 5 patterns.
Yes, the chosen pattern matters.
We can store these pattern combinations and recall them successfully
[[0, 1, 2, 3, 4], [0, 1, 2, 4, 6], [0, 1, 2, 4, 7], [0, 1, 3, 4, 7], [0, 1, 4, 5, 7],
 [0, 1, 4, 6, 7], [0, 1, 4, 7, 8], [0, 1, 4, 7, 9], [1, 2, 3, 4, 7], [1, 2, 4, 5, 7],
 [1, 2, 4, 6, 7], [1, 2, 4, 7, 8], [1, 2, 4, 7, 9], [1, 3, 4, 7, 8], [1, 3, 4, 7, 9],
 [1, 4, 5, 7, 8], [1, 4, 5, 7, 9], [1, 4, 6, 7, 8], [1, 4, 6, 7, 9]]

'''
# Test orthogonality of valid combinations
for pattern in patterns:
    print pattern
    for x in range(len(pattern)):
        for y in range(x+1,len(pattern)):
            i, j = pattern[x], pattern[y]
            if abs(np.dot(s[i], s[j].transpose())) <= 3:
                print i, j, np.dot(s[i], s[j].transpose())
'''
As we see from the results, if we define abs(dot product) is no larger than 3 is nearly orthogonal.
(0,1),(0,4),(0,7),(1,3),(1,5),(1,6),(1,9),(1,7),(4,7),(4,8),(4,9),(6,7),(7,8),(7,9) are nearly orthogonal.
As digit 1 and 7 are nearly orthogonal to many otehr digits, we can see 7 appears in almost all pattern combinations.
All the number in pattens are close to nearly orthogonal and such nearly non-orthogonal combination such as 0
'''


# noise generate function
def add_noise(vector, n=1, type='mistake'):
    noise = np.random.random_integers(0, 34, n)
    for i in noise:
        if type == 'mistake':
            vector[0,i] *= -1
        else:
            vector[0,i] = 0
    return vector

# test noise output, chose 0,1,2,3,4 as input pattern
sp_v = []
w = sum(np.dot(s[i].transpose(), s[i]) for i in range(5))
for n in range(1,15):
    count = 0
    for _ in range(2000):
        test = np.matrix(raw_d)
        for i in range(5):
            noise_v = add_noise(test[i], n, 'mistake') # 'mistake' will be replaced for generating missing noise
            out_v = bp(np.dot(noise_v, w))
            if np.array_equal(out_v, s[i]):
                # output(bp(np.dot(add_noise(test[i], n, 'a'), w))) for output purpose
                count += 1
            if np.array_equal(out_v, noise_v):
                sp_v.append(noise_v)  # find spurious pattern
    print str(n) + ' ' + str(count/10000.0) + '%;'
'''
2.
I calculate the ratio of classifying vector with noise successfully
Result for mistake noise
number of noise element, ratio of the correctly classified patterns (I choose few results here)
1, 0.8652%; 2, 0.814%; 3, 0.7308%; 5, 0.6258%; 10, 0.4616%; 20, 0.1794%; 34, 0.0632%;

Result for missing noise
1, 0.8983%; 2, 0.9128%; 3, 0.8397%; 5, 0.8139%; 10, 10 0.7483%; 20, 0.6112%; 34, 0.4581%;
'''

for x in sp_v:
    output(x)

'''
I record if a pattern which does not belong to the training set can be classified to itself
 while generating the noise.

Spurious Patterns:
  #
 ##
# ##
  #
  #
 ##
#####

 ###
#   #
    #
#   #
#   #
#   #
 ###

 ###
#   #
   #
  #

##
####

 ###
#   #

  #
  #

#####

# #
 ##
####
  #
  #
 ###
#####

 ###
###
#  #
  #
  #
 ##
#####

 ###
###
#
  #
  #
  #
#####
'''