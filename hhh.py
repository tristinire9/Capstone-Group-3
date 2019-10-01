destinations_list = ['/', "/data"]
components_list = [[22,"hh"], [56,"po"]]

result_list = []
for i in range(0, len(destinations_list)):
    component = components_list[i]
    destination = destinations_list[i]
    result = component + [destination]
    print(result)
    result_list.append(result)

print(result_list)