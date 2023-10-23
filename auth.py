from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import google.auth
import google.auth.transport.requests
import google.oauth2.credentials

# 定义API范围
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def authorize_and_get_credentials():
    # 1. 使用OAuth 2.0授权流进行用户身份验证
    flow = InstalledAppFlow.from_client_secrets_file('ga4-project-402014-54f684c5ca17.json', SCOPES)
    credentials = flow.run_local_server(port=0)

    # 2. 使用凭证访问Google API
    service = build('analytics', 'v3', credentials=credentials)
    results = service.data().ga().get(
        ids='ga:exit407449646',
        start_date='7daysAgo',
        end_date='today',
        metrics='ga:users'
    ).execute()

    # 处理结果
    print('View (Profile): %s' % results.get('profileInfo').get('profileName'))
    print('Total Users: %s' % results.get('totalsForAllResults').get('ga:users'))

if __name__ == '__main__':
    authorize_and_get_credentials()
