import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
import sys

def create_feature(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['url_obfuscation_score'] = df['Shortining_Service'] + df['double_slash_redirecting'] + df['having_At_Symbol'] + df['Prefix_Suffix']
        df['ui_deception_score'] = df['on_mouseover'] + df['RightClick'] + df['popUpWidnow'] + df['Iframe']
        df['trust_score'] = df['SSLfinal_State'] + df['HTTPS_token'] + df['Google_Index']
        df['redirection_risk_score'] = df['Redirect'] + df['Submitting_to_email'] + df['Abnormal_URL']
        return df
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def drop_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    try:
        excluded_features = [
            'Shortining_Service','double_slash_redirecting','having_At_Symbol','Prefix_Suffix',
            'on_mouseover','RightClick','popUpWidnow','Iframe',
            'SSLfinal_State','HTTPS_token','Google_Index',
            'Redirect','Submitting_to_email','Abnormal_URL',
            'URL_Length','Domain_registeration_length','Favicon','port',
            'Links_in_tags','SFH','age_of_domain','DNSRecord',
            'Page_Rank','Links_pointing_to_page','Statistical_report'
        ]
        dataframe = dataframe.drop(columns=excluded_features, axis=1)
        return dataframe
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def feature_engineering(dataframe: pd.DataFrame) -> pd.DataFrame:
    try:
        # Step - 1 : Replacing -1 with 0.
        dataframe = dataframe.replace(-1, 0)

        # Step - 2 : Filling missing values with 0.
        for col in dataframe.columns:
            if col != "Result":
                dataframe[col] = dataframe[col].fillna(0)

        # Step - 3 : Creating new features.
        dataframe = create_feature(dataframe)

        # Step - 4 : Dropping correlated features.
        dataframe = drop_features(dataframe)
        return dataframe
    except Exception as e:
        raise NetworkSecurityException(e, sys)