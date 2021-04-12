table = "boujour_tois"
table = ''.join(word.title() for word in table.split())
CamelCase = table.replace('_','')[:-1]
label = table.replace('_',' ')[:-1]
labelSingu = table.replace('_',' ')

print(CamelCase)
print(label)
print(labelSingu)