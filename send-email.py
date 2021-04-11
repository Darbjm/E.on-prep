# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(from_email='jamesdarby1@hotmail.com',
#                to_emails='anchor.fashion.studios@gmail.com',
#                subject='testing',
#                plain_text_content='testing',
#                html_content='<strong>testing<strong>')

# try:
#     sg = SendGridAPIClient(os.environ.get('SENDGRID'))
#     res = sg.send(message)
#     print(res.statues_code)
#     print(res.body)
#     print(res.headers)
# except Exception as e:
#     print(e.message)

# SENDGRID_API_KEY = os.getenv('SENDGRID')

# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
