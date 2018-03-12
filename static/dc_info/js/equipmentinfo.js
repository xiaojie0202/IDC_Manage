$(function () {
    init_menu();
    selectCabinet();
    selectAllCabinet();
    showRemoveCabinetInfo();
    bulkRemoveCabinetAjax();
    affirmRemoveCabinet();
    showNetworkEquipmentPortInfo();
});

//确认删除按钮事件处理
function affirmRemoveCabinet() {
    $('#remove_equipment_btn').click(function () {
        var equipment_id = {};
        var value_td = $('#show_remove_equipment').find('.get_equipment_id_td');
        $.each(value_td, function (item, date) {
            equipment_id[item] = [parseInt(value_td.eq(item).html())];
        });
        $.ajax({
            url: '/delete_equipment/',
            type: 'POST',
            headers: {'X-CSRFToken': $.cookie('csrftoken')},
            data: equipment_id,
            dataType: 'JSON',
            success: function (data) {
                if (data.status) {
                    $('#myModal').modal('hide');
                    $('#show_remove_cabinet').html("");
                    $.each(data.delete_id, function (item, date) {
                        $('#select_equipment_' + date).parent().parent().remove()
                    });
                    $('#remove_equipment_list_str').html('删除成功：' + data.delete_list).show()
                } else {
                    alert('删除失败')
                }
            }
        })
    })
}

//删除机柜按钮事件处理
function showRemoveCabinetInfo() {
    var removeBtn = $('#equipmentinfo').find('button');
    removeBtn.on('click', function () {
        var equipment_id = $(this).parent().parent().find('input').val();
        var equipment_cabinet = $('#equipment_cabinet_' + equipment_id).html();
        var equipment_place = $('#equipment_place_' + equipment_id).html();
        var equipment_manufacturers = $('#equipment_manufacturers_' + equipment_id).html();
        var equipment_model = $('#equipment_model_' + equipment_id).html();
        var equipment_u = $('#equipment_u_' + equipment_id).html();
        var equipment_sn = $('#equipment_sn_' + equipment_id).html();
        var equipment_customet = $('#equipment_customet_' + equipment_id).html();
        var equipment_ip = $('#equipment_ip_' + equipment_id)[0].outerHTML;
        $('#show_remove_equipment').html(
            "<tr class=\"danger\"><td class=\"get_equipment_id_td\">" + equipment_id +
            "</td><td>" + equipment_cabinet +
            "</td><td>" + equipment_place +
            "</td><td>" + equipment_manufacturers +
            "</td><td>" + equipment_model +
            "</td><td>" + equipment_u +
            "</td><td>" + equipment_sn +
            "</td><td>" + equipment_customet +
            "</td><td>" + equipment_ip +
            "</td></tr>"
        );
        $('#remove_equipment_div').show();
        $('#network_port_info_div').hide();
        $('#remove_equipment_btn').show();
        $('#myModal').modal('show');
    })
}

//批量删除机柜按钮事件处理
function bulkRemoveCabinetAjax() {
    var showmotai = false;
    $('#bulk_remove_equipment').click(function () {
        var selectIput = $('#equipmentinfo').find('input');
        var show_remove_cabinet = $('#show_remove_equipment');
        show_remove_cabinet.html("");
        for (var i = 0; i < selectIput.length; i++) {
            if (selectIput.eq(i).is(':checked')) {
                showmotai = true;
                var equipment_id = selectIput.eq(i).attr('value');
                var equipment_cabinet = $('#equipment_cabinet_' + equipment_id).html();
                var equipment_place = $('#equipment_place_' + equipment_id).html();
                var equipment_manufacturers = $('#equipment_manufacturers_' + equipment_id).html();
                var equipment_model = $('#equipment_model_' + equipment_id).html();
                var equipment_u = $('#equipment_u_' + equipment_id).html();
                var equipment_sn = $('#equipment_sn_' + equipment_id).html();
                var equipment_customet = $('#equipment_customet_' + equipment_id).html();
                var equipment_ip = $('#equipment_ip_' + equipment_id)[0].outerHTML;
                show_remove_cabinet.append(
                    "<tr class=\"danger\"><td class=\"get_equipment_id_td\">" + equipment_id +
                    "</td><td>" + equipment_cabinet +
                    "</td><td>" + equipment_place +
                    "</td><td>" + equipment_manufacturers +
                    "</td><td>" + equipment_model +
                    "</td><td>" + equipment_u +
                    "</td><td>" + equipment_sn +
                    "</td><td>" + equipment_customet +
                    "</td><td>" + equipment_ip +
                    "</td></tr>"
                );
            }
        }
        if (showmotai) {
            $('#remove_equipment_div').show();
            $('#network_port_info_div').hide();
            $('#remove_equipment_btn').show();
            $('#myModal').modal('show');
        } else {
            $('#remove_equipment_seccuse').show();
        }
    })
}

// 初始化菜单部分
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

//选中全部的单选框按钮
function selectAllCabinet() {
    $('#thead_checkbox').click(function () {
        var selectIput = $('#equipmentinfo').find('input');
        if ($(this).is(':checked')) {
            selectIput.prop('checked', true);
            selectIput.parent().parent().addClass('info');
            $('#equipmentinfo').find('table').find('tr').addClass('info')
        } else {
            selectIput.prop('checked', false);
            selectIput.parent().parent().removeClass('info');
            $('#equipmentinfo').find('table').find('tr').removeClass('info')
        }
    });
}

//单选按钮事件处理
function selectCabinet() {
    var selectIput = $('#equipmentinfo').find('input');
    selectIput.click(function () {
        if ($(this).is(':checked')) {
            $(this).prop('checked', true).parent().parent().addClass('info');
            $('#equipment_ip_' + $(this).val()).find('tr').addClass('info');
            $('#equipment_portinfo_' + $(this).val()).find('tr').addClass('info');
        } else {
            $(this).prop('checked', false).parent().parent().removeClass('info');
            $('#equipment_ip_' + $(this).val()).find('tr').removeClass('info');
            $('#equipment_portinfo_' + $(this).val()).find('tr').removeClass('info');
        }
    })
}

//查看网络设备互联端口信息
function showNetworkEquipmentPortInfo() {
    $('.show_portinfo').click(function () {
        equipment_id = $(this).parent().parent().find('input').val();
        $.ajax({
            url: '/show_network_port/',
            type: 'POST',
            headers: {'X-CSRFToken': $.cookie('csrftoken')},
            data: {id: equipment_id},
            dataType: 'JSON',
            success: function (data) {
                var portBody = $('#show_network_port_info_tbody');
                portBody.html('')
                $.each(data.data, function (item, data) {
                    //['102-A01', 'H3CS9804', '23412AS1D32123AS1D', 'G0/0/1', '102-A01', 'HUAWEI S9306', '4154156151351', 'T0/0/1']
                    portBody.append(
                        "<tr><td>" + data[0] +
                        "</td><td>" + data[1] +
                        "</td><td>" + data[2] +
                        "</td><td>" + data[3] +
                        "</td><td>-----</td><td>" + data[4] +
                        "</td><td>" + data[5] +
                        "</td><td>" + data[6] +
                        "</td><td>" + data[7] +
                        "</td></tr>"
                    );
                    $('#remove_equipment_div').hide();
                    $('#network_port_info_div').show();
                    $('#remove_equipment_btn').hide();
                    $('#myModal').modal('show');
                })
            }
        });

        //$('#motai_conter').html()
    })
}