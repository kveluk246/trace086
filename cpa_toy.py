import random


def oracle(x):
	S = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]	
	secret_key = 4
	return HW(S[x ^ secret_key])

def HW(a):
	h = 0
	while(a != 0):
		if (a & 1): h = h + 1
		a = a >> 1
	return h

def get_guessed(x, k):
	S = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]	
	return S[x ^ k]



def correlate(trace):
	corr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for t in trace:
		oracle_hw = t[0]
		guess_hw = t[1]
		
	
		for i in range(16):
			corr[i] = corr[i] + oracle_hw * guess_hw[i]

	ind = corr.index(max(corr))
	print(ind, corr)
	


def cpa():
	trace = []
	for i in range(10):
		hw = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		rand_x = random.randint(0, 15)
		hw1 = oracle(rand_x)
		for k in range(16):
			hw[k] = HW(get_guessed(rand_x, k))	
		trace.append([hw1, hw])

	correlate(trace)


cpa()




