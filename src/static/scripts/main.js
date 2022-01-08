
async function LoadRoom() {
    console.log('Attempting to load page data...');
    let response = await window.fetch("http://grotto.wileywiggins.com/api/v1/tableau/", {method: "GET"});
    console.log(response.text());
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