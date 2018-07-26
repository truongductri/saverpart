(function (scope) {
    const __$$jobWorking_id = "HCSSYS0460";
    const __$$jobWorkingGroup_id = "HCSSYS0450";
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.redirect = {
        jobWorkingPage: function () {
            debugger
            var $his = scope.$root.$history.data();
            window.location.href = "#page=" + $his.page + "&f=" + _.findWhere(scope.mapName, { "function_id": __$$jobWorking_id }).function_id;
            scope.display.viewDetail = false;
        },
        jobWorkingGroupPage: function () {
            debugger
            var $his = scope.$root.$history.data();
            window.location.href = "#page=" + $his.page + "&f=" + _.findWhere(scope.mapName, { "function_id": __$$jobWorkingGroup_id }).function_id;
            scope.display.viewDetail = false;
        }
    }

    scope.currentFunction = '';
    scope.mapName = [];
    scope.jobWorkingMap = [];
    scope.jobWorking = {};
    scope.jobWorkingGroup = {};
    scope.$jobWorking = {
        selectedFunction : ''
    }
    scope.display = { viewDetail : false };
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

        this.jobWorkingMap = [];

        this.jobWorking = {};

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        var jobWorking = _.findWhere(this.mapName, { "function_id": __$$jobWorking_id });

        this._jobWorking = jobWorking;

        this.jobWorkingMap = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(jobWorking.function_id)
                && f.level_code.length == jobWorking.level_code.length + 1;
        });


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
        scope.jobWorkingMap = scope.handleData.jobWorkingMap;
        scope.jobWorking = _.findWhere(scope.mapName, { "function_id": __$$jobWorking_id });
        scope.jobWorkingGroup = _.findWhere(scope.mapName, { "function_id": __$$jobWorkingGroup_id });
        scope.currentFunction = scope.mapName[0];
        console.log(scope.jobWorking, scope.jobWorkingGroup);
    }

    /*                                                                                          */
    /* ===============================  Implementation - END  ==================================*/
    /*                                                                                          */

    scope.$watch("$jobWorking.selectedFunction", function (function_id) {
        if (function_id) {
            var $his = scope.$root.$history.data();
            scope.$partialView = _.findWhere(scope.jobWorkingMap, { "function_id": function_id }).url;
        }
    });

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    scope.$partialpage = func[0].url;
                    scope.currentFunction = func[0];
                } else {
                    window.location.href = "#";
                }
            }else {
                scope.$partialpage = scope.mapName[0].url;
                scope.display.viewDetail = false;
            }
            scope.$apply();
        } else {
            window.location.href = "#";
        }
    });
});