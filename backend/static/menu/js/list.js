document.addEventListener('htmx:configRequest', function (event) {
    const tokenElement = document.querySelector('[name="csrfmiddlewaretoken"]');
    if (tokenElement) {
        event.detail.headers['X-CSRFToken'] = tokenElement.value;
    }
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        event.detail.parameters[input.name] = input.value;
    });
});


function triggerRecordUpdate(elementId, action) {
    const element = document.getElementById(elementId);
    if (element) {
        // Perform the desired action, such as triggering an HTMX request
        htmx.trigger(element, action);
    }
}
