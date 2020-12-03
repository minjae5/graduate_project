
import korean as ko
#normalize(text)
with open('/home/leeyoungsu/son_changed_script.txt', encoding='utf-8') as f:
    with open('/home/leeyoungsu/make.txt', 'w',encoding='utf-8') as k:
         for line in f:
             part=line.strip().split('|')
             text=part[2]
             tx_norm=ko.normalize(text)
             print('f number'+ part[2])
             #print('normalize'+ko.normalize(tx_norm))
             #print('='*30)
             k.write(part[0]+"|"+part[1]+"|"+tx_norm+"\n")
