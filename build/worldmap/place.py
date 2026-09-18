"""Put the party and the airship somewhere they can actually stand.

`is_passable` is the wrong question for a square you are going to stand on -
`Stairs K` is passable and blocked left and right - so both squares are chosen
with `flags & 0x0F == 0`, and the spawn is flood-filled to prove it reaches the
continent rather than a pocket. The airship additionally refuses 0x0800 (the
no-landing bit the road tiles carry) and any square with an event on it.
"""
import collections
import json
import sys


def flags_at(d, ts, w, h, x, y):
    for z in (3, 2, 1, 0):
        t = d[(z * h + y) * w + x]
        if t and not (ts[t] & 0x10):
            return ts[t]
    return ts[0]


def place(map_id, near, project="staging"):
    m = json.load(open("%s/data/Map%03d.json" % (project, map_id)))
    ts = json.load(open("%s/data/Tilesets.json" % project))[m["tilesetId"]]["flags"]
    w, h, d = m["width"], m["height"], m["data"]
    ev = {(e["x"], e["y"]) for e in m["events"] if e}

    def openv(x, y):
        return (flags_at(d, ts, w, h, x, y) & 0x0F) == 0

    def flood(sx, sy):
        seen, q = {(sx, sy)}, collections.deque([(sx, sy)])
        while q:
            x, y = q.popleft()
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and openv(nx, ny):
                    seen.add((nx, ny)); q.append((nx, ny))
        return seen

    def search(ok):
        for r in range(0, 20):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) != r:
                        continue
                    x, y = near[0] + dx, near[1] + dy
                    if 0 <= x < w and 0 <= y < h and ok(x, y):
                        return (x, y)
        return None

    spawn = search(lambda x, y: openv(x, y) and len(flood(x, y)) > 2000)
    air = search(lambda x, y: openv(x, y) and (x, y) not in ev
                 and not (flags_at(d, ts, w, h, x, y) & 0x0800)
                 and (x, y) != spawn)
    s = json.load(open("%s/data/System.json" % project))
    s["airship"].update(startMapId=map_id, startX=air[0], startY=air[1])
    s.update(startMapId=map_id, startX=spawn[0], startY=spawn[1])
    json.dump(s, open("%s/data/System.json" % project, "w"), ensure_ascii=False)
    return spawn, air


if __name__ == "__main__":
    mid = int(sys.argv[1])
    print(place(mid, (int(sys.argv[2]), int(sys.argv[3]))))
