var tblProducts;
var tblSearchProducts;
var args = {};

var purchases = {
    items: {
        driv: '',
        date_joined: '',
        products: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "cant"},
                {"data": "serieinicial"},
                {"data": "seriefinal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat btn-custom-icon" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span">' + data + '</span>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="serieinicial" value="' + row.serieinicial + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="seriefinal" value="' + row.seriefinal + '">';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 100000,
                    step: 1
                });
            },
            initComplete: function (settings, json) {

            }
        });
        // console.clear();
        // console.log(this.items);
        // console.log(this.get_ids());
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '<br>' +
        '<b>Precio:</b> ' + repo.price + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    var action = $('input[name="action"]').val();
    if (action === 'add') {
        purchases.list();
        $('#loading-indicator').hide();
        $('#main-form').show();
    } else if (action === 'edit') {
        $.ajax({
            type: 'GET',
            url: pathname,
            data: {
                action: 'get_details'
            },
            beforeSend: function() {
                $('#loading-indicator').show();
                $('#main-form').hide();
            },
            success: function (response) {
                //$('#tblProducts').DataTable().destroy();
                purchases.items.products = response;
            },
            error: function (error) {
                alert_message({'title' : 'Error!', 'icon' : 'error', 'msg' : error, 'timer': 5000});
            },
            complete: function() {
                $('#loading-indicator').hide();
                $('#main-form').show();
                setTimeout(function() {
                    purchases.list();
                }, 300); 
            }
        });
    }

    var formGroup = document.querySelectorAll('.custom-file-div');
    formGroup.forEach(function(group) {
        var nodes = group.childNodes;
        nodes.forEach(function(node) {
            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() === "Modificar:") {
                node.textContent = '';
            }
        });
    });

    document.getElementById("id_file").addEventListener("change", function() {
        var customLabel = document.getElementById("file-path");
        if (this.files.length>0){
            var fileName = this.files[0].name;
            customLabel.textContent = fileName;
        } else{
            customLabel.textContent = '';
        }
    });

    // Search tickets with autocomplete use select2
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken 
            },
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(purchases.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 0,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.cant = 1;
        data.serieinicial = 1;
        data.seriefinal = 1;
        purchases.add(data);
        $(this).val('').trigger('change.select2');
    });

    // Search Drivers
    $('select[name="driv"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken 
            },
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_drivers'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un nombre',
        minimumInputLength: 0,
    });

    // Show modal to create driver
    $('.btnAddDriver').on('click', function () {
        $('#myModalDriver').modal('show');
    });

    // Clear value fields create driver form
    $('#myModalDriver').on('hidden.bs.modal', function (e) {
        $('#frmDriver').trigger('reset');
    })
    
    // Select or Create driver
    $('#frmDriver').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_driver');
        var btnsubmit = $(this).find('[type="submit"]').first();
        btnsubmit.prop('disabled', true);
        args = {
            'url' : pathname,
            'content' : '¿Estás seguro de crear al siguiente chofer?',
            'parameters' : parameters,
            'btnsubmit' : btnsubmit,
            'success' : function (response) {
                alert_message({});
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="driv"]').append(newOption).trigger('change');
                $('#myModalDriver').modal('hide');
            }
        }
        submit_with_ajax(args);
    });

    // Delete all records ticket of details table
    $('.btnRemoveAll').on('click', function () {
        if (purchases.items.products.length === 0) return false;
        args = {
            'type': 'red',
            'content': '¿Estás seguro de eliminar todos los ítems de tu detalle?',
            'yesaction': function () {
                purchases.items.products = [];
                purchases.list();
            }
        }
        alert_confirm(args);
    });

    // Events cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            args = {
                'type': 'red',
                'content': '¿Estás seguro de eliminar el ítem de tu detalle?',
                'yesaction': function () {
                    purchases.items.products.splice(tr.row, 1);
                    purchases.list();
                }
            }
            alert_confirm(args);
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            purchases.items.products[tr.row].cant = cant;
        })
        .on('change', 'input[name="serieinicial"]', function () {
            console.clear();
            var serieinicial1 = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            purchases.items.products[tr.row].serieinicial = serieinicial1;
        })
        .on('change', 'input[name="seriefinal"]', function () {
            console.clear();
            var seriefinal1 = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            purchases.items.products[tr.row].seriefinal = seriefinal1;
        });
    
    // Event submit create/update purchase
    $('#frmPurchase').on('submit', function (e) {
        e.preventDefault();

        if (purchases.items.products.length === 0) {
            alert_message({'title' : 'Alerta!', 'icon' : 'warning', 
                            'msg' : 'Debe tener al menos un ítem en su detalle de compra.', 'timer': 3000});
            return false;
        }
        purchases.items.date_joined = $('input[name="date_joined"]').val();
        purchases.items.driv = $('select[name="driv"]').val();

        var parameters = new FormData(this);
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('purchases', JSON.stringify(purchases.items));

        // parameters.forEach(function(value, key){
        //     if (key === "file" && value instanceof File) {
        //         console.log(key + ": " + value.name + ", " + value.type + ", " + value.size + " bytes");
        //     } else {
        //         console.log(key + ": " + value);
        //     }
        //  });

        var btnsubmit = $(this).find('[type="submit"]').first();
        btnsubmit.prop('disabled', true);

        args = {
            'url' : pathname,
            'parameters' : parameters,
            'btnsubmit' : btnsubmit,
            'success' : function (response) {
                alert_message({'redirect': '/menu/purchase/list/'});
            }
        }
        submit_with_ajax(args);
    });
});

