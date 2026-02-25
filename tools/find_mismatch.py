from pathlib import Path
p=Path(r'D:/Projects/Tuteur intelligent/Frontend/src/pages/Statistiques/Statistiques.tsx')
s=p.read_text(encoding='utf-8')
pairs={'(':')','[':']','{':'}'}
stack=[]
for idx,ch in enumerate(s,1):
    if ch in pairs:
        stack.append((ch,idx))
    elif ch in pairs.values():
        if not stack:
            print('Unmatched closing',ch,'at',idx)
            break
        last,pos=stack.pop()
        if pairs[last]!=ch:
            print('Mismatched',last,'from',pos,'closed by',ch,'at',idx)
            # print context around positions
            def show(pos):
                line = s.count('\n',0,pos)+1
                col = pos - s.rfind('\n',0,pos)
                start = max(0,pos-40)
                end = min(len(s),pos+40)
                return line,col,s[start:end].replace('\n','\n')
            l1,c1,ctx1=show(pos)
            l2,c2,ctx2=show(idx)
            print('Open at',l1,':',c1, 'context:\n',ctx1)
            print('Close at',l2,':',c2, 'context:\n',ctx2)
            break
else:
    print('All matched')
