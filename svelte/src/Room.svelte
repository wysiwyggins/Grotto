<script>
import { get } from "./api.js";

import TextRoom from "./textView/TextRoom.svelte";
import GuiRoom from "./guiView/GuiRoom.svelte";
import PlayerMessages from "./textView/components/PlayerMessages.svelte";

import { tableauPromise, tableau } from "./stores.js";
export let user;

const viewModes = [
	{
		name: "text",
		component: TextRoom,
		bodyClasses: ["room"]
	},
  {
  	name: "gui",
  	component: GuiRoom,
  	bodyClasses: ["icon-ui-view"]
  }
];

let viewModeIdx = 1;

let viewMode = viewModes[viewModeIdx];

function initTableau() {
  tableauPromise.set(get(`v1/tableau/`));
}
initTableau();

function clearBodyClasses() {
	viewMode.bodyClasses.forEach(value => {
		document.body.classList.remove(value);
	})
}

const illuminationLevels = ["dark", "dim", "full"]

function setBodyClasses() {
	illuminationLevels.forEach(value => {
		document.body.classList.remove(`illuminate-${value}`);
	})
	if ($tableau && $tableau.room) {
		const level = illuminationLevels[$tableau.room.attributes.brightness];
		document.body.classList.add(`illuminate-${level}`);
	}
	viewMode.bodyClasses.forEach(value => {
		document.body.classList.add(value);
	})
}

function handleKeydown(event) {
	switch (event.key) {
		// other keypresses are handled by the GuiRoom
		case "`":
			clearBodyClasses();
			viewModeIdx = (viewModeIdx + 1) % viewModes.length;
			viewMode = viewModes[viewModeIdx];
			setBodyClasses();
		  break;
		default:
		  console.log(`[Room] useless key pressed: ${event.key}`);
	}
}

tableau.subscribe(value => {
	if (! value || !value.room) {
		return
	}
	setBodyClasses()
  document.title = value.room.name;
})



</script>


<svelte:window on:keydown={handleKeydown}/>

{#if $tableau}
	{#if $tableau.room}
		<svelte:component this={viewMode.component} user={user}/>
	{:else}
		<h1>You have died. Sorry.</h1>
		<PlayerMessages />
	{/if}
{/if}
