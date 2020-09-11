from calcs import limits
import numpy as np 
d = np.array([1,2,3,4])
ans = limits.check_bounds(d,-2,4)
print(ans)