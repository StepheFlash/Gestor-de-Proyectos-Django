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
    $('#addActivityModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var stageId = button.data('idstage');
        var modal = $(this);
        modal.find('#id_stage').val(stageId);
        //alert("Id estapa: "+stageId);
    });

    $('#resourcesActivityModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var activityId = button.data('idactivity');
        var modal = $(this);
        modal.find('#id_activity').val(activityId);
    })

    $('#resourcesActivityModalEdit').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var resourcesId = button.data('idresource');
        var modal = $(this);
        modal.find('#id_multimedia').val(resourcesId);
    })

    $('#addNoteCalendarModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var meetingId = button.data('idmeeting');
        var modal = $(this);
        modal.find('#meeting_id').val(meetingId);
    })



    $(document).on("click", ".btn-edit-project", function () {
        let id = $(this).data("id");
        // let name = $(this).data("name");
        // let horario = $(this).data("horario");
        // let tema = $(this).data("tema");

        // Llenar los inputs del modal
        $("#editProjectForm").attr("action", `/projects/${id}/edit`);
        // $("#editProjectForm #name").val(name);
        // $("#editProjectForm #horario_reunion").val(horario);
        // $("#editProjectForm #tema_investigacion").val(tema);

        // Si quieres también cargar integrantes por AJAX
        // $.get(`/projects/${id}/integrantes/`, function (html) {
        //     $("#integrantes-container").html(html);
        // });
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
document.addEventListener("DOMContentLoaded", function () {


});
; (function () {

    document.body.addEventListener("activityAdded", function (e) {
        $('#addActivityModal').modal('hide');

        if (window.swal) {
            swal("¡Éxito!", e.detail.message, { icon: "success" });
        } else {
            alert(e.detail.message);
        }

    });

//Funcion para  cerrar el modal despues de editar recursos multimedia, actualizar la tabla y mostrar el mensaje de exito
document.addEventListener("submit", function (e) {
    if (e.target && e.target.id === "EditResourceForm") {
        e.preventDefault();

        let form = e.target;
        let formData = new FormData(form);
        let table = $("#multimedia-table").DataTable();

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                $("#resourcesActivityModalEdit").modal("hide");
                swal("¡Éxito!", data.message, "success");
                table.ajax.reload(null, false);
            } else {
                swal("Error", data.error, "error");
            }
        })
        .catch(err => {
            console.error(err);
            swal("Error", "Error en la petición AJAX.", "error");
        });
    }
});


    //Funcion para  cerrar el modal despues de editar actividades, actualizar la tabla y mostrar el mensaje de exito
document.addEventListener("submit", function (e) {
    if (e.target && e.target.id === "EditActivityForm") {
        e.preventDefault();

        let form = e.target;
        let formData = new FormData(form);
        let table = $("#add-activity").DataTable();

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                $("#editActivityModal").modal("hide");
                swal("¡Éxito!", data.message, "success");
                table.ajax.reload(null, false);
            } else {
                swal("Error", data.error, "error");
            }
        })
        .catch(err => {
            console.error(err);
            swal("Error", "Error en la petición AJAX.", "error");
        });
    }
});

    //Funcion para cerrar el modal despues de editar los miembros de proyecto,
    //  actualizar la tabla de los proyectos con el nombre de los miembros y mostrar el mensaje de exito
    document.addEventListener("DOMContentLoaded", function() {
        var form = document.getElementById("addProjectMembersForm");
        if (form !== null) {
            form.addEventListener("submit", function (e) {
                e.preventDefault();

                let form = e.target;
                let formData = new FormData(form);
                let table = $("#add-row-project").DataTable();


                fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") }
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            //cerrar modal si todo salió bien
                            $("#addModalProjectMembers").modal("hide");
                            //  mostrar mensaje de éxito
                            swal("¡Éxito!", data.message, "success");

                            table.ajax.reload(null, false);
                        } else {
                            //mostrar error sin cerrar modal
                            swal("Error", data.error, "error");
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        swal("Error", "Error en la petición AJAX.", "error");
                    });
            });
        }
    });
    //Funcion para cerrar el modal despues de agregar recursos multumedia, recargar la tabla y mostrar un mensaje
    document.addEventListener("DOMContentLoaded", function() {
        var form = document.getElementById("addActivityResourcesForm");
        if (form !== null) {
            form.addEventListener("submit", function (e) {
                e.preventDefault();

                let form = e.target;
                let formData = new FormData(form);
                let table = $("#sources-table").DataTable();


                fetch(form.action, {
                    method: "POST",
                    body: formData,
                    headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") }
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            //cerrar modal si todo salió bien
                            $("#resourcesActivityModal").modal("hide");
                            //  mostrar mensaje de éxito
                            swal("¡Éxito!", data.message, "success");

                            table.ajax.reload(null, false);
                        } else {
                            //mostrar error sin cerrar modal
                            swal("Error", data.error, "error");
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        swal("Error", "Error en la petición AJAX.", "error");
                    });
            });
        }
    });

})()

function loadForm(projectId) {
    $.ajax({
        type: "GET",
        url: "/projects/" + projectId + "/edit",
        success: function (data) {
            $("#modal-body-project-edit").html(data);
        },
        error: function () {
            $("#modal-body-project-edit").html("<p>Error al cargar el formulario.</p>");
        }
    });
}

function formEditActivity(activityId) {
    $.ajax({
        type: "GET",
        url: "/activities/" + activityId + "/edit",
        success: function (data) {
            $("#modal-body-activity-edit").html(data);
        },
        error: function () {
            $("#modal-body-activity-edit").html("<p>Error al cargar el formulario.</p>");
        }
    })
}


function formEditResource(resourceId) {
    $.ajax({
        type: "GET",
        url: "/activity_resources/" + resourceId + "/edit",
        success: function (data) {
            $("#modal-body-resource-edit").html(data);
        },
        error: function () {
            $("#modal-body-resource-edit").html("<p>Error al cargar el formulario.</p>");
        }
    })
}

function tableDetailResource(resourceId) {
    $.ajax({
        type: "GET",
        url: "/activity_resources/" + resourceId + "/detail",
        success: function (data) {
            $("#modal-body-detail-resource").html(data);
        },
        error: function () {
            $("#modal-body-detail-resource").html("<h3>Error al cargar los datos.</h3>");
        }
    })
}