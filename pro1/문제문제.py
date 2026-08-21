def odd(par):
    return par % 2 == 1
c={i for i in range(11) if odd(i)}
print(c) 