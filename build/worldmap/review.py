"""Old map against new: what a player can still walk to, and what changed."""
import json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT,'tools'))
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

    # The site list is the finished map's own events, not the sidecar.
    # `generated.meta.json` will describe worldgen's twenty-one for ever, so the
    # moment a site moved (Penultima) or was added by hand (7.1-7.4) it stopped
    # being the authority - and a reachability check read off it reports on a
    # field Penultima no longer stands in. WORLDMAP.md 7.6.
    sites={}
    for e in (nm.get('events') or ()):
        if e and ('<worldgen-site' in (e.get('note') or '')
                  or '<worldmap-site' in (e.get('note') or '')):
            sites.setdefault(e['name'],[]).append(
                ((e['x'],e['y']), '<aironly>' in (e.get('note') or '')))
    lost=[n for n,ds in sites.items()
          if not any(True for d,air in ds if air) and not any(d in new for d,air in ds)]
    air=[n for n,ds in sites.items() if any(air for d,air in ds)]
    walked=[n for n in air if any(d in new for d,_ in sites[n])]
    print("sites on the map: %d (%d air-only)"%(len(sites),len(air)))
    print("sites unreachable on foot:", lost or "none")
    print("air-only sites that can be WALKED to:", walked or "none")

    gl=[(17+AT[0],y+AT[1]) for y in range(19,29)]
    r=walk(nw,nh,nopen,(24+AT[0],45+AT[1]),avoid=gl)
    print("Tower reachable without the Gloamwood:", (31+AT[0],8+AT[1]) in r)

    # The four places off the mainland, cell by cell. `decor.py` cannot see
    # these: two of them are narrowed to one landing square by a layer-3
    # scenery tile, which it does check, but the Middle Distance's back row is
    # a `W_HILLS` on **layer 1**, and a layer-1 diff of a regenerated world
    # reports the whole world. So they are checked by name. Each wants walkable
    # cells, at least one airship-landable square, and region 0 - nothing lives
    # out there, and a party that has just set down on the Isle of Uncertain
    # Ownership should not be met by turnips.
    ts=json.load(open('staging/data/Tilesets.json'))[nm['tilesetId']]['flags']
    def flags(x,y):
        for z in (3,2,1,0):
            t=nm['data'][(z*nh+y)*nw+x]
            if t and not (ts[t]&0x10): return ts[t]
        return ts[0]
    ROCKS={'the Isle':[(55+i,83) for i in range(4)],
           "Attempt 112's stack":[(37+i,40) for i in range(3)],
           'the Middle Distance':[(82+dx,65+dy) for dy in range(3) for dx in range(2)],
           'The Former Premises':[(79,88),(80,88),(81,88)]}
    for name,cells in ROCKS.items():
        std=[c for c in cells if (flags(*c)&0x0F)==0]
        land=[c for c in std if not (flags(*c)&0x0800)]
        reg={nm['data'][(5*nh+c[1])*nw+c[0]] for c in cells}
        onfoot=[c for c in std if c in new]
        print("  %-21s %d cells, %d walkable, %d landable, regions %s%s%s"
              %(name,len(cells),len(std),len(land),sorted(reg),
                "  WALKABLE FROM THE MAINLAND: %s"%onfoot if onfoot else "",
                "  NO LANDING SQUARE" if not land else ""))

    # The road network, in pieces. WORLDMAP.md section 4 measured eleven and
    # accepted them; a hand-placed site gets no road unless `put_road` draws
    # one, so this is how a change to `run_finish.py` reports what it joined.
    import rmmzdata as R
    ROADS={29,30}                                   # Road (Dirt), Road (Paved)
    road={(x,y) for y in range(nh) for x in range(nw)
          for t in [nm['data'][(1*nh+y)*nw+x]]
          if t and R.is_autotile(t) and R.autotile_kind(t) in ROADS}
    seen,nets=set(),[]
    for c in sorted(road):
        if c in seen: continue
        grp,q={c},[c]
        while q:
            x,y=q.pop()
            for n in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if n in road and n not in grp: grp.add(n); q.append(n)
        seen|=grp; nets.append((len(grp),min(grp)))
    nets.sort(reverse=True)
    print("road network: %d cells in %d pieces; biggest %s"
          %(len(road),len(nets),nets[:5]))

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
