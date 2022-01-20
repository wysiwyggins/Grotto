<script>
import { post } from "../api.js";
import { tableau, tableauPromise } from "../stores.js";

function take(itemPk) {tableauPromise.set(post(`v1/items/${itemPk}/take/`, {}))}

let takeable_items = [];

tableau.subscribe(_tableau => {
  takeable_items = []
  if (! _tableau.room) {
    return
  }
  _tableau.room.items.forEach(item => {
    if (item.is_takeable) {
      takeable_items = [...takeable_items, item];
    }
  })
})
</script>

<div class="room-inventory">
  {#if takeable_items.length > 0}
    {#if $tableau.room.attributes.brightness == 2}
      <p>Items are scattered on the ground:</p>
    {:else}
      <p>In the darkness you can see several items in the room:</p>
    {/if}
    <ul>
      {#each takeable_items as item, pk}
        {#if item.is_takeable}
          <li>{item.name} &mdash; <a href="#" on:click="{() => take(item.pk)}">take</a></li>
        {/if}
      {/each}
    </ul>
  {:else}
    <p>Nothing in the room can be taken.</p>
  {/if}
</div>

