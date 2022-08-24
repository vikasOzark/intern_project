# import datetime
# from datetime import timedelta

# import pytz

# from google.oauth2 import service_account

# from googleapiclient.discovery import build

# service_account_email = "project@internship-project-360406.iam.gserviceaccount.com"
# SCOPES = ["https://www.googleapis.com/auth/calendar"]

# credentials = service_account.Credentials.from_service_account_file('client_secret_200284731842-0i542ral2qlshrte9dqiv7q30bdoocs0.apps.googleusercontent.com.json')
# scoped_credentials = credentials.with_scopes(SCOPES)


# def build_service():
#     service = build("calendar", "v3", credentials=scoped_credentials)
#     return service


# def create_event(doctor, discription, date):
#     service = build_service()

#     start_datetime = datetime.datetime.now(tz=pytz.utc)
#     event = (
#         service.events()
#         .insert(
#             calendarId="primary",
#             body={
#                 "summary": f'{doctor} has appointment reqeust',
#                 "description": discription,
#                 "start": {date : start_datetime.isoformat()},

#             },
#         )
#         .execute()
#     )

#     print(event)

# create_event()