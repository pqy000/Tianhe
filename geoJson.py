import json
import os

f = file('/Users/panqingyi/Desktop/dat.txt')
s = json.load(f)
f.close()
#s1 = json.dumps(f, sort_keys=True)

#print s.keys()
value = s["features"][1]["geometry"]["coordinates"][0]
#print value

if os.path.exists('thefile.txt'):
    os.remove('thefile.txt')

for item in value:
    #print item[0]
    file_object = open('thefile.txt', 'a')
    file_object.write("boatPositions.add(new Point("+str(item[0]) + ","+str(item[1]) + "));\n")
    file_object.close()

