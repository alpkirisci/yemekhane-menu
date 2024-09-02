document.addEventListener('htmx:afterSwap', function (event) {
    $('#requirements-datatable').DataTable({
        language: {
            // TODO: TRANSLATE
            search: "_INPUT_",
            searchPlaceholder: "Search..."
        },
        responsive: true,
        autoWidth: true,

        drawCallback: function (settings) {
            let searchInput = $('input[type="search"]');
            searchInput.addClass('form-control form-control-sm bg-dark text-white border-secondary');

            let tableLengthSelect = $('select[name="requirements-datatable_length"]');
            tableLengthSelect.addClass('bg-dark text-white');
        },


        // got this from https://datatables.net/examples/api/multi_filter.html
        initComplete: function () {
        this.api()
            .columns()
            .every(function () {
                let column = this;
                let title = column.header().textContent;

                // Create input element
                let input = document.createElement('input');
                input.classList.add('form-control');
                input.classList.add('bg-dark');
                input.classList.add('text-white');
                input.classList.add('bright-placeholder')

                input.placeholder = title;

                column.header().replaceChildren(input);

                // Event listener for user input
                input.addEventListener('keyup', () => {
                    if (column.search() !== this.value) {
                        column.search(input.value).draw();
                    }
                });
            });
        },
    columnDefs: [
    { className: 'text-start', targets: '_all' },
    ],

    });
});