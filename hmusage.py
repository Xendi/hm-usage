#HM usage stats

import numpy as np

a = np.asarray(
 [[[ 44,  38,  50,  72,  51,   2,   2],
 [ 42,  56,  41,  23,  19,  53,  45],
 [ 33,  59,  19,  63,  38,  40,  18],
 [ 50,  58,  11,  25,  23,  63,  27]]


,
[[ 22,  45,  29,  23,  20,  43,  17],
 [ 62,  20,  19,  53,  25,  31,  26],
 [ 34,  46,   8,  29,   3,  25,   0],
 [ 27,  31,  10,  34,  18,  14,   5]]
,
[[ 42,  59,   0,  22,   9,   1,  18],
 [  0,  36,   0,  11,   9,  11,  19],
 [ 21,  36,  12,  50,   4,  41,   3],
 [ 25,  37,  19,  36,   2,  29,  14]]
,
[[  4,  39,  23,  34,  13,  12,  23],
 [  2,  45,   0,  33,   1,  58,  29],
 [ 31,  69,  29,  67,  27,   2,   4],
 [ 43,  63,  23,  42,  28,  18,  19]]])


# print a[:,:,0]

meandailyusage = []
for i in range(7):
  meandailyusage.append(np.mean(a[:,:,i]))

   
meanmonthlyusage = []
for i in range(4):
  meanmonthlyusage.append(np.mean(a[i,:,:]))

print "mean daily usage [M T W T F S S]"
print meandailyusage

print "mean monthly usage [J J A S]"
print meanmonthlyusage
