odoo.define('weather.btn_test_123', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    
    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);            
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons.on('click', '.btn_thoi_tiet_ngay_mai', this._onBtnClick.bind(this)); // add event listener
            }
			if (!this.noLeaf && this.hasButtons) {
                this.$buttons.on('click', '.btn_thoi_tiet_hom_nay', this._onBtnClick2.bind(this)); // add event listener
            }
        },
        _onBtnClick: function (ev) {
            // we prevent the event propagation because we don't want this event to
            // trigger a click on the main bus, which would be then caught by the
            // list editable renderer and would unselect the newly created row
            if (ev) {
                ev.stopPropagation();
            }
            var self = this;
            return this._rpc({
                model: 'weather.forecast',
                method: 'set_forecast_to_tomorrow',
                args: [],
                context: this.initialState.context,
            }).then(function(result) {
                 location.reload();
                // self.do_action(result);
            });
        },

		_onBtnClick2: function (ev) {
            // we prevent the event propagation because we don't want this event to
            // trigger a click on the main bus, which would be then caught by the
            // list editable renderer and would unselect the newly created row
            if (ev) {
                ev.stopPropagation();
            }
            var self = this;
            return this._rpc({
                model: 'weather.forecast',
                method: 'set_forecast_to_current',
                args: [],
                context: this.initialState.context,
            }).then(function(result) {
                 location.reload();
                // self.do_action(result);
            });
        },

    });
});