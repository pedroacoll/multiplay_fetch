import numpy as np
from operator import itemgetter, attrgetter
s=['X','D','C']

print(s)
n=len(s)
L = map(lambda x:[str(x), s[x]], range(0,n))
L=sorted(L,key=itemgetter(1))
Q = np.array(L).flatten()
print(Q)
print(n)
data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
sorted(data, key=itemgetter(1))
print(data)