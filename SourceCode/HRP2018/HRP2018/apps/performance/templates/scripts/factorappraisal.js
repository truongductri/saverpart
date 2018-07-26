(function (scope) {
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.triggerResize = function () {
        $(window).trigger('resize');
    };
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.onAdd = function (callback) { callback; };
    scope.onEdit = function (callback) { callback; };
    scope.onDelete = function (callback) { callback; };
    scope.onImport = function (callback) { callback; };
    scope.onExport = function (callback) { callback; };
    scope.onAttach = function (callback) { callback; };
    scope.onRefresh = function (callback) { callback; };
    /*                                                         */
    /* ==================== Property Scope - END ==============*/
    /*                                                         */

    /*                                                         */
    /* ==================== Initialize - START=================*/
    /*                                                         */
    activate();
    init();
    /*                                                         */
    /* ==================== Initialize - END ==================*/
    /*                                                         */

    /*                                                                                          */
    /* ===============================  Implementation - START  ================================*/
    /*                                                                                          */

    /* Object handle data */
    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = _.where(scope.$root.$function_list, { "function_id": scope.$root.currentFunction.function_id });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
    }

    /*                                                                                          */
    /* ===============================  Implementation - END  ==================================*/
    /*                                                                                          */

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.page) {
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.page;
                });
                if (func.length > 0) {
                    //scope.$partialpage = func[0].url;
                    scope.currentFunction = func[0];
                } else {
                    window.location.href = "#";
                }
            }
            scope.$apply();
        } else {
            window.location.href = "#";
        }
    });
});