import csv
from django.http import HttpResponse
import pandas as pd
import os
import glob
from datetime import datetime, timedelta

headers = (
    'RecType',
    'CltRefNumber',
    'AcctNumber',
    'CurBalance1',
    'InterestAmt',
    'Curr3',
    'Curr4',
    'Curr5',
    'Curr6',
    'Curr7',
    'Curr8',
    'Curr9',
    'CLIDLC',
    'LastPaidDate',
    'UserDate1',
    'UserDate2',
    'UserDate3',
    'OriginalCreditor',
    'LastInterest (date)',
    'InterestRate',
    'CustDivision',
    'CustDistrict',
    'CustBranch',
    'ID1',
    'ID2',
    'DeskID',
    'CustomerID',
    'ChargeOffDate',
    'DelinquencyDate',
    'Last paid amount',
    'ContractDate',
    'clidlp',
    '2_clidlc',
    'clialp',
    'clialc',
    'Previous creditor',
    'Purchased date',
    'Customer alphacode',
    'Customer company',
    'Customer name',
    'AIM Investor Group Name',
    'AIM Seller Group Name',
    'Filler',
    '2_RecType'
    '2_Number',
    '2_Master.Account',
    'Name',
    'Street1',
    'Street2',
    'City',
    'State',
    'ZipCode',
    'HomePhone',
    'WorkPhone',
    'SSN (or Tax ID)',
    'MR',
    'OtherName',
    'DOB',
    'JobName',
    'JobAddr1',
    'JobAddr2',
    'JobCSZ',
    'Spouse',
    'SpouseJobName',
    'SpouseJobAddr1',
    'SpouseJobAddr',
    'SpouseJobCSZ',
    'SpouseHomePhone',
    'SpouseWorkPhone',
    'DebtorID',
    'County',
    'Country',
    'Attorney name',
    'Attorney firm',
    'Attorney street1',
    'Attorney street2',
    'Attorney city',
    'Attorney state',
    'Attorney zipcode',
    'Attorney phone',
    'Attorney fax',
    'attorney notes',
    'Filler2',
    '3_RecType',
    'Alternate ID',
    'Charge-Off Creditor',
    'Entity',
    'PLACEMENT STATE OF RESIDENCE',
    'Received',
    'Customer',
    'Internal Account_Number',
    'File_Date',
    'TSYS_Account_Number',
    'ChargeOffAmount',
    'Merchant',
    'Merchant Category',
    'CO_PRIN',
    'CO_INT',
    'CO_FEE',
    '2_Previous Creditor',
    'Product_Type_Code',
    'Vertical_Code',
    'Brand_Name',
    'Original Creditor',
    'Original Creditor Address',
    'Previous Creditor Address',
    'Previous Creditor Purchase DT',
    'EMAIL',
    'ISSUING_BANK'

)

# headers_CACT = [
#     'CANumber',
#     'Account',
#     'Current1',
#     'Current2',
#     'Current3',
#     'Current4',
#     'Current5',
#     'Current6',
#     'Current7',
#     'Current8',
#     'Current9',
#     'CLIDLC',
#     'Last Paid Date',
#     'UserDate1',
#     'UserDate2',
#     'UserDate3',
#     'OriginalCreditor',
#     'ID1',
#     'ID2',
#     'DeskID',
#     'CustomerID',
#     'ChargeOffDate',
#     'DelinquencyDate',
#     'Last paid amount',
#     'ContractDate',
#     'clidlp',
#     'clialp',
#     'clialc',
#     'Previouscreditor',
#     # 'Assign Amount'
#
# ]
#
# headers_CD00 = [
#
#     'CD0Number',
#     'Name ',
#     'Street1 ',
#     'Street2 ',
#     'City ',
#     'State ',
#     'ZipCode ',
#     'HomePhone',
#     'WorkPhone',
#     'SSN',
#     'MR',
#     'OtherName',
#     'DOB',
#     'JobName',
#     'JobAddr1',
#     'JobAddr2',
#     'JobCSZ',
#     'Spouse',
#     'SpouseJobName',
#     'SpouseJobAddr1',
#     'SpouseJobAddr',
#     'SpouseJobCSZ',
#     'SpouseHomePhone',
#     'SpouseWorkPhone',
#     'Attorney name',
#     'Attorney firm',
#     # 'Attorney Address(Att Address1+ Att Address2)',
#     'Attorney street1',
#     'Attorney street2',
#
#     # 'Attorney CSZ (AttCityStateZip)',
#     'Attorney city',
#     'Attorney state',
#     'Attorney zipcode',
#
#     'Attorney phone',
#     'Attorney fax'
#
# ]
#
# remove_other_CACT_headers = [
#     'RecType',
#     '2_RecType',
#     '2_Number',
#     '2_RecType2_Number',
#     'Purchased date',
#     'Customer alphacode',
#     'Customer company',
#     'Customer name',
#     'AIM Investor Group Name',
#     'AIM Seller Group Name',
#     'Filler2',
#     '3_RecType',
#     '2_Previous Creditor',
#     '2_clidlc',
#     'LastInterest (date)',
#     'InterestRate',
#     'CustDivision',
#     'CustDistrict',
#     'CustBranch',
#     '2_Master.Account',
#     'Name',
#     'Street1',
#     'Street2',
#     'City',
#     'State',
#     'ZipCode',
#     'HomePhone',
#     'WorkPhone',
#     'SSN (or Tax ID)',
#     'MR',
#     'OtherName',
#     'DOB',
#     'JobName',
#     'JobAddr1',
#     'JobAddr2',
#     'JobCSZ',
#     'Spouse',
#     'SpouseJobName',
#     'SpouseJobAddr1',
#     'SpouseJobAddr',
#     'SpouseJobCSZ',
#     'SpouseHomePhone',
#     'SpouseWorkPhone',
#     'DebtorID',
#     'County',
#     'Country',
#     'Attorney name',
#     'Attorney firm',
#     'Attorney street1',
#     'Attorney street2',
#     'Attorney city',
#     'Attorney state',
#     'Attorney zipcode',
#     'Attorney phone',
#     'Attorney fax',
#     'attorney notes',
#     'Filler',
#     'debtor_number',
#     'file_number',
#     'relationship',
#     'phone_type_id',
#     'phone_status_id',
#     'on_hold',
#     'phone_number',
#     'phone_ext',
#     'phone_name',
#     'source',
#     'filler',
#     'Alternate ID',
#     'Charge-Off Creditor',
#     'Entity',
#     'PLACEMENT STATE OF RESIDENCE',
#     'Received',
#     'Customer',
#     'Internal Account_Number',
#     'File_Date',
#     'TSYS_Account_Number',
#     'ChargeOffAmount',
#     'Merchant',
#     'Merchant Category',
#     'CO_PRIN',
#     'CO_INT',
#     'CO_FEE',
#     'Previous Creditor',
#     'Product_Type_Code',
#     'Vertical_Code',
#     'Brand_Name',
#     'Original Creditor',
#     'Original Creditor Address',
#     'Previous Creditor Address',
#     'Previous Creditor Purchase DT',
#     'EMAIL',
#     'ISSUING_BANK'
#
# ]
#
# remove_other_CD00_headers = [
#     'RecType',
#     'CltRefNumber',
#     'AcctNumber',
#     'CurBalance1',
#     'InterestAmt',
#     'Curr3',
#     'Curr4',
#     'Curr5',
#     'Curr6',
#     'Curr7',
#     'Curr8',
#     'Curr9',
#     'CLIDLC',
#     'LastPaidDate',
#     'UserDate1',
#     'UserDate2',
#     'UserDate3',
#     'OriginalCreditor',
#     'LastInterest (date)',
#     'InterestRate',
#     'CustDivision',
#     'CustDistrict',
#     'CustBranch',
#     'ID1',
#     'ID2',
#     'DeskID',
#     'CustomerID',
#     'ChargeOffDate',
#     'DelinquencyDate',
#     'Last paid amount',
#     'ContractDate',
#     'clidlp',
#     '2_clidlc',
#     'clialp',
#     'clialc',
#     'Previous creditor',
#     'Purchased date',
#     'Customer alphacode',
#     'Customer company',
#     'Customer name',
#     'AIM Investor Group Name',
#     'AIM Seller Group Name',
#     'Filler',
#     '2_RecType',
#     '2_Master.Account',
#     'DebtorID',
#     'County',
#     'Country',
#     'attorney notes',
#     'Filler2',
#     '3_RecType',
#     'Alternate ID',
#     'Charge-Off Creditor',
#     'Entity',
#     'PLACEMENT STATE OF RESIDENCE',
#     'Received',
#     'Customer',
#     'Internal Account_Number',
#     'File_Date',
#     'TSYS_Account_Number',
#     'ChargeOffAmount',
#     'Merchant',
#     'Merchant Category',
#     'CO_PRIN',
#     'CO_INT',
#     'CO_FEE',
#     '2_Previous Creditor',
#     'Product_Type_Code',
#     'Vertical_Code',
#     'Brand_Name',
#     'Original Creditor',
#     'Original Creditor Address',
#     'Previous Creditor Address',
#     'Previous Creditor Purchase DT',
#     'EMAIL',
#     'ISSUING_BANK'
#
# ]

remove_unnecessary_columns = [

    'RecType_x',
    'Curr4_x',
    'Curr5_x',
    'Curr6_x',
    'Curr7_x',
    'Curr8_x',
    'Curr9_x',
    'LastInterest (date)_x',
    'InterestRate_x',
    'CustDivision_x',
    'CustDistrict_x',
    'CustBranch_x',
    '2_clidlc_x',
    'Purchased date_x',
    'Customer alphacode_x',
    'Customer company_x',
    'Customer name_x',
    'AIM Investor Group Name_x',
    'AIM Seller Group Name_x',
    'Filler_x',
    '2_RecType2_Number_x',
    'Name_x',
    'County_x',
    'Country_x',
    'Attorney name_x',
    '3_RecType_x',
    'Alternate ID_x',
    'Charge-Off Creditor_x',
    'Entity_x',
    'PLACEMENT STATE OF RESIDENCE_x',
    'Received_x',
    'Customer_x',
    'Internal Account_Number_x',
    'File_Date_x',
    'TSYS_Account_Number_x',
    'ChargeOffAmount_x',
    'Merchant_x',
    'Merchant Category_x',
    'CO_PRIN_x',
    'CO_INT_x',
    'CO_FEE_x',
    '2_Previous Creditor_x',
    'Product_Type_Code_x',
    'Vertical_Code_x',
    'Brand_Name_x',
    'Original Creditor_x',
    'Original Creditor Address_x',
    'Previous Creditor Address_x',
    'Previous Creditor Purchase DT_x',
    'EMAIL_x',
    'ISSUING_BANK_x',

    'UserDate2_x',
    'UserDate3_x',
    'ID1_x',
    'ID2_x',
    'DeskID_x',

    # 2nd x
    '2_Master.Account_x',
    'Street1_x',
    'Street2_x',
    'City_x',
    'State_x',
    'ZipCode_x',
    'HomePhone_x',
    'WorkPhone_x',
    'SSN (or Tax ID)_x',
    'MR_x',
    'OtherName_x',
    'DOB_x',
    'JobName_x',
    'JobAddr1_x',
    'JobAddr2_x',
    'JobCSZ_x',
    'Spouse_x',
    'SpouseJobName_x',
    'SpouseJobAddr1_x',
    'SpouseJobAddr_x',
    'SpouseJobCSZ_x',
    'SpouseHomePhone_x',
    'SpouseWorkPhone_x',
    'DebtorID_x',
    'Attorney firm_x',
    'Attorney street1_x',
    'Attorney street2_x',
    'Attorney city_x',
    'Attorney state_x',
    'Attorney zipcode_x',
    'Attorney phone_x',
    'Attorney fax_x',
    'attorney notes_x',
    'Filler2_x',

    # start removing y
    'RecType_y',
    'AcctNumber_y',
    'Customer name_y',
    'AIM Investor Group Name_y',
    'AIM Seller Group Name_y',
    'Filler_y',
    '2_RecType2_Number_y',
    '2_Master.Account_y',
    'Name_y',
    'Street1_y',
    'Street2_y',
    'City_y',
    'State_y',
    'ZipCode_y',
    'HomePhone_y',
    'WorkPhone_y',
    'SSN (or Tax ID)_y',
    'MR_y',
    'OtherName_y',
    'DOB_y',
    'JobName_y',
    'JobAddr1_y',
    'JobAddr2_y',
    'JobCSZ_y',
    'Spouse_y',
    'SpouseJobName_y',
    'SpouseJobAddr1_y',
    'SpouseJobAddr_y',
    'SpouseJobCSZ_y',
    'SpouseHomePhone_y',
    'SpouseWorkPhone_y',
    'DebtorID_y',
    'County_y',
    'Country_y',
    'Attorney name_y',
    'Attorney firm_y',
    'Attorney street1_y',
    'Attorney street2_y',
    'Attorney city_y',
    'Attorney state_y',
    'Attorney zipcode_y',
    'Attorney phone_y',
    'Attorney fax_y',
    'attorney notes_y',
    'Filler2_y',
    '3_RecType_y',
    'Alternate ID_y',
    'Charge-Off Creditor_y',
    'Entity_y',
    'PLACEMENT STATE OF RESIDENCE_y',
    'Received_y',
    'Customer_y',
    'Internal Account_Number_y',
    'File_Date_y',
    'TSYS_Account_Number_y',
    'ChargeOffAmount_y',
    'Merchant_y',
    'Merchant Category_y',
    'CO_PRIN_y',
    'CO_INT_y',
    'CO_FEE_y',
    '2_Previous Creditor_y',
    'Product_Type_Code_y',
    'Vertical_Code_y',
    'Brand_Name_y',
    'Original Creditor_y',
    'Original Creditor Address_y',
    'Previous Creditor Address_y',
    'Previous Creditor Purchase DT_y',
    'EMAIL_y',
    'ISSUING_BANK_y',

    # 2nd y
    'ChargeOffDate_y',
    'DelinquencyDate_y',
    # 'CustomerID_y',

    # removal for CD01
    'CDRecType',
    'CDCustomerID',
    'CDChargeOffDate',
    'CDDelinquencyDate',
    'CDLast paid amount',
    'CDContractDate',
    'CDclidlp',
    'CD2_clidlc',
    'CDclialp',
    'CDclialc',
    'CDPrevious creditor',
    'CDPurchased date',
    'CDCustomer alphacode',
    'CDCustomer company',
    'CDCustomer name',
    'CDAIM Investor Group Name',
    'CDAIM Seller Group Name',
    'CDFiller',
    'CD2_RecType2_Number',
    'CD2_Master.Account',
    'CDName',
    'CDStreet1',
    'CDStreet2',
    'CDCity',
    'CDState',
    'CDZipCode',
    'CDHomePhone',
    'CDWorkPhone',
    'CDSSN (or Tax ID)',
    'CDMR',
    'CDOtherName',
    'CDDOB',
    'CDJobName',
    'CDJobAddr1',
    'CDJobAddr2',
    'CDJobCSZ',
    'CDSpouse',
    'CDSpouseJobName',
    'CDSpouseJobAddr1',
    'CDSpouseJobAddr',
    'CDSpouseJobCSZ',
    'CDSpouseHomePhone',
    'CDSpouseWorkPhone',
    'CDDebtorID',
    'CDCounty',
    'CDCountry',
    'CDAttorney name',
    'CDAttorney firm',
    'CDAttorney street1',
    'CDAttorney street2',
    'CDAttorney city',
    'CDAttorney state',
    'CDAttorney zipcode',
    'CDAttorney phone',
    'CDAttorney fax',
    'CDattorney notes',
    'CDFiller2',
    'CD3_RecType',
    'CDAlternate ID',
    'CDCharge-Off Creditor',
    'CDEntity',
    'CDPLACEMENT STATE OF RESIDENCE',
    'CDReceived',
    'CDCustomer',
    'CDInternal Account_Number',
    'CDFile_Date',
    'CDTSYS_Account_Number',
    'CDChargeOffAmount',
    'CDMerchant',
    'CDMerchant Category',
    'CDCO_PRIN',
    'CDCO_INT',
    'CDCO_FEE',
    'CD2_Previous Creditor',
    'CDProduct_Type_Code',
    'CDVertical_Code',
    'CDBrand_Name',
    'CDOriginal Creditor',
    'CDOriginal Creditor Address',
    'CDPrevious Creditor Address',
    'CDPrevious Creditor Purchase DT',
    'CDEMAIL',
    'CDISSUING_BANK',

    '2_JobName',
    '2_JobAddr1',
    '2_JobAddr2',
    '2_JobCSZ',
    '2_Spouse',
    '2_SpouseJobName',
    '2_SpouseJobAddr1',
    '2_SpouseJobAddr',
    '2_SpouseJobCSZ',
    '2_SpouseHomePhone',
    '2_SpouseWorkPhone',
    'CltRefNumber',
    'LastPaidDate',
    'CMNumber',

    'CltRefNumber_y',
    'LastPaidDate_y',

]

headers_updated = (

    'CANumber',
    'AcctNumber',
    'Current1',
    'Current2',
    'Current3',
    # 'Current4',
    # 'Current5',
    # 'Current6',
    # 'Current7',
    # 'Current8',
    # 'Current9',
    'CLIDLC',
    'Last Paid Date',
    'UserDate1',
    #  'UserDate2',
    # 'UserDate3',
    'OriginalCreditor',
    # 'ID1',
    # 'ID2',
    # 'DeskID',
    'CustomerID',
    'ChargeOffDate',
    'DelinquencyDate',
    'Last paid amount',
    'ContractDate',
    'clidlp',
    'clialp',
    'clialc',
    'Previouscreditor',
    'Assign Amount',

    # CDO
    # 'CD0Number',
    'Name ',
    'Street1 ',
    'Street2 ',
    'City ',
    'State ',
    'ZipCode ',
    'HomePhone',
    'WorkPhone',
    'SSN',
    'MR',
    # 'OtherName',
    'DOB',
    'JobName',
    'JobAddr1',
    'JobAddr2',
    'JobCSZ',
    'Spouse',
    'SpouseJobName',
    'SpouseJobAddr1',
    'SpouseJobAddr',
    'SpouseJobCSZ',
    'SpouseHomePhone',
    'SpouseWorkPhone',
    'DebtorID',

    'Attorney name',
    'Attorney firm',
    'Attorney street1',
    'Attorney street2',
    'Attorney city',
    'Attorney state',
    'Attorney zipcode',
    'Attorney phone',
    'Attorney fax',
    'attorney notes',
    'Attorney Address',
    'Attorney CSZ',

    # remove for CD01
    'CDRecType',
    'CD1Number',
    '2_Name ',
    '2_Street1 ',
    '2_Street2 ',
    '2_City ',
    '2_State ',
    '2_ZipCode ',
    '2_HomePhone',
    '2_WorkPhone',
    '2_SSN',
    '2_MR',
    '2_OtherName',
    '2_DOB',
    '2_JobName',
    '2_JobAddr1',
    '2_JobAddr2',
    '2_JobCSZ',
    '2_Spouse',
    '2_SpouseJobName',
    '2_SpouseJobAddr1',
    '2_SpouseJobAddr',
    '2_SpouseJobCSZ',
    '2_SpouseHomePhone',
    '2_SpouseWorkPhone',
    'CDCustomerID',
    'CDChargeOffDate',
    'CDDelinquencyDate',
    'CDLast paid amount',
    'CDContractDate',
    'CDclidlp',
    'CD2_clidlc',
    'CDclialp',
    'CDclialc',
    'CDPrevious creditor',
    'CDPurchased date',
    'CDCustomer alphacode',
    'CDCustomer company',
    'CDCustomer name',
    'CDAIM Investor Group Name',
    'CDAIM Seller Group Name',
    'CDFiller',
    'CD2_RecType2_Number',
    'CD2_Master.Account',
    'CDName',
    'CDStreet1',
    'CDStreet2',
    'CDCity',
    'CDState',
    'CDZipCode',
    'CDHomePhone',
    'CDWorkPhone',
    'CDSSN (or Tax ID)',
    'CDMR',
    'CDOtherName',
    'CDDOB',
    'CDJobName',
    'CDJobAddr1',
    'CDJobAddr2',
    'CDJobCSZ',
    'CDSpouse',
    'CDSpouseJobName',
    'CDSpouseJobAddr1',
    'CDSpouseJobAddr',
    'CDSpouseJobCSZ',
    'CDSpouseHomePhone',
    'CDSpouseWorkPhone',
    'CDDebtorID',
    'CDCounty',
    'CDCountry',
    'CDAttorney name',
    'CDAttorney firm',
    'CDAttorney street1',
    'CDAttorney street2',
    'CDAttorney city',
    'CDAttorney state',
    'CDAttorney zipcode',
    'CDAttorney phone',
    'CDAttorney fax',
    'CDattorney notes',
    'CDFiller2',
    'CD3_RecType',
    'CDAlternate ID',
    'CDCharge-Off Creditor',
    'CDEntity',
    'CDPLACEMENT STATE OF RESIDENCE',
    'CDReceived',
    'CDCustomer',
    'CDInternal Account_Number',
    'CDFile_Date',
    'CDTSYS_Account_Number',
    'CDChargeOffAmount',
    'CDMerchant',
    'CDMerchant Category',
    'CDCO_PRIN',
    'CDCO_INT',
    'CDCO_FEE',
    'CD2_Previous Creditor',
    'CDProduct_Type_Code',
    'CDVertical_Code',
    'CDBrand_Name',
    'CDOriginal Creditor',
    'CDOriginal Creditor Address',
    'CDPrevious Creditor Address',
    'CDPrevious Creditor Purchase DT',
    'CDEMAIL',
    'CDISSUING_BANK',

)

remove_att_columns = [

    # Remove Att columns
    'Attorney street1',
    'Attorney street2',
    'Attorney city',
    'Attorney state',
    'Attorney zipcode',
    'attorney notes',

]

define_CMIS_columns = (

    'ACTNumber',
    'CANumber',
    'PI_ALT_ID',

    'Alternate ID',
    'Charge-Off Creditor',
    'Entity',
    'PLACEMENT STATE OF RESIDENCE',
    'Received',

    'Internal Account_Number',
    'File_Date',
    'TSYS_Account_Number',
    'ChargeOffAmount',
    'Merchant',
    'Merchant Category',
    'CO_PRIN',
    'CO_INT',
    'CO_FEE',
    'Product_Type_Code',
    'Vertical_Code',
    'Brand_Name',
    'OriginalCreditor',
    'OriginalCreditorAddress',
    'Previous Creditor',
    'PreviCreditorAddress',
    'PrevCreditorPurchaseDT',
    'EMAIL',
    'ISSUING_BANK',
    'Buyer1Name',
    'Buyer1Address',
    'Buyer1PurchaseDate',
    'ReceivedDate',
    'Retailer',
    'Customer',

)

define_CDEC_Columns = (
    'CANumber',
    'CDNumber',
    'State',
    'Date of Death',
)

remove_extra_columns = (

    'Current4',
    'Current5',
    'Current6',
    'Current7',
    'Current8',
    'Current9',

)


def process_file(request):
    if request.method == "POST":
        getfilename = request.FILES["galaxy_filename"].name

        df = pd.read_csv(request.FILES["galaxy_filename"], sep="|", names=headers)

        df = pd.DataFrame(df)
        df = df.fillna("")

        # FILE CREATION
        #
        get_CACT_data_row = df[df['RecType'] == "CACT"]
        get_CD00_data_row = df[df['RecType'] == "CD00"]
        get_CD01_data_row = df[df['RecType'] == "CD01"]
        get_CMIS_data_row = df[df['RecType'] == "CMIS"]
        get_CDEC_data_row = df[df['RecType'] == "CDEC"]
        get_CBKP_data_row = df[df['RecType'] == "CBKP"]
        get_CRegF_data_row = df[df['RecType'] == "RegF"]

        dataframe_CACT = pd.DataFrame(get_CACT_data_row, index=None)

        # dataframe_CACT['LastPaidDate'] = pd.to_datetime(dataframe_CACT['LastPaidDate'], format='%Y%m%d')
        # dataframe_CACT['UserDate1'] = dataframe_CACT['UserDate1'].astype(str)
        # if dataframe_CACT['UserDate1'].str.endswith('.0'):
        #dataframe_CACT['UserDate1'] = dataframe_CACT['UserDate1']
        dataframe_CACT['UserDate1'] = pd.to_datetime(dataframe_CACT['UserDate1'],  errors='coerce', format='%Y%m%d',
                                                     yearfirst=True).dt.strftime('%m/%d/%Y')

        # dataframe_CACT['UserDate1'] = pd.to_datetime(dataframe_CACT['UserDate1'], format='%mm%dd%YYYY')
        # dataframe_CACT['UserDate2'] = pd.to_datetime(dataframe_CACT['UserDate2'], format='%Y%m%d')
        # dataframe_CACT['UserDate3'] = pd.to_datetime(dataframe_CACT['UserDate3'], format='%Y%m%d')
        # dataframe_CACT['ChargeOffDate'] = pd.to_datetime(dataframe_CACT['ChargeOffDate'], format='%Y%m%d',
        #                                                  yearfirst=True).dt.strftime('%m/%d/%Y')
        dataframe_CACT['DelinquencyDate'] = dataframe_CACT['DelinquencyDate'].astype(str)

        dataframe_CACT['DelinquencyDate'] = dataframe_CACT['DelinquencyDate'].str.replace('.0', '')
        # dataframe_CACT['DelinquencyDate'] = dataframe_CACT['DelinquencyDate'].str.replace('', '30001212 00:00:00')
        dataframe_CACT['DelinquencyDate'] = pd.to_datetime(dataframe_CACT['DelinquencyDate'], errors='coerce',
                                                           format='%Y%m%d')
        dataframe_CACT['DelinquencyDate'] = dataframe_CACT['DelinquencyDate'].dt.strftime('%m/%d/%Y')
        # dataframe_CACT['DelinquencyDate'] = pd.to_datetime(dataframe_CACT['DelinquencyDate'], format='%Y%m%d %H:%M:%S',
        #                                                        yearfirst=True).dt.strftime('%m/%d/%Y')

        # dataframe_CACT['ContractDate'] = pd.to_datetime(dataframe_CACT['ContractDate'], format='%Y%m%d',
        #                                                 yearfirst=True).dt.strftime('%m/%d/%Y')
        # dataframe_CACT['clidlp'] = dataframe_CACT['clidlp'].astype(int)
        # dataframe_CACT = dataframe_CACT.astype({'clidlp': 'int'})
        dataframe_CACT['clidlp'] = pd.to_datetime(dataframe_CACT['clidlp'], errors='coerce', format='%Y%m%d.0',
                                                  yearfirst=True).dt.strftime('%m/%d/%Y')

    # else:
    #     dataframe_CACT['clidlp'] = ''

    # data_userdate1 = dataframe_CACT['UserDate1']

    # dataframe_CACT['UserDate1'] = dataframe_CACT['UserDate1'].astype('datetime64[ns]')
    # dataframe_CACT['UserDate1'] = datetime(year=data_userdate1[0:4], month=data_userdate1[4:6], day=data_userdate1[6:8])
    # dataframe_CACT['UserDate1'] = dataframe_CACT['UserDate1'].dt.strftime("%m-%d-%Y")
    # dataframe_CACT['ID2'] = dataframe_CACT['ID2'].astype(int)
    dataframe_CACT['ChargeOffDate'] = dataframe_CACT['ChargeOffDate'].astype(int)
    dataframe_CACT['CurBalance1'] = dataframe_CACT['CurBalance1'].astype(float)
    dataframe_CACT['CurBalance1'] = dataframe_CACT['CurBalance1'].astype(float)
    dataframe_CACT['InterestAmt'] = dataframe_CACT['InterestAmt'].astype(float)
    dataframe_CACT['Curr3'] = dataframe_CACT['Curr3'].astype(float)
    dataframe_CACT['Curr4'] = dataframe_CACT['Curr4'].astype(float)
    dataframe_CACT['Curr5'] = dataframe_CACT['Curr5'].astype(float)
    dataframe_CACT['Curr6'] = dataframe_CACT['Curr6'].astype(float)
    dataframe_CACT['Curr7'] = dataframe_CACT['Curr7'].astype(float)
    dataframe_CACT['Curr8'] = dataframe_CACT['Curr8'].astype(float)
    dataframe_CACT['Curr9'] = dataframe_CACT['Curr9'].astype(float)

    dataframe_CACT['Assign Amount'] = round(dataframe_CACT['CurBalance1'].astype(float), 2) + round(
        dataframe_CACT['InterestAmt'].astype(float),
        2) + \
                                      round(dataframe_CACT['Curr3'].astype(float), 2) + round(
        dataframe_CACT['Curr4'].astype(float), 2) + round(
        dataframe_CACT['Curr5'].astype(float), 2) + \
                                      round(dataframe_CACT['Curr6'].astype(float), 2) + round(
        dataframe_CACT['Curr7'].astype(float), 2) + round(
        dataframe_CACT['Curr8'].astype(float), 2) + \
                                      round(dataframe_CACT['Curr9'].astype(float), 2)

    dataframe_CACT['Assign Amount'] = round(dataframe_CACT['Assign Amount'].astype(float), 2)
    # dataframe_CACT = dataframe_CACT.loc[:, ~dataframe_CACT.columns.isin(remove_other_CACT_headers)]
    # dataframe_CACT.columns = headers_CACT

    dataframe_CD00 = pd.DataFrame(get_CD00_data_row, index=None)

    # dataframe_CD00['UserDate1'] = dataframe_CD00['UserDate1'].astype(str)
    # dataframe_CD00['UserDate1'] = dataframe_CD00['UserDate1'].str.replace('.0','')
    # dataframe_CD00['UserDate1'] = dataframe_CD00['UserDate1'].astype(str)
    dataframe_CD00['UserDate1'] = dataframe_CD00['UserDate1'].astype(str)
    dataframe_CD00['UserDate1'] = dataframe_CD00['UserDate1'].str.replace('.0', '')
    dataframe_CD00['UserDate1'] = pd.to_datetime(dataframe_CD00['UserDate1'], format='%Y%m%d', errors='coerce')
    dataframe_CD00['UserDate1'] = dataframe_CD00['UserDate1'].dt.strftime('%m/%d/%Y')

    dataframe_CD00['clidlp'] = dataframe_CD00['clidlp'].astype(str)
    dataframe_CD00['2_clidlc'] = dataframe_CD00['2_clidlc'].astype(str)
    dataframe_CD00['clialp'] = dataframe_CD00['clialp'].astype(str)
    dataframe_CD00['clialc'] = dataframe_CD00['clialc'].astype(str)
    dataframe_CD00['Previous creditor'] = dataframe_CD00['Previous creditor'].astype(str)

    dataframe_CD00['UserDate1'] = pd.to_datetime(dataframe_CD00['UserDate1'], format='%m/%d/%Y',
                                                 yearfirst=True).dt.strftime('%Y%m%d')

    dataframe_CD00['Attorney Address'] = dataframe_CD00['clidlp'] + ' ' + dataframe_CD00['2_clidlc']
    dataframe_CD00['Attorney CSZ'] = dataframe_CD00['clialp'] + ' ' + dataframe_CD00['clialc'] + ' ' + \
                                     dataframe_CD00['Previous creditor']

    # dataframe_CD00= dataframe_CD00.loc[:, ~dataframe_CD00.columns.isin(remove_other_CACT_headers)]
    # dataframe_CD00.columns = headers_CD00

    # empty_dataframe_CD00 = pd.DataFrame()

    # dataframe_CD00.rename(columns=dataframe_CD00.iloc[0]).drop(df.index[0])
    # dataframe_CD00 = dataframe_CD00.loc[:, ~dataframe_CD00.index.isin(remove_other_CD00_headers)]
    # dataframe_CD00.columns = headers_CD00

    dataframe_CD01 = pd.DataFrame(get_CD01_data_row, index=None)

    dataframe_CMIS = pd.DataFrame(get_CMIS_data_row, index=None)
    # dataframe_CMIS['PI_ALT_ID'] = ""
    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('PI_ALT_ID')]

    if len(CMIS_data) < 1:
        CMIS_data['CltRefNumber'] = dataframe_CACT['CltRefNumber']
    else:
        CMIS_data['CltRefNumber'] = CMIS_data['CltRefNumber']

    # CMIS_data['AcctNumber'] = dataframe_CACT['CltRefNumber']
    CMIS_data_PIALTID = CMIS_data[['AcctNumber', 'CltRefNumber', 'InterestAmt']]
    CMIS_data_PIALTID = pd.DataFrame(CMIS_data_PIALTID)
    CMIS_data_PIALTID.fillna('')
    #
    # CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.contains('Alternate ID')]
    # CMIS_data_AlternateID = CMIS_data[['AcctNumber', 'CltRefNumber', 'InterestAmt']]
    # CMIS_data_AlternateID = pd.DataFrame(CMIS_data_AlternateID)
    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Alternate ID')]
    CMIS_data_AlternateID = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_AlternateID = pd.DataFrame(CMIS_data_AlternateID)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.startswith('Charge-Off Creditor')]
    CMIS_data_ChgOffCrd = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_ChgOffCrd = pd.DataFrame(CMIS_data_ChgOffCrd)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Entity')]
    CMIS_data_Entity = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_Entity = pd.DataFrame(CMIS_data_Entity)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('PLACEMENT STATE OF RESIDENCE')]
    CMIS_data_PSoR = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_PSoR = pd.DataFrame(CMIS_data_PSoR)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Received')]
    # CMIS_data['InterestAmt'] = pd.to_datetime(CMIS_data['InterestAmt'], format='%Y-%m-%d').dt.strftime(
    #     '%m/%d/%Y')
    CMIS_data_Received = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_Received = pd.DataFrame(CMIS_data_Received)

    # CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.contains('Customer')]
    # CMIS_Customer = CMIS_data[['CltRefNumber', 'InterestAmt']]
    # CMIS_Customer = pd.DataFrame(CMIS_Customer)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Internal Account_Number')]
    CMIS_data_IAN = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_IAN = pd.DataFrame(CMIS_data_IAN)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('File_Date')]
    CMIS_data['InterestAmt'] = pd.to_datetime(CMIS_data['InterestAmt'], format='%m/%d/%Y %H:%M:%S AM').dt.strftime(
        '%m/%d/%Y')
    CMIS_data_File_Date = CMIS_data[['CltRefNumber', 'InterestAmt']]

    # CMIS_data_File_Date = CMIS_data_File_Date['InterestAmt'].astype({'date': 'datetime64[ns]'})
    # CMIS_data_File_Date = CMIS_data_File_Date['InterestAmt'].dt.strftime('%m/%d/%Y')
    CMIS_data_File_Date = pd.DataFrame(CMIS_data_File_Date)
    # CMIS_data_File_Date['InterestAmt'] = pd.to_datetime(CMIS_data_File_Date['InterestAmt'], format='%m%dd%YYYY  %H:%M:%S').dt.date
    # CMIS_data_File_Date['InterestAmt'] = CMIS_data_File_Date['InterestAmt'].dt.date
    # CMIS_data_File_Date['InterestAmt'] = pd.to_datetime(CMIS_data_File_Date['InterestAmt'], format='%m%d%YY')

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('TSYS_Account_Number')]
    CMIS_data_TSYS_AN = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_TSYS_AN = pd.DataFrame(CMIS_data_TSYS_AN)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('ChargeOffAmount')]
    CMIS_data_ChgOffAmt = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_ChgOffAmt = pd.DataFrame(CMIS_data_ChgOffAmt)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Merchant')]
    CMIS_data_Merchant = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_Merchant = pd.DataFrame(CMIS_data_Merchant)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Merchant Category')]
    CMIS_data_Merchant_Ctg = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_Merchant_Ctg = pd.DataFrame(CMIS_data_Merchant_Ctg)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('CO_PRIN')]
    CMIS_data_CO_PRIN = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_CO_PRIN = pd.DataFrame(CMIS_data_CO_PRIN)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('CO_INT')]
    CMIS_data_CO_INT = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_CO_INT = pd.DataFrame(CMIS_data_CO_INT)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('CO_FEE')]
    CMIS_data_CO_FEE = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_CO_FEE = pd.DataFrame(CMIS_data_CO_FEE)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Product_Type_Code')]
    CMIS_data_PrvTypCode = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_PrvTypCode = pd.DataFrame(CMIS_data_PrvTypCode)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Vertical_Code')]
    CMIS_data_VrtCode = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_VrtCode = pd.DataFrame(CMIS_data_VrtCode)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Brand_Name')]
    CMIS_data_BrdName = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_BrdName = pd.DataFrame(CMIS_data_BrdName)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Original Creditor')]
    CMIS_data_OrgCrd = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_OrgCrd = pd.DataFrame(CMIS_data_OrgCrd)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Original Creditor Address')]
    CMIS_data_OrgCrdAdr = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_OrgCrdAdr = pd.DataFrame(CMIS_data_OrgCrdAdr)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Previous Creditor')]
    CMIS_data_PrvCrd = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_PrvCrd = pd.DataFrame(CMIS_data_PrvCrd)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Previous Creditor Address')]
    CMIS_data_PrvCrdAdr = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_PrvCrdAdr = pd.DataFrame(CMIS_data_PrvCrdAdr)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.match('Previous Creditor Purchase DT')]
    CMIS_data['InterestAmt'] = pd.to_datetime(CMIS_data['InterestAmt'], format='%m/%d/%Y').dt.strftime('%m/%d/%Y')
    CMIS_data_PrvCrdAdrDT = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_PrvCrdAdrDT = pd.DataFrame(CMIS_data_PrvCrdAdrDT)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('EMAIL') &
                               dataframe_CMIS['InterestAmt'].str.contains('@', '.com')]
    CMIS_data_Email = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_Email = pd.DataFrame(CMIS_data_Email)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('ISSUING_BANK')]
    CMIS_data_IssBank = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_IssBank = pd.DataFrame(CMIS_data_IssBank)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Buyer1 Name')]
    CMIS_data_ByrName = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_ByrName = pd.DataFrame(CMIS_data_ByrName)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Buyer1 Address')]
    CMIS_data_ByrAdr = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_ByrAdr = pd.DataFrame(CMIS_data_ByrAdr)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Buyer1 Purchase Date')]
    CMIS_data_ByrPrchDate = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_ByrPrchDate = pd.DataFrame(CMIS_data_ByrPrchDate)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Received Date')]
    CMIS_data_RcdDate = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_RcdDate = pd.DataFrame(CMIS_data_RcdDate)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Retailer')]
    CMIS_data_Retailer = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_data_Retailer = pd.DataFrame(CMIS_data_Retailer)

    CMIS_data = dataframe_CMIS[dataframe_CMIS['CurBalance1'].str.endswith('Customer')]
    CMIS_Customer = CMIS_data[['CltRefNumber', 'InterestAmt']]
    CMIS_Customer = pd.DataFrame(CMIS_Customer)

    final_dataframe_CMIS = pd.merge(CMIS_data_PIALTID, CMIS_data_AlternateID, on='CltRefNumber', how='outer')
    # final_dataframe_CMIS = pd.merge(CMIS_data_PIALTID, CMIS_data_AlternateID, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_ChgOffCrd, on='CltRefNumber', how='outer')
    # final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_ChgOffCrd, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_Entity, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_PSoR, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_Received, on='CltRefNumber', how='outer')
    #
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_IAN, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_File_Date, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_TSYS_AN, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_ChgOffAmt, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_Merchant, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_Merchant_Ctg, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_CO_PRIN, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_CO_INT, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_CO_FEE, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_PrvTypCode, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_VrtCode, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_BrdName, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_OrgCrd, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_OrgCrdAdr, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_PrvCrd, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_PrvCrdAdr, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_PrvCrdAdrDT, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_Email, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_IssBank, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_ByrName, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_ByrAdr, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_ByrPrchDate, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_RcdDate, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_data_Retailer, on='CltRefNumber', how='outer')
    final_dataframe_CMIS = pd.merge(final_dataframe_CMIS, CMIS_Customer, on='CltRefNumber', how='outer')

    # check_Alternate_ID = 'Alternate ID' in set(dataframe_CMIS['CurBalance1']

    final_dataframe_CMIS = final_dataframe_CMIS.fillna("")

    final_dataframe_CMIS.columns = define_CMIS_columns

    # empty_dataframe_CMIS['Entity'] = df_Entity['InterestAmt']
    # empty_dataframe_CMIS['PLACEMENT STATE OF RESIDENCE'] = df_PSoR['InterestAmt']
    # empty_dataframe_CMIS['Received'] = df_Received['InterestAmt']
    # empty_dataframe_CMIS['Customer'] = df_Customer['InterestAmt']
    # empty_dataframe_CMIS['Internal Account_Number'] = df_IAN['InterestAmt']
    # empty_dataframe_CMIS['File_Date'] = df_File_Date['InterestAmt']
    # empty_dataframe_CMIS['TSYS_Account_Number'] = df_TYAN['InterestAmt']
    # empty_dataframe_CMIS['ChargeOffAmount'] = df_ChgOffAmt['InterestAmt']
    # empty_dataframe_CMIS['Merchant'] = df_Merchant['InterestAmt']
    # empty_dataframe_CMIS['Merchant Category'] = df_MerCtg['InterestAmt']
    # empty_dataframe_CMIS['CO_PRIN'] = df_CoPrin['InterestAmt']
    # empty_dataframe_CMIS['CO_INT'] = df_CoInt['InterestAmt']
    # empty_dataframe_CMIS['CO_FEE'] = df_CoFee['InterestAmt']
    # empty_dataframe_CMIS['Previous Creditor'] = df_PrvCrd['InterestAmt']
    # empty_dataframe_CMIS['Product_Type_Code'] = df_PrdTypeCod['InterestAmt']
    # empty_dataframe_CMIS['Vertical_Code'] = df_VrtCode['InterestAmt']
    # empty_dataframe_CMIS['Brand_Name'] = df_BrandName['InterestAmt']
    # empty_dataframe_CMIS['Original Creditor'] = df_OrgCrd['InterestAmt']
    # empty_dataframe_CMIS['Original Creditor Address'] = df_OrgCrdAdr['InterestAmt']
    # empty_dataframe_CMIS['Previous Creditor Address'] = df_PrvCrdAdr['InterestAmt']
    # empty_dataframe_CMIS['Previous Creditor Purchase DT'] = df_PrvCrdAdrDT['InterestAmt']
    # #empty_dataframe_CMIS['EMAIL'] = df_Email['InterestAmt']
    # empty_dataframe_CMIS['ISSUING_BANK'] = df_IssBank['InterestAmt']
    check_value = dataframe_CACT['CltRefNumber']
    # dataframe_CDEC = pd.DataFrame(get_CDEC_data_row, index=None)
    #
    #
    #
    # dataframe_CDEC['CANumber'] = check_value
    # dataframe_CDEC['CDNumber'] = check_value
    # dataframe_CDEC['CDState'] = ""
    # dataframe_CDEC['Date of Death'] = ""
    #
    # dataframe_CDEC = dataframe_CDEC[['CANumber', 'CDNumber', 'CDState', 'Date of Death']]
    # dataframe_CDEC.columns = define_CDEC_Columns
    # #
    # #
    # #
    # dataframe_CBKP = pd.DataFrame(get_CBKP_data_row, index=None)
    #
    # dataframe_CBKP['CANumber'] = check_value
    # dataframe_CBKP['CBNumber'] = check_value
    # dataframe_CBKP['Chapter'] = ""
    # dataframe_CBKP['Date Filed'] = ""
    # dataframe_CBKP['Case Number'] = ""
    # dataframe_CBKP['Court District'] = ""
    # dataframe_CBKP['Status'] = ""
    #
    # dataframe_CBKP = dataframe_CBKP[
    #     ['CANumber', 'CBNumber', 'Chapter', 'Date Filed', 'Case Number', 'Court District', 'Status']]

    #
    #
    #
    #
    #
    dataframe_CRegF = pd.DataFrame(get_CRegF_data_row, index=None)

    dataframe_CRegF['CANumber'] = check_value
    dataframe_CRegF['ItemizationType'] = ""
    dataframe_CRegF['ItemizatoinCreditor'] = ""
    dataframe_CRegF['ItemizatonDate'] = ""
    dataframe_CRegF['ItemizatonBalance'] = ""
    dataframe_CRegF['ItemizationPayments'] = ""
    dataframe_CRegF['ItemizationInterest'] = ""
    dataframe_CRegF['ItemizationFee'] = ""
    dataframe_CRegF['ItemizationCurrBalance'] = ""

    dataframe_CRegF = dataframe_CRegF[
        ['CANumber', 'ItemizationType', 'ItemizatoinCreditor', 'ItemizatonDate', 'ItemizatonBalance',
         'ItemizationPayments',
         'ItemizationInterest', 'ItemizationFee', 'ItemizationCurrBalance']]

    # dataframe_CMIS = dataframe_CMIS.groupby(['CurBalance1']).last().reset_index()

    # dataframe_CMIS['Alternate ID'] = dataframe_CMIS['InterestAmt'].astype(str)

    # combined_df_con = pd.concat([dataframe_CACT, dataframe_CD00], axis=1, ignore_index=True)
    # combined_df_app = dataframe_CACT.append(dataframe_CD00, ignore_index=True)
    merged_data_CACT_CD00 = pd.merge(dataframe_CACT, dataframe_CD00, on='AcctNumber', how='outer')
    merged_data_CACT_CD00 = merged_data_CACT_CD00.loc[:,
                            ~merged_data_CACT_CD00.columns.isin(remove_unnecessary_columns)]

    # merged_data.columns = headers_updated

    merged_data_add_CD01 = pd.merge(merged_data_CACT_CD00, dataframe_CD01, on='AcctNumber',
                                    how='outer')
    # merged_data_add_CD01 = merged_data_add_CD01.loc[:, ~merged_data_add_CD01.columns.isin(remove_test_columns)]
    #

    merged_data_add_CD01.columns = headers_updated
    merged_data_add_CD01 = pd.merge(merged_data_add_CD01, final_dataframe_CMIS, on='CANumber',
                                    how='outer')
    # #
    # merged_data_add_CD01 = pd.merge(merged_data_add_CD01, dataframe_CDEC, on='CANumber',
    #                                 how='outer')
    #
    # merged_data_add_CD01 = pd.merge(merged_data_add_CD01, dataframe_CBKP, on='CANumber',
    #                                 how='outer')

    merged_data_add_CD01 = pd.merge(merged_data_add_CD01, dataframe_CRegF, on='CANumber',
                                    how='outer')

    merged_data_add_CD01 = merged_data_add_CD01.loc[:,
                           ~merged_data_add_CD01.columns.isin(remove_unnecessary_columns)]
    #
    merged_data_add_CD01 = merged_data_add_CD01.loc[:,
                           ~merged_data_add_CD01.columns.isin(remove_att_columns)]

    # merged_data_add_CD01 = merged_data_add_CD01.loc[:,
    #                        ~merged_data_add_CD01.columns.isin(remove_extra_columns)]

    # merged_data_add_CD01 = pd.merge(merged_data_add_CD01, final_dataframe_CMIS, on='CltRefNumber',
    #                                 how='outer')

    cols = list(merged_data_add_CD01.columns)
    cols.pop(cols.index('Attorney Address'))
    cols.pop(cols.index('Attorney CSZ'))
    cols.insert(len(cols) - 52, 'Attorney Address')
    cols.insert(len(cols) - 52, 'Attorney CSZ')
    merged_data_add_CD01 = merged_data_add_CD01[cols]

    # CACT_data_to_csv = dataframe_CACT.to_csv(index=False)

    # CD00_data_to_csv = dataframe_CD00.to_csv(index=False)

    # Empty_dataframe_to_csv = final_dataframe_CMIS.to_csv(index=False)

    # CD01_data_to_csv = dataframe_CD01.to_csv(index=False)
    # CMIS_data_to_csv = dataframe_CMIS.to_csv(index=False)

    # final dataframe

    # merged_data_add_CD01['ZipCode'] = merged_data_add_CD01['ZipCode'].astype(str)
    # merged_data_add_CD01['ZipCode'] = merged_data_add_CD01['ZipCode'].str.replace('.0', '')

    final_dataframe = merged_data_add_CD01

    final_dataframe.columns = final_dataframe.columns.str.replace('_x', '')
    final_dataframe.columns = final_dataframe.columns.str.replace('_y', '')

    # final_dataframe['ContractDate'] = final_dataframe['ContractDate'].astype(int)
    # final_dataframe['ContractDate'] = round(final_dataframe['ContractDate'].astype(float))
    # final_dataframe['ContractDate'] = final_dataframe['ContractDate'].astype(int)
    # final_dataframe['ContractDate'] = final_dataframe['ContractDate'].str.replace('.0', '')

    final_dataframe['ContractDate'] = final_dataframe['ContractDate'].astype(str)

    final_dataframe['ContractDate'] = final_dataframe['ContractDate'].str.replace('.0', '')
    # dataframe_CACT['DelinquencyDate'] = dataframe_CACT['DelinquencyDate'].str.replace('', '30001212 00:00:00')
    final_dataframe['ContractDate'] = pd.to_datetime(final_dataframe['ContractDate'], errors='coerce',
                                                     format='%Y%m%d')

    # final_dataframe['ContractDate'] = dataframe_CACT['ContractDate'].str.replace('.0', '')

    # chekc = final_dataframe['ZipCode']
    # final_dataframe['ZipCode'] = final_dataframe['ZipCode'].astype(str)
    # final_dataframe['ZipCode'] = final_dataframe['ZipCode'].str.replace('.0', '')

    # final_dataframe['ZipCode'] = final_dataframe['ZipCode'].astype(int)
    final_dataframe['SSN'] = final_dataframe['SSN'].astype(str)
    final_dataframe['SSN'] = final_dataframe['SSN'].str.replace('.0', '')
    final_dataframe['SSN'] = final_dataframe['SSN'].fillna("")
    final_dataframe['SSN'] = final_dataframe['SSN'].str.replace('nan','')
    # Remove any NaN Quikc brown fox
    final_dataframe = final_dataframe.drop(['ACTNumber'], axis=1)
    final_dataframe = final_dataframe.fillna("")

    merge_to_html = final_dataframe.to_html(index=None)
    merge_to_csv = final_dataframe.to_csv(index=None)
    # combined_data_to_csv = combined_df_con.to_csv(index=False)

    response = HttpResponse(
        merge_to_csv,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="GXY_"' + getfilename + '".csv"'},
    )
    #return HttpResponse(merge_to_html)
    return response
