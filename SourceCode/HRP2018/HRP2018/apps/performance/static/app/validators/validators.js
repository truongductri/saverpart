﻿var lv;
(function (lv) {
    var _Validator = (function (val) {
        var __val;
        function _Validator(val) {
            __val = val;
        }
        _Validator.prototype.isNullOrEmpty = isNullOrWhiteSpace;

        _Validator.prototype.isNullOrWhiteSpace = isNullOrWhiteSpace;

        _Validator.prototype.isNumber = isNumber;

        _Validator.prototype.isEmail = isEmail;

        _Validator.prototype.isPhoneNumber = isPhoneNumber;

        _Validator.prototype.isString = isString;

        _Validator.prototype.isContainWhiteSpace = isContainWhiteSpace;

        _Validator.prototype.isDate = isDate;

        _Validator.prototype.isLoginAccount = function () {
            return (isNullOrWhiteSpace() == true || isContainWhiteSpace() == true) ? true : false;
        }

        _Validator.prototype.isPassword = function () {
            return (isNullOrWhiteSpace() == true || isContainWhiteSpace() == true) ? true : false;
        }

        function isNullOrWhiteSpace() {
            if (__val && __val.trim())
                return false;
            return true;
        }

        function isNullOrWhiteSpace() {
            if (__val && __val.trim())
                return false;
            return true;
        }

        function isNumber() {
            if (__val === null || __val === undefined)
                return false;
            return !isNaN(__val);
        }

        function isEmail() {
            var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(String(__val).toLowerCase());
        }

        function isPhoneNumber() {

        }

        function isString() {
            return typeof (__val) === "string";
        }

        function isContainWhiteSpace() {
            var re = new RegExp("/\s/");
            return re.test(__val);
        }

        function isDate() {
            if (__val) {
                var current = __val;
                var date = new Date(current);
                return date instanceof Date && !isNaN(date.valueOf());
            }
            return false;
            //return __val instanceof Date && !isNaN(__val.valueOf());
            //return true;
        }

        return _Validator;
    }());
    lv.Validate = function (val) {
        return new _Validator(val);
    };
})(lv || (lv = {}));
