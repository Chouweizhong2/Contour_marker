import pickle
test_scal = "1.15"
print(str(test_scal))
db = [['添加..',], [-1,]]
dbpath = "C:/Users/Cjay/PycharmProjects/Contour_marker/data/Material/mc-enep.txt"
with open(dbpath) as f:
    lines = f.readlines()
    if len(lines) > 1:
        if lines[0].split('#')[1] is 'None':
            scale = None
        else:
            scale = lines[0].split('#')[1]
        for i in range(len(lines) - 1):
            db[0].insert(i, lines[i + 1].split('\t')[0])
            list_point = []
            print(lines[i + 1].split('\t')[1][2:-3])
            for j in lines[i + 1].split('\t')[1][2:-3].split('),('):
                list_point.append(tuple(eval(j)))
            print(list_point)
            db[1].insert(i, list_point)

print(db)