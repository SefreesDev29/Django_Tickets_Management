function get_datenow(format){
    return new moment().format(format);
}
var input_daterange;
var accessusers = {
    parameters : {
        action: 'searchdata',
        start_date : get_datenow('YYYY-MM-DD'),
        end_date : get_datenow('YYYY-MM-DD')
    },
    details: [],
    initTable: function () {
        return $('#data').DataTable({
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
            data: this.details,
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
                    title: 'Reporte de Accesos de Usuarios',
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
                        doc.content[1].table.widths = ['10%', '20%', '28%', '12%', '15%', '15%'];
                        doc.content[1].margin = [0, 5, 0, 0];
                        doc.content[1].layout = {};
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: get_datenow('DD/MM/YYYY')}]
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
            columns: [
                {"data": "id"},
                {"data": "user.username"},
                {"data": "user.full_name"},
                {"data": "is_success"},
                {"data": "timestamp"},
                {"data": "ip_address"}, 
                {"data": "user_agent"}, 
                {"data": "id"},
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
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var html = '';
                        if(row.is_success)
                        {
                            html += '<span class="badge badge-success">Exitoso</span> ';
                        }else{
                            html += '<span class="badge badge-danger">Fallido</span> ';
                        }
                        return html;
                    }
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
                        var button = '<a href="/config/access/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat btn-custom-icon" data-toggle="tooltip" title="Eliminar Registro"><i class="fas fa-trash-alt"></i></a>';
                        return button;
                    }
                }
            ],
            initComplete: function (settings, json) {
                this.api().buttons().container().appendTo('#data_wrapper .col-md-6:eq(0)');
                $(this.api().table().header()).css('background-color', '#ADD8E6');
                $("#data").show();
                $('[data-toggle="tooltip"]').tooltip();
            }
        });
    },
    list: function () {
        var table = this.initTable(); 
    },
};

$(function () {
    input_daterange = $('input[name="date_range"]');
    input_daterange.daterangepicker({
        languaje: 'auto',
        startDate: new Date(),
        locale : {
            format: 'YYYY-MM-DD',
            applyLabel: 'Aplicar',
            cancelLabel: 'Cancelar',
            daysOfWeek: ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'],
            monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        }
    });

    function search_data() {
        $.ajax({
            type: 'POST',
            url: pathname,
            data: accessusers.parameters,
            headers: {
                'X-CSRFToken': csrftoken 
            },
            beforeSend: function() {

            }
        }).done(function (data) {
            accessusers.details = data;
        }).fail(function (jqXHR, textStatus, errorThrown) {
            dict_error['msg'] = 'Error interno. ' + jqXHR.statusText + '.';
            alert_message(dict_error);
        }).always(function (data) {
            setTimeout(function() {
                accessusers.list();
            }, 300); 
        });
    }

    search_data();

    $('.btnSearch').on('click', function () {
        accessusers.parameters.start_date = input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD');
        accessusers.parameters.end_date = input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD');
        search_data();
        $(this).blur();
    });

    $('.btnSearchAll').on('click', function () {
        accessusers.parameters.start_date = '';
        accessusers.parameters.end_date = '';
        search_data();
        $(this).blur();
    });
});

