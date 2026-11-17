import os,json,urllib.request
U=os.environ['MAKEFUN_ENV_URL'];V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
D={'n':(-33,-31,-18,-14,14,18,31,33),'b':(-17,-15,15,17),'r':(-16,1,16,-1),'q':(-17,-16,-15,1,15,16,17,-1),'k':(-17,-16,-15,1,15,16,17,-1)}
def post(p,x):
 r=urllib.request.urlopen(urllib.request.Request(U+p,data=json.dumps(x).encode(),headers={'content-type':'application/json'}));return json.load(r)
def pos(f):
 a=['.']*128;y=112
 for z in f.split()[0].split('/'):
  x=0
  for c in z:
   if c.isdigit():x+=int(c)
   else:a[y+x]=c;x+=1
  y-=16
 return a
def mv(a,s):
 x=int(s[0])+16*(int(s[1])-1);y=int(s[2])+16*(int(s[3])-1);return x,y,(s[4] if len(s)>4 else '')
def put(a,m):
 x,y,p=m;b=a[:];c=b[x];b[x]='.';b[y]=p.upper() if c.isupper() else p or c
 if c.lower()=='p' and x%16!=y%16 and b[y]=='.':b[y+(-16 if c.isupper() else 16)]='.'
 if c.lower()=='k' and abs(y-x)==2:
  q=y+1 if y>x else y-2;b[y-1 if y>x else y+1]=b[q];b[q]='.'
 return b
def atk(a,k,w):
 for i,c in enumerate(a):
  if i&8 or c=='.' or c.isupper()!=w:continue
  t=c.lower();
  if t=='p':
   for d in (15,17):
    if 0<=i+(-d if w else d)<128 and i+(-d if w else d)==k:return 1
  elif t=='n':
   if any(i+d==k and not(i+d&8) for d in D[t]):return 1
  else:
   for d in D[t]:
    j=i+d
    while 0<=j<128 and not(j&8):
     if j==k:return 1
     if a[j]!='.':break
     if t=='k':break
     j+=d
 return 0
def check(a,w):
 k=next((i for i,c in enumerate(a) if c==('K' if w else 'k')), -1);return k<0 or atk(a,k,not w)
def gen(a,w):
 r=[]
 for i,c in enumerate(a):
  if i&8 or c=='.' or c.isupper()!=w:continue
  t=c.lower()
  if t=='p':
   q=i+(16 if w else -16)
   if 0<=q<128 and not(q&8) and a[q]=='.':
    r += [fmt(i,q,'q' if q//16 in(0,7) else '')]
    if i//16==(1 if w else 6) and a[q+(16 if w else -16)]=='.':r+=[fmt(i,q+(16 if w else -16),'')]
   for d in (15,17):
    q=i+(d if w else -d)
    if 0<=q<128 and not(q&8) and a[q]!='.' and a[q].isupper()!=w:r+=[fmt(i,q,'q' if q//16 in(0,7) else '')]
  elif t in D:
   for d in D[t]:
    q=i+d
    while 0<=q<128 and not(q&8):
     if a[q]=='.' or a[q].isupper()!=w:r.append(fmt(i,q,''))
     if a[q]!='.' or t=='n' or t=='k':break
     q+=d
 return [s for s in r if not check(put(a,mv(s)),w)]
def fmt(x,y,p):return 'abcdefgh'[x%16]+str(x//16+1)+'abcdefgh'[y%16]+str(y//16+1)+p
def score(a,w):
 n=sum((V.get(c.lower(),0))*(1 if c.isupper()==w else -1) for c in a if c!='.')
 return n
def search(a,w,d,al=-10**9,be=10**9):
 L=gen(a,w)
 if not L:return (-999999 if check(a,w) else 0),''
 if d<1:return score(a,w),''
 best=-10**9;bm=L[0]
 for s in L:
  v=-search(put(a,mv(s)),not w,d-1,-be,-al)[0]
  if v>best:best,bm=v,s
  al=max(al,v)
  if al>=be:break
 return best,bm
def choose(f,legal):
 a=pos(f);w=f.split()[1]=='w';best=(-10**9,legal[0])
 for s in legal:
  v=-search(put(a,mv(s)),not w,2,-10**9,10**9)[0]
  if v>best[0]:best=v,s
 return best[1]
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
