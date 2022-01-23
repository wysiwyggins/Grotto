import { writable, derived } from "svelte/store";

export const tableauPromise = writable(new Promise(() => {}));
export const tableau = derived(tableauPromise, async ($tableauPromise, set) => {
  const tableau = await $tableauPromise;
  console.log(tableau.messages);
  if (tableau.room) {
    console.log(tableau.room.warnings);
  }
  set(await $tableauPromise);
});

