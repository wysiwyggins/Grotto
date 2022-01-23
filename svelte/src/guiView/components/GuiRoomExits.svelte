<script>
import { post } from "../../api.js";

export let exits;
const categoryIndex = 0;

import { tableauPromise } from "../../stores.js";
import { selectedIndex } from "../stores.js";

function handleClick(roomPk) {
  tableauPromise.set(post(`v1/rooms/${roomPk}/move/`, {}))
}

</script>

<ul class="exits panelItems">
  {#each exits as exit, idx}
    <li
      class="{exit.classes.join(' ')}"
      class:selected="{categoryIndex == $selectedIndex.categoryIndex && idx == $selectedIndex.index}"
      data-type="{exit.dataType}"
      on:mouseenter={() => {selectedIndex.set({categoryIndex: categoryIndex, index: idx})}}
      on:click={() => handleClick(exit.dataPk)}
    >
  </li>
  {/each}
</ul>