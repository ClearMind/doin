$("#menu").find("a").each(function () {
    if ($(this).attr("href") == window.location.pathname + window.location.search)
        $(this).parent("li").addClass("current");
});

$("div.form td.required input").each(function () {
    $(this).bind('keyup', function () {
        if ($(this).val() != "") {
            $(this).css({"background": "#afee95"});
        } else {
            $(this).css({"background": "#ffd1cf"});
        }
    });
    if ($(this).val() != "") {
        $(this).css({"background": "#afee95"});
    }
});

$("div.form td.required textarea").each(function () {
    $(this).bind('keyup', function () {
        if ($(this).val() != "") {
            $(this).css({"background": "#afee95"});
        } else {
            $(this).css({"background": "#ffd1cf"});
        }
    });
    if ($(this).val() != "") {
        $(this).css({"background": "#afee95"});
    }
});


$("div.form td.required select").each(function () {
    $(this).bind('change', function () {
        if ($(this).val() != "") {
            $(this).css({"background": "#afee95"});
        } else {
            $(this).css({"background": "#ffd1cf"});
        }
    });
    if ($(this).val() != "") {
        $(this).css({"background": "#afee95"});
    }
});


$("#with_qualification").find("select").bind("change", function () {
    var ed = $("#expiration_date");
    if ($(this).val() != "") {
        ed.addClass("required");
    } else {
        ed.removeClass("required");
    }
});

$('input[name="group1"]').on("change", function () {
    var tf = $(".territory_field");
    var of = $(".organization_field");
    var value = $(this).filter(":checked").val();
    if (value == 0) {
        tf.show();
        tf.find("input, select").closest("td").addClass("required");
        of.hide();
        of.find("input, select").val("");
        of.find("input, select").closest("td").removeClass("required");
    } else {
        of.show();
        of.find("input, select").closest("td").addClass("required");
        tf.hide();
        tf.find("input, select").val("");
        tf.find("input, select").closest("td").removeClass("required");
    }
});

var radio = $('input[type="radio"]:checked');
if (radio.val() == "1") {
    radio.trigger('change');
}

$.datepicker.setDefaults({
    closeText: 'Закрыть',
    prevText: '&#x3c;Пред',
    nextText: 'След&#x3e;',
    currentText: 'Сегодня',
    monthNames: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
    monthNamesShort: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
        'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
    dayNames: ['воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота'],
    dayNamesShort: ['вск', 'пнд', 'втр', 'срд', 'чтв', 'птн', 'сбт'],
    dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
    weekHeader: 'Нед',
    dateFormat: 'dd.mm.yy',
    changeYear: true,
    firstDay: 1,
    isRTL: false,
    showMonthAfterYear: false,
    yearSuffix: ''});

$('#id_expiration_date').datepicker();
$('#id_birth_date').datepicker();
$('#id_post_date').datepicker();
$('#attestation_date').datepicker();
$('#order_date').datepicker();
$('#id_fromdate').datepicker();
$('#id_todate').datepicker();

$('a#print').on('click', function (e) {
    e.preventDefault();
    window.print();
});

var ase = $('#add_second_education');
$('.second').hide();
ase.on('click', function (e) {
    e.preventDefault();
    var s = $('.second');
    if ($(this).data("hidden") == 1) {
        s.show();
        $(this).text('Удалить второе образование');
        $(this).data('hidden', 0);
    } else {
        s.hide();
        var si = $('.second input[type="text"]');
        si.val('');
        si.attr('value', '');
        $(this).text('Добавить второе образование');
        $(this).data('hidden', 1);
    }
});

if ($('input[name="edu2_id"]').length) {
    ase.trigger("click");
}

$('a.remote').on('click', function (e) {
    e.preventDefault();
    var ref = $(this).attr('href');

    var td = $(this).parent();
    var span = td.find('span');

    var flow_td = td.prev();
    var self = $(this);
    var spinner = self.next('img.spinner');

    $.ajax(ref, {
        type: 'POST',
        data: {
            rid: $(this).data('rid')
        },
        beforeSend: function () {
            spinner.show();
        },
        complete: function () {
            spinner.hide();
        },
        success: function (data) {
            span.text(data.status);
            span.addClass('changed');
            flow_td.find('ol').append('<li>' + data.date + ' <emph>' + data.status + '</emph></li>');
            self.hide();
        }
    });
});

var more = $('a#more');
more.on('click', function (e) {
    e.preventDefault();
    $(this).parents('table').find('tr').removeClass('hidden');
    $(this).parents('tr').hide();
});

var tdg = $('td.grade');
tdg.on('click', function (e) {
    e.preventDefault();
    var i = $(this).find('input');
    i.focus();
});

tdg.on('dblclick', function (e) {
    e.preventDefault();
    var i = $(this).find('input');
    i.select();
});

tdg.find('input').on('change', function () {
    $(this).addClass('changed');
    $('#changes').text('Имеются несохраненные данные.');
    $('#changes+a').show();
});

$('#save-grades').on('click', function (e) {
    var ref = $(this).attr('href');
    e.preventDefault();
    var inputs = $('td.grade input.changed');
    var data = Object();
    var self = $(this);

    var spinner = $('.spinner');
    inputs.each(function (index) {
        var id = $(this).data('id');
        var stage = $(this).data('stage');
        var value = $(this).val();
        data[index] = {
            'id': id,
            'stage': stage,
            'value': Number(value.replace(',', '.'))
        }
    });

    $.ajax(ref, {
        type: 'POST',
        data: {
            'data': JSON.stringify(data)
        },
        beforeSend: function () {
            spinner.show();
        },
        complete: function () {
            spinner.hide();
        },
        success: function () {
            inputs.removeClass('changed');
            self.hide();
            $('#changes').text('Все данные сохранены.');
        }
    });
});

var sc = $('select.chosen');
if (sc && sc.length > 0) {
    sc.chosen({
        placeholder_text: 'Выберите'
    });
}

var acd = $('#id_achievements, #id_degrees');
if (acd && acd.length > 0) {
    acd.chosen({
        placeholder_text: 'Выберите'
    });
}

var dt = $('table.data');
if (dt && dt.length > 0) {
    jQuery.extend(jQuery.fn.dataTableExt.oSort, {
        "num-html-pre": function (a) {
            var x = a.replace(/<.*?>/g, "");
            return parseFloat(x);
        },

        "num-html-asc": function (a, b) {
            return ((a < b) ? -1 : ((a > b) ? 1 : 0));
        },

        "num-html-desc": function (a, b) {
            return ((a < b) ? 1 : ((a > b) ? -1 : 0));
        }
    });

    dt.dataTable({
        "bLengthChange": false,
        "oLanguage": {
            "sProcessing": "Подождите...",
            "sLengthMenu": "Показать _MENU_ записей",
            "sZeroRecords": "Записи отсутствуют.",
            "sInfo": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "sInfoEmpty": "Записи с 0 до 0 из 0 записей",
            "sInfoFiltered": "(отфильтровано из _MAX_ записей)",
            "sInfoPostFix": "",
            "sSearch": "Поиск:",
            "sUrl": "",
            "oPaginate": {
                "sFirst": "Первая",
                "sPrevious": "Предыдущая",
                "sNext": "Следующая",
                "sLast": "Последняя"
            }
        },
        'aoColumns': [
            {'sSortDataType': 'dom-text', 'sType': 'num-html'},
            {'sSortDataType': 'dom-text'},
            {'sSortDataType': 'dom-text'},
            {'sSortDataType': 'dom-text'},
            {'sSortDataType': 'dom-text'},
            {'sSortDataType': 'dom-text'}
        ]
    });
}

var edt = $('table.experts');
if (edt && edt.length > 0) {
    jQuery.extend(jQuery.fn.dataTableExt.oSort, {
        "num-html-pre": function (a) {
            var x = a.replace(/<.*?>/g, "");
            return parseFloat(x);
        },

        "num-html-asc": function (a, b) {
            return ((a < b) ? -1 : ((a > b) ? 1 : 0));
        },

        "num-html-desc": function (a, b) {
            return ((a < b) ? 1 : ((a > b) ? -1 : 0));
        }
    });

    edt.dataTable({
        "bLengthChange": false,
        "oLanguage": {
            "sProcessing": "Подождите...",
            "sLengthMenu": "Показать _MENU_ записей",
            "sZeroRecords": "Записи отсутствуют.",
            "sInfo": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "sInfoEmpty": "Записи с 0 до 0 из 0 записей",
            "sInfoFiltered": "(отфильтровано из _MAX_ записей)",
            "sInfoPostFix": "",
            "sSearch": "Поиск:",
            "sUrl": "",
            "oPaginate": {
                "sFirst": "Первая",
                "sPrevious": "Предыдущая",
                "sNext": "Следующая",
                "sLast": "Последняя"
            }
        },
        'aoColumns': [
            {'sSortDataType': 'dom-text'},
            {'sSortDataType': 'dom-text', 'sType': 'num-html'},
            {'sSortDataType': 'dom-text'}
        ]
    });
}

$('#order-print').bind('click', function (e) {
    var self = $(this);
    e.preventDefault();

    var hf = [];
    $('#high-fail').find(':selected').each(function () {
        hf.push($(this).val());
    });

    var ff = [];
    $('#first-fail').find(':selected').each(function () {
        ff.push($(this).val());
    });

    var cf = [];
    $('confirm-fail').find(':selected').each(function () {
        cf.push($(this).val());
    });

    $.ajax('/attestation/order/', {
        async: true,
        type: 'post',
        data: {
            'high-fail': hf,
            'first-fail': ff,
            'confirm-fail': cf
        },
        success: function (data, status, xhr) {
            if (data[0] != '/') {
                console.log(data);
            } else {
                $('#frame').attr('src', data);
            }
        },
        beforeSend: function () {
            self.attr('disabled', 'disabled');
            $('.spinner').show();
        },
        complete: function () {
            self.removeAttr('disabled');
            $('.spinner').hide();
        }
    });
});

$('#addit-print').bind('click', function (e) {
    var self = $(this);
    e.preventDefault();

    var hf = [];
    $('#high-fail').find(':selected').each(function () {
        hf.push($(this).val());
    });

    var ff = [];
    $('#first-fail').find(':selected').each(function () {
        ff.push($(this).val());
    });

    var cf = [];
    $('confirm-fail').find(':selected').each(function () {
        cf.push($(this).val());
    });

    $.ajax('/attestation/addition/', {
        async: true,
        type: 'post',
        data: {
            'high-fail': hf,
            'first-fail': ff,
            'confirm-fail': cf
        },
        success: function (data, status, xhr) {
            if (data[0] != '/') {
                console.log(data);
            } else {
                $('#frame').attr('src', data);
            }
        },
        beforeSend: function () {
            self.attr('disabled', 'disabled');
            $('.spinner').show();
        },
        complete: function () {
            self.removeAttr('disabled');
            $('.spinner').hide();
        }
    });
});