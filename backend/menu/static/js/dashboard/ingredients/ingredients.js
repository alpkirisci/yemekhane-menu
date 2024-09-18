
function createIngredientsForm(){
    if(document.getElementById('create-row-ingredients') === null){
        let event = new Event("create_event_ingredients");
        document.querySelector('a[onclick="createIngredientsForm()"]').dispatchEvent(event);
    }
}