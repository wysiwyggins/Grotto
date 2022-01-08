let UIPanels= [];
let statusMessage = document.querySelector('#status-bar');
let actionMessage = document.querySelector('#action-bar');


// on document load we get all of the ui panel divs and for each one we make a UIPanel object that is stored in the UIPanels array
// when navigation keys are pressed, the input script loops through all the items of each of the ui panels and highlights the li of the corresponding item by
// adding the selected class, when return is hit, the use function of that item is run

//we get items, move them, and run their functions using django-rest-framework

document.addEventListener("DOMContentLoaded", function() {
    // code
  });

class UIPanel {
    constructor(panelName, panelItems, id){
        this.panelName = panelName;
        this.items = [];
        this.id = document.getElementById(id);
        //this.maxRows = getComputedStyle(this.id).height * numberOfRows;
        //register the panel
        UIPanels.push(this);   
    }
    
    getItems() {

    }

    pushItems(){

    }

}