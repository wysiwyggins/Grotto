<script>
import { tableau, insertedMessage } from "../../stores.js";
</script>

<p>There are some entities in the room:</p>
<ul class="here">
  {#each $tableau.room.occupants as occupant}
    <li>
      {#if occupant.pk == $tableau.character.pk}
        you
      {:else}
        <a href="/guild/character/{occupant.pk}/">{occupant.name}</a>
      {/if}
    </li>
  {/each}
  {#each $tableau.room.npcs as npc}
    <li>{npc.name} is here! &mdash; <a href="#" on:click="{() => insertedMessage.set(npc.greeting)}">greet</a></li>
  {/each}
</ul>
