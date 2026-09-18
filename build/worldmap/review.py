"""Old map against new: what a player can still walk to, and what changed."""
import json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.chdir(ROOT)
from reach import grid, walk
AT=(35,35)

def main(map_id=941):
    om,ow,oh,oopen=grid('thistlewick',8)
    old=walk(ow,oh,oopen,(24,45))
    nm,nw,nh,nopen=grid('staging',map_id)
    new=walk(nw,nh,nopen,(24+AT[0],45+AT[1]))
    print("walkable from Thistlewick:  old %d   new %d" % (len(old),len(new)))

    ev=[e for e in json.load(open('thistlewick/data/Map008.json'))['events'] if e]
    changed=[]
    for e in ev:
        x,y=e['x'],e['y']
        o = 'walk' if (x,y) in old else ('open' if oopen(x,y) else 'blocked')
        n = ('walk' if (x+AT[0],y+AT[1]) in new
             else ('open' if nopen(x+AT[0],y+AT[1]) else 'blocked'))
        if o!=n: changed.append("  %-32s %s -> %s  at (%d,%d)"%(e['name'],o,n,x+AT[0],y+AT[1]))
    print("events whose access changed: %d"%len(changed)); print("\n".join(changed))

    meta=json.load(open(os.path.join(HERE,'generated.meta.json')))
    lost=[m['name'] for m in meta['markers'] if (m['x'],m['y']) not in new]
    print("new sites unreachable on foot:", lost or "none")

    gl=[(17+AT[0],y+AT[1]) for y in range(19,29)]
    r=walk(nw,nh,nopen,(24+AT[0],45+AT[1]),avoid=gl)
    print("Tower reachable without the Gloamwood:", (31+AT[0],8+AT[1]) in r)

    allopen={(x,y) for y in range(nh) for x in range(nw) if nopen(x,y)}
    seen=set(); pockets=[]
    for c in sorted(allopen):
        if c in seen: continue
        r=walk(nw,nh,nopen,c); seen|=r
        if c not in new: pockets.append((len(r),c))
    pockets.sort(reverse=True)
    print("walkable pockets off the mainland: %d; biggest %s"%(len(pockets),pockets[:5]))

if __name__=='__main__':
    main(int(sys.argv[1]) if len(sys.argv)>1 else 941)
