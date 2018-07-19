angular.module('ZebraApp.components', [
    'ui.select',
    'ui.bootstrap',
    'ui.bootstrap.tpls',
    'ui.bootstrap.collapse',
    'ZebraApp.components.inputs',
    'ZebraApp.components.tables',
    'ZebraApp.components.trees'
])
.run(['$templateCache', function ($templateCache) {
    $templateCache.put('app/components/input/checkbox/checkbox.html', '<div class="checkbox zb-form-checkbox"><label class="custom-checkbox"><input type="checkbox" ng-model="model"><span>{{caption}}</span></label></div>');
    $templateCache.put('app/components/input/datepicker/datepicker.html', '<span class="input-group zb-form-date-picker"><input type="text" class="form-control" uib-datepicker-popup="{{format}}" datepicker-options="options" ng-model="dt" is-open="opened" close-text="Close" alt-input-formats="altInputFormats" show-button-bar="true" placeholder="{{placeholder}}"><span class="input-group-btn"><button type="button" class="btn btn-default"><i class="glyphicon glyphicon-calendar"></i></button></span></span>');
    $templateCache.put('app/components/input/select/select.html', '<div ng-controller="SelectpickerPanelCtrl as selectpickerVm" class="zb-form-select"><ui-select ng-model="selectedItem.selected" class="btn-group bootstrap-select form-control" ng-disabled="false" append-to-body="false" search-enabled="true" title="{{$select.selected.__fieldCaption}}"><ui-select-match placeholder="{{placeholder}}">{{$select.selected.__fieldCaption}}</ui-select-match><ui-select-choices repeat="searchItem in selectWithSearchItems | filter: $select.search"><span ng-bind-html="searchItem.__fieldCaption" title="{{searchItem.__fieldCaption}}"></span></ui-select-choices></ui-select></div>');
    $templateCache.put('app/components/table/table-data/table-data.html', '<table class="display zb-data-table responsive nowrap" cellspacing="0"></table>');
    $templateCache.put('app/components/tree/tree/tree.html', '<div class="zb-tree"><div id="tree"></div></div>');
    $templateCache.put('app/components/tree/tree-table/tree-table.html','<div id="scrolling_table" class="zb-tree-table"><table id="treetable"><thead><tr><th style="background-color:white" class="fixed freeze" ng-if="multiSelect"><label class="custom-checkbox"><input type="checkbox" class="zb-tree-table-checkall"> <span></span></label></th><th style="background-color:white" class="zb-tree-table-th fixed freeze">{{displayName}}</th><th ng-repeat="f in fields" style="background-color:white;min-width:{{f.width ? f.width : \'auto\'}}" class="fixed freeze_vertical {{f.width ? \'\' : \'zb-tree-table-nowrap\'}}">{{f.title}}</th></tr></thead><tbody><tr><td class="fixed freeze_horizontal zb-tree-table-checkbox" ng-if="multiSelect"></td><td class="fixed freeze_horizontal zb-tree-table-nowrap"></td><td ng-repeat="f in fields"></td></tr></tbody></table></div>');
}]);



