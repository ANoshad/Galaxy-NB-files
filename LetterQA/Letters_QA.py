import re
import time

import pandas as pd
from django.http import HttpResponse

current_date = time.strftime("%m-%d-%Y")
current_date_check = time.strftime("%m/%d/%Y")


def QA_file(request):
    if request.method == 'POST':

        if request.FILES['letter_file'].name.endswith('.csv'):

            df = pd.read_csv(request.FILES['letter_file'])

            df = df.fillna('')

            response = ""

            # <-----------------------Check if the LetterCode is not blank-------------------------->
            LetterCode_Response = "ClientCode is correct"
            for i in df['LetterCode']:
                if i == '':
                    LetterCode_Response = 'The file has a blank LetterCode'
                    for i in df['LetterCode']:
                        if i == '':
                            df_blank_LetterCode = df[df['LetterCode'] == '']
                            df_blank_LetterCode = df_blank_LetterCode[['UnifinID', 'LetterCode']]
                            df_blank_LetterCode = df_blank_LetterCode.rename(columns={'LetterCode': 'Blank ClientCode'})
                            df_blank_LetterCode = df_blank_LetterCode.to_html()
                            LetterCode_Response = df_blank_LetterCode
                    break

            # <--------------------Check if the Letter Date has the correct dates-------------------------->
            df['LetterDate'] = pd.to_datetime(df['LetterDate']).dt.strftime('%m/%d/%Y')
            letterDate_response = 'Letterdate is correct'
            for i in df['LetterDate']:
                if i != current_date_check:
                    letterDate_response = 'The file is not from today'
                    for i in df['LetterDate']:
                        if i != current_date_check:
                            df_wrong_date = df[df['LetterDate'] != current_date_check]
                            df_wrong_date = df_wrong_date[['UnifinID', 'LetterDate']]
                            df_wrong_date = df_wrong_date.rename(columns={'LetterDate': 'Wrong Date'})
                            df_wrong_date = df_wrong_date.to_html()
                            letterDate_response = df_wrong_date
                    break

            # <-----------------Check if the MailType has only M-------------------------->
            MailType_Response = "MailType is correct"
            for i in df['MailType']:
                if i != 'M':
                    MailType_Response = 'The file has a MailType different than M'
                    for i in df['MailType']:
                        if i != 'M':
                            df_wrong_MailType = df[df['MailType'] != 'E']
                            df_wrong_MailType = df_wrong_MailType[['UnifinID', 'MailType']]
                            df_wrong_MailType = df_wrong_MailType.rename(columns={'MailType': 'Wrong MailType'})
                            df_wrong_MailType = df_wrong_MailType.to_html()
                            MailType_Response = df_wrong_MailType
                    break

            # <------------------------Check if the ClientCode should not be blank-------------------------->
            ClientCode_Response = "ClientCode is correct"
            for i in df['ClientCode']:
                if i == '':
                    ClientCode_Response = 'The file has a blank ClientCode'
                    for i in df['ClientCode']:
                        if i == '':
                            df_blank_ClientCode = df[df['ClientCode'] == '']
                            df_blank_ClientCode = df_blank_ClientCode[['UnifinID', 'ClientCode']]
                            df_blank_ClientCode = df_blank_ClientCode.rename(columns={'ClientCode': 'Blank ClientCode'})
                            df_blank_ClientCode = df_blank_ClientCode.to_html()
                            ClientCode_Response = df_blank_ClientCode
                    break

            # <---------------------Check if the OOSFlag is not blank OR NULL-------------------------->
            OOSFlag_Response = "OOSFlag is correct"
            for i in df['OOSFlag']:
                if i == '' or i == 'NULL':
                    OOSFlag_Response = 'The file has a blank OOSFlag'
                    for i in df['OOSFlag']:
                        if i == '' or i == 'NULL':
                            df_blank_OOSFlag = df[df['OOSFlag'] == '']
                            df_blank_OOSFlag = df_blank_OOSFlag[['UnifinID', 'OOSFlag']]
                            df_blank_OOSFlag = df_blank_OOSFlag.rename(columns={'OOSFlag': 'Blank OOSFlag'})
                            df_blank_OOSFlag = df_blank_OOSFlag.to_html()
                            OOSFlag_Response = df_blank_OOSFlag
                    break

            # <------------------------Check if the CRFlag is not blank OR NULL-------------------------->
            CRFlag_Response = "CRFlag is correct"
            for i in df['CRFlag']:
                if i == '' or i == 'NULL':
                    CRFlag_Response = 'The file has a blank CRFlag'
                    for i in df['CRFlag']:
                        if i == '' or i == 'NULL':
                            df_blank_CRFlag = df[df['CRFlag'] == '']
                            df_blank_CRFlag = df_blank_CRFlag[['UnifinID', 'CRFlag']]
                            df_blank_CRFlag = df_blank_CRFlag.rename(columns={'CRFlag': 'Blank CRFlag'})
                            df_blank_CRFlag = df_blank_CRFlag.to_html()
                            CRFlag_Response = df_blank_CRFlag
                    break

            # <-----------------Check if the CRNegFlag is not blank OR NULL-------------------------->
            CRNegFlag_Response = "CRNegFlag is correct"
            for i in df['CRNegFlag']:
                if i == 'NULL':
                    CRNegFlag_Response = 'The file has a blank CRNegFlag'
                    for i in df['CRNegFlag']:
                        if i == 'NULL':
                            df_blank_CRNegFlag = df[df['CRNegFlag'] == '']
                            df_blank_CRNegFlag = df_blank_CRNegFlag[['UnifinID', 'CRNegFlag']]
                            df_blank_CRNegFlag = df_blank_CRNegFlag.rename(columns={'CRNegFlag': 'Blank CRNegFlag'})
                            df_blank_CRNegFlag = df_blank_CRNegFlag.to_html()
                            CRNegFlag_Response = df_blank_CRNegFlag
                    break

            # <-----------------Validate EmailAddress column-------------------------->
            EmailAddress_Response = "EmailAddress is correct"
            for i in df['EmailAddress']:

                if re.search(r'[\(\)\+\=\]\}\[\{\\\|\;\/\?\>\<\,\'\"]', i):
                    EmailAddress_Response = 'The file has a wrong EmailAddress'
                    for i in df['EmailAddress']:
                        if re.search(r'[\(\)\+\=\]\}\[\{\\\|\;\/\?\>\<\,\'\"]', i):
                            df_wrong_EmailAddress = df[
                                df['EmailAddress'].str.contains(r'[\(\)\+\=\]\}\[\{\\\|\;\/\?\>\<\,\'\"]')]
                            df_wrong_EmailAddress = df_wrong_EmailAddress[['UnifinID', 'EmailAddress']]
                            df_wrong_EmailAddress = df_wrong_EmailAddress.rename(
                                columns={'EmailAddress': 'Wrong EmailAddress'})
                            df_wrong_EmailAddress = df_wrong_EmailAddress.to_html()
                            EmailAddress_Response = df_wrong_EmailAddress
                    break

            for i in df['EmailAddress']:
                if i == '' or i == 'NULL' or '@' not in i or '.' not in i:
                    IncorrectEmailAddress_Response = 'The file has a wrong EmailAddress'
                    for i in df['EmailAddress']:
                        if i == '' or i == 'NULL' or '@' not in i or '.' not in i:
                            df_wrong_EmailAddress = df[df['EmailAddress'] == '']
                            df_wrong_EmailAddress = df_wrong_EmailAddress[['UnifinID', 'EmailAddress']]
                            df_wrong_EmailAddress = df_wrong_EmailAddress.rename(
                                columns={'EmailAddress': 'Incorrect EmailAddress'})
                            df_wrong_EmailAddress = df_wrong_EmailAddress.to_html()
                            IncorrectEmailAddress_Response = df_wrong_EmailAddress
                    break

            return HttpResponse(
                LetterCode_Response + '<br>' +
                letterDate_response + '<br>' +
                MailType_Response + '<br>' +
                ClientCode_Response + '<br>' +
                OOSFlag_Response + '<br>' +
                CRFlag_Response + '<br>' +
                CRNegFlag_Response + '<br>' +
                EmailAddress_Response + '<br>'
            )






        else:
            return HttpResponse('File not uploaded: due to wrong extension or the wrong file date')
    else:
        return HttpResponse('Something went wrong please try again | You are not hitting the post method')
