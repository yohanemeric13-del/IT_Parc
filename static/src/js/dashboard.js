/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class ItParcDashboard extends Component {
    static template = "gestion_parc.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            loading: true,
            data: {
                kpis: {},
                by_type: [],
            },
        });
        onWillStart(async () => {
            this.state.data = await this.orm.call("gestion.materiel", "get_dashboard_data", []);
            this.state.loading = false;
        });
    }

    get maxTypeCount() {
        return Math.max(...this.state.data.by_type.map((item) => item.count), 1);
    }

    barWidth(count) {
        return Math.max(8, Math.round((count / this.maxTypeCount) * 180));
    }
}

registry.category("actions").add("gestion_parc.dashboard", ItParcDashboard);
