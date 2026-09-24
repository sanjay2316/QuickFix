import frappe

def get_context(context):

    context.jobs = frappe.get_all(
        "Job Card",
        fields=[
            "name",
            "status",
            "workflow_state",
            "parts_total",
            "labour_charge",
            "final_amount"
        ],
        order_by="creation desc"
    )

    return context