x = 5
y = 5

print(id(x))
print(id(y))

x = [1, 2, 3]
y = x
x.append(4)
print(x) #1, 2, 3, 4
print(y) #1, 2, 3
