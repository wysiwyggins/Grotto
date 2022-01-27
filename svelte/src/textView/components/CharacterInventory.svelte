<script>
import { post } from "../../api.js";
import { tableau, tableauPromise } from "../../stores.js";

function place(itemPk) {tableauPromise.set(post(`v1/items/${itemPk}/place/`, {}))}
function drop(itemPk) {tableauPromise.set(post(`v1/items/${itemPk}/drop/`, {}))}
function use(itemPk) {tableauPromise.set(post(`v1/items/${itemPk}/use/`, {}))}
</script>

<h2>Inventory:</h2>
<ul class="character-inventory">
  {#each $tableau.character.inventory as item, pk}
    <li>{item.name} &mdash;
      {#if item.is_active}
        <a href="#" on:click="{() => place(item.pk)}">place</a>
      {:else if item.is_usable}
        <a href="#" on:click="{() => use(item.pk)}">use</a>
      {:else}
        <a href="#" on:click="{() => drop(item.pk)}">drop</a>
      {/if}
  {/each}
</ul>