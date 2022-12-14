import os
import subprocess
from random import randint
import argparse, sys
import array
import numpy as np
import aes as finj

POSITIONS = [[0, 13, 10, 7],[4, 1, 14, 11],[8, 5, 2, 15],[12, 9, 6, 3]]

def intersection(total_cand,candidates):
	print(total_cand)
	#print(len(total_cand), len(candidates))
	nlen = 0
	new_total =[]
	for i in total_cand:
	 	for j in candidates:
	 		if i == j:
	 			total_cand = j
	 			#new_total.append(j)
	 			break
	# print(total_cand)
	#print(new_total)
	return total_cand

def key10_candidate(ct_list_i,fct_list_i,cand_len,column,list_diff):
	#print(list_diff)
	good = [0] * 4
	faulty = [0] * 4
	candidates = []
	for i in range(0,4):
		good[i] = ct_list_i[POSITIONS[column][i]]
		faulty[i] = fct_list_i[POSITIONS[column][i]];
	#print(good,faulty)
	for i in range(0, len(list_diff)):
		for k0 in range(0,256):
			diff = finj.isbox[good[0] ^ k0] ^ finj.isbox[faulty[0] ^ k0]
			if diff != list_diff[i][0]: continue
			for k1 in range(0,256):
				diff = finj.isbox[good[1] ^ k1] ^ finj.isbox[faulty[1] ^ k1]
				if diff != list_diff[i][1]: continue
				for k2 in range(0,256):
					diff = finj.isbox[good[2] ^ k2] ^ finj.isbox[faulty[2] ^ k2]
					if diff != list_diff[i][2]: continue
					for k3 in range(0,256):
						diff = finj.isbox[good[3] ^ k3] ^ finj.isbox[faulty[3] ^ k3]
						if diff != list_diff[i][3]: continue
						print(k0,k1,k2,k3)
						tlist = []
						tlist.append(k0)
						tlist.append(k1)
						tlist.append(k2)
						tlist.append(k3)
						#print(tlist)
						candidates.append(tlist)
						#print(candidates)
						#tlist.clear()
	
	#print(len(candidates))
	print("Candidate Found",candidates)
	return(candidates)

def reverse_key(key10):
	subkeys = [0] * 176

	for i in range(160,176):
		subkeys[i] = key10[i - 160]

	for i in range(156,-1,-4):
		if i % 16 == 0 :
			subkeys[i] = subkeys[i + 16] ^ finj.sbox[subkeys[i + 13]] ^ finj.rcon[i>>4]
			subkeys[i + 1] = subkeys[i + 17] ^ finj.sbox[subkeys[i + 14]]
			subkeys[i + 2] = subkeys[i + 18] ^ finj.sbox[subkeys[i + 15]]
			subkeys[i + 3] = subkeys[i + 19] ^ finj.sbox[subkeys[i + 12]]
		else:
			subkeys[i] = subkeys[i + 16] ^ subkeys[i + 12]
			subkeys[i + 1] = subkeys[i + 17] ^ subkeys[i + 13]
			subkeys[i + 2] = subkeys[i + 18] ^ subkeys[i + 14]
			subkeys[i + 3] = subkeys[i + 19] ^ subkeys[i + 15]

	return subkeys

def exhaustive_search(pt, ct, total_cand, cand_len):
	print(bytes(ct).hex())
	found = 0
	key10 = [0] * 16

	for i in range(0, cand_len[0]):
		print("Validating: ", str(i + 1)+"/"+str(cand_len[0]))
		key10[0] = total_cand[0][i+0]
		key10[13] = total_cand[0][i+1]
		key10[10] = total_cand[0][i+2]
		key10[7] = total_cand[0][i+3]

		for j in range(0, cand_len[1]):
			key10[4] = total_cand[1][j+0]
			key10[1] = total_cand[1][j+1]
			key10[14] = total_cand[1][j+2]
			key10[11] = total_cand[1][j+3]

			for k in range(0, cand_len[2]):
				key10[8] = total_cand[2][k+0]
				key10[5] = total_cand[2][k+1]
				key10[2] = total_cand[2][k+2]
				key10[15] = total_cand[2][k+3]

				for l in range(0, cand_len[3]):
					key10[12] = total_cand[3][l+0]
					key10[9] = total_cand[3][l+1]
					key10[6] = total_cand[3][l+2]
					key10[3] = total_cand[3][l+3]

					subkeys = reverse_key(key10)
					print(key10)
					print(subkeys)
					ct1 = finj.encrypt_aes_subkeys(pt, subkeys)
					if (ct1.hex() == bytes(ct).hex()):
						print("Found the Key :", bytes(subkeys[0:16]).hex())
						return 1

	return 0


def newsearch(pt, ct, total_cand, cand_len):
	found = 0
	key10 = [0] * 16
	#print(total_cand)

	llist = total_cand[0]
	for i in range(0, cand_len[0]):
		print("Validating: ", str(i + 1)+"/"+str(cand_len[0]))
		key10[0] = llist[i][0]
		key10[13] = llist[i][1]
		key10[10] = llist[i][2]
		key10[7] = llist[i][3]

		llist1 = total_cand[1]
		for j in range(0, cand_len[1]):
			key10[4] = llist1[j][0]
			key10[1] = llist1[j][1]
			key10[14] = llist1[j][2]
			key10[11] = llist1[j][3]

			llist2 = total_cand[2]
			for k in range(0, cand_len[2]):
				key10[8] = llist2[k][0]
				key10[5] = llist2[k][1]
				key10[2] = llist2[k][2]
				key10[15] = llist2[k][3]

				llist3 = total_cand[3]
				for l in range(0, cand_len[3]):
					key10[12] = llist3[l][0]
					key10[9] = llist3[l][1]
					key10[6] = llist3[l][2]
					key10[3] = llist3[l][3]
					print(key10)
					subkeys = reverse_key(key10)
					ct1 = finj.encrypt_aes_subkeys(pt, subkeys)
					if (ct1.hex() == bytes(ct).hex()):
						print("Found the Key :", bytes(subkeys[0:16]).hex())
						return 1

	return 0

def find_faulty_column(ct_list_i, fct_list_i):
	ctr = 0
	column = -1
	nzpos = [0] * 4
	# print(ct_list_i, fct_list_i)
	for i in range(0,16):
		if ct_list_i[i] ^ fct_list_i[i] != 0:
			#print(i,ct_list_i[i],fct_list_i[i])
			if ctr != (int)(i/4) : 
				break
			nzpos[ctr] = i
			ctr +=1
			#print(ctr)

	#print(nzpos)
	c1 = np.array([0,7,10,13])
	c2 = np.array([1,4,11,14])
	c3 = np.array([2,5,8,15])
	c4 = np.array([3,6,9,12])
	if ctr == 4 :
		if np.array_equal(c1,nzpos):
			column = 0
		elif np.array_equal(c2,nzpos):
			column = 1
		elif np.array_equal(c3,nzpos):
			column = 2
		elif np.array_equal(c4,nzpos):
			column = 3

	return column

def get_diff_MC(fault_list,fault_len):
	row_start = 0
	row_end = 4
	col = []
	col = [0] * 4
	list_diff = []
	for i in range(row_start,row_end):
		for j in range(0, fault_len):
			col = [0] * 4
			col[i] = fault_list[j]
			#print(col)
			finj.mixcolumn(col)
			#print(col)
			list_diff.append(col)

	return list_diff



def round9_find_candidates(ct_list_i,fct_list_i,cand_len,column):
	print("Find the candidates for ct:",ct_list_i," fct:",fct_list_i,"\n")
	fault_list = [0] *255
	col = find_faulty_column(ct_list_i, fct_list_i)
	print("Column : ",col)
	for i in range(0,255):
		fault_list[i] = i + 1
	fault_len = 255

	print(fault_list)
	list_diff = get_diff_MC(fault_list,fault_len)

	return list_diff,col

def round9_key_recovery(pt, ct, ct_list, fct_list, ln):
	print("9th round Analysis")
	found = -1
	column = 0
	cand_len1 = 0
	cand_len = [-1, -1, -1,-1]  
	candidates = []
	total_cand = dict()
	for i in range(0,ln):
		list_diff,column = round9_find_candidates(ct_list[i],fct_list[i],cand_len,column)
		candidates = key10_candidate(ct_list[i],fct_list[i],cand_len1,column,list_diff)
		#print(candidates)
		if cand_len[column] == -1:
			total_cand[column] = candidates
			cand_len[column] = len(candidates)
		else:
			total_cand[column] = (intersection(total_cand[column], candidates))
			cand_len[column] = (int)(len(total_cand[column])/4)
			print(total_cand[column],cand_len[column])
		 	#print(len(new))

	nb_cand = 1
	for i in range(0,4):
		nb_cand *= int(cand_len[i])

	print("Number of candidates for state\t {0, 13, 10, 7}:",cand_len[0],"\n",
    "\t\t\t\t {4,  1, 14, 11}:",cand_len[1],"\n",
    "\t\t\t\t {8,  5,  2, 15}:",cand_len[2],"\n",
    "\t\t\t\t {12,  9,  6,  3}:",cand_len[3],"\n",
    "Number of Master Key candidates: ", nb_cand)

	if nb_cand == 1 :
		print("Perform Exhaustive Search")
		found = exhaustive_search(pt, ct, total_cand, cand_len)
		if found == 0:
			print("The Attack was Unsuccessful : Check the Analysis\n")
		elif found == 1:
			print("The Attack was Successful")
	else:

		newsearch(pt, ct, total_cand, cand_len)

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = []
    while v:
        b.append(int(v & 0xff))
        v >>= 8
    #print b
    return b[::-1]

def readfile(filename):
	ct_list = []
	fct_list = []
	print("Read the contents of the File")
	fn= open(filename,'r')
	cont = fn.readlines()
	type(cont) 
	data = cont[0].split(',')

	# load plaintext and ciphertext from first line
	pt = bitstring_to_bytes(bin(int(data[0], 16)))
	ct_t = data[1].replace('\n','')
	ct = bitstring_to_bytes(bin(int(ct_t, 16)))
	# print("Plaintext",bytes(pt).hex())
	print("\nCiphertext",bytes(pt).hex(),"\n")

	print("FaultyCiphertext")
	for i in range(1,len(cont)):
		data = cont[i].split(',')
		ct1 = bitstring_to_bytes(bin(int(data[0], 16)))
		ct_list.append(ct1)
		fct_t = data[1].replace('\n','')
		fct = bitstring_to_bytes(bin(int(fct_t, 16)))
		fct_list.append(fct)
		print(bytes(fct).hex())
		
	return pt,ct, ct_list,fct_list, len(fct_list)

def parse_parameters():
	parser = argparse.ArgumentParser(description='Differential Fault Analysis')
	parser.add_argument("-round", help = "input the round where fault injected", type=str, required=True)
	parser.add_argument("-input", help = "File containing ciphertext details", type=str, required=True)
	args = parser.parse_args()
	mode = int(args.round)
	filename = args.input
	found  = 0
	pt,ct, ct_list,fct_list,ln = readfile(filename)
	
	if mode == 9:
		print("Fault Injection at the 9th round\n")
		round9_key_recovery(pt, ct, ct_list, fct_list, ln)
	elif mode == 10:
		print("Fault Injection at the 10th round\n")
		print("Happy Hacking!!!\n")

if __name__=="__main__":
	parse_parameters()
