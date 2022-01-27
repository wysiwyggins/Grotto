<script>
import { tableau } from "../../stores.js";
</script>

<ul class="warnings">
  {#each $tableau.room.warnings as warning}
    <li>{@html warning}</li>
  {/each}
</ul>

