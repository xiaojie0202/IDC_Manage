var ajax_cabinet_data = null;

$.ajax({
        url: '/ajax_cabinet_broken_line/',
        type: 'POST',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        dataType: 'JSON',
        success: function (data) {
            ajax_cabinet_data = data;
            $(function () {
                autocabinet();
                idcCabinetCount();
                customerCabinetCount();
                customerEquipmentCount();
            });
        }
    });


//机房机柜增减统计图
function autocabinet(){
    var cabinet = echarts.init(document.getElementById('cablein-count'));
    var option = {
            baseOption: {
                timeline: {
                    axisType: 'category',
                    autoPlay: true,
                    playInterval: 1000,
                    data: ajax_cabinet_data.year //年份
                },
                title: {
                    textStyle:{
                        color:'#CD0000' //主标题颜色
                    },
                    left:'center',
                    subtext: 'by:小杰'
                },
                legend: {
                    top:'12%',
                    orient:'horizontal',  //图例类型的布局 垂直
                    itemGap:50,   //类型之间的间隔
                    tooltip: {   //hover提示文本
                        show: true
                    },
                    "data": ajax_cabinet_data.dc
                },
                calculable : true,
                grid: {         //窗口组件位置
                    top:"20%",
                    left: '1%',
                    right: '4%',
                    bottom: '15%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                            type: 'cross' //十字准星指示器

                        },
                    //formatter: "{b}<br/> {a*}:{c*}"
                },
                xAxis: [
                    {
                        'type':'category',
                        'axisLabel':{'interval':0},
                        name:'日期',
                        splitLine: {show: false},
                        axisTick:{  //坐标轴刻度相关设置
                            alignWithLabel:true //保证刻度线和标签对齐
                        },
                        data:['Jan', 'Feb','Mar','Apr','May','Jun','jul','Aug','Sept','Oct','Nov','Dec']

                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '数量'
                    }
                ],
                series: ajax_cabinet_data.series
            },
            options: ajax_cabinet_data.options
        };
    cabinet.setOption(option);

}

//IDC机柜数量总统计图
function idcCabinetCount(){
    var idc = echarts.init(document.getElementById('idc-count'));
    var option = {
            title: {
                text: '机柜数量统计图',
                left: 'center',
                top: '0',
                textStyle: {
                    color: '#000'
                },
                subtext: 'by:小杰'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                data:ajax_cabinet_data.dc,
                bottom:'5%'
            },
            series: [
                {
                    name:'总机柜数量',
                    type:'pie',
                    radius: ['2%', '20%'],
                    roseType: 'radius',
                    label: {
                        normal: {
                            formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                            backgroundColor: '#eee',
                            borderColor: '#aaa',
                            borderWidth: 1,
                            borderRadius: 4,
                            rich: {
                                a: {
                                    color: '#999',
                                    lineHeight: 22,
                                    align: 'center'
                                },
                                abg: {
                                    backgroundColor: '#333',
                                    width: '100%',
                                    align: 'right',
                                    height: 22,
                                    borderRadius: [4, 4, 0, 0]
                                },
                                hr: {
                                    borderColor: '#aaa',
                                    width: '100%',
                                    borderWidth: 0.5,
                                    height: 0
                                },
                                b: {
                                    fontSize: 16,
                                    lineHeight: 33
                                },
                                per: {
                                    color: '#eee',
                                    backgroundColor: '#334455',
                                    padding: [2, 4],
                                    borderRadius: 2
                                }
                            }
                        }
                    },
                    data:ajax_cabinet_data.cabinet_count_list
                }
            ]
        };
    idc.setOption(option);

}

//客户机柜数量统计图
function customerCabinetCount(){
    var customer_cabinet = echarts.init(document.getElementById('customet_caninet_count'));
    var option = {
            title: {
                text: '客户机柜数量统计图',
                left: 'center',
                top: '0',
                textStyle: {
                    color: '#000'
                },
                subtext: 'by:小杰'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                data:ajax_cabinet_data.customer_name,
                bottom:'5%'
            },
            series: [
                {
                    name:'机柜数量',
                    type:'pie',
                    radius: ['5%', '40%'],
                    roseType: 'radius',
                    label: {
                        normal: {
                            formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                            backgroundColor: '#eee',
                            borderColor: '#aaa',
                            borderWidth: 1,
                            borderRadius: 4,
                            rich: {
                                a: {
                                    color: '#999',
                                    lineHeight: 22,
                                    align: 'center'
                                },
                                abg: {
                                    backgroundColor: '#333',
                                    width: '100%',
                                    align: 'right',
                                    height: 22,
                                    borderRadius: [4, 4, 0, 0]
                                },
                                hr: {
                                    borderColor: '#aaa',
                                    width: '100%',
                                    borderWidth: 0.5,
                                    height: 0
                                },
                                b: {
                                    fontSize: 16,
                                    lineHeight: 33
                                },
                                per: {
                                    color: '#eee',
                                    backgroundColor: '#334455',
                                    padding: [2, 4],
                                    borderRadius: 2
                                }
                            }
                        }
                    },
                    data:ajax_cabinet_data.customer_value
                }
            ]
        };
    customer_cabinet.setOption(option);

}

//客户设备数量统计图
function customerEquipmentCount(){
    var customer_equipment = echarts.init(document.getElementById('customet_equipment_count'));
    var option = {
            title: {
                text: '客户机设备量统计图',
                left: 'center',
                top: '0',
                textStyle: {
                    color: '#000'
                },
                subtext: 'by:小杰'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                data:ajax_cabinet_data.customer_name,
                bottom:'5%'
            },
            series: [
                {
                    name:'设备数量',
                    type:'pie',
                    radius: ['5%', '40%'],
                    roseType: 'radius',
                    label: {
                        normal: {
                            formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                            backgroundColor: '#eee',
                            borderColor: '#aaa',
                            borderWidth: 1,
                            borderRadius: 4,
                            rich: {
                                a: {
                                    color: '#999',
                                    lineHeight: 22,
                                    align: 'center'
                                },
                                abg: {
                                    backgroundColor: '#333',
                                    width: '100%',
                                    align: 'right',
                                    height: 22,
                                    borderRadius: [4, 4, 0, 0]
                                },
                                hr: {
                                    borderColor: '#aaa',
                                    width: '100%',
                                    borderWidth: 0.5,
                                    height: 0
                                },
                                b: {
                                    fontSize: 16,
                                    lineHeight: 33
                                },
                                per: {
                                    color: '#eee',
                                    backgroundColor: '#334455',
                                    padding: [2, 4],
                                    borderRadius: 2
                                }
                            }
                        }
                    },
                    data:ajax_cabinet_data.equipment_value
                }
            ]
        };
    customer_equipment.setOption(option);

}