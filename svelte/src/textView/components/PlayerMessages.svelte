<script>
import { messages } from "../../stores.js";
</script>

{#if $messages}
  <ul class="messages">
    {#each $messages.reverse() as message}
      <li>{message}</li>
    {/each}
  </ul>
{/if}
