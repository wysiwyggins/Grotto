<script>
import { post } from "../../api.js";

export let items;
export let occupants;
export let npcs;

import { tableauPromise } from "../../stores.js";
import { selectedIndex } from "../stores.js";

function handleOccupantClick(occupant) {}
function handleNpcClick(npc) {}
function handleItemClick(item) {
  if (! items.is_takeable) {
    return
  }
  tableauPromise.set(post(`v1/item/${item.pk}/take/`, {}))
}

</script>

<ul class="room-items items panelItems">
  {#each items as item, idx}
    <li
      class="{item.classes.join(' ')}"
      class:selected="{1 == $selectedIndex.categoryIndex && idx == $selectedIndex.index}"
      data-type="{item.dataType}"
      on:mouseenter={() => {selectedIndex.set({categoryIndex: 1, index: idx})}}
      on:click={() => handleItemClick(item)}
    ></li>
  {/each}
  {#each occupants as occupant, idx}
    <li
      class="{occupant.classes.join(' ')}"
      class:selected="{2 == $selectedIndex.categoryIndex && idx == $selectedIndex.index}"
      data-type="{occupant.dataType}"
      on:mouseenter={() => {selectedIndex.set({categoryIndex: 2, index: idx})}}
      on:click={() => handleOccupantClick(occupant)}
    >
    <!-- TODO: link to character sheet -->
    </li>
  {/each}
  {#each npcs as npc, idx}
    <li
      class="{npc.classes.join(' ')}"
      class:selected="{3 == $selectedIndex.categoryIndex && idx == $selectedIndex.index}"
      on:mouseenter={() => {selectedIndex.set({categoryIndex: 3, index: idx})}}
      on:click={() => handleNpcClick(npc)}
      data-type="{npc.dataType}"
    >
    <!-- TODO: talk to npc -->
    </li>
  {/each}
</ul>