/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

const MONTHS_SHORT = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const MONTHS_FULL  = ['January','February','March','April','May','June',
                      'July','August','September','October','November','December'];

export class BirthdayDashboard extends Component {
    static template = "odoo_employee_birthday.BirthdayDashboard";

    setup() {
        this.action = useService("action");
        this.notify = useService("notification");

        this.state = useState({
            loading:       true,
            today_count:   0,
            days3_count:   0,
            days7_count:   0,
            days15_count:  0,
            today_ids:     [],
            days3_ids:     [],
            days7_ids:     [],
            days15_ids:    [],
            today_list:    [],
            upcoming:      [],
            monthly_stats: Array(12).fill(0),
        });

        onMounted(async () => { await this._loadData(); });
    }

    async _loadData() {
        try {
            const data = await rpc("/odoo_employee_birthday/dashboard_data");
            Object.assign(this.state, data);
        } catch (e) {
            this.notify.add("Failed to load birthday data", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    /** Pre-computed bar descriptors for SVG chart rendering */
    get chartBars() {
        const stats    = this.state.monthly_stats;
        const max      = Math.max(...stats, 1);
        const barW     = 28, gap = 16, chartH = 130, padTop = 18;
        const curMonth = new Date().getMonth();
        return stats.map((count, i) => ({
            x:         i * (barW + gap),
            y:         padTop + chartH - (Math.round((count / max) * chartH) || 2),
            h:         Math.round((count / max) * chartH) || 2,
            count,
            month:     MONTHS_SHORT[i],
            isCurrent: i === curMonth,
        }));
    }

    get chartViewBox() { return "0 0 528 185"; }

    get currentMonthLabel() { return MONTHS_FULL[new Date().getMonth()]; }

    openGroup(label, idsKey) {
        const ids = this.state[idsKey] || [];
        if (!ids.length) {
            this.notify.add(`No birthdays in "${label}"`, { type: "info" });
            return;
        }
        this.action.doAction({
            name: label,
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            views: [[false, "list"], [false, "form"]],
            domain: [["id", "in", ids]],
        });
    }

    openAll() {
        this.action.doAction("odoo_employee_birthday.action_employee_birthday_list");
    }
}

registry.category("actions").add("odoo_employee_birthday.BirthdayDashboard", BirthdayDashboard);
