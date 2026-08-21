odoo.define('sf_vendor_portal.vendor_portal', function (require) {
    'use strict';

    var ajax = require('web.ajax');

    function post(url, params) {
        return ajax.jsonRpc(url, 'call', params);
    }

    function vendorAccept(btn) {
        var id = parseInt(btn.getAttribute('data-id'), 10);
        post('/my/vendor/rfq/' + id + '/accept').then(function () {
            location.reload();
        });
    }

    function vendorDecline(btn) {
        var id = parseInt(btn.getAttribute('data-id'), 10);
        var comment = window.prompt('Reason for declining (optional)') || '';
        post('/my/vendor/rfq/' + id + '/decline', {comment: comment}).then(function () {
            location.reload();
        });
    }

    function vendorCounter(btn) {
        var id = parseInt(btn.getAttribute('data-id'), 10);
        var amount = window.prompt('Propose your total price');
        if (amount === null) {
            return;
        }
        post('/my/vendor/rfq/' + id + '/counter', {amount: parseFloat(amount) || 0}).then(function () {
            location.reload();
        });
    }

    return {
        vendorAccept: vendorAccept,
        vendorDecline: vendorDecline,
        vendorCounter: vendorCounter,
    };
});