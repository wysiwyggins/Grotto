<script>
import { post } from "../../api.js";
import { tableau, tableauPromise } from "../../stores.js";

import RoomInventory from "./RoomInventory.svelte";
import RoomManifest from "./RoomManifest.svelte";
import RoomVisits from "./RoomVisits.svelte";
import RoomWarnings from "./RoomWarnings.svelte";

function sanctityAdjective() {
  return ["Cursed", "Mundane", "Sacred"][$tableau.room.attributes.sanctity]
}

function cleanlinessAdjective() {
  return ["Profane", "Dirty", "Clean"][$tableau.room.attributes.cleanliness]
}

</script>

<h2>
  {#if $tableau.room.attributes.brightness == 0}
    Dark Room
  {:else}
    {$tableau.room.name}
  {/if}
</h2>
<p class="room-attributes">
  The room is {sanctityAdjective()} and {cleanlinessAdjective()}.
  {#if $tableau.room.attributes.brightness == 1}
    The flicker of your held candle dimly lights the room. A candle-holder on the wall is empty.
  {:else if $tableau.room.attributes.brightness == 2}
    A burning candle lights the room.
  {/if}
</p>
{#if $tableau.room.attributes.brightness > 0}
  {#if $tableau.room.attributes.brightness == 2}
    <p class="description">{$tableau.room.description}</p>
  {/if}
  <RoomInventory />
  <RoomManifest />
  <RoomVisits />
  <RoomWarnings />
{/if}