
$(document).ready(function(){
    // Remove if there is already a backdrop
    $(".modal-backdrop").remove()
    // Show modal when rendered
    // Initialize all Select2 widgets on page load
    $('.django-select2').select2();
    $("#daily_menus-modal").modal('show');
    // Close model when POSTing
    $("#request_submitter").click(function(){
        $("#daily_menus-modal").modal('hide')
    });

    // Hide formset.DELETE when rendered
    $("input[type='checkbox']").each(function(){
        $(this).attr('hidden', true);
    })


    // Delete button
    $('.modal-body .delete-btn').click(function() {
        // Get parent row
        let row = $(this).closest('.row');
        // Select hidden formset.DELETE checkbox
        row.find('input[type="checkbox"]').prop('checked', true);
        // Hide the entire row
        row.hide();
    })


    // Add MenuItem
    let addButton = $('#add-row-btn');
    let managerTotal = $('#id_form-TOTAL_FORMS');
    // Saves empty row since extra=1 in forms.
    // clone() must have 'true' for delete button to work.
    let emptyBaseRow = $('.modal-body .row').last().clone(true);
    let anchor = addButton.parent()

    addButton.click(function(){
        // Update django formset manager value.
        let totalCount = parseInt(managerTotal.val());
        managerTotal.val(totalCount + 1);

        let emptyRow = emptyBaseRow.clone(true)
        // Update each id, name and for in row.
        // Attributes that need updating.
        let attributes = ['id', 'name', 'for']
        attributes.forEach(function(attr){
            // Get elements with attr*=form-
            emptyRow.find(`[${ attr }*="form-"]`).each(function() {
                // Get value to be changed
                let currentAttr = $(this).attr(attr);
                // Replace the identifier number in attribute.
                currentAttr = currentAttr.replace(/form-(\d+)-/, `form-${totalCount}-`);
                $(this).attr(attr, currentAttr);
            })
        });

        anchor.before(emptyRow)
    })



    // Quantity Unit Functions
    // Function to update the data-unit attribute for the quantity input
    function updateQuantityUnit(selectElement, quantityInput) {
        let selectedOption = $(selectElement).find('option:selected');
        let unitType = selectedOption.data('unit');
        $(quantityInput).attr('data-unit', unitType);
        // Also update the label to reflect the unit type
        $(quantityInput).siblings('label').find('.unit-type').text(unitType);
    }
    // name$="-ingredient" each formset has names by default.
    // To run upon render for edits.
    $('.form-control[name$="-ingredient"]')
        .each(function() {
        let selectElement = $(this);
        let quantityInput = selectElement.closest('.row').find('input[name$="-quantity"]');
        updateQuantityUnit(selectElement, quantityInput);
    })
    // To run upon changes.
        .change(function() {
        let selectElement = $(this);
        let quantityInput = selectElement.closest('.row').find('input[name$="-quantity"]');
        updateQuantityUnit(selectElement, quantityInput);
    });
});