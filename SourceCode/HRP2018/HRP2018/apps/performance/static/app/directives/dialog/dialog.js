﻿/**
 * USAGE
 * $msg.confirm('Nội dung title', 'Nội dung content', function(){ //Xử lí khi nhấn đồng ý })
 * $msg.message('Nội dung title', 'Nội dung content', function(){ //Xử lí khi nhấn đồng ý })
 */
var $msg = _Dialog();
var $dialog = {
    "closeDialog": function () { $('.hcs-modal-dialog:last').modal('hide'); },
    "draggable": function () {
        $('.hcs-modal-dialog:last').ready(function () {
            $('.hcs-modal-dialog:last .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                $('.hcs-modal-dialog:last .modal-dialog').draggable();
            }).bind('mouseup touchend', function () {
                $('.hcs-modal-dialog:last .modal-dialog').draggable('destroy');
            });
        })
    },
    "fullScreen": function () {
        var ele = $('.hcs-modal-dialog:last .modal-dialog');
        ele.toggleClass('resize-width');
        ele.removeAttr("style");
        setTimeout(function () {
            $(window).trigger('resize');
        }, 200)
    }
}
const $type_alert = Object.freeze({
    "DEFAULT": 0,
    "PRIMARY": 1,
    "SECONDARY": 2,
    "SUCCESS": 3,
    "DANGER": 4,
    "WARNING": 5,
    "INFO": 6,
    "LIGHT": 7,
    "DARK": 8
});
function _Dialog() {
    function ret() {
        var me = this;

        /**
         * Hộp thoại thông báo xác nhận
         * @param {string} title Tiêu đề của hộp thoại thông báo
         * @param {string} content Nội dung thông báo
         * @param {function} callback Xử lí khi nhấn đồng ý
         */
        me.confirm = function (title, content, callback) {
            var me = this;

            //UI form dialog
            me._form = $('<div class="modal fade hcs-modal-dialog" id="myConfirmModal" role="dialog">' +
                '<div class="modal-dialog combobox-dialog">' +
                '<div class="modal-content">' +
                '<div class="modal-header">' +
                '<div class="left-content pull-left">' +
                '<span class="modal-title" id="title"></span>' +
                '</div>' +
                '<div class="right-content pull-right">' +
                '<button type="button" class="close" data-dismiss="modal"><i class="la la-close"></i></button>' +
                '</div>' +
                '</div>' +
                '<div class="modal-body">' +
                '</div>' +
                '<div class="modal-footer">' +
                '<div class="right-content pull-right">' +
                '<button type="button"><i class="bowtie-icon bowtie-check-light"></i></button>' +
                '<button type="button"><i class="bowtie-icon bowtie-status-no"></i></button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
            );

            //Render form dialog
            me._form.appendTo('body');
            //Set title
            $('#myConfirmModal #title').text(title);
            //Set content
            $('#myConfirmModal .modal-body').text(content);
            //Set event nhấn phím ESC để thoát dialog
            $(document).keyup(function (event) {
                if (event.keyCode == 27) {
                    if ($('#myConfirmModal').length == 1)
                        closeDialog();
                }
            })
            //Show Dialog
            $('#myConfirmModal').modal({backdrop: 'static', keyboard: false});

            //Draggble Dialog
            $('#myConfirmModal').ready(function () {
                $('#myConfirmModal .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                    $('#myConfirmModal .modal-dialog').draggable();
                }).bind('mouseup touchend', function () {
                    $('#myConfirmModal .modal-dialog').draggable('destroy');
                });
            })

            //Event nhấn đồng  ý
            var btnConfirm = $('#myConfirmModal .modal-footer button:first');
            btnConfirm.click(function () {
                callback();
                closeDialog();
            })

            //Event nhấn từ chối
            var btnDeny = $('#myConfirmModal .modal-footer button:last');
            btnDeny.click(function () {
                closeDialog();
            })

            //Event nhấn nút thoát
            var btnClose = $('#myConfirmModal .close');
            btnClose.click(function () {
                closeDialog();
            })

            //Thoát Dialog
            function closeDialog() {
                $('#myConfirmModal').remove();
                $('.modal-backdrop:last').remove();
            }

            return me;
        }

        /**
         * Hộp thoại thông báo
         * @param {string} title Tiêu đề của hộp thoại thông báo
         * @param {string} content Nội dung thông báo
         * @param {function} callback Xử lí khi nhấn đồng ý
         */
        me.message = function (title, content, callback) {
            var me = this;

            //UI form dialog
            me._form = $('<div class="modal fade hcs-modal-dialog" id="myMessageModal" role="dialog">' +
                '<div class="modal-dialog combobox-dialog">' +
                '<div class="modal-content">' +
                '<div class="modal-header">' +
                '<div class="left-content pull-left">' +
                '<span class="modal-title" id="title"></span>' +
                '</div>' +
                '<div class="right-content pull-right">' +
                '<button type="button" class="close" data-dismiss="modal"><i class="la la-close"></i></button>' +
                '</div>' +
                '</div>' +
                '<div class="modal-body">' +
                '</div>' +
                '<div class="modal-footer">' +
                '<div class="right-content pull-right">' +
                '<button type="button"><i class="bowtie-icon bowtie-check-light"></i></button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
            );

            //Render form dialog
            me._form.appendTo('body');
            //Set title
            $('#myMessageModal #title').text(title);
            //Set content
            $('#myMessageModal .modal-body').text(content);
            //Set Event nhấn phím ESC để thoát dialog
            $(document).keyup(function (event) {
                if (event.keyCode == 27) {
                    if ($('#myMessageModal').length == 1)
                        closeDialog();
                }
            })
            //Show form dialog
            $('#myMessageModal').modal({backdrop: 'static', keyboard: false});

            //Draggble Dialog
            $('#myMessageModal').ready(function () {
                $('#myMessageModal .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                    $('#myMessageModal .modal-dialog').draggable();
                }).bind('mouseup touchend', function () {
                    $('#myMessageModal .modal-dialog').draggable('destroy');
                });
            })

            //Event nhấn phím đồng ý
            var btnConfirm = $('#myMessageModal .modal-footer button');
            btnConfirm.click(function () {
                callback();
                closeDialog();
            })

            //Event nhấn phím thoát dialog
            var btnClose = $('#myMessageModal .close');
            btnClose.click(function () {
                closeDialog();
            })

            //Hàm thoát dialog
            function closeDialog() {
                $('#myMessageModal').remove();
                $('.modal-backdrop:last').remove();
            }

            return me;
        }

        me.alert = function (content, type = 0) {
            var vm = this;
            vm._color;
            switch (type) {
                case $type_alert.DEFAULT:
                    vm._color = "background-color:#fff; color:#212529; border-color: 1px solid Black"; break;
                case $type_alert.PRIMARY:
                    vm._color = "background-color:#cce5ff; color:#004085; border-color: 1px solid #b8daff"; break;
                case $type_alert.SECONDARY:
                    vm._color = "background-color:#e2e3e5; color:#383d41; border-color: 1px solid #d6d8db"; break;
                case $type_alert.SUCCESS:
                    vm._color = "background-color:#d4edda; color:#155724; border-color: 1px solid #c3e6cb"; break;
                case $type_alert.DANGER:
                    vm._color = "background-color:#f8d7da; color:#721c24; border-color: 1px solid #f5c6cb"; break;
                case $type_alert.WARNING:
                    vm._color = "background-color:#fff3cd; color:#856404; border-color: 1px solid #ffeeba"; break;
                case $type_alert.INFO:
                    vm._color = "background-color:#d1ecf1; color:#0c5460; border-color: 1px solid #bee5eb"; break;
                case $type_alert.LIGHT:
                    vm._color = "background-color:#fefefe; color:#818182; border-color: 1px solid #fdfdfe"; break;
                case $type_alert.DARK:
                    vm._color = "background-color:#d6d8d9; color:#1b1e21; border-color: 1px solid #c6c8ca"; break;
                default:
                    vm._color = "background-color:#fff; color:#212529; border-color: 1px solid Black";
            }
            vm._alert = $(('<div id="hcs-toast-alert" style="#####;"></div>').replace('#####', vm._color));
            //Render form toast if not exsit
            if ($('#hcs-toast-alert').length == 0)
                vm._alert.appendTo('body');
            //Set content
            $('#hcs-toast-alert').text(content);
            //Show toast
            var ele = $("#hcs-toast-alert");
            ele.addClass("show");
            setTimeout(function () { ele.remove(); }, 3000);
        }

        /**
         * Dialog message lỗi từ server
         * @param {string} title
         * @param {string} content
         * @param {string} detail
         * @param {function} callback
         */
        me.error = function(title, content, detailMsg, callback) {
            var me = this;

            //UI form dialog
            me._form = $('<div class="modal fade hcs-modal-dialog" id="myErrorModal" role="dialog">' +
                '<div class="modal-dialog combobox-dialog">' +
                '<div class="modal-content">' +
                '<div class="modal-header">' +
                '<div class="left-content pull-left">' +
                '<span class="modal-title" id="title"></span>' +
                '</div>' +
                '<div class="right-content pull-right">' +
                '<button type="button" class="close" data-dismiss="modal"><i class="la la-close"></i></button>' +
                '</div>' +
                '</div>' +
                '<div class="modal-body">' +
                '</div>' +
                '<div class="modal-footer">' +
                '<div class="right-content pull-right">' +
                '<button type="button"><i class="bowtie-icon bowtie-status-info-outline"></i></button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
            );

            //Render form dialog
            me._form.appendTo('body');
            //Set title
            $('#myErrorModal #title').text(title);
            //Set content
            $('#myErrorModal .modal-body').text(content);
            //Set Event nhấn phím ESC để thoát dialog
            $(document).keyup(function (event) {
                if (event.keyCode == 27) {
                    if ($('#myErrorModal').length == 1)
                        closeDialog();
                }
            })
            //Show form dialog
            $('#myErrorModal').modal({backdrop: 'static', keyboard: false});

            //Draggble Dialog
            $('#myErrorModal').ready(function () {
                $('#myErrorModal .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                    $('#myErrorModal .modal-dialog').draggable();
                }).bind('mouseup touchend', function () {
                    $('#myErrorModal .modal-dialog').draggable('destroy');
                });
            })

            var btnDetail = $('#myErrorModal .modal-footer button:first');
            btnDetail.click(function () {
                detail(detailMsg);
            })

            //Event nhấn phím thoát dialog
            var btnClose = $('#myErrorModal .close');
            btnClose.click(function () {
                closeDialog();
            })

            //Hàm thoát dialog
            function closeDialog() {
                $('#myErrorModal').remove();
                $('.modal-backdrop:last').remove();
            }

            function detail(content) {
                var me = this;

                //UI form dialog
                me._form = $('<div class="modal fade hcs-modal-dialog" id="myErrorDetailModal" role="dialog">' +
                    '<div class="modal-dialog combobox-dialog" style="width:85%; top:1.5vh;">' +
                    '<div class="modal-content">' +
                    '<div class="modal-header">' +
                    '<div class="left-content pull-left">' +
                    '<span class="modal-title"><i class="bowtie-icon bowtie-status-info-outline"></i></span>' +
                    '</div>' +
                    '<div class="right-content pull-right">' +
                    '<button type="button" class="close" data-dismiss="modal"><i class="la la-close"></i></button>' +
                    '</div>' +
                    '</div>' +
                    '<div class="modal-body" style="padding: 15px;height: 85vh;overflow: auto;">' +
                    '</div>' +
                    '<div class="modal-footer">' +
                    '</div>' +
                    '</div>'
                );

                //Render form dialog
                me._form.appendTo('body');
                //Set content
                $('#myErrorDetailModal .modal-body').append(content);
                //Set Event nhấn phím ESC để thoát dialog
                $(document).keyup(function (event) {
                    if (event.keyCode == 27) {
                        if ($('#myErrorDetailModal').length == 1)
                            closeDialog();
                    }
                })
                //Show form dialog
                $('#myErrorDetailModal').modal({backdrop: 'static', keyboard: false});

                //Draggble Dialog
                $('#myErrorDetailModal').ready(function () {
                    $('#myErrorDetailModal .modal-dialog .modal-content .modal-header').on('mousedown touchstart', function (e) {
                        $('#myErrorDetailModal .modal-dialog').draggable();
                    }).bind('mouseup touchend', function () {
                        $('#myErrorDetailModal .modal-dialog').draggable('destroy');
                    });
                })

                //Event nhấn phím thoát dialog
                var btnClose = $('#myErrorDetailModal .close');
                btnClose.click(function () {
                    closeDialog();
                })

                //Hàm thoát dialog
                function closeDialog() {
                    $('#myErrorDetailModal').remove();
                    $('.modal-backdrop:last').remove();
                }
            }

            return me;
        }

        return me;
    }
    return new ret();
}
