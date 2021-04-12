#!/usr/bin/python
import os
import shutil

from datetime import datetime

d = open("PASTHERE.txt", "r")
diagram = d.read()
d.close()

i           =   0
word        =   ""
listTable   =   {}
key         =   0

searchTab   =   "value%3D%22"
countTab    =   len(searchTab)
start       =   diagram.find(searchTab) + countTab

while True:
    while True:
        if diagram[start + i] != '%':
            key = start
            word = word + diagram[start + i]
            i    = i + 1
        else:
            break
    if word != '':
        listTable[key] = word

    i     = 0
    word  = ""
    if diagram.find(searchTab, start) != -1:
        start = diagram.find(searchTab, start) + countTab
    else:
        break

i           =   0
nameCol     =   ""
typeCol     =   ""
listCol     =   []
x           =   {}

searchCol   =   "value%3D%22%2B%20"
countCol    =   len(searchCol)
start       =   diagram.find(searchCol) + countCol
controlKey  =   0
switch      =   False


while True:
    while True:

        if controlKey + 1 < len(list(listTable.keys())):
            if start > list(listTable.keys())[1 + controlKey]:
                controlKey = controlKey + 1
                switch = True

        if switch:

            x[list(listTable.values())[controlKey - 1]] = listCol
            listCol = []
            switch = False

        if diagram[start + i] != '%':

            nameCol = nameCol + diagram[start + i]
            i    = i + 1
        else:
            while True:
                if diagram[start + i + 9] != '%':
                    typeCol = typeCol + diagram[start + i + 9]
                    i    = i + 1
                else:
                    break
            break

    listCol.append({nameCol: typeCol})

    i        = 0
    nameCol  = ""
    typeCol  = ""
    if diagram.find(searchCol, start) != -1:
        start = diagram.find(searchCol, start) + countCol
    else:
        x[list(listTable.values())[controlKey]] = listCol
        break

# x = {
#     "codes":[
#         {"lo":"string"},
#         {"sdds":"string"},
#         {"no":"string"},
#         {"lul":"string"},
#     ],
#     "sections":[
#         {"ooo":"string"},
#         {"kl":"string"},
#         {"lm":"string"},
#     ]
# }

check = ""

for table in x:
    print('***********')
    print('*', table, '*')
    print('***********')

    for col in x[table]:
        print(list(col.keys())[0] + ' -> ' + list(col.values())[0])
    print(' ')

print('Generate migration for (Symfony[s], Laravel[l], cancel[c])')
check = input('-> ')

# shutil.rmtree('out/')

if check == 'l':

    os.makedirs('out/database/migrations/')
    os.makedirs('out/app/Models/')
    os.makedirs('out/app/Nova/')

    migrate = open("resources/laravelMigration", "r")
    model   = open("resources/laravelModel", "r")
    nova    = open("resources/laravelNova", "r")

    laravelMigration = migrate.read()
    laravelModel     = model.read()
    laravelNova      = nova.read()

    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H%M%S")

    for table in x:

        fieldList  = ""
        fields     = ""

        tableSplit  = ''.join(word.title() for word in table.split())
        CamelCase   = tableSplit.replace('_','')[:-1]
        labelSingu  = table.replace('_',' ')[:-1]
        label       = table.replace('_',' ')

        wMiName = date_time + "_create_" + table + "_table.php"
        wMoName = CamelCase + ".php"

        wMi = open("out/database/migrations/" + wMiName, "a")
        wMo = open("out/app/Models/" + wMoName, "a")

        wNo = open("out/app/Nova/" + wMoName, "a")

        for col in x[table]:
            if list(col.values())[0] == 'index':
                fieldList = fieldList + "$table->integer('"+ list(col.keys())[0] +"')->index()->nullable();\n\t\t\t"
            else:
                if list(col.values())[0] in ['text', 'string']:
                    fields = fields + "Text::make('"+ list(col.keys())[0] +"'),\n\n\t\t\t"
                if list(col.values())[0] in ['int']:
                    fields = fields + "Number::make('"+ list(col.keys())[0] +"'),\n\n\t\t\t"
                if list(col.values())[0] in ['dateTime']:
                    fields = fields + "DateTime::make('"+ list(col.keys())[0] +"'),\n\n\t\t\t"
                if list(col.values())[0] in ['date']:
                    fields = fields + "Date::make('"+ list(col.keys())[0] +"'),\n\n\t\t\t"
                if list(col.values())[0] in ['bool']:
                    fields = fields + "Boolean::make('"+ list(col.keys())[0] +"'),\n\n\t\t\t"
                if list(col.values())[0] in ['time']:
                    fields = fields + "//https://novapackages.com/packages/michielfb/laravel-nova-time-field \n\n\t\t\t"
                if list(col.values())[0] != 'id':
                    fieldList = fieldList + "$table->" + list(col.values())[0] + "('"+ list(col.keys())[0] +"')->nullable();\n\t\t\t"

        className = "Create" + table.capitalize() + "Table"

        wMi.write(laravelMigration % (className, table, fieldList, table))
        wMo.write(laravelModel % (CamelCase))
        wNo.write(laravelNova % (CamelCase, label, labelSingu, CamelCase, fields))

        print('Create [Migration]       ->  ' + wMiName)
        print('Create [Model]           ->  ' + wMoName)
        print('Create [Ressource Nova]  ->  ' + wMoName)

        wMi.close()
        wMo.close()
        wNo.close()
    
    print('Laravel migration are created check /out folder')

print('End')


# last passenger no value
