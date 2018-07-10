#import unicodecsv as csv
import csv

a = open('question_data.txt' , 'r')
b = a.readlines()

c = []
for bla in b:
    if bla != '\n':
        c.append(bla)



d = []

for bla in c:
    if bla != '//practice:\n':
        d.append(bla)

d = d[1:]


e = []

for bla in d:
    helplist = []
    if '$qs' in bla:
        helplist.append(bla)
        helplist.append(d[d.index(bla)+10])
        helplist.append(d[d.index(bla)+20])
        e.append(helplist)

    elif '$pqs' in bla:
        helplist.append(bla)
        helplist.append(d[d.index(bla) + 16])
        helplist.append(d[d.index(bla) + 32])
        e.append(helplist)

#cleaning
f = []
for bla in e:
    helplist = []
    for blu in bla:
        nice = blu[blu.index('"')+1:blu.rindex('"')]
        helplist.append(nice)
    f.append(helplist)




for load in f[50:]:
    print(load)


g = []
for bla in f:
    helplist = []
    helplist.append(bla[0].replace('\\', ''))

    corrlist = bla[1].split(',')
    corrlist2 = bla[2].split(',')
    if len(corrlist) <5:
        print(bla)
    if len(corrlist2) < 5:
        print(corrlist2)




    for i in range(5):

        if "pills" in helplist[0]:
            print("IM HERE")

        almost = corrlist[i] + '*' + corrlist2[i]
        almostlist = almost.split('*')

        seen = set()
        #remove duplicates without destroying order (set would destroy order)
        almostlist = [x for x in almostlist if not ( x in seen or seen.add(x)) ]
        app = '*'.join(almostlist)
        helplist.append(app)

    g.append(helplist)



for question in g:
    print(question)



#g is desired

def writeCSV_fromList(name,list, firstrow_list=None):
    bfile =  open(name,"w", newline='')
    writer = csv.writer(bfile)
    if firstrow_list != None:
        writer.writerow(firstrow_list)
    writer.writerows(list)
    bfile.close()

writeCSV_fromList('data.csv',g)






with open('data.csv') as f:
    reads = csv.reader(f)
    questions = list(reads)


quizload = []
for term in questions:
    quizload.append({'question': term[0],
                     's1': term[1].split('*'),
                     's2': term[2].split('*'),
                     's3': term[3].split('*'),
                     's4': term[4].split('*'),
                     's5': term[5].split('*'),})





print('hi')
