import { derived, writable } from "svelte/store";
import { tableau } from "../stores.js";

export const selectedIndex = writable({"index": 0, "categoryIndex": 0});

function resolveInventoryAction(item) {
  if (item.is_active) {
    return "Place"
  } else if (item.is_usable) {
    return "Use"
  } else {
    return "Drop"
  }
}

export const selectable = derived(tableau, ($tableau, set) => {
  const _selectable = {
    exits: [],
    cenotaph: [],
    items: [],
    occupants: [],
    npcs: [],
    inventory: []
  };
  if (! $tableau || ! $tableau.room) {
    set(_selectable);
    return
  }

  $tableau.room.exits.forEach(room => {
    _selectable.exits.push({
      "dataPk": room.pk,
      "dataType": "exit",  // used to generate element
      "classes": ["exit"],  // TODO: add up/down functionality
      "actionUrl": `v1/rooms/${room.pk}/move/`,
      "actionText": `Move to ${room.name}`
    })
  });

  if ($tableau.room.cenotaph) {
    console.log("populating cenotaph");
    _selectable.cenotaph.push({
      "dataPk": $tableau.room.cenotaph.pk,
      "dataType": "cenotaph",  // used to generate element
      "classes": ["item", "cenotaph"],
      "linkUrl": `/rooms/cenotaph/${$tableau.room.colorSlug}/`,
      "actionText": `View the ${$tableau.room.colorName} cenotaph`
    })
  }

  $tableau.room.items.forEach(item => {
    let itemClass = item.abstract_item.itemType.toLowerCase();
    if (item.is_active) {
      itemClass += "-active";
    }
    let actionText = "Can't touch this";
    let actionUrl = null;
    if (item.is_takeable) {
      actionUrl = `v1/items/${item.pk}/take/` ;
      actionText = `Take ${item.name}`
    }
    _selectable.items.push({
      "dataPk": item.pk,
      "dataType": item.abstract_item.itemType.toLowerCase(),  // used to generate element
      "classes": ["item", itemClass],
      "actionUrl": actionUrl,
      "actionText": actionText
    })
  });

  $tableau.room.occupants.forEach(character => {
    if (character.pk != $tableau.character.pk) {
      _selectable.occupants.push({
        "dataPk": character.pk,
        "dataType": "character",  // used to generate element
        "classes": ["character", character.kind.toLowerCase()],  // TODO: add up/down functionality
        "actionUrl": null,  // TODO: link to view character sheet
        "linkUrl": `/guild/character/${character.pk}/`,
        "actionText": `Inspect ${character.name}`
      })
    }
  });

  $tableau.room.npcs.forEach(character => {
    _selectable.npcs.push({
      "dataPk": character.pk,
      "dataType": "character",  // used to generate element
      "classes": ["character", character.name.toLowerCase()],  // TODO: add up/down functionality
      "actionUrl": null,  // TODO: talk to npc
      "actionMessage": `"${character.greeting}"`,
      "actionText": `Greet ${character.name}`
    })
  });

  $tableau.character.inventory.forEach(item => {
    let action = resolveInventoryAction(item);
    let itemClass = item.abstract_item.itemType.toLowerCase();
    if (item.is_active) {
      itemClass += "-active";
    }
    _selectable.inventory.push({
      "dataPk": item.pk,
      "dataType": item.name.toLowerCase(),
      "classes": ["item", itemClass],
      "actionUrl": `v1/items/${item.pk}/${action.toLowerCase()}/`,
      "actionText": `${action} ${item.name}`
    })
  });
  console.log(_selectable);
  set(_selectable)
});




