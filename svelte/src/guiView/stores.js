import { derived, writable } from "svelte/store";
import { tableau } from "../stores.js";

export const selectedIndex = writable({"index": 0, "categoryIndex": 0});

function resolveInventoryAction(item) {
  if (item.is_usable) {
    return "Use"
  } else if (item.is_active) {
    return "Place"
  } else {
    return "Drop"
  }
}

export const selectable = derived(tableau, ($tableau, set) => {
  const _selectable = {};
  const exits = [];
  console.log("watch me whip")
  $tableau.room.exits.forEach(room => {
    exits.push({
      "dataPk": room.pk,
      "dataType": "exit",  // used to generate element
      "classes": ["exit"],  // TODO: add up/down functionality
      "actionUrl": `v1/rooms/${room.pk}/move/`,
      "actionText": `Move to ${room.name}`
    })
  });
  _selectable["exits"] = exits;

  const items = [];
  $tableau.room.items.forEach(item => {
    let itemClass = item.abstract_item.itemType.toLowerCase();
    if (item.is_active) {
      itemClass += "-active";
    }
    let actionMessage = "Can't touch this";
    let actionUrl = null;
    if (item.is_takeable) {
      actionUrl = `v1/rooms/${item.pk}/move/` ;
      actionMessage = `Take ${item.name}`
    }
    items.push({
      "dataPk": item.pk,
      "dataType": item.abstract_item.itemType.toLowerCase(),  // used to generate element
      "classes": ["item", itemClass],
      "actionUrl": actionUrl,
      "actionText": actionMessage
    })
  });
  _selectable["items"] = items;

  const occupants = [];
  $tableau.room.occupants.forEach(character => {
    occupants.push({
      "dataPk": character.pk,
      "dataType": "character",  // used to generate element
      "classes": ["character", character.kind.toLowerCase()],  // TODO: add up/down functionality
      "actionUrl": null,  // TODO: link to view character sheet
      "redirectUrl": null,
      "actionText": `Inspect ${character.name}`
    })
  });
  _selectable["occupants"] = occupants;

  const npcs = [];
  $tableau.room.npcs.forEach(character => {
    npcs.push({
      "dataPk": character.pk,
      "dataType": "character",  // used to generate element
      "classes": ["character", character.name.toLowerCase()],  // TODO: add up/down functionality
      "actionUrl": null,  // TODO: talk to npc
      "actionText": `Inspect ${character.name}`
    })
  });
  _selectable["npcs"] = npcs;

  const inventory = [];
  $tableau.character.inventory.forEach(item => {
    let action = resolveInventoryAction(item);
    inventory.push({
      "dataPk": item.pk,
      "dataType": item.name.toLowerCase(),
      "classes": ["item", item.name.toLowerCase()],
      "actionUrl": `v1/items/${item.pk}/${action.toLowerCase()}/`,
      "actionText": `${action} ${item.name}`
    })
  });
  _selectable["inventory"] = inventory;
  console.log(_selectable);
  set(_selectable)
});




