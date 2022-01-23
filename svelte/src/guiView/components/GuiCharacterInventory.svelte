<script>
import { post } from "../../api.js";

export let items;
const categoryIndex = 4;

import { tableauPromise } from "../../stores.js";
import { selectedIndex } from "../stores.js";

function handleItemClick(item) {
  tableauPromise.set(post(item.actionUrl, {}))
}

</script>

<ul class="character-items items panelItems">
  {#each items as item, idx}
    <li
      class="{item.classes.join(' ')}"
      class:selected="{categoryIndex == $selectedIndex.categoryIndex && idx == $selectedIndex.index}"
      data-type="{item.dataType}"
      on:mouseenter={() => {selectedIndex.set({categoryIndex: categoryIndex, index: idx})}}
      on:click={() => handleItemClick(item)}
    >
    </li>
  {/each}
</ul>
