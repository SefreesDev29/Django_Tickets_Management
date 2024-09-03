$(function () {
    var today = moment().format('YYYY-MM-DD');
    var args = {};

    $('input[name="date_birthday"]').attr('max', today);

    $('input[name="date_birthday"]').on('change', function() {
        var selectedDate = $(this).val();
        if (moment(selectedDate).isAfter(today)) {
            args = {
                'title' : 'Alerta!',
                'icon' : 'warning',
                'msg' : 'La fecha de nacimiento no puede ser futura.',
                'timer' : 3000
            }
            alert_message(args);
            $(this).val(''); 
        }
    });
});

