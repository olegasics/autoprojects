arr = [1, 2, 3]
print(','.join(str(arr)))
print(','.join(map(str, arr)))
print(','.join(str(k) for k in arr))
print([str(k) for k in arr])
print(str(k) for k in arr)
print(dict([(str(k), 0) for k in arr]))

A = [5, 3, 2, 4, 1]
for k in range(len(A)-1):
    for i in range(len(A) - 1):
        if A[i] >= A[i + 1]:
            A[i], A[i + 1] = A[i + 1], A[i]

print(A)