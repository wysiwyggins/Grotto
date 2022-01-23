
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function getElementByTagNames(tags) {
    let ptr = document
    tags.forEach(tag => { ptr = ptr.getElementsByTagName(tag)[0]});
    return ptr
}


function renderItemClass(item) {
    let itemClass = item.abstract_item.itemType.toLowerCase()
    if (item.is_active) {
        itemClass += "-active";
    }
    return itemClass;
}


async function PaintRoom(tableau) {
    const headerElement = getElementByTagNames(["header", "h1"])
    console.log(headerElement);
    headerElement.innerHTML = tableau.room.name;

    const bodyElement = getElementByTagNames(["body"])
    bodyElement.style.backgroundColor = tableau.room.colorHex;

    const exitsElement = document.querySelector("ul.exits");
    let first = "selected"
    exitsElement.innerHTML = ""
    tableau.room.exits.forEach(exit => {
        exitsElement.innerHTML += `<li class="exit ${first}" data-type="exit"><a href="${exit.pk}"></a></li>`;
        first = "";
    })

    const itemsElement = document.querySelector("ul.room-items");
    itemsElement.innerHTML = ""
    tableau.room.items.forEach(item => {
        itemsElement.innerHTML += `<li class="item ${renderItemClass(item)}" data-type="${item.abstract_item.itemType.toLowerCase()}"><a href="${item.pk}"></a></li>`
    })
    tableau.room.occupants.forEach(character => {
        itemsElement.innerHTML += `<li class="character ${character.kind.toLowerCase()}" data-type="character"><a href="${character.pk}"></a></li>`
    })
    tableau.room.npcs.forEach(character => {
        itemsElement.innerHTML += `<li class="character npc ${character.name.toLowerCase()}" data-type="character"><a href="${character.pk}"></a></li>`
    })

    const statusElement = document.querySelector("div.status-bar");
    statusElement.innerHTML = "";
    tableau.messages.forEach(message => {
        statusElement.innerHTML += `<span>${message}</span>`;
    })

    const inventoryElement = document.querySelector("ul.character-items");
    inventoryElement.innerHTML = "";
    tableau.character.inventory.forEach(item => {
        inventoryElement.innerHTML += `<li class="item ${renderItemClass(item)}" data-type="${item.abstract_item.itemType.toLowerCase()}"><a href="${item.pk}"></a></li>`
    })

}


async function LoadRoom() {
    console.log('Attempting to load page data...');
    let tableau = await window.fetch("/api/v1/tableau/", {method: "GET"})
        .then((r) => r.text())
        .then((json) => {
            try {
                return JSON.parse(json);
            } catch (err) {
                throw "Bad response";
            }
        }).catch((e) => {
            throw "bad response";
        });
    console.log(tableau);
    PaintRoom(tableau);
}

async function main() {
    try {
        await LoadRoom();
    } catch (e) {
        console.log(`Loading failed: ${e}`);
    }
    initPanels();
}

document.addEventListener('DOMContentLoaded', main);