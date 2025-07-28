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

    // Add Row
    $('#add-row').DataTable({
        "pageLength": 5,
    });

    var action = '<td> <div class="form-button-action"> <button type="button" data-toggle="tooltip" title="" class="btn btn-link btn-primary btn-lg" data-original-title="Edit Project"> <i class="fa fa-edit"></i> </button> <button type="button" data-toggle="tooltip" title="" class="btn btn-link btn-danger" data-original-title="Remove"> <i class="fa fa-times"></i> </button> </div> </td>';

    // $('#addRowButton').click(function () {
    //     // $('#add-row').dataTable().fnAddData([
    //     //     $("#addName").val(),
    //     //     $("#addPosition").val(),
    //     //     $("#addOffice").val(),
    //     //     action
    //     // ]);
    //     $('#addRowModal').modal('hide');

    // });

    $('#addRowModalMembers').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Botón que abrió el modal
    var projectId = button.data('id');   // Extrae el id del atributo data-id
    var projectName = button.data('name');
    var modal = $(this);
    modal.find('#project_id').val(projectId); // Asigna el id del proyecto al campo oculto
    modal.find('#project_name').text(projectName); //Asignar el nombre del proyecto al modal
    });


    $('#alert_demo_1_1').click(function(e) {
					swal("¡Exito!", "!Datos guardados correctamente!", {
						icon : "success",
						buttons: {        			
							confirm: {
								className : 'btn btn-success'
							}
						},
					});
	});

    $('#addRowModalEdit').on('show.bs.modal', function (event){
        //var button = $(event.relatedTarget);
        //var projectId = button.data('idprojects');
        //var form = $('#editProjectForm');
        //var actionUrl = "{% url 'project_detail' 0 %}".replace('0', projectId);
        //form.attr('action', actionUrl)
    });

});


  document.body.addEventListener('projectUpdated', function(event) {
    document.querySelector('#messages').innerHTML = `
      <div class="alert alert-success">${event.detail}</div>
    `;
  });

  // Cerrar modal automáticamente
  document.body.addEventListener('closeModal', function() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('projectModal'));
    if (modal) {
      modal.hide();
    }
  });

