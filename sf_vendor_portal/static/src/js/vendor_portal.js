/** @odoo-module **/
import { Component, mount } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc_service";

class VendorRfqButtons extends Component {
    static template = `
        <div class="d-flex gap-2">
            <button class="btn btn-success" t-on-click="onAccept">Accept</button>
            <button class="btn btn-danger" t-on-click="onDecline">Decline</button>
            <button class="btn btn-warning" t-on-click="onCounter">Propose a counter-offer</button>
        </div>`;
    static props = { orderId: { type: Number } };

    async onAccept() {
        await this._call("accept");
    }

    async onDecline() {
        const comment = window.prompt("Reason for declining (optional)") || "";
        await this._call("decline", { comment });
    }

    async onCounter() {
        const amount = window.prompt("Propose your total price");
        if (amount === null) {
            return;
        }
        await this._call("counter", { amount: parseFloat(amount) || 0 });
    }

    async _call(action, params) {
        await rpc(`/my/vendor/rfq/${this.props.orderId}/${action}`, params || {});
        window.location.reload();
    }
}

function mountButtons() {
    const target = document.querySelector("[data-vendor-rfq-buttons]");
    if (target) {
        mount(VendorRfqButtons, {
            target,
            props: { orderId: Number(target.dataset.orderId) },
        });
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountButtons);
} else {
    mountButtons();
}