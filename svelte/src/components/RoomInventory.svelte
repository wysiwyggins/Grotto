<script>
import { post } from "../api.js";
import { tableau, tableauPromise } from "../stores.js";

function take(itemPk) {tableauPromise.set(post(`v1/items/${itemPk}/take/`, {}))}

</script>


<div class="room-inventory">
  {#if $tableau.room.items}
    {#if $tableau.room.attributes.brightness == 2}
      Items are scattered on the ground:
    {:else}
      In the darkness you can see several items in the room:
    {/if}
    <ul>
      {#each $tableau.room.items as item, pk}
        <li>{item.name}
          {#if item.is_takeable}
            &mdash; <a href="#" on:click="{() => take(item.pk)}">take</a>
          {/if}
        </li>
      {/each}
    </ul>
  {:else}
    Nothing can be taken.
  {/if}
</div>

