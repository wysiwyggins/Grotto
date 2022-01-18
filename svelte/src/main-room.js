import Room from './Room.svelte';

const target = document.getElementById("room-target");

function replaceTarget(target) {
	const room = new Room({
		target: target.parentElement,
		anchor: target,
		props: JSON.parse(document.getElementById("room-props").textContent),
	});
	target.remove();
	return room
}

const room = replaceTarget(target)

export default room;
