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

let viewModeIdx = 0;  // This sets the default view for players

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
function setIlluminationLevel(numericLevel) {
	illuminationLevels.forEach(value => {
		document.body.classList.remove(`illuminate-${value}`);
	})
	const level = illuminationLevels[numericLevel];
	document.body.classList.add(`illuminate-${level}`);
}

const cleanlinessLevels = ["profane", "dirty", "clean"]
function setCleanlinessLevel(numericLevel) {
	cleanlinessLevels.forEach(value => {
		document.body.classList.remove(`cleanliness-${value}`);
	})
	const level = cleanlinessLevels[numericLevel];
	document.body.classList.add(`cleanliness-${level}`);
}

function setBodyClasses() {
	if ($tableau && $tableau.room) {
		setIlluminationLevel($tableau.room.attributes.brightness);
		setCleanlinessLevel($tableau.room.attributes.cleanliness);
	} else {
		setIlluminationLevel(2);
		setCleanlinessLevel(2);
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
		document.body.classList.add("dead");
		setIlluminationLevel(2);
		return
	}
	document.body.classList.remove("dead");
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
		<a href="/guild/">Return to guild hall</a>
		<img src="/static/images/reaper.png" alt="The grim reaper leers at you."/>
	{/if}
{/if}
