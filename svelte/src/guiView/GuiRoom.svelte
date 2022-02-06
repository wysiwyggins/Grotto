<script>
import { tick } from "svelte";
import { post } from "../api.js";
import { invertColor, lightenColor } from "../util.js";
import { tableauPromise, tableau } from "../stores.js";

import GuiRoomExits from "./components/GuiRoomExits.svelte"
import GuiRoomItems from "./components/GuiRoomItems.svelte"
import GuiCharacterInventory from "./components/GuiCharacterInventory.svelte"

// IMPORTANT: Do see what's going on with selected/selectable in the file below!!! A lot of stuff happening there!
import { selectable, selectedIndex } from "./stores.js";

export let user;

const categories = ["exits", "cenotaph", "items", "occupants", "npcs", "inventory"];

// let selectedIndex = {"index": 0, "categoryIndex": 0};

function resetSelected() {
  selectedIndex.set({"index": 0, "categoryIndex": 0});
}

function incrementCategory() {
  let newCategory = 0;
  switch ($selectedIndex.categoryIndex) {
    case 0:
      newCategory = 1;
      break;
    case 1:
    case 2:
    case 3:
    case 4:
      newCategory = 5;
      break;
    case 5:
      newCategory = 0;
      break;
    default:
      newCategory = 0;
      break;
  }
  selectedIndex.set({"index": 0, "categoryIndex": newCategory});
}

function decrementCategory() {
  let newCategory = 0;
  switch ($selectedIndex.categoryIndex) {
    case 0:
      newCategory = 5;
      break;
    case 1:
      break;
      newCategory = 0;
    case 2:
    case 3:
    case 4:
    case 5:
      newCategory = 1;
      break;
    default:
      newCategory = 0;
      break;
  }
  selectedIndex.set({"index": 0, "categoryIndex": newCategory});
}

function incrementSelected() {
  // This is kinda ugly, but it works!
  let newIndex = $selectedIndex.index;
  let newCategory = $selectedIndex.categoryIndex;
  const maxLen = $selectable[categories[newCategory]].length
  newIndex += 1;
  while (newIndex >= $selectable[categories[newCategory]].length) {
    newCategory = (newCategory + 1) % categories.length;
    newIndex = 0;
  }
  selectedIndex.set({"index": newIndex, "categoryIndex": newCategory});
}

function decrementSelected() {
  let newIndex = $selectedIndex.index;
  let newCategory = $selectedIndex.categoryIndex;
  newIndex -= 1
  while (newIndex < 0) {
    newCategory -= 1
    if (newCategory < 0) {
      newCategory = categories.length - 1
    }
    newIndex = $selectable[categories[newCategory]].length - 1
  }
  selectedIndex.set({"index": newIndex, "categoryIndex": newCategory});
}

let selected;

function getSelected() {
  selected = $selectable[categories[$selectedIndex.categoryIndex]][$selectedIndex.index];
  if (selected === undefined) {
    decrementSelected()
  }
  return selected;
}

async function doSelected() {
  // each thing (indicated by `selectedIndex`) has a singular action
  const _selected = getSelected()
  if (_selected.linkUrl !== null && _selected.linkUrl !== undefined) {
    console.log("Linking to another page");
    location.href = _selected.linkUrl;
  }
  if (_selected.actionUrl === null || _selected.actionUrl === undefined) {
    console.log("No action for this thing!");
    return
  }
  tableauPromise.set(post(_selected.actionUrl, {}));
  await $tableauPromise;
  await tick();
  getSelected();
}

function handleKeydown(event) {
  switch (event.key) {
    case "a":
    case "ArrowLeft":
      console.log("change selected (left)")
      decrementSelected();
      console.log($selectedIndex);
      break;
    case "d":
    case "ArrowRight":
      console.log("change selected (right)")
      incrementSelected();
      console.log($selectedIndex);
      break;
    case "w":
    case "ArrowUp":
      incrementCategory();
      break;
    case "s":
    case "ArrowDown":
      decrementCategory();
      break;
    case "Enter":
    case " ":
      console.log("do thing with selected!")
      doSelected()
      break;
    default:
      console.log(`[GuiRoom] useless key pressed: ${event.key}`);
  }
}

selectedIndex.subscribe(value => {
  getSelected()
})

let contrastColor = "#FFFFFF";
tableau.subscribe(value => {
  contrastColor = lightenColor(invertColor(value.room.colorHex), 20)
})

</script>

<svelte:window on:keydown={handleKeydown}/>


<div class="content" style="background-color: {$tableau.room.colorHex};">
  <header>
    <h1>{$tableau.room.name}</h1>
    <span>grotto.wileywiggins.com/rooms/{$tableau.room.colorName}/</span>
  </header>
  <div class="main">
    <div class="UIpanel" id="room-panel">
      <GuiRoomExits exits="{$selectable.exits}"/>
      <div class="room-view UIpanel">
        <GuiRoomItems
          cenotaph="{$selectable.cenotaph}"
          items="{$selectable.items}"
          occupants="{$selectable.occupants}"
          npcs="{$selectable.npcs}"
        />
      </div>
    </div>
  </div>
  <div class="characterPanel" style="background-color: {contrastColor};">
    <div class="status-bar" id="status-bar">
      {#each $tableau.messages as message}
        <span>{message}</span>
      {/each}
    </div>
    <div class="action-bar" id="action-bar">
      {selected.actionText}
    </div>
    <div class= "UIpanel " id="inventory-panel">
      <GuiCharacterInventory items="{$selectable.inventory}"/>
    </div>
  </div>

</div>