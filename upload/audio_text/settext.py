import os,re
s1= set()
s2= set()

in_dir="./"
filters="([.!?])"
with open(os.path.join(in_dir,"makescript_v1.txt"), encoding='utf-8') as f:
    index=1
    checklist=""
    for line in f:
        parts=line.strip().split('|')
        wv_name=parts[1]
       # print("wv_name=",wv_name)
        _parts=wv_name.strip().split('.')
        wv_number=_parts[0]
        if checklist==wv_number:
            index+=1
        else:
            print(checklist,index)
            checklist=wv_number
            index=1
       # print("wv_number=\n",wv_number)
       # print("index=",index)
        s1.update([wv_number])
    print(s1)

        
            
