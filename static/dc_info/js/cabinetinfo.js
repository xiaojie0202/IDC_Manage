$(function () {
    init_menu();
    showRemoveCabinetInfo();
    selectAllCabinet();
    selectCabinet();
    bulkRemoveCabinetAjax();
    affirmRemoveCabinet();


});

// 初始化菜单
function init_menu() {
    var dcname = $('#dcname-title').html();
    var idcname = $('#idcname-title').html();
    // 初始化菜单部分
    $('#showye').removeClass('active');
    $("a[href='#subPages']").removeClass('collapsed').addClass('active').attr("aria-expanded", true); //展开数据中心信息
    $('#subPages').addClass('in').attr("aria-expanded", true);

    $("a[href='#" + dcname).removeClass('collapsed').addClass('active').attr("aria-expanded", true); //展开数据中心对应菜单
    $("#" + dcname).addClass('in').attr("aria-expanded", true);

    $("a[href='#" + dcname + idcname).removeClass('collapsed').addClass('active').attr("aria-expanded", true); //展开机房菜单
    $("#" + dcname + idcname).addClass('in').attr("aria-expanded", true);
    $('#cabinet-info' + dcname + idcname).addClass('active'); // 激活机柜信息
}

//确认删除按钮事件处理
function affirmRemoveCabinet() {
    $('#remove_cabinet_btn').click(function () {
        var cabinet_id = {};
        var value_td = $('#show_remove_cabinet').find('.get_cabinet_id_td');
        $.each(value_td, function (item, date) {
            cabinet_id[item] = [parseInt(value_td.eq(item).html())];
        });
        $.ajax({
            url: '/delete_cabinet/',
            type: 'POST',
            headers: {'X-CSRFToken': $.cookie('csrftoken')},
            data: cabinet_id,
            dataType: 'JSON',
            success: function (data) {
                if (data.status) {
                    $('#myModal').modal('hide');
                    $('#show_remove_cabinet').html("");
                    $.each(data.delete_id, function (item, date) {
                        $('#select_cabinet_' + date).parent().parent().remove()
                    });
                    $('#remove_cabinet_list_str').html('删除成功：' + data.delete_list).show()
                } else {
                    alert('删除失败')
                }
            }
        })
    })
}

//删除机柜按钮事件处理
function showRemoveCabinetInfo() {
    var dcname = $('#dcname-title').html();
    var idcname = $('#idcname-title').html();
    var removeBtn = $('#cabinet_info').find('button');
    removeBtn.on('click', function () {
        cabinet_id = $(this).parent().parent().find('.action-checkbox').children().first().attr('value');
        cabinet_num = $('#cabinet_number_' + cabinet_id).html();
        customer = $('#cabinet_customer_' + cabinet_id).html();
        $('#show_remove_cabinet').html(
            "<tr class=\"danger\"><td class=\"get_cabinet_id_td\">" + cabinet_id + "</td><td>" + dcname + "</td><td>" + idcname + "</td><td>" + cabinet_num + "</td><td>" + customer + "</td></tr>"
        )
    })
}

//批量删除机柜按钮事件处理
function bulkRemoveCabinetAjax() {
    var showmotai = false;
    var dcname = $('#dcname-title').html();
    var idcname = $('#idcname-title').html();
    $('#bulk_remove_cabinet').click(function () {
        var selectIput = $('#cabinet_info').find('input');
        var show_remove_cabinet = $('#show_remove_cabinet');
        show_remove_cabinet.html("");
        for (var i = 0; i < selectIput.length; i++) {
            if (selectIput.eq(i).is(':checked')) {
                showmotai = true;
                cabinet_id = selectIput.eq(i).attr('value');
                cabinet_num = $('#cabinet_number_' + cabinet_id).html();
                customer = $('#cabinet_customer_' + cabinet_id).html();
                show_remove_cabinet.append(
                    "<tr class=\"danger\"><td class=\"get_cabinet_id_td\">" + cabinet_id + "</td><td>" + dcname + "</td><td>" + idcname + "</td><td>" + cabinet_num + "</td><td>" + customer + "</td></tr>"
                )
            }
        }
        if (showmotai) {
            $('#myModal').modal('show');
        } else {
            $('#remove_cabinet_seccuse').show();
        }
    })
}

//选中全部的单选框按钮
function selectAllCabinet() {
    $('#thead_checkbox').click(function () {
        var selectIput = $('#cabinet_info').find('input');
        if ($(this).is(':checked')) {
            selectIput.prop('checked', true);
            selectIput.parent().parent().addClass('info')
        } else {
            selectIput.prop('checked', false);
            selectIput.parent().parent().removeClass('info')
        }
    });
}

//单选按钮事件处理
function selectCabinet() {
    var selectIput = $('#cabinet_info').find('input');
    selectIput.click(function () {
        if ($(this).is(':checked')) {
            $(this).prop('checked', true).parent().parent().addClass('info');
        } else {
            $(this).prop('checked', false).parent().parent().removeClass('info');
        }
    })
}