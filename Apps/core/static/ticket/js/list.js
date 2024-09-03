var date_now = new moment().format('DD/MM/YYYY');
$(function () {
    var table =  $('#data').DataTable({
        paging: true,
        destroy: true,
        deferRender: true,
        ordering: true,
        lengthChange: false,
        searching: true,
        info: true,
        responsive: true,
        autoWidth: false,
        order: [[ 0, "asc" ]],
        buttons: [
            {
                extend: 'copyHtml5',
                text: 'Copiar Tabla <i class="fas fa-file-import"></i>',
                titleAttr: 'Copiar',
                className: 'btn btn-primary btn-flat btn-xs btn-custom-min',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            },
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs btn-custom-min',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                }
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                title: 'Reporte de Boletos',
                className: 'btn btn-danger btn-flat btn-xs btn-custom-min',
                download: 'open',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4, 5]
                },
                customize: function (doc) {
                    doc.styles = {
                        title: {
                            fontSize: 20,
                            bold: true,
                            alignment: 'center'
                        },
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['10%', '25%', '10%', '20%', '15%', '20%'];
                    doc.content[1].margin = [0, 5, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }],
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            headers: {
                'X-CSRFToken': csrftoken 
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "name"},
            {"data": "price"},
            {"data": "date_create"},
            {"data": "user_create.full_name"},
            {"data": "date_update"},
            {"data": "user_update.full_name"},
            {"data": "name"},
        ],
        columnDefs: [
            {
                targets: [0],
                class: 'text-center'
            },
            {
                targets: [-7],
                class: 'text-center'
            },
            {
                targets: [-6],
                class: 'text-center'
            },
            {
                targets: [-5],
                class: 'text-center'
            },
            {
                targets: [-4],
                class: 'text-center'
            },
            {
                targets: [-3],
                class: 'text-center'
            },
            {
                targets: [-2],
                class: 'text-center'
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/menu/ticket/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" title="Editar Registro"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/menu/ticket/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" title="Eliminar Registro"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            table.buttons().container().appendTo('#data_wrapper .col-md-6:eq(0)');
            $(this.api().table().header()).css('background-color', '#ADD8E6');
            $("#data").show();
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
});