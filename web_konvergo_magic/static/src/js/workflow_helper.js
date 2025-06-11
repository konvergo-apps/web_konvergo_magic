/**
 * Konvergo Allo Helper Script
 * Provides utility functions for Konvergo Allo integration
 */
odoo.define("web_konvergo_magic.helper", function (require) {
  "use strict";

  var ajax = require("web.ajax");
  var WorkflowHelper = {
    /**
     * Get the current model and record ID from URL
     */
    getContextParameters: function () {
      var result = {};
      try {
        const hash = window.location.hash.substring(1);
        result = hash.split("&").reduce(function (res, item) {
          var parts = item.split("=");
          res[parts[0]] = parts[1];
          return res;
        }, {});
      } catch (e) {
        console.error(
          "[KONVERGO-ALLO-HELPER] Error extracting context parameters:",
          e
        );
      }

      return result;
    },

    /**
     * Fetch the Konvergo Allo workflow configuration for the model.
     * @returns The object of the workflow configuration.
     */
    loadWorkflowConfig: function () {
      var self = this;
      var context = this.getContextParameters();

      console.debug(
        "[KONVERGO-ALLO-HELPER] Getting configuration for",
        context
      );

      return ajax
        .jsonRpc("/workflow/get_config", "call", {
          model: context.model,
          record_id: context.id,
          view_type: context.view_type,
        })
        .then(function (config) {
          if (config && config.display) {
            self.initWorkflow(config);
            return config;
          } else {
            console.debug(
              "[KONVERGO-ALLO] Workflow not configured for this context"
            );
            return false;
          }
        })
        .fail(function (error) {
          console.error("[KONVERGO-ALLO-HELPER] Error loading config:", error);
          return false;
        });
    },

    /**
     * Initializes the Konvergo Allo workflow configuration to be displayed.
     * @param {*} config - The workflow configuration to initialize.
     */
    initWorkflow: function (config) {
      if (!config.auth_token) {
        var message =
          "Konvergo Allo authentication token is missing. Please set it in your user preferences.";
        alert(message);
        console.warn("[KONVERGO-ALLO-HELPER] " + message);
        return;
      }

      var workflowUrl = config.instance_url;

      var workflowProps = {
        workflow: config.workflow_id,
        apiHost: workflowUrl,
      };

      if (config.prefilledVariables) {
        workflowProps.prefilledVariables = config.prefilledVariables;
      }

      if (config.theme) {
        Object.assign(workflowProps, config.theme);
      }

      if (config.preview_message) {
        Object.assign(workflowProps, config.preview_message);
      }

      var script = document.createElement("script");
      script.setAttribute("type", "module");
      script.textContent = `
                try {
                    import('${config.instance_url}/embed/web.js')
                        .then(module => {
                            const Workflow = module.default;
                            console.debug('[KONVERGO-ALLO-HELPER] Konvergo Allo loaded');
                            
                            const props = ${JSON.stringify(workflowProps)};

                            const instance = Workflow.initBubble(props);
                            window.workflowInstance = instance;
                            window.WORKFLOW_CONFIG = props;
                            
                            console.debug('[KONVERGO-ALLO-HELPER] Konvergo Allo initialized');
                        })
                        .catch(err => {
                            console.error('[KONVERGO-ALLO-HELPER] Error loading Konvergo Allo:', err);
                        });
                } catch (e) {
                    console.error('[KONVERGO-ALLO-HELPER] Error in Konvergo Allo loading:', e);
                }
            `;

      document.head.appendChild(script);
    },
  };

  // Initialize when the page is fully loaded
  $(document).ready(function () {
    console.debug("[KONVERGO-ALLO-HELPER] Document ready, initializing");
    WorkflowHelper.loadWorkflowConfig();
  });

  return WorkflowHelper;
});
