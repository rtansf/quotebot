class Controls():

    def __init__(self):

        self.message_attachments_company_name_options = [
            {
                "fallback": "Company name options",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "company_name_options",
                "actions": [
                    {
                        "name": "company_name_list",
                        "text": "Pick a company...",
                        "type": "select",
                        "data_source": "external"
                    }
                ]
            }
        ]