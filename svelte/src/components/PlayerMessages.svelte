<script>
import { tableau } from "../stores.js";
</script>

{#if $tableau.messages}
  <ul class="messages">
    {#each $tableau.messages.reverse() as message}
      <li>{message}</li>
    {/each}
  </ul>
{/if}
