<script>
// export let name;
import { get } from "./api.js";
import Header from "./components/Header.svelte";
import RoomExits from "./components/RoomExits.svelte";
import RoomActions from "./components/RoomActions.svelte";
import RoomContent from "./components/RoomContent.svelte";
import PlayerMessages from "./components/PlayerMessages.svelte";
import CharacterInventory from "./components/CharacterInventory.svelte";

import { tableauPromise, tableau } from "./stores.js";
export let user;

function initTableau() {
  tableauPromise.set(get(`v1/tableau/`));
}

initTableau();
</script>

{#if $tableau}
	<Header user={user} />
	{#if $tableau.room}
		<main style="background-color: {$tableau.room.colorHex};" id="room-target">
			<sidebar>
				<RoomExits />
				<CharacterInventory />
			</sidebar>
			<section class="content">
				<RoomContent />
				<PlayerMessages />
			</section>
			<RoomActions />
		</main>
	{:else}
		<h1>You have died. Sorry.</h1>
		<PlayerMessages />
	{/if}
{/if}

<style>
</style>