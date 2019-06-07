

odoo.define('dn_enterprise.ExpirationPanel', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var utils = require('web.utils');
var HomeMenu = require('web_enterprise.HomeMenu');

var QWeb = core.qweb;

HomeMenu.include({
    events: _.extend(HomeMenu.prototype.events, {
        'click .oe_instance_buy': '_onEnterpriseBuy',
        'click .oe_instance_renew': '_onEnterpriseRenew',
        'click .oe_instance_upsell': '_onEnterpriseUpsell',
        'click a.oe_instance_register_show': '_onEnterpriseRegisterShow',
        'click #confirm_enterprise_code': '_onEnterpriseCodeSubmit',
        'click .oe_instance_hide_panel': '_onEnterpriseHidePanel',
        'click .check_enterprise_status': '_onEnterpriseCheckStatus',
    }),
    /**
     * @override
     */
    start: function () {
        return this._super.apply(this, arguments).then(this._enterpriseExpirationCheck.bind(this));
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Checks for the database expiration date and display a warning accordingly.
     *
     * @private
     */
    _enterpriseExpirationCheck: function () {
        // alert('tes 21')
        var self = this;

        // don't show the expiration warning for portal users
        if (!(session.warning))  {
            return;
        }
        var today = new moment();
        // if no date found, assume 1 month and hope for the best
        var dbexpirationDate = new moment(session.expiration_date || new moment().add(30, 'd'));
        var duration = moment.duration(dbexpirationDate.diff(today));
        var options = {
            'diffDays': Math.round(duration.asDays()),
            'dbexpiration_reason': session.expiration_reason,
            'warning': session.warning,
        };
        // self._enterpriseShowPanel(options);
    },
    /**
     * Show expiration panel 30 days before the expiry
     *
     * @private
     * @param {Object} options
     * @param {number} options.diffDays Number of days before expiry
     * @param {string|false} options.dbexpiration_reason E.g. 'trial','renewal','upsell',...
     * @param {'admin'|'user'} options.warning Type of logged-in accounts addressed by message
     */
    _enterpriseShowPanel: function (options) {
        // alert('tes 3')
        var self = this;
        var hideCookie = utils.get_cookie('oe_instance_hide_panel');
        // if ((options.diffDays <= 30 && !hideCookie) || options.diffDays <= 0) {

        //     var expirationPanel = $(QWeb.render('WebClient.database_expiration_panel', {
        //         has_mail: _.includes(session.module_list, 'mail'),
        //         diffDays: options.diffDays,
        //         dbexpiration_reason:options.dbexpiration_reason,
        //         warning: options.warning
        //     })).insertBefore(self.$menuSearch);

        //     if (options.diffDays <= 0) {
        //         expirationPanel.children().addClass('alert-danger');
        //         expirationPanel.find('.oe_instance_buy')
        //                        .on('click.widget_events', self.proxy('_onEnterpriseBuy'));
        //         expirationPanel.find('.oe_instance_renew')
        //                        .on('click.widget_events', self.proxy('_onEnterpriseRenew'));
        //         expirationPanel.find('.oe_instance_upsell')
        //                        .on('click.widget_events', self.proxy('_onEnterpriseUpsell'));
        //         expirationPanel.find('.check_enterprise_status')
        //                        .on('click.widget_events', self.proxy('_onEnterpriseCheckStatus'));
        //         expirationPanel.find('.oe_instance_hide_panel').hide();
        //         $.blockUI({message: expirationPanel.find('.database_expiration_panel')[0],
        //                    css: { cursor : 'auto' },
        //                    overlayCSS: { cursor : 'auto' } });
        //     }
        // }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onEnterpriseBuy: function () {
        var limitDate = new moment().subtract(15, 'days').format("YYYY-MM-DD");
        this._rpc({
                model: 'res.users',
                method: 'search_count',
                args: [[["share", "=", false],["login_date", ">=", limitDate]]],
            })
            .then(function (users) {
                window.location =
                    $.param.querystring("https://www.odoo.com/odoo-enterprise/upgrade", {num_users: users});
            });
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onEnterpriseCheckStatus: function (ev) {
        // alert('tes')
        ev.preventDefault();
        var self = this;
        this._rpc({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['database.expiration_date'],
            })
            .then(function (oldDate) {
                var dbexpirationDate = new moment(oldDate);
                var duration = moment.duration(dbexpirationDate.diff(new moment()));
                if (Math.round(duration.asDays()) < 30) {
                    self._rpc({
                            model: 'publisher_warranty.contract',
                            method: 'update_notification',
                            args: [[]],
                        })
                        .then(function () {
                            self._rpc({
                                    model: 'ir.config_parameter',
                                    method: 'get_param',
                                    args: ['database.expiration_date']
                                })
                                .then(function (dbexpiration_date) {
                                    // $('.oe_instance_register').hide();
                                    // $('.database_expiration_panel .alert')
                                    //         .removeClass('alert-info alert-warning alert-danger');
                                    // if (dbexpirationDate !== oldDate && new moment(dbexpirationDate) > new moment()) {
                                    //     $.unblockUI();
                                    //     $('.oe_instance_hide_panel').show();
                                    //     $('.database_expiration_panel .alert').addClass('alert-success');
                                    //     $('.valid_date').html(moment(dbexpirationDate).format('LL'));
                                    //     $('.oe_subscription_updated').show();
                                    // } else {
                                    //     window.location.reload();
                                    // }
                                    window.location.reload();
                                });
                        });
                }
            });
    },
    /**
     * Save the registration code then triggers a ping to submit it
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onEnterpriseCodeSubmit: function (ev) {
        ev.preventDefault();
        var self = this;
        var enterpriseCode = $('.database_expiration_panel').find('#enterprise_code').val();
        if (!enterpriseCode) {
            var $c = $('#enterprise_code');
            $c.attr('placeholder', $c.attr('title')); // raise attention to input
            return;
        }
        $.when(
            this._rpc({
                    model: 'ir.config_parameter',
                    method: 'get_param',
                    args: ['database.expiration_date']
                }),
            this._rpc({
                    model: 'ir.config_parameter',
                    method: 'set_param',
                    args: ['database.enterprise_code', enterpriseCode]
                })
        ).then(function (oldDate) {
            utils.set_cookie('oe_instance_hide_panel', '', -1);
            self._rpc({
                    model: 'publisher_warranty.contract',
                    method: 'update_notification',
                    args: [[]],
                })
                .then(function () {
                    $.unblockUI();
                    $.when(
                        self._rpc({
                                model: 'ir.config_parameter',
                                method: 'get_param',
                                args: ['database.expiration_date']
                            }),
                        self._rpc({
                                model: 'ir.config_parameter',
                                method: 'get_param',
                                args: ['database.expiration_reason']
                            })
                    ).then(function (dbexpirationDate) {
                        $('.oe_instance_register').hide();
                        $('.database_expiration_panel .alert')
                                .removeClass('alert-info alert-warning alert-danger');
                        if (dbexpirationDate !== oldDate) {
                            $('.oe_instance_hide_panel').show();
                            $('.database_expiration_panel .alert').addClass('alert-success');
                            $('.valid_date').html(moment(dbexpirationDate).format('LL'));
                            $('.oe_instance_success').show();
                        } else {
                            $('.database_expiration_panel .alert').addClass('alert-danger');
                            $('.oe_instance_error, .oe_instance_register_form').show();
                            $('#confirm_enterprise_code').html('Retry');
                        }
                    });
                });
        });
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onEnterpriseHidePanel: function (ev) {
        ev.preventDefault();
        utils.set_cookie('oe_instance_hide_panel', true, 24*60*60);
        $('.database_expiration_panel').hide();
    },
    /**
     * @private
     */
    _onEnterpriseRegisterShow: function () {
        this.$('.oe_instance_register_form').slideToggle();
    },
    /**
     * @private
     */
    _onEnterpriseRenew: function () {
        var self = this;
        this._rpc({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['database.expiration_date'],
            })
            .then(function (oldDate) {
                utils.set_cookie('oe_instance_hide_panel', '', -1);
                self._rpc({
                        model: 'publisher_warranty.contract',
                        method: 'update_notification',
                        args: [[]],
                    })
                    .then(function () {
                        $.when(
                            self._rpc({
                                    model: 'ir.config_parameter',
                                    method: 'get_param',
                                    args: ['database.expiration_date']
                                }),
                            self._rpc({
                                    model: 'ir.config_parameter',
                                    method: 'get_param',
                                    args: ['database.expiration_reason']
                                }),
                            self._rpc({
                                    model: 'ir.config_parameter',
                                    method: 'get_param',
                                    args: ['database.enterprise_code']
                                })
                        ).then(function (newDate, dbexpirationReason, enterpriseCode) {
                            var mtNewDate = new moment(newDate);
                            if (newDate !== oldDate && mtNewDate > new moment()) {
                                $.unblockUI();
                                $('.oe_instance_register').hide();
                                $('.database_expiration_panel .alert')
                                        .removeClass('alert-info alert-warning alert-danger');
                                $('.database_expiration_panel .alert')
                                        .addClass('alert-success');
                                $('.valid_date').html(moment(newDate).format('LL'));
                                $('.oe_instance_success, .oe_instance_hide_panel').show();
                            } else {
                                var params = enterpriseCode ? {contract: enterpriseCode} : {};
                                window.location =
                                    $.param.querystring("https://www.odoo.com/odoo-enterprise/renew", params);
                            }
                        });
                    });
            });
    },
    /**
     * @private
     */
    _onEnterpriseUpsell: function () {
        var self = this;
        var limitDate = new moment().subtract(15, 'days').format("YYYY-MM-DD");
        this._rpc({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ['database.enterprise_code'],
            })
            .then(function (contract) {
                self._rpc({
                        model: 'res.users',
                        method: 'search_count',
                        args: [[["share", "=", false],["login_date", ">=", limitDate]]],
                    })
                    .then(function (users) {
                        var params =
                            contract ? {contract: contract, num_users: users} : {num_users: users};
                        window.location =
                            $.param.querystring("https://www.odoo.com/odoo-enterprise/upsell", params);
                    });
            });
    },
});

});
