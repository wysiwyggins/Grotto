<script>
import Time from "svelte-time";

import { tableau } from "../../stores.js";
</script>

{#if $tableau.room.visits}
  <p>There are some names scrawled on the wall, past visitors...</p>
  <ul class="visits">
    {#each $tableau.room.visits as visit}
      <li>
        <span class:died={visit.died_here}>{visit.character.name} &mdash; <Time timestamp={visit.stamp_date} relative /></span>
        {#if visit.died_here}RIP{/if}
      </li>
    {/each}
  </ul>
{:else}
  <p>Nobody else has been here in quite some time</p>
{/if}

<style>
.died {
  text-decoration: line-through;
}
</style>