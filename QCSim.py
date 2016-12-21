# Quantum Computer Simulator
# Luis Villasenor
# lvillasen@gmail.com
# 12/16/2016
# Usage
# python QCSim.py prog.ql
from __future__ import print_function
import numpy as np
import sys
import string
def printf(str, *args):
    print(str % args, end='')
def set_bit(value, bit):
    return value | (1<<bit)
def clear_bit(value, bit):
    return value & ~(1<<bit)
def print_state(g,n_qbits,A,B,C):
	if g != 'cx': print('Gate',g,'on qbit', qbit), 
	printf('  resulted in state |psi> = '),
	k1=0
	psi=''
	for k in range(2**n_qbits):
		s_i=("{:0%db}"%n_qbits).format(k)[::-1]
		if B[k] != 0: 
			k1+=1
			if k1==1:psi+=str(B[k])+'|'+s_i+'> '
			else:psi+='+ '+str(B[k])+str('|'+s_i+'> ')
	psi=string.replace(psi,'+ -', '- ')
	print(psi)
	print
	for  k in range(2**n_qbits): C[k]=B[k]
	for  k in range(2**n_qbits): A[k]=B[k]
	return
def get_qbits(command):
	before, sep, after = command.rpartition(";")
	before1, sep1, after1 = before.split()[1].rpartition(":")
	g=before.split( )[0]
	if g != 'cx':
		if sep1 == ':': 
			a=[int(s) for s in before1.split()[0] if s.isdigit()]
			if len(a)==1:qbit_i= a[0]
			if len(a)==2:qbit_i= 10*a[0]+a[1]
			a=[int(s) for s in after1.split()[0] if s.isdigit()]
			if len(a)==1:qbit_f= a[0]
			if len(a)==2:qbit_f= 10*a[0]+a[1]
		else:
			a=[int(s) for s in before.split()[1] if s.isdigit()]
			if len(a)==1:qbit_i= a[0]
			if len(a)==2:qbit_i= 10*a[0]+a[1]
			qbit_f=qbit_i
		qbit_c_i = qbit_i
		qbit_c_f = qbit_f
		qbit_t_i = -1
		qbit_t_f = -1
	else:
		if sep1 == ':': 
			a=[int(s) for s in before1.split()[0] if s.isdigit()]
			if len(a)==1:qbit_c_i= a[0]
			if len(a)==2:qbit_c_i= 10*a[0]+a[1]
			a=[int(s) for s in after1.split()[0] if s.isdigit()]
			if len(a)==1:qbit_c_f= a[0]
			if len(a)==2:qbit_c_f= 10*a[0]+a[1]
		else:
			a=[int(s) for s in before.split()[1] if s.isdigit()]
			if len(a)==1:qbit_c_i= a[0]
			if len(a)==2:qbit_c_i= 10*a[0]+a[1]
			qbit_c_f=qbit_c_i
		before2, sep2, after2 = before.split()[2].rpartition(":")
		if sep2 == ':': 
			a=[int(s) for s in before2.split()[0] if s.isdigit()]
			if len(a)==1:qbit_t_i= a[0]
			if len(a)==2:qbit_t_i= 10*a[0]+a[1]
			a=[int(s) for s in after2.split()[0] if s.isdigit()]
			if len(a)==1:qbit_t_f= a[0]
			if len(a)==2:qbit_t_f= 10*a[0]+a[1]
		else:
			a=[int(s) for s in before.split()[2] if s.isdigit()]
			if len(a)==1:qbit= a[0]
			if len(a)==2:qbit= 10*a[0]+a[1]
			qbit_t_i=qbit
			qbit_t_f=qbit
	return qbit_c_i,qbit_c_f,qbit_t_i,qbit_t_f
		
if len(sys.argv) > 1:
	file=sys.argv[1]
f = open(file,"r") #opens file with qc program
List = []
for line in f:
    List.append(line)
n_qbits =0
for i in range(len(List)):
	command=List[i]
	before, sep, after = command.rpartition(";")
	before1, sep1, after1 = before.split()[1].rpartition(":")
	g=before.split( )[0]
	if g =='id' or g=='h' or g=='x' or g=='y' or g=='z' or g=='s' or g=='sdg' or g=='t' or g=='tdg' or g=='measure':
		qbit_i,qbit_f,q,q = get_qbits(command)
		n_qbits=max(n_qbits, qbit_i+1)
		n_qbits=max(n_qbits, qbit_f+1)
	elif g =='cx':
		qbit_c_i,qbit_c_f,qbit_t_i,qbit_t_f = get_qbits(command)
		n_qbits=max(n_qbits, qbit_c_f+1)
		n_qbits=max(n_qbits, qbit_t_f+1)

print('Number of qbits: ',n_qbits)
A = [0 for i in range(2**n_qbits)]
B = [0 for i in range(2**n_qbits)]
C = [0 for i in range(2**n_qbits)]
M = [0 for i in range(n_qbits)]
A[0]=1
printf('Initial state: |psi> = '),
for i in range(2**n_qbits):
	s_i=("{:0%db}"%n_qbits).format(i)[::-1]
	if A[i] != 0: 
		printf(str(A[i])), 
		printf(str('|'+s_i+'>')),
printf('\n')
for i in range(len(List)):
	command=List[i]
	before, sep, after = List[i].rpartition(";")
	before1, sep1, after1 = before.split()[1].rpartition(":")
############ 1-qubit gates
################### gate id
	g = before.split( )[0]
	if g=='id' or g=='h' or g=='x' or g=='y' or g=='z' or g=='s' or g=='sdg' or g=='t' or g=='tdg' or g=='measure':
		qbit_i,qbit_f,q,q = get_qbits(command)
		if g =='id':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					for j in range(2**n_qbits):
						if A[j] != 0:
							B[j]+=A[j]
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					for j in range(2**n_qbits):
						if A[j] != 0:
							B[j]+=A[j]
					print_state(g,n_qbits,A,B,C)
################### gate h
		if g=='h':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=1/np.sqrt(2)*A[j]
								B[set_bit(j,qbit)]+=1/np.sqrt(2)*A[j]
							if bit_parity == 1:
								B[clear_bit(j,qbit)]+=1/np.sqrt(2)*A[j]
								B[j]+=-1/np.sqrt(2)*A[j]
					print_state(g,n_qbits,A,B,C)		
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=1/np.sqrt(2)*A[j]
								B[set_bit(j,qbit)]+=1/np.sqrt(2)*A[j]
							if bit_parity == 1:
								B[clear_bit(j,qbit)]+=1/np.sqrt(2)*A[j]
								B[j]+=-1/np.sqrt(2)*A[j]
					print_state(g,n_qbits,A,B,C)
################### gate x			
		if g=='x':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[set_bit(j,qbit)]+=A[j]
							if bit_parity == 1:
								B[clear_bit(j,qbit)]+=A[j]	
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[set_bit(j,qbit)]+=A[j]
							if bit_parity == 1:
								B[clear_bit(j,qbit)]+=A[j]	
					print_state(g,n_qbits,A,B,C)
################### gate y
		if g =='y':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[set_bit(j,qbit)]+=1j*A[j]
							if bit_parity == 1:
								B[clear_bit(j,qbit)]+=-1j*A[j]	
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[set_bit(j,qbit)]+=1j*A[j]
							if bit_parity == 1:
								B[clear_bit(j,qbit)]+=-1j*A[j]	
					print_state(g,n_qbits,A,B,C)
################### gate z					
		if g =='z':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=-A[j]	
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=-A[j]	
					print_state(g,n_qbits,A,B,C)
################### gate s
		if g =='s':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=1j*A[j]	
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=1j*A[j]	
					print_state(g,n_qbits,A,B,C)
################### gate sdg
		if g =='sdg':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=-1j*A[j]
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=-1j*A[j]
					print_state(g,n_qbits,A,B,C)
################### gate t
		if g =='t':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=1/np.sqrt(2)*(1+1j)*A[j]
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=1/np.sqrt(2)*(1+1j)*A[j]
					print_state(g,n_qbits,A,B,C)
################### gate tdg
		if g =='tdg':
			if qbit_f >= qbit_i:
				for qbit in range(qbit_i,qbit_f+1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=1/np.sqrt(2)*(1-1j)*A[j]
					print_state(g,n_qbits,A,B,C)
			elif qbit_f < qbit_i:
				for qbit in range(qbit_i,qbit_f-1,-1):
					B = [0 for i in range(2**n_qbits)]
					for j in range(2**n_qbits):
						if A[j] != 0:
							bit_parity=(j>>qbit)%2
							if bit_parity == 0:
								B[j]+=A[j]
							if bit_parity == 1:
								B[j]+=1/np.sqrt(2)*(1-1j)*A[j]
					print_state(g,n_qbits,A,B,C)
############ 2-qubit gates
################### gate cx
	if g == 'cx':
		qbit_c_i,qbit_c_f,qbit_t_i,qbit_t_f = get_qbits(command)
		if qbit_c_f > qbit_c_i and qbit_t_i == qbit_t_f: # qbit_c_f > qbit_c_i qbit_t_i == qbit_t_f
			qbit_t = qbit_t_i
			for qbit_c in range(qbit_c_i,qbit_c_f+1):
				B = [0 for i in range(2**n_qbits)]
				for j in range(2**n_qbits):
					if A[j] != 0:
						bit_parity_c=(j>>qbit_c)%2
						bit_parity_t=(j>>qbit_t)%2
						if bit_parity_c == 0:
							B[j]+=A[j]
						else:
							if bit_parity_t== 0:
								B[set_bit(j,qbit_t)]+=A[j]
							else:
								B[clear_bit(j,qbit_t)]+=A[j]
				print('Gate cx on control qbit =', qbit_c,' and target qbit =',qbit_t),
				print_state(g,n_qbits,A,B,C)
		elif qbit_c_f < qbit_c_i and qbit_t_i == qbit_t_f: # qbit_c_f < qbit_c_i qbit_t_i == qbit_t_f
			qbit_t = qbit_t_i
			for qbit_c in range(qbit_c_i,qbit_c_f-1,-1):
				B = [0 for i in range(2**n_qbits)]
				for j in range(2**n_qbits):
					if A[j] != 0:
						bit_parity_c=(j>>qbit_c)%2
						bit_parity_t=(j>>qbit_t)%2
						if bit_parity_c == 0:
							B[j]+=A[j]
						else:
							if bit_parity_t== 0:
								B[set_bit(j,qbit_t)]+=A[j]
							else:
								B[clear_bit(j,qbit_t)]+=A[j]
				print('Gate cx on control qbit =', qbit_c,' and target qbit =',qbit_t),
				print_state(g,n_qbits,A,B,C)
		elif qbit_c_f == qbit_c_i and qbit_t_i >= qbit_t_f: # qbit_c_f == qbit_c_i and qbit_t_i >= qbit_t_f
			qbit_c = qbit_c_i
			for qbit_t in range(qbit_t_i,qbit_t_f+1):
				B = [0 for i in range(2**n_qbits)]
				for j in range(2**n_qbits):
					if A[j] != 0:
						bit_parity_c=(j>>qbit_c)%2
						bit_parity_t=(j>>qbit_t)%2
						if bit_parity_c == 0:
							B[j]+=A[j]
						else:
							if bit_parity_t == 0:
								B[set_bit(j,qbit_t)]+=A[j]
							else:
								B[clear_bit(j,qbit_t)]+=A[j]
				print('Gate cx on control qbit =', qbit_c,' and target qbit =',qbit_t),
				print_state(g,n_qbits,A,B,C)
		elif qbit_c_f == qbit_c_i and qbit_t_i >= qbit_t_f: # qbit_c_f == qbit_c_i and qbit_t_i < qbit_t_f
			qbit_c = qbit_c_i
			for qbit_t in range(qbit_t_i,qbit_t_f-1,-1):
				B = [0 for i in range(2**n_qbits)]
				for j in range(2**n_qbits):
					if A[j] != 0:
						bit_parity_c=(j>>qbit_c)%2
						bit_parity_t=(j>>qbit_t)%2
						if bit_parity_c == 0:
							B[j]+=A[j]
						else:
							if bit_parity_t == 0:
								B[set_bit(j,qbit_t)]+=A[j]
							else:
								B[clear_bit(j,qbit_t)]+=A[j]
				print('Gate cx on control qbit =', qbit_c,' and target qbit =',qbit_t),
				print_state(g,n_qbits,A,B,C)
################### measure
	if g == 'measure':
		if qbit_f >= qbit_i:
			for qbit in range(qbit_i,qbit_f+1):
				M[qbit]=1
				print('Measure qbit', qbit) 
		elif qbit_f < qbit_i:
			for qbit in range(qbit_i,qbit_f-1,-1):
				M[qbit]=1
				print('Measure qbit', qbit) 
P=[0 for i in range(2**np.sum(M))]
for i in range(2**n_qbits):
	s_i = ("{:0%db}"%n_qbits).format(i)
	num=0
	k=0
	for j in range(len(M)):
		if M[j] == 1:
			num+=((i>>j)&1)*2**k
			k+=1
	P[num]+=+np.absolute(C[i])**2
print('Probabilities after measurement:')
for i in range(2**np.sum(M)):
	s_i = ("{:0%db}"%np.sum(M)).format(i)[::-1]
	if P[i] != 0: 
		printf('P('+str(s_i)+') = '),
		print(P[i])	