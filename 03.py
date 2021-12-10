# Day3:
# 3-1
r = {i: {'0':0, '1':0} for i in range(12)}
for b in data:
    for i, bit in enumerate(b):
    r[i][bit] += 1
    
 gamma = epsilon = ''
 for valeurs in r.values():
    nb_0 = valeurs['0']
    nb_1 = valeurs['1']
    if nb_0 > nb_1:
        gamma += '0'
        epsilon += '1'
    else:
        gamma += '1'
        epsilon += '0'
        
int(gamma, 2) * int(epsilon, 2)

# 3-2
def filter_data(data, actual_value='', comparaison_func=max):
    if len(data) == 1:
        return(data[0])
    comptage = {'0': 0, '1': 0}
    index = len(actual_value)
    for d in data:
        comptage[d[index]] += 1
    comptage = {v: k for k, v in comptage.items()}
    if len(comptage) == 1:
        actual_value += str(comparaison_func(0, 1))
    else:
        actual_value += comptage[comparaison_func(comptage.keys())]
    data = [d for d in data if d.startswith(actual_value)]
    return filter_data(data, actual_value=actual_value, comparaison_func=comparaison_func)
    
oxygen = filter_data(data)
co2 = filter_data(data, comparaison_func=min)

int(oxygen, 2) * int(co2, 2)