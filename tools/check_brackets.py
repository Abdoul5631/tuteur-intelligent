from pathlib import Path
p=Path(r'D:/Projects/Tuteur intelligent/Frontend/src/pages/Statistiques/Statistiques.tsx')
s=p.read_text(encoding='utf-8')
pairs={'(':')','[':']','{':'}'}
opens=set(pairs.keys()); closes=set(pairs.values())
stack=[]
for i,ch in enumerate(s,1):
    if ch in opens:
        stack.append((ch,i))
    elif ch in closes:
        if not stack:
            print('Unmatched closing',ch,'at',i)
            break
        last, pos = stack.pop()
        if pairs[last]!=ch:
            print('Mismatched',last,'from',pos,'closed by',ch,'at',i)
            break
else:
    if stack:
        for last,pos in stack:
            print('Unclosed',last,'from',pos)
    else:
        print('All matched')
