
function createMenuItemsForm(){
    if(document.getElementById('create-row-menu_items') === null){
        let event = new Event("create_event_menu_items");
        document.querySelector('a[onclick="createMenuItemsForm()"]').dispatchEvent(event);
    }
}