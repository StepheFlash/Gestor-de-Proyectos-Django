$(document).ready(function () {
    $('#basic-datatables').DataTable({
    });

    $('#multi-filter-select').DataTable({
        "pageLength": 5,
        initComplete: function () {
            this.api().columns().every(function () {
                var column = this;
                var select = $('<select class="form-control"><option value=""></option></select>')
                    .appendTo($(column.footer()).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );

                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });

                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        }
    });

document.body.addEventListener("htmx:afterSwap", function(evt) {
    // Inicializar la tabla una sola vez
const table = $('#multi-filter-select-ejemplo').DataTable({
    pageLength: 50,
    initComplete: function () {
        const api = this.api();

        api.columns().every(function (index) {
            if (index === 0 || index === api.columns().nodes().length - 1) return;

            const column = this;
            const select = $('<select class="form-control"><option value=""></option></select>')
                .appendTo($(column.footer()).empty())
                .on('change', function () {
                    const val = $.fn.dataTable.util.escapeRegex($(this).val());
                    column.search(val ? '^' + val + '$' : '', true, false).draw();
                });

            column.data().unique().sort().each(function (d) {
                select.append('<option value="' + d + '">' + d + '</option>');
            });
        });
    }
});

});


    // Add Row
    $('#add-row').DataTable({
        "pageLength": 5,
    });

    $('#add-activity').DataTable({
        ajax:{
            url: "/activities/list/json/",
            dataSrc: "data"
        },
        columns: [
            { data: "Nro" },
            { data: "name" },
            { data: "stage" },
            { data: "actions", orderable: false }
        ],
        pageLength: 10
    });

    //Funcion para  dibujar y contruir la tabla con los recursos guia que solo estan para ese actividad
    var activityId = $("#resources-container").data("activity-id");
    $('#multimedia-table').DataTable({
        ajax:{
            url: `/activity/${activityId}/resources/list`,
            dataSrc: "data"
        },
        columns: [
            { data: "Nro" },
            { data: "Titulo" },
            { data: "Link Contenido" },
            { data: "Acciones", orderable: false }
        ],
        pageLength: 5
    });
    
    $('#add-row-project').DataTable({
            ajax: {
                //path de la url que genera el cuepo de la tabla
                url: "/projects/json/",
                dataSrc: "data"
            },
            columns: [
                { data: "id" },
                { data: "name" },
                { data: "tema" },
                { data: "horario" },
                { data: "integrantes" },
                { data: "actions", orderable: false }
            ],
            pageLength: 10
    });

    $('#list-members-project').DataTable({
            ajax: {
                //path de la url que genera el cuepo de la tabla
                url: "/projects/list/menbers/json/",
                dataSrc: "data"
            },
            columns: [
                { data: "nombre" },
                { data: "codigo" },
                { data: "Correo institucional" },
                { data: "actions", orderable: false }
            ],
            pageLength: 5
    });

    

});


