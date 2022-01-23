<script>
import { tableau } from "../../stores.js";
</script>



<p>There are some entities in the room:</p>
<ul class="here">
  {#each $tableau.room.occupants as occupant}
    <li>
      {#if occupant.pk == $tableau.character.pk}
        you
      {:else}
        {occupant.name}
      {/if}
    </li>
  {/each}
  {#each $tableau.room.npcs as npc}
    <li>{npc.name} is here!</li>
  {/each}
</ul>
