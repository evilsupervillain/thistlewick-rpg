// Paste into the browser console with the game LOADED FROM A SAVE (you must be
// on the map, not the title screen), then SAVE THE GAME - this only edits the
// live session, and a save you do not re-save keeps the old switches.
//
// (The save export/import tools that used to sit beside this now live in the
// workspace, in tools/console/ - they are not specific to this game.)
//
// Why: switches 72-80 mean "has been in the party at some point". They are what
// stops a returning companion introducing themselves again and, more
// importantly, what stops Change Party Member re-initialising them down to
// their database level. A save made before those switches existed has them all
// clear, so anybody you had already recruited looks, to the rebuilt game, like
// a stranger.
(() => {
  const KNOWN = {2: 72, 3: 73, 4: 74, 5: 75, 6: 76, 7: 77, 8: 78, 9: 79, 10: 80};
  const RECRUIT = {2: 11, 3: 12, 4: 13, 5: 14, 6: 15, 7: 16, 8: 17, 9: 18, 10: 19};

  const rows = [];
  for (const id of Object.keys(KNOWN).map(Number)) {
    const data = $dataActors[id];
    // Read the actor straight out of the save rather than through
    // $gameActors.actor(), which CREATES one on a miss and would make every
    // never-met companion look like a levelled veteran sitting at level 1.
    const live = $gameActors._data[id] || null;
    const inParty = $gameParty.allMembers().some(a => a.actorId() === id);
    const recruited = $gameSwitches.value(RECRUIT[id]);
    const levelled = !!live && live.level > data.initialLevel;
    rows.push({
      id, name: data.name, inParty, recruited, levelled,
      level: live ? live.level : "-",
      known: $gameSwitches.value(KNOWN[id]),
      verdict: inParty || recruited || levelled
    });
  }

  console.table(rows);

  const fixed = rows.filter(r => r.verdict && !r.known);
  fixed.forEach(r => $gameSwitches.setValue(KNOWN[r.id], true));
  $gameMap.requestRefresh();

  // For anyone the heuristic cannot see: somebody you dismissed under the old
  // build who never gained a level. Call it with a name, e.g. known("Roland").
  window.known = name => {
    const id = Object.keys(KNOWN).map(Number)
      .find(i => $dataActors[i].name.toLowerCase() === String(name).toLowerCase());
    if (!id) return "no companion called " + name;
    $gameSwitches.setValue(KNOWN[id], true);
    $gameMap.requestRefresh();
    return $dataActors[id].name + " is now marked as previously known";
  };

  return fixed.length
    ? `marked ${fixed.map(r => r.name).join(", ")} as previously known - NOW SAVE THE GAME`
    : "nothing to fix; every companion you have met is already marked";
})();
