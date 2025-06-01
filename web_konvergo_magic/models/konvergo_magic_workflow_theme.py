from odoo import fields, models

class KonvergoMagicWorkflowTheme(models.Model):
    _name = "konvergo_magic.workflow.theme"
    _description = "Konvergo Allo workflows theme templates"

    name = fields.Char(
        string="Name", 
        required=True
    )
    active = fields.Boolean(
        default=True
    )
    placement = fields.Selection(
        [("left", "Left"), ("right", "Right")],
        string="Bubble placement",
        default="right",
        required=True
    )
    chat_window_background = fields.Char(
        string="Chat window background color",
        default="#FFF"
    )
    button_background = fields.Char(
        string="Background color",
        help="The HEX code of the button background color",
        required=True
    )
    button_size = fields.Selection(
        [("medium", "Medium"), ("large", "Large")],
        string="Size",
        default="medium",
        required=True
    )
    preview_message = fields.Boolean(
        string="Preview message",
        required=True
    )
    preview_message_text = fields.Char(
        string="Preview message text"
    )
    preview_message_autoshow = fields.Boolean(
        string="Auto-show",
        help="Automatically displays a preview message after an elapsed time"
    )
    preview_message_autoshow_seconds = fields.Integer(
        string="Seconds to auto-show",
        help="Number of seconds before automatically showing the preview message"
    )
    preview_message_background = fields.Char(
        string="Background color",
        help="The HEX code of the preview message background color"
    )
    preview_message_text_color = fields.Char(
        string="Text color",
        help="The HEX code of the preview message text color",
    )
    preview_message_close_button_background = fields.Char(
        string="Button background color",
        help="The HEX code of the preview message close button background color"
    )
    preview_message_close_button_icon = fields.Char(
        string="Button icon color",
        help="The HEX code of the preview message close icon color"
    )
    workflow_ids = fields.Many2many(
        "konvergo_magic.workflow",
        string="Workflows"
    )
