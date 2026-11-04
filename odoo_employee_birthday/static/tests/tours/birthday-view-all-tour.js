import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("odoo_employee_birthday_view_all_tour", {
    steps: () => [
        {
            content: "Open the full birthday list from the dashboard",
            trigger: ".o_ebd_panel_head button:contains(View All)",
            run: "click",
        },
        {
            content: "The All Birthdays list is shown",
            trigger: ".o_breadcrumb:contains(All Birthdays)",
        },
        {
            content: "Employees with a birthday are listed",
            trigger: ".o_list_view .o_data_row:contains(Birthday Tour Employee)",
        },
    ],
});
