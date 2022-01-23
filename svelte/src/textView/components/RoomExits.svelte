<script>
import { post } from "../../api.js";
import { tableau, tableauPromise } from "../../stores.js";

function move(roomPk) {
  tableauPromise.set(post(`v1/rooms/${roomPk}/move/`, {}))
}

function fireArrow(roomPk) {
  tableauPromise.set(post(`v1/rooms/${roomPk}/fire_arrow/`, {}))
}
</script>

<h2>Exits:</h2>
<ul class="exits">
  {#each $tableau.room.exits as exit, pk}
    <li>
      <a href="#" on:click="{() => move(exit.pk)}">
        {#if $tableau.room.attributes.brightness == 0}
          Too dark to see
        {:else}
          {exit.name}
        {/if}
      </a>
      {#if $tableau.character.arrow_count > 0}
        &mdash; <a href="#" on:click="{() => fireArrow(exit.pk)}">Fire arrow through door</a>
      {/if}
    </li>
  {/each}
</ul>

<style>
</style>