<script>
// export let name;
import { get } from "./api.js";
import RoomExits from "./components/RoomExits.svelte";
import RoomActions from "./components/RoomActions.svelte";
import RoomContent from "./components/RoomContent.svelte";
import CharacterInventory from "./components/CharacterInventory.svelte";
import PlayerMessages from "./components/PlayerMessages.svelte";

import { tableauPromise, tableau } from "./stores.js";

function initTableau() {
  tableauPromise.set(get(`v1/tableau/`));
}

initTableau();
</script>

{#if $tableau}
	{#if $tableau.room}
		<main style="background-color: {$tableau.room.colorHex};" >
			<div class="main" >
				<sidebar>
					<RoomExits />
					<CharacterInventory />
				</sidebar>
				<section class="content">
					<RoomContent />
					<PlayerMessages />
				</section>
			</div>
			<RoomActions />
		</main>
	{:else}
		<h1>You have died. Sorry.</h1>
		<PlayerMessages />
	{/if}
{/if}

<style>
</style>