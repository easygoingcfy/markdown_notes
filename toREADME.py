import os
import sys
headpath = "/onboard_data/bags/meishangang"
lst = os.listdir(headpath)
ans = []
for x in lst:
    currentFile = headpath +"/" + x +"/" + sys.argv[1] 
    if os.path.exists(currentFile):
        lstInDate = os.listdir(currentFile)
        for y in lstInDate:
            fullPath = currentFile +"/" + y + "/README"
            ans += fullPath + ":\n"
            f = open(currentFile +"/" + y + "/README","r")
            ans += f.readlines()
            f.close()
for line in ans:
    print(line,end = "")

