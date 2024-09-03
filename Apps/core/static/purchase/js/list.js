var tblPurchase;
var date_now = new moment().format('DD/MM/YYYY');

function format(d) {
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Boleto</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">SerieInicial</th>';
    html += '<th scope="col">SerieFinal</th>';
    html += '</thead>';
    html += '<tbody>';
    $.each(d.det, function (key, value) {
        html+='<tr>'
        html+='<td>'+value.prod.name+'</td>'
        html+='<td>'+value.cant+'</td>'
        html+='<td>'+value.serieinicial+'</td>'
        html+='<td>'+value.seriefinal+'</td>'
        html+='</tr>';
    });
    html += '</tbody>';
    return html;
}

$(function () {
    tblPurchase = $('#data').DataTable({
        paging: true,
        destroy: true,
        deferRender: true,
        ordering: true,
        lengthChange: false,
        searching: true,
        info: true,
        responsive: true,
        autoWidth: false,
        order: [[ 0, "desc" ]],
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
                title: 'Reporte de Compras de Boletos',
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
                    doc.content[1].table.widths = ['5%', '25%', '15%', '20%', '15%', '20%'];
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
            {"data": "id"},
            {"data": "driv.full_name"},
            {"data": "date_joined"},
            {"data": "date_create"},
            {"data": "date_update"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [0],
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
                    var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" title="Ver Detalles"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/menu/purchase/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" title="Editar Registro"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/menu/purchase/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" title="Eliminar Registro"><i class="fas fa-trash-alt"></i></a> ';
                    if (row.file !== '/static/img/FileEmpty.pdf'){
                        buttons += '<a href="'+ row.file + '" class="btn btn-info btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" target="_blank" title="Ver Documento"><i class="fas fa-file-export"></i></a> ';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            tblPurchase.buttons().container().appendTo('#data_wrapper .col-md-6:eq(0)');
            $(this.api().table().header()).css('background-color', '#ADD8E6');
            $("#data").show();
            $('[data-toggle="tooltip"]').tooltip();
        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblPurchase.cell($(this).closest('td, li')).index();
            var data = tblPurchase.row(tr.row).data();

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    headers: {
                        'X-CSRFToken': csrftoken 
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "prod.name"},
                    {"data": "cant"},
                    {"data": "serieinicial"},
                    {"data": "seriefinal"},
                ],
                columnDefs: [
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
                        class: 'text-center'
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#ModalPurchaseDet').modal('show');
        });
});