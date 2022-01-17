import Room from './Room.svelte';

const room = new Room({
	target: document.getElementById("room-target"),
	props: JSON.parse(document.getElementById("room-props").textContent),
});

export default room;