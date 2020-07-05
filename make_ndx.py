import sys
if len(sys.argv)==1:
    print("usage: python *.py lammps.data")
    sys.exit(1)
data_file=sys.argv[1]
with open(data_file,'r') as reader:
    all_content=reader.readlines()
    for index,line in enumerate(all_content):
        if "atoms" in line:
            atomnums=int(line.split()[0])
        if "Atoms" in line:
            startline=index
            break
id_type = []
for i in range(startline+2,startline+2+atomnums):
    line=all_content[i]
    id_type.append([int(line.split()[0]),int(line.split()[2])])
all_type=[i[1] for i in id_type]
type_num=len(set(all_type))
with open("index.ndx",'w') as writer:
    writer.write("[ System ]\n")
    yushu = atomnums%15
    hangshu =  atomnums//15
    index = 1
    for i in range(hangshu):
        tmp=''
        for j in range(15):
            tmp+=" %d" %index
            index+=1
        tmp+="\n"
        writer.write(tmp.lstrip())
        #writer.write("\n")
    tmp=''
    for i in range(yushu):
        tmp+=" %d" %index
        index+=1
    writer.write(tmp.lstrip())
    writer.write("\n")
    for ii in range(1,type_num+1):
        writer.write("[ type%d ]\n" %(ii))
        gaizhongyuyanzi=sorted([o for o in id_type if o[1]==ii],key=lambda x:x[0])
        atomnums = len(gaizhongyuyanzi)
        yushu = atomnums%15
        hangshu =  atomnums//15
        index = 0
        for i in range(hangshu):
            tmp=''
            for j in range(15):
                tmp+=" %d" %gaizhongyuyanzi[index][0]
                index+=1
            tmp+="\n"
            writer.write(tmp.lstrip())
            #writer.write("\n")
        tmp=''
        for i in range(yushu):
            tmp+=" %d" %gaizhongyuyanzi[index][0]
            index+=1
        writer.write(tmp.lstrip()) 
        writer.write("\n")        

      
            