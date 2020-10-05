n = int(input())
arr = []
for i in range(n):
    arr.append(input())

str = "[\"" + arr[0] + "\""
for i in range(1, n):
    str += "," + "\"" + arr[i] + "\""
str += "]"
print(str)

print("{", end='')
for i in range(n):
    for j in range(i, n):
        print("(\"", arr[i], "\", \"", arr[j], "\"): ", 0, sep='', end='')
        if i != n - 1: print(",", end='')
    print()
print("}")
