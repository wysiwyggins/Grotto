import { writable, derived } from "svelte/store";

export const tableauPromise = writable(new Promise(() => {}));
export const insertedMessage = writable(null)
export const tableau = derived(tableauPromise, async ($tableauPromise, set) => {
  insertedMessage.set(null);
  set(await $tableauPromise);
});
export const baseUrl = writable(null);
export const messages = derived(
  [tableau, insertedMessage], ([$tableau, $insertedMessage]) => {
    const _messages = []
    if ($insertedMessage !== null) {
      _messages.push($insertedMessage);
    }
    $tableau.messages.forEach(m => _messages.push(m));
    return _messages;
})