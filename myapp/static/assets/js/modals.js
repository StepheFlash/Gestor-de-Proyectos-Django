$(document).ready(function () {
    $('#addModalProjectMembers').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Botón que abrió el modal
        var projectId = button.data('id');   // Extrae el id del atributo data-id
        var projectName = button.data('name');
        var modal = $(this);
        modal.find('#project_id').val(projectId); // Asigna el id del proyecto al campo oculto
        modal.find('#project_name').text(projectName); //Asignar el nombre del proyecto al modal
    });

    $('#modalActivityView').on('show.bs.modal', function (event) {
        $('#addViewActivityButton').focus();
        var button = $(event.relatedTarget);
        var activityTitle = button.data('activitytitle');
        var modal = $(this);
        modal.find('#activity_title').text(activityTitle);
    });

    $('#ModalAddDocument').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var projectIdDoc = button.data('idproject');
        var projectNameDoc = button.data('nameproject');
        var modal = $(this);
        modal.find('#id_project_doc').val(projectIdDoc);
        modal.find('#name_project_doc').val(projectNameDoc);
        //alert("Id project: "+projectIdDoc);
    });

     $('#addTaskModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var projectId = button.data('idproject');
        var activityId = button.data('idactivity');
        var modal = $(this);
        modal.find('#id_project').val(projectId);
        modal.find('#id_activity').val(activityId);
        //alert("Id project: "+projectIdDoc);
    });

    $('#addRowModalEdit').on('show.bs.modal', function (event) {
        //var button = $(event.relatedTarget);
        //var projectId = button.data('idprojects');
        //var form = $('#editProjectForm');
        //var actionUrl = "{% url 'project_detail' 0 %}".replace('0', projectId);
        //form.attr('action', actionUrl)
    });

});


document.body.addEventListener('projectUpdated', function (event) {
    document.querySelector('#messages').innerHTML = `<div class="alert alert-success">${event.detail}</div>`;
});

// Cerrar modal automáticamente
document.body.addEventListener('closeModal', function () {
    const modal = bootstrap.Modal.getInstance(document.getElementById('projectModal'));
    if (modal) {
        modal.hide();
    }
});


document.body.addEventListener("closeModal", () => {
    $("#ModalEditTask").modal("hide");
});

document.body.addEventListener("showMessage", (e) => {
    // Puedes mostrar el mensaje en un alert o en un div de mensajes
    alert(e.detail);
    // O mejor, en un div:
    // document.querySelector('#messages').innerHTML = `<div class="alert alert-success">${e.detail}</div>`;
});
