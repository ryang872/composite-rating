$(document).ready(function() {
    // Initially highlight the first column
    $('#sortTable tbody tr').each(function() {
        $(this).find('td:first').addClass('active-column');
    });

    $("#sortTable thead th").click(function(e) {
        e.preventDefault();

        // Remove 'sorting-active' from other headers and 'active-column' from all cells
        $('.sorting-active').not(this).removeClass('sorting-active');
        $('#sortTable tbody tr td').removeClass('active-column');

        // Toggle 'sorting-active' class on the clicked header
        $(this).toggleClass('sorting-active');
        var orderClass = $(this).hasClass('asc') ? 'desc' : 'asc';
        $(this).removeClass('asc desc').addClass(orderClass);

        var index = $(this).index();
        var $table = $('#sortTable');
        var rows = $table.find('tbody tr').get();
        var isSelected = $(this).hasClass('sorting-active');
        var isNumber = $(this).hasClass('sorting-number');

        // Sorting logic
        rows.sort(function(a, b) {
            var x = $(a).find('td').eq(index).text();
            var y = $(b).find('td').eq(index).text();

            if(isNumber) {
                return isSelected ? parseFloat(x) - parseFloat(y) : parseFloat(y) - parseFloat(x);
            } else {
                return isSelected ? x.localeCompare(y) : y.localeCompare(x);
            }
        });

        $.each(rows, function(index, row) {
            $table.children('tbody').append(row);
        });

        // Highlight the active column
        $('#sortTable tbody tr').each(function() {
            $(this).find('td').eq(index).addClass('active-column');
        });

        return false;
    });
});
