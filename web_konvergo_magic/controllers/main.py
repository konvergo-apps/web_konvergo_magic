import logging
from odoo import http
from odoo.http import request


class KonvergoMagicController(http.Controller):
    @http.route('/workflow/get_config', type='json', auth='user')
    def get_workflow_config(self, model=None, record_id=None, view_type=None):
        _log_prefix = '[KONVERGO-ALLO-API]'
        logging.info(f"{_log_prefix} Config requested. Model: {model}, Record ID: {record_id}")
        
        WorkflowConfig = request.env['konvergo_magic.workflow']
    
        # Try to find a workflow configuration for the model
        config = False
        if model:
            config = WorkflowConfig.get_workflow_for_model(model)
            if config:
                logging.info(f"{_log_prefix} Found specific config for model {model}: {config.name}")
            
        # If there is no workflow specific to the model, try to find a global one
        if not config:
            config = WorkflowConfig.search([
                ('active', '=', True),
                ('is_global', '=', True)
            ], limit=1)
            if config:
                logging.info(f"{_log_prefix} Found global config: {config.name}")
            
        if not config:
            logging.warning(f"{_log_prefix} No config found. Returning display=False")
            return {'display': False}
            
        ###
        # Konvergo Allo bubble additional UI configuration
        ###
        # Add theme configuration
        if config.theme_id:
            theme = config.theme_id
            result['theme'] = {
                'theme': {
                    'placement': theme.placement,
                    'button': {
                        'backgroundColor': theme.button_background,
                        'size': theme.button_size ,
                    },
                    'previewMessage': {
                        'backgroundColor': theme.preview_message_background,
                        'textColor': theme.preview_message_text_color,
                        'closeButtonBackgroundColor': theme.preview_message_close_button_background,
                        'closeButtonIconColor': theme.preview_message_close_button_icon,
                    },
                'chatWindow': {
                    'backgroundColor': theme.chat_window_background,
                    },
                }
            }
            if theme.preview_message:
                result['preview_message'] = {
                    'previewMessage': {
                        'message': theme.preview_message_text,
                        'autoShowDelay': theme.preview_message_autoshow_seconds * 1000,
                    }
                }
                
        # Get current user's auth token
        auth_token = None
        if request.session.uid:
            user = request.env['res.users'].sudo().browse(request.session.uid)
            auth_token = user.konvergo_magic_auth_token
            
        result = {
            'display': bool(config),
            'workflow_id': config.workflow_id,
            'instance_url': config.instance_url,
            'auth_token': auth_token,
        }

        # Add context variables if enabled
        if config.include_context and model:
            result['prefilledVariables'] = {
                'erp_model': model,
                "erp_db_uuid": request.env["ir.config_parameter"].sudo().get_param("database.uuid"),
                "erp_db_name": request.session.db,
                "erp_base_url": request.env["ir.config_parameter"].sudo().get_param("web.base.url"),      
                "erp_view_type": view_type,          
            }

            if request.session.uid:
                user = request.env["res.users"].sudo().browse(request.session.uid)
                result["prefilledVariables"]["erp_auth_token"] = user.konvergo_magic_auth_token
                result["prefilledVariables"]["erp_user_id"] = user.id
                result["prefilledVariables"]["erp_username"] = user.login

            if record_id:
                result['prefilledVariables']['erp_record_id'] = int(record_id)
                
                # Attempt to get the record's name
                try:
                    record = request.env[model].browse(int(record_id))
                    if hasattr(record, 'name'):
                        result['prefilledVariables']['erp_record_name'] = record.name
                except Exception as e:
                    logging.exception(f"{_log_prefix} Error getting record name: {str(e)}")
                    pass
  
            logging.debug(f"{_log_prefix} Context variables: {result['prefilledVariables']}")
        else:
            logging.debug(f"{_log_prefix} Context variables not included. include_context: {config.include_context}, model: {model}")
               
        logging.debug(f"{_log_prefix} Returning config: {result}")
        return result
    