#!/usr/bin/env python3
import copy

# Read a matrix from a file and return it as an 2D-array 
def read_matrix(file_name):
	matrix = []
	with open(file_name, "r") as f:
		for line in f:
			line_array = [temp for temp in line.strip().split()]
			matrix.append(line_array)
	return matrix

# Print a matrix in normal format
def print_matrix(matrix):
	# Check if the argument is not a matrix
	if isinstance(matrix[0], list):
		for line in matrix:
			# Convert matrix values to string values
			print(" ".join(["{}".format(temp) for temp in line]))
	else:
		print("Your argument is not a matrix.")

	# One more print() function to clear a line
	print()

# Transpose of a matrix
def transpose(matrix):
	columns = len(matrix[0])
	rows = len(matrix)

	new_matrix = [[i for i in range(rows)] for _ in range(columns)]

	for i in range(columns):
		for j in range(rows):
			new_matrix[i][j] = matrix[j][i]

	return new_matrix

# Multiply a matrix to another matrix
# Matrix A: N x M; 
# Matrix B: M x P;
# Matrix C(result): N x P.
def multiply_matrix(A, B):
	N = len(A)
	M = len(A[0])
	P = len(B[0])

	C = [[i for i in range(P)] for j in range(N)]

	for i in range(N):
		for j in range(P):
			sum = 0
			for k in range(M):
				sum += int(A[i][k]) * int(B[k][j])
			C[i][j] = sum
	return C

# Raise a matrix to the nth power
def pow_matrix(matrix, n):
	new_matrix = matrix[:]

	for i in range(n - 1):
		new_matrix = multiply_matrix(matrix, new_matrix)

	return new_matrix

# Observability
# Matrix A is the state matrix
# Matrix C is the control matrix
def observability_matrix(A, C):
	result_matrix = []
	result_matrix.append(C)

	for n in range(1, len(A)):
		power = pow_matrix(A, n)
		product = multiply_matrix(C, power)
		result_matrix.append(product)

	for i in range(len(result_matrix)):
		result_matrix[i] = result_matrix[i][0]

	return result_matrix

def is_observable(matrix):
	return rank(matrix) == len(matrix[0])

# Controllability
# Matrix A is the state matrix
# Matrix B is the input matrix
def controllability_matrix(mat_A, mat_B):
	A = copy.deepcopy(mat_A)
	B = copy.deepcopy(mat_B)

	result_matrix = []
	result_matrix.append(B)

	for n in range(1, len(A)):
		power = pow_matrix(A, n)
		product = multiply_matrix(power, B)
		result_matrix.append(product)

	for i in range(len(result_matrix)):
		temp_arr = []
		for item in result_matrix[i]:
			temp_arr.append(item[0])
		result_matrix[i] = temp_arr

	return result_matrix

def is_controllable(matrix):
	return is_observable(matrix)

# Rank
def swap_rows(a, row1, row2):
	a[row2], a[row1] = a[row1], a[row2]
	return a

def transform_rows(a, x, row1, row2):
	for i in range(len(a[row2])):
		a[row2][i] += a[row1][i] * x
	return a

def rank(matrix):
	a = copy.deepcopy(matrix)
	columns = len(a[0])
	rows = len(a)
	rank = min(columns, rows)

	if rows > columns:
		a = transpose(a)
		columns, rows = rows, columns

	for r in range(rank):
		if a[r][r] != 0:
			for j in range(r + 1, rows):
				a = transform_rows(a, -(a[j][r] // a[r][r]), r, j)
		else:
			count1 = True
			for k in range(r + 1, rows):
				if a[k][r] != 0:
					a = swap_rows(a, r, k)
					count1 = False
					break

			if count1:
				for i in range(rows):
					a[i][r], a[i][rank - 1] = a[i][rank - 1], a[i][r]
			rows -= 1

		count2 = 0
		for i in a:
			if i == [0] * columns:
				count2 += 1

		return (rank - count2)
  
