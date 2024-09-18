
function createCategoriesForm(){
    if(document.getElementById('create-row-categories') === null){
        let event = new Event("create_event_categories");
        document.querySelector('a[onclick="createCategoriesForm()"]').dispatchEvent(event);
    }
}