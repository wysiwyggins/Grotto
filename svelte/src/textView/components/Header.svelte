<script>
export let user;

import { tableau } from "../../stores.js";
function characterEmoji() {
  switch ($tableau.character.kind.toLowerCase()) {
    case 'fungus':
      return "🍄"
    case 'animal':
      return "🐴"
    case 'bird':
      return "🐤"
    case 'robot':
      return "🤖"
    case 'human':
      return "🤨"
    case 'ghost':
      return "👻"
    case 'vegetable':
      return "🥕"
  }
}

const defaultHeaderBackgroundColor = "#050505";

let headerBackgroundColor = defaultHeaderBackgroundColor;

tableau.subscribe(_tableau => {
  console.log("tableau did change?")
  headerBackgroundColor = defaultHeaderBackgroundColor
  if (_tableau.room) {
    headerBackgroundColor = _tableau.room.colorHex
  }
})

</script>

<header style="background-color: {headerBackgroundColor};">
  <div>
    <span class="header-title">
      <a href="/guild/character/{$tableau.character.pk}/">{characterEmoji()} "{$tableau.character.name}"</a>
    </span>
    <ul class="nav">
      {#if user.is_anonymous}
        <li><a href="/accounts/login/">Log Out</a></li>
      {:else}
        <li><a href="/accounts/logout/">Log Out</a></li>
        {#if user.is_staff}
          <li><a href="/admin/">Admin</a></li>
        {/if}
      {/if}
    </ul>
  </div>
</header>