import numpy as np
import pandas as pd

def object_cols_clean(df):
    """
    Replaces 'X', 'XX' with np.nan and strings to float on columns CAMEO_DEUG_2015
 
    """
    df["CAMEO_DEUG_2015"] = df["CAMEO_DEUG_2015"].replace({"X": np.nan, "XX": np.nan})
    df["CAMEO_DEUG_2015"] = df["CAMEO_DEUG_2015"].astype(float)
   
    return df



def attribute_values_clean(values):
    """ 
    Converts string/numerical values to numbers
    """
    if '-1, 0' in values[1]:
        values[1].remove('-1, 0')
        values[1].extend([-1,0])
    if '-1, 9' in values[1]:
        values[1].remove('-1, 9')
        values[1].extend([-1, 9])
    if '-1' in values[1]:
        values[1].remove('-1')
        values[1].extend([-1])
    values[1] = list(set(values[1]))
    return values



def replace_strange_with_nan(strange, values):
    "Replaces a strange value (not in attr_values_clean) with np.nan"
    if (strange in values) or (np.isnan(strange)):
        return strange
    else:
        #print("Replacing {} to NaN".format(strange))
        return np.nan
    
    
    
def strange_vals_replace(df, attr_values_clean):
    for column in df.columns:
        for value in attr_values_clean:
            if value[0] == column:
                #print("In column {} ...".format(column))
                df[column] = df[column].apply(replace_strange_with_nan, args =([value[1]]))
    return df



def attr_unknown_value(attr, unknown_values):
    "Returns unknown value associated to attriubute 'attr'"
    
    value = unknown_values[unknown_values['Attribute'] == attr]['Value']
    value = value.astype(str).str.cat(sep = ',')
    value = [int(n) for n in value.split(',')]
    return [value]



def replace_unknown(value, unknowns):
    'Replaces value with np.nan val if described as unknown on DIAS Attributes - Values 2017.xlsx'
    
    if value in unknowns:
        return np.nan
    else:
        return value
    
    

def unknown_to_nans(df, unknown_values):
    "Replaces unknown values to np.nan in columns appearing on unknown_values"
    
    for attr in unknown_values.Attribute:
        value = attr_unknown_value(attr, unknown_values)
        if attr in df.columns:
            df[attr] = df[attr].apply(replace_unknown, args = (value))
    return df



def drop_nan_cols(df1, df2, nullc_p = .3):
    """
    Drops columns from df1 and df2 with more than null_p percentage of NaN values in both df1 and df2
    
    Inputs: df1, df2 - two data frames, null_p - percentange threshold of number of nan values in a column
    Returns: df1, df2 - dataframes with columns of more than null_p NaN values droped, and list of columns droped
    
    """
    #dictonaries of columns in df1 and df2 with corresponding percentage of Nans
    df1_percentage_nans = df1.isnull().mean()
    df2_percentage_nans = df2.isnull().mean()
    
    #names of colums in df1 and df2 that don't meet the threshold null_p
    nan_cols_df1 = set(df1_percentage_nans[df1_percentage_nans > nullc_p].keys())
    #print('Cols in first dataframe to be dropped {} \n'.format(nan_cols_df1))
    
    nan_cols_df2 = set(df2_percentage_nans[df2_percentage_nans > nullc_p].keys())
    #print('Cols in second to be dropped {} \n'.format(nan_cols_df2))
    
    #columns that don't meet the null_p in both df1 and df2
    common_nan_cols = nan_cols_df1.intersection(nan_cols_df2)
    #print('Common columns to drop: {} \n'.format(common_nan_cols))
    
    #print('A total of {} columns were removed from both dataframes'.format(len(common_nan_cols)))
    
    #drop the common cols
    df1 = df1.drop(common_nan_cols, axis = 1)
    df2 = df2.drop(common_nan_cols, axis = 1)
    
    return df1, df2


#originally nullr_c set at 50 by default but changed it Feb 11
def drop_nan_rows(df, nullr_c):
    """
    Input: Dataframe df and threshold nullr_c
    Returns: Dataframe df after droping those rows with more than nullr_c NaN values
    """
    nans_in_row = df.isnull().sum(axis=1)
    df_droped = df[nans_in_row <= nullr_c]
    original_n_rows = df.shape[0]
    new_n_rows = df_droped.shape[0]
    #print('{} rows dropped at {} threshold from the dataframe'.format(original_n_rows - new_n_rows, nullr_c))
    return df_droped



def dummies(df, to_dummies):
    """Generates dummy variables to columns in to_dummies"""
    df = pd.get_dummies(df, columns = to_dummies)
    return df



def mean_imputer(df):
    """Fills in NaN values in numerical columns with their mean"""
    num_cols = df.select_dtypes('number')
    df[num_cols.columns] = num_cols.fillna(num_cols.mean())
    return df


def clean_data(df1, df2, attributes, nullc_p = .3, nullr_c = 50, drop_unknown_cols = True):
    """
    Processes df1 (AZDIAS data) and df2 (CUSTOMERS data)
        - Converts missing or strange values to np.nan
        - Drops columns with percentange of nans > nullc_p
        - Drops rows with count of nans > nullr_c
        - Generates dummy variables for categorical volumns of type pd.string
    
    Args:
        df1, df2 (pd.Dataframe): data to be cleaned
        nullc_p (float): max percentage threshold of missing values allowed in a column
        nullr_c (int): max. number of missing values allowed in a row
    
    Returns:
        cleaned_df1, cleaned_df2 (pd.Dataframe): cleaned dataframes
    """
    
    clean_azdias = df1.copy()
    clean_customers = df2.copy()
    attributes = attributes.drop(['Unnamed: 0'], axis=1)
    
    # Drop CAMEO_DEU_2015, CAMEO_INTL_2015 and keep CAMEO_DEUG_2015
    clean_azdias.drop(['CAMEO_DEU_2015', 'CAMEO_INTL_2015'], axis=1, inplace = True)
    clean_customers.drop(['CAMEO_DEU_2015', 'CAMEO_INTL_2015'], axis=1, inplace = True)
    
    
    # Columns corresponding to transactions
    transaction_cols = {'D19_BANKEN_DIREKT','D19_BANKEN_GROSS', 'D19_BANKEN_LOKAL', 'D19_BANKEN_REST', 'D19_BEKLEIDUNG_GEH', 'D19_BEKLEIDUNG_REST', 'D19_BILDUNG','D19_BIO_OEKO','D19_DIGIT_SERV','D19_DROGERIEARTIKEL','D19_ENERGIE', 'D19_FREIZEIT', 'D19_GARTEN', 'D19_HANDWERK', 'D19_HAUS_DEKO', 'D19_KINDERARTIKEL', 'D19_KOSMETIK', 'D19_LEBENSMITTEL', 'D19_LOTTO','D19_NAHRUNGSERGAENZUNG', 'D19_RATGEBER', 'D19_REISEN', 'D19_SAMMELARTIKEL', 'D19_SCHUHE', 'D19_SONSTIGE', 'D19_TECHNIK', 'D19_TELKO_MOBILE', 'D19_TELKO_REST', 'D19_TIERARTIKEL', 'D19_VERSAND_REST', 'D19_VERSICHERUNGEN', 'D19_VOLLSORTIMENT', 'D19_WEIN_FEINKOST'}
    
    cols_not_described = (set(clean_azdias.columns.values) - transaction_cols) - set(attributes['Attribute'].values)
    
    # Drop columns that don't appear in attributes 
    if drop_unknown_cols == True:
        clean_azdias.drop(list(cols_not_described), axis = 'columns', inplace = True)
        clean_customers.drop(list(cols_not_described), axis = 'columns', inplace = True)
        #print('Dropping unknown columns {}'.format(cols_not_described))
    
    # Clean some values on columns CAMEO_DEUG_2015, CAMEO_DEU_2015
    clean_azdias = object_cols_clean(clean_azdias)
    clean_customers = object_cols_clean(clean_customers)
    
    # Replace strange values
    # Reformat the data frame so each value is in line with its corresponding attribute
    attributes["Attribute"] = attributes["Attribute"].ffill()
    
    # Create a list possible values paired with their corresponding attribute and drop attributes whose value is '...'
    colons_drop = attributes[attributes['Value']=='…'].Attribute.values
    lista = list(attributes.groupby(['Attribute', 'Value']).count().drop(colons_drop).index)
    
    #merge values with common attributes
    result = {}
    for sub_tuple in lista:
        if sub_tuple[0] in result:
            result[sub_tuple[0]] = (*result[sub_tuple[0]], *sub_tuple[1:])
        else:
            result[sub_tuple[0]] = sub_tuple
        
    lista2 = list(result.values())
    
    #create list of sublist with attributes and its values
    lista3 = [[x[0],list(x[1:])] for x in lista2]
    
    attr_values_clean = list(map(attribute_values_clean,lista3))
    
    
    # Last step in replacing strange values with nans
    
    clean_azdias = strange_vals_replace(clean_azdias, attr_values_clean)
    clean_customers = strange_vals_replace(clean_customers, attr_values_clean)
    
    
    # Replace unknown values with nans
    unknown_values = attributes[(attributes["Meaning"] == "unknown") | (attributes["Meaning"] == "no transactions known") | (attributes["Meaning"] == "no transaction known")]
    
    clean_azdias = unknown_to_nans(clean_azdias, unknown_values)
    clean_customers = unknown_to_nans(clean_customers, unknown_values)
    
    # Drop columns with large percentage of nans
    clean_azdias, clean_customers = drop_nan_cols(clean_azdias, clean_customers, nullc_p)
    
    # Drop rows with large count of nans
    clean_azdias = drop_nan_rows(clean_azdias, nullr_c)
    clean_customers = drop_nan_rows(clean_customers, nullr_c)
    
    # Categorical columns to dummy variables
    to_dummies = clean_azdias.select_dtypes(np.dtype("O")).columns
    clean_azdias = dummies(clean_azdias, to_dummies)
    clean_customers = dummies(clean_customers, to_dummies)
    
    # Impute each nan with the mean of its corresponding column
    clean_azdias = mean_imputer(clean_azdias)
    clean_customers = mean_imputer(clean_customers)
    
    
    return clean_azdias, clean_customers
        
    

