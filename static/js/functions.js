var dict_error = {
    'title' : 'Error!',
    'icon' : 'error',
    'timer' : 5000
}

const defaultArgs = (args) => {
    if (!args.hasOwnProperty('theme')) {
        args['theme'] = 'material';
    }
    if (!args.hasOwnProperty('type')) {
        args['type'] = 'blue';
    }
    if (!args.hasOwnProperty('title')) {
        args['title'] = 'Notificación';
    }
    if (!args.hasOwnProperty('icon')) {
        args['icon'] = 'fa fa-info';
    }
    if (!args.hasOwnProperty('content')) {
        args['content'] = '¿Estás seguro de realizar la siguiente acción?';
    }
    if (!args.hasOwnProperty('columnClass')) {
        args['columnClass'] = 'small';
    }
    return args;
};

function alert_message(args) {
    var html = '';
    var confirmButtonColor = '';

    if (!args.hasOwnProperty('title')) {
        args['title'] = 'Genial!';
    }
    if (!args.hasOwnProperty('icon')) {
        args['icon'] = 'success';
    }
    if (!args.hasOwnProperty('msg')) {
        args['msg'] = 'Operación realizada exitósamente.';
    }
    if (!args.hasOwnProperty('timer')) {
        args['timer'] = 1500;
    }
    if (!args.hasOwnProperty('textbtn')) {
        args['textbtn'] = 'Está bien';
    }

    if (typeof (args.msg) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(args.msg, function (key, value) {
            html += '<li>' + value + '</li>';
        });
        html += '</ul>';
    }
    else{
        try{
            html = '<p>'+args.msg+'</p>';
            const errorobj = JSON.parse(args.msg.replace(/'/g, '"'));
            if (typeof (errorobj) === 'object'){
                html = '<ul style="text-align: left;">';
                $.each(errorobj, function(key, value) {
                    html += '<li>' + value + '</li>';
                });
                html += '</ul>';
            }
        } catch (e) {
            html = '<p>'+args.msg+'</p>';
        }
    }
    Swal.fire({
        title: args.title,
        html: html,
        timer: args.timer,
        icon: args.icon,
        confirmButtonText: args.textbtn,
        heightAuto: false,
        willClose: () => {
            if (args.hasOwnProperty('redirect')) {
                location.href = args.redirect;
            }
        }
    });
    
    if (args.icon == 'success'){
        confirmButtonColor = '#28a745';  
    } else if (args.icon == 'info'){
        confirmButtonColor = '#17a2b8';  
    } else if (args.icon == 'error'){
        confirmButtonColor = '#dc3545';  
    } else{
        confirmButtonColor = '#ffc107';  
    }

    const swalButton = document.querySelector('.swal2-confirm');
    swalButton.style.backgroundColor = confirmButtonColor;
    swalButton.style.borderColor = confirmButtonColor;
    swalButton.style.outline = 'none';
    swalButton.style.boxShadow = `0 0 0 2px ${confirmButtonColor}`;
}

function alert_confirm(args) {
    var args = defaultArgs(args);

    $.confirm({
        theme: args.theme,
        type: args.type,
        title: args.title,
        icon: args.icon,
        content: args.content,
        columnClass: args.columnClass,
        typeAnimated: true,
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'Si',
                btnClass: 'btn-primary',
                action: function () {
                    if (args.hasOwnProperty('yesaction')) {
                        args.yesaction();
                    } 
                }
            },
            danger: {
                text: 'No',
                btnClass: 'btn-red',
                action: function () {
                    if (args.hasOwnProperty('notaction')) {
                        args.notaction();
                    }
                }
            },
        }
    })
}

function submit_with_ajax(args) {
    var args = defaultArgs(args);
    $.confirm({
        theme: args.theme,
        type: args.type,
        title: args.title,
        icon: args.icon,
        content: args.content,
        columnClass: args.columnClass,
        typeAnimated: true,
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: 'Si',
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: args.url,
                        type: 'POST',
                        data: args.parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                        headers: {
                            'X-CSRFToken': csrftoken 
                        },
                        beforeSend: function (){
                            $.LoadingOverlay('show', {
                                image       : '',
                                fontawesome : 'fas fa-spinner fa-pulse',
                                custom : $('<div>', {
                                    'class': 'loading',
                                    'text': 'Cargando...'
                                })
                            });
                        }
                    }).done(function (data) {
                        $.LoadingOverlay('hide');
                        if (!data.hasOwnProperty('error')) {
                            if (args.hasOwnProperty('success')) {
                                args.success(data);
                            } 
                            return false;
                        }
                        dict_error['msg'] = data.error;
                        alert_message(dict_error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        $.LoadingOverlay('hide');
                        dict_error['msg'] = 'Error interno. ' + jqXHR.statusText + '.';
                        alert_message(dict_error);
                    }).always(function (data) {
                        args.btnsubmit.prop('disabled', false);
                    });
                }
            },
            danger: {
                text: 'No',
                btnClass: 'btn-red',
                action: function () {
                    args.btnsubmit.prop('disabled', false);
                }
            },
        }
    })
}