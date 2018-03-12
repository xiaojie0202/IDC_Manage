$(function () {
    init_menu();
    createIpAddressForm();
    createPortInfoForm();
});

function init_menu() {
    var dcname = $('#dcname-title').html();
    var idcname = $('#idcname-title').html();
    $('#showye').removeClass('active');
    $("a[href='#subPages']").removeClass('collapsed').addClass('active').attr("aria-expanded", true);
    $('#subPages').addClass('in').attr("aria-expanded", true);
    $("a[href='#" + dcname).removeClass('collapsed').addClass('active').attr("aria-expanded", true);
    $("#" + dcname).addClass('in').attr("aria-expanded", true);
    $("a[href='#" + idcname).removeClass('collapsed').addClass('active').attr("aria-expanded", true);
    $("#" + dcname + idcname).addClass('in').attr("aria-expanded", true);
    $('#equipmen-info' + dcname + idcname).addClass('active');
}


//增加IP地址信息
function createIpAddressForm() {
    $('#create_ipaddress_form').click(function () {
        var ipTall = $('#id_ip-TOTAL_FORMS');
        var formcount = parseInt(ipTall.val());
        var setval = formcount + 1;
        ipTall.val(setval);
        $('#ipaddress_panel').append(
            '<div class="form-inline"><div class="form-group"><span>IPV4地址#' + setval + '：</span></div>\n' +
            '<div class="form-group"><label for="id_ip-' + formcount + '-tags">IP标签:</label>\n' +
            '<input type="text" name="ip-' + formcount + '-tags" maxlength="64" id="id_ip-' + formcount + '-tags" class="form-control"></div>\n' +
            '<div class="form-group"><label for="id_ip-' + formcount + '-ipaddre">IP地址:</label>\n' +
            '<input type="text" name="ip-' + formcount + '-ipaddre" id="id_ip-' + formcount + '-ipaddre" class="form-control"></div>\n' +
            '<div class="form-group"><label for="id_ip-' + formcount + '-gateway">网关地址:</label>\n' +
            '<input type="text" name="ip-' + formcount + '-gateway" id="id_ip-' + formcount + '-gateway" class="form-control"></div>\n' +
            '<div class="form-group"><label for="id_ip-' + formcount + '-netmask">子网掩码:</label>\n' +
            '<input type="text" name="ip-' + formcount + '-netmask" id="id_ip-' + formcount + '-netmask" class="form-control"></div>\n' +
            '<input type="hidden" name="ip-' + formcount + '-id" id="id_ip-' + formcount + '-id"></div>'
        )
    });
}

//增加互联信息
function createPortInfoForm() {
    $('#create_portinfo_forms').click(function () {
        var portTall = $('#id_port-TOTAL_FORMS');
        var formcount = parseInt(portTall.val());
        var setval = formcount + 1;
        portTall.val(setval);
        var dcOption = '';
        $.ajax({
            url: '/selectinput/get_dc/',
            type: 'POST',
            headers: {'X-CSRFToken': $.cookie('csrftoken')},
            data: {id: 1},
            dataType: 'JSON',
            success: function (data) {
                $.each(data.data, function (item, data) {
                    dcOption += '<option value="' + data[0] + '">' + data[1] + '</option>'
                });
                $('#portinfo_panel').append(
                    '<div class="form-inline">\n' +
                    '<div class="form-group col-md-1"><span>互联信息#' + setval + '：</span></div>\n' +
                    '<div class="form-group"><label for="id_port-' + formcount + '-self_equipment_port">本端端口号:</label>\n' +
                    '<input type="text" name="port-' + formcount + '-self_equipment_port" class="form-control" maxlength="32" id="id_port-' + formcount + '-self_equipment_port"></div>\n' +
                    '<div class="form-group"><label for="id_port-' + formcount + '-up_equipment">上联设备:</label>\n' +
                    '<select name="port-' + formcount + '-dcname" class="form-control" id="id_port-' + formcount + '-dcname" onchange="getDcChange($(this))">' + dcOption + '</select>' +
                    '<select name="port-' + formcount + '-idcname" class="form-control" id="id_port-' + formcount + '-idcname" onchange="getIdcChange($(this))"></select>\n' +
                    '<select name="port-' + formcount + '-cabinet" class="form-control" id="id_port-' + formcount + '-cabinet" onchange="getCabinetChange($(this))"></select>\n' +
                    '<select name="port-' + formcount + '-up_equipment" class="form-control" id="id_port-' + formcount + '-up_equipment">\n' +
                    '<option value="" selected="">---------</option></select></div>\n' +
                    '<div class="form-group"><label for="id_port-' + formcount + '-up_equipment_port">上联端口号:</label>\n' +
                    '<input type="text" name="port-' + formcount + '-up_equipment_port" class="form-control" maxlength="32" id="id_port-' + formcount + '-up_equipment_port"></div>\n' +
                    '<input type="hidden" name="port-' + formcount + '-id" id="id_port-' + formcount + '-id">\n' +
                    '</div>'
                );

            }
        });

    })
}

function getDcChange(a) {
    var thisSlecet = a;
    var data = {id: thisSlecet.val()};
    $.ajax({
        url: '/selectinput/get_idc/',
        type: 'POST',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: data,
        dataType: 'JSON',
        success: function (data) {
            thisSlecet.next().html('');
            $.each(data.data, function (item, data) {
                thisSlecet.next().append('<option value="' + data[0] + '">' + data[1] + '</option>')
            })
        }
    });

}

function getIdcChange(a) {
    var thisSlecet = a;
    var data = {id: thisSlecet.val()};
    $.ajax({
        url: '/selectinput/get_cabinet/',
        type: 'POST',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: data,
        dataType: 'JSON',
        success: function (data) {
            thisSlecet.next().html('');
            $.each(data.data, function (item, data) {
                thisSlecet.next().append('<option value="' + data[0] + '">' + data[1] + '</option>')
            })
        }
    });
}

function getCabinetChange(a) {
    var thisSlecet = a;
    var data = {id: thisSlecet.val()};
    $.ajax({
        url: '/selectinput/get_equipment/',
        type: 'POST',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: data,
        dataType: 'JSON',
        success: function (data) {
            thisSlecet.next().html('');
            $.each(data.data, function (item, data) {
                thisSlecet.next().append('<option value="' + data[0] + '">' + data[1] + '-' + data[2] + ':' + data[3] + '</option>')
            })
        }
    });
}