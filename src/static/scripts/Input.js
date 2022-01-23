function initPanels() {
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      useSelected();
    }
    if (event.key === 'ArrowLeft') {
      onChangeSelectedItem(-1);
    }
    if (event.key === 'ArrowRight') {
      onChangeSelectedItem(1);
    }
    if (event.key === 'ArrowUp') {
      onChangeSelectedPanel(-1);
    }
    if (event.key === 'ArrowDown') {
      onChangeSelectedPanel(1);
    }
    if (event.key === '`') {
      //stub for changing view hotkey
    }
  });
}

function useSelected() {
  let selected = getSelectedItem();
  let type = selected.getAttribute('data-type');
  let mine = isSelectedInInventory();
  if (type === 'exit') {
    console.log(`Followed the exit to ${selected.firstElementChild.href}`);
  } else if (mine) {
    console.log(`Used the ${type}`);
  } else {
    console.log(`Picked up the ${type}`);
  }
}

function updateActionMessage(next) {
  let selected = next;
  let mine = isSelectedInInventory();
  let type = selected.getAttribute('data-type');
  if (type === 'character') {
    console.log(`Examine ${selected.firstElementChild.href}`);
    actionMessage.textContent = `Examine ${selected.firstElementChild.href}`;
  } else if (type === 'exit') {
    console.log(`Follow the exit to ${selected.firstElementChild.href}`);
    actionMessage.textContent = `Follow the exit to ${selected.firstElementChild.href}`;
    // do POST to make action occu
    // use response to get room name
    // redirect to appropriate room name
    //actionMessage.classList.add("attention");
  } else if (type === 'cenotaph') {
    console.log(`Use the ${type}`);
    actionMessage.textContent = `View the ${type}`;
  } else if (type === 'npc'){
    actionMessage.textContent = `Greet the wanderer`;
    actionMessage.textContent = `Greet the wanderer`;
  }
    else if (mine) {
    console.log(`Use the ${type}`);
    actionMessage.textContent = `Use the ${type}`;
    
  } else {
    console.log(`Pickup the ${type}`);
    actionMessage.textContent = `Pickup the ${type}`;
   
  }
}


function onChangeSelectedItem(direction) {
  let selected = getSelectedItem();
  let next = direction === 1 ? selected.nextElementSibling : selected.previousElementSibling;
  if (next) {
    setSelection(next);
    updateActionMessage(next);
  } else {
    let panel = getSelectedPanel();
    let next = direction === 1 ? panel.firstElementChild : panel.lastElementChild;
    setSelection(next);
    updateActionMessage(next);
  }
  
  
}

function onChangeSelectedPanel(direction) {
  let selected = getSelectedPanel();
  let panels = document.querySelectorAll('.panelItems');
  let next = false;
  panels.forEach((panel, idx) => {
    if (panel === selected) {
      let nextIndex = idx + direction;
      if (direction === 1) {
        nextIndex = nextIndex % panels.length;
      } else {
        if (nextIndex === -1) {
          nextIndex = panels.length - 1;
        }
      }
      next = panels[nextIndex];
    }
  });
  selectPanel(next);
}

function isSelectedInInventory() {
  let selected = getSelectedItem();
  let selectedPanel = selected.parentElement;
  let inventory = document.getElementById('inventory-panel');
  while(selectedPanel !== inventory) {
    selectedPanel = selectedPanel.parentElement;
    if (selectedPanel === document.body) {
      return false;
    }
  }
  return true;
}

function setSelection(ele) {
  let selected = getSelectedItem();
  selected.classList.remove('selected');
  ele.classList.add('selected');
}

function selectPanel(panel) {
  setSelection(panel.firstElementChild);
}

function getSelectedItem() {
  return document.querySelector('.selected');
}

function getSelectedPanel() {
  let selected = getSelectedItem();
  let selectedPanel = selected.parentElement;
  while(!selectedPanel.classList.contains('panelItems')) {
    selectedPanel = selectedPanel.parentElement;
  }
  return selectedPanel;
}

