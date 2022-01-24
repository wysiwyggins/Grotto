import { writable, derived } from "svelte/store";

export const tableauPromise = writable(new Promise(() => {}));
export const tableau = derived(tableauPromise, async ($tableauPromise, set) => {
  set(await $tableauPromise);
});

