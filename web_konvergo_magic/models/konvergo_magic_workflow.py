from odoo import api, fields, models


def remove_trailing_slash(url):
    if url.endswith('/'):
        return url.rstrip('/')

class KonvergoMagicWorkflow(models.Model):
    _name = "konvergo_magic.workflow"
    _description = "Konvergo MAGIC workflows configuration"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(default=True)
    workflow_id = fields.Char(string="Workflow ID", required=True,
                            help="The ID of your Konvergo Allo workflow")
    instance_url = fields.Char(
        string="Instance URL", 
        required=True, 
        help="The URL of your Konvergo Allo instance"
    )
    model_ids = fields.Many2many(
        "ir.model", 
        string="Active models", 
        help="Models where the workflow should be displayed"
    )
    include_context = fields.Boolean(
        string="Include Context", 
        default=True,
        help="Send context information (model, record_id) to the workflow as pre-filled variables"
    )
    is_global = fields.Boolean(
        string="Global integration", 
        default=False,
        help="Whether to display the workflow on every model."
    )
    theme_id = fields.Many2one(
        "konvergo_magic.workflow.theme",
        string="Theme template",
        help="Bubble theme template to use"
    )
    
    @api.onchange('instance_url')
    def _onchange_instance_url(self):
        """Ensure the URL is properly formatted for API calls"""
        if self.instance_url:
            # Remove trailing slash if present
            if self.instance_url.endswith('/'):
                self.instance_url = self.instance_url.rstrip('/')
                
    @api.model
    def create(self, vals):
        if vals.get('instance_url') and vals['instance_url'].endswith('/'):
            vals['instance_url'] = vals['instance_url'].rstrip('/')
        return super(KonvergoMagicWorkflow, self).create(vals)
        
    def write(self, vals):
        if vals.get('instance_url') and vals['instance_url'].endswith('/'):
            vals['instance_url'] = vals['instance_url'].rstrip('/')
        return super(KonvergoMagicWorkflow, self).write(vals)

    @api.model
    def get_workflow_for_model(self, model_name):
        """Get the workflow configuration for a specific model"""
        domain = [
            ("active", "=", True),
            "|",
            ("is_global", "=", True),
            ("model_ids.model", "=", model_name),
        ]
        return self.search(domain, limit=1)