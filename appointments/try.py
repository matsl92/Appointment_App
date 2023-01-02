a = ['a', 'b', 'c', None, None, None]
for i in a:
    if i == None:
        a.remove(i)
    print(a)