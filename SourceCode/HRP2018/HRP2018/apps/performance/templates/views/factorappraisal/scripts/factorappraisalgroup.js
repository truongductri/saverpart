(function (scope) {

    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields" : [
            { "data": "factor_group_code", "title": "${get_res('function_list','Mã nhóm')}", width: "100px", className: "text-center"},
            { "data": "note", "title": "${get_res('note','Ghi chú')}", width: "100px", className: "text-center"},
            { "data": "ordinal", "title": "${get_res('ordinal','Thứ tự')}", width: "100px", className: "text-center"},
            { "data": "lock", "title": "${get_res('lock','Ngưng sử dụng')}", format: "checkbox", width: "100px", className: "text-center" }
        ],
        "selectTreeNode" : function (node) {

        },
        "treeCurrentNode": {},
        "treeSelectedNodes": [],
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 2,
        "treeDisabled": false,
       
       
        
    };

    scope.onAdd = onAdd;
    scope.onEdit = onEdit;
    scope.onDelete = onDelete;
    scope.onImport = onImport;
    scope.onExport = onExport;
    scope.onAttach = onAttach;
    scope.onRefresh = onRefresh;

    //page load first
    scope.$$tableTree.dataTableTree = _factorAppraisalGroup;
    scope._reloadpage = _factorAppraisalGroup;
    // reload data
    function _factorAppraisalGroup() {
        services.api("${get_api_key('app_main.api.TMLS_FactorAppraisalGroup/get_tree')}")
            .data()
            .done()
            .then(function (res) {
                scope.$$tableTree.dataTableTree = res;
                scope.$applyAsync();
            })
    }

   

    function onAdd() {
        debugger
            scope.mode = 1;
            openDialog("${get_res('Factor_Appraisal_Group_Detail','Chi tiết nhóm yếu tố đánh giá')}", 'factorappraisal/form/addFactorAppraisalGroup', function () { });
    };
    function onDelete() {
        debugger
        if (!scope.$$tableTree.treeSelectedNodes[0]) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
        else
        {
            //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
            
                services.api("${get_api_key('app_main.api.TMLS_FactorAppraisalGroup/check_before_delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes[0].factor_group_code)
                    .done()
                    .then(function (res) {
                        if (res == true) {
                            $msg.alert("${get_global_res('Handle_Not_Allow','Nhóm được chọn đã được sử dụng bởi yếu tố đánh giá')}", $type_alert.WARNING);
                        }
                        else {
                            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                                services.api("${get_api_key('app_main.api.TMLS_FactorAppraisalGroup/delete')}")
                                    .data(scope.$$tableTree.treeSelectedNodes)
                                    .done()
                                    .then(function (res) {
                                        if (res.deleted > 0) {
                                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                                        }
                                    })
                            });
                        }
                    });
        }
    };
    function onEdit() {
        debugger
        if (scope.$$tableTree.treeSelectedNodes[0]) {
            scope.mode = 2; 
            openDialog("${get_res('Factor_Appraisal_Group_Detail','Chi tiết nhóm yếu tố đánh giá')}", 'factorappraisal/form/addFactorAppraisalGroup', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };

    function onImport() {

    };
    function onExport() {

    };
    function onAttach() {

    };
    function onRefresh() {

    };

   
    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {

        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

    _factorAppraisalGroup();
});