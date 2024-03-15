# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:58:18 2024

@author: Karandeep.Kaur
"""

import pandas as pd

from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data, format_args



# Need to work on validation checks  
def reference_pop_checks(df, group_cols=[],ref=None):
    
    counts=df.groupby(group_cols).count()
    non_groups= df.columns.difference(group_cols)
    for col in non_groups:
        if not (counts[col]== counts[col].iloc[0]).all():
            raise ValueError("Data must contain the same number of rows for each group")
    for group_name, count_value in counts.items():
        ref_siz = len(ref[ref["refcount"]==group_name])
        if ref_siz !=count_value:        


            raise ValueError("count_ref length must equal number if rows in each group data")



def calculate_ISRatio(df, observations, population, count_ref, pop_ref, group_cols = [],
                       confidence=0.95, refvalue=1,df_type="full", refpoptype="series",
                       observed_totals=None):
    
    """Calculates standard mortality ratios (or indirectly standardised ratios) with
    confidence limits using Byar's (1) or exact (2) CI method.
    
    Args:
        df: DataFrame containing the data to calculate IS ratios for.
        observations (str): field name from data containing the observed number of events for
        each standardisation category (e.g. ageband) within each grouping set (eg area).
        population (str): field name from data containing the population for each standardisation 
        category (e.g. age band).
        
        count_ref: the observed number of events in the reference population for
        each standardisation category (eg age band); series, array or field name from data 
        depending on value of refpoptype.
        
        pop_ref: the reference population for each standardisation category (eg age band); series,
        array or field name from data depending on value of refpoptype.
        
        group_cols (list): A list of column name(s) to group the data by. Defaults to None.
        confidence: Confidence interval(s) to use, either as a float, list of float values or None.
        
        Confidence intervals must be between 0.9 and 1. Defaults to 0.95 (2 std from mean).
        
        refvalue (int): the standardised reference ratio, default = 1
        
        df_type (str): returns a DataFrame based on data that is required for the user. When df_type = "full",
        returns a dataframe of observed events, expected events, standardised mortality ratios, 
        lower confidence limits, upper confidence limits, confidence level, statistic and method for each 
        grouping set. Options "full", "lower", "upper", "value", "standard". Default= "full".
        
        refpoptype (str): whether count_ref and pop_ref have been specified as series, array or a field name from 
        data; quoted string "field" or "series" or "array"; default = "series"     
           
    
    """
    
    metadata=True
    
    confidence, group_cols = format_args(confidence, group_cols)
    
    validate_data(df, observations,group_cols, metadata, population)
    
    if refpoptype =="series" or refpoptype=="array":
        

        ref= pd.DataFrame({"refcount":count_ref,"refpop":pop_ref})
        ref["Rates"]=ref["refcount"]/ref["refpop"]
    
        population_info= len(df)//len(ref)
        
        repeat= pd.concat([ref]*population_info, ignore_index=True)
        
        df= pd.concat([df,repeat],axis=1)
        
        df["expected"]= df[population]*df["Rates"]
        
    elif refpoptype =="field":

        df["Rates"]= df[count_ref]/df[pop_ref]
        
        df["expected"]=df[population]*df["Rates"]

    else:
        raise ValueError('refpoptype value must either be "array", "series" or "field"')
        
    
    if len(group_cols) > 0:
    
        ISRatio_df= df.groupby(group_cols)[[observations,"expected"]].sum().reset_index()
    
        ISRatio_df["Value"]=ISRatio_df[observations]/ISRatio_df["expected"]*refvalue
                                    

    if len(confidence)== 2:    
        for c in confidence:
            
            ISRatio_df[ci_col(c, 'lower')]= ISRatio_df.apply(lambda y: byars_lower(y[observations],(1-c))/y["expected"],axis=1)
            ISRatio_df[ci_col(c, 'upper')]= ISRatio_df.apply(lambda y: byars_upper(y[observations],(1-c))/y["expected"],axis=1)
            ISRatio_df[ci_col(c, 'lower')]= ISRatio_df.apply(lambda y: byars_lower(y[observations],(1-c))/y["expected"],axis=1)
            ISRatio_df[ci_col(c, 'upper')]= ISRatio_df.apply(lambda y: byars_upper(y[observations],(1-c))/y["expected"],axis=1)
    else:
        
        for c in confidence:
            
            ISRatio_df[ci_col(c, 'lower')]= ISRatio_df.apply(lambda y: byars_lower(y[observations],(1-c))/y["expected"],axis=1)
            ISRatio_df[ci_col(c, 'upper')]= ISRatio_df.apply(lambda y: byars_upper(y[observations],(1-c))/y["expected"],axis=1)
        
    
    statistic = f'indirectly standardised ratio x {refvalue}'
    ISRatio_df['Method']= ISRatio_df.apply(lambda y: "Exact" if y[observations]<10 else "Byars",axis=1)
    ISRatio_df=metadata_cols(ISRatio_df, statistic, confidence, method = ISRatio_df['Method'])
       
    if df_type =="lower":
        if len(confidence)==2:
                ISRatio_df=ISRatio_df[['lower_95_ci', 'lower_99_8_ci']]
        else:
            ISRatio_df=ISRatio_df[[ci_col(c, 'lower')]]
        
    elif df_type =="upper":
        if len(confidence)==2:
                ISRatio_df=ISRatio_df[['upper_95_ci', 'upper_99_8_ci']]
        else:
        
            ISRatio_df=ISRatio_df[[ci_col(c, 'upper')]]
        
    elif df_type == "value":
        
        ISRatio_df=ISRatio_df[["Value"]]
    
    elif df_type =="standard":
        
        ISRatio_df=ISRatio_df.drop(columns=["Confidence","Statistic","Method"])   
       
    return ISRatio_df
       
# data exported from R. Used the R example  and set.seed(2) 
df= pd.read_csv("tests/test_data/isr_dummydata.csv")
ref=pd.read_csv("tests/test_data/isr_refdummydata.csv")


t=calculate_ISRatio(df, observations="obs", population="pop",  count_ref=ref["refcount"], pop_ref=ref["refpop"], group_cols = ["year","sex","indicatorid"],
                        confidence=[0.95,0.998], refvalue=1,df_type="lower",refpoptype="series") 

b=ref["refcount"].values
c=ref["refpop"].values
w=calculate_ISRatio(df, observations="obs", population="pop",  count_ref=b, pop_ref=c, group_cols = ["year","sex","indicatorid"],
                        confidence=[0.95,0.998], refvalue=1,df_type="standard",refpoptype="array") 
x=calculate_ISRatio(df, observations="obs", population="pop",  count_ref=ref["refcount"], pop_ref=ref["refpop"], group_cols = ["year","sex","indicatorid"],
                        confidence=[0.95,0.998], refvalue=1,df_type="lower") 

y=calculate_ISRatio(df, observations="obs", population="pop",  count_ref=ref["refcount"], pop_ref=ref["refpop"], group_cols = ["year","sex","indicatorid"],
                        confidence=0.92, refvalue=1,df_type="lower") 

z=calculate_ISRatio(df, observations="obs", population="pop", count_ref=ref["refcount"], pop_ref=ref["refpop"], group_cols = ["year","sex","indicatorid"],
                        confidence=0.95, refvalue=1)   




ref1= ref
ref1["Rates"]=ref1["refcount"]/ref1["refpop"]


population_info= len(df)//len(ref1)

repeat= pd.concat([ref1]*population_info, ignore_index=True)

full_df1= pd.concat([df,repeat],axis=1)

field_test=calculate_ISRatio(full_df1, observations="obs", population="pop",  count_ref="refcount", pop_ref="refpop", group_cols = ["year","sex","indicatorid"],
                        confidence=0.95, refvalue=1,refpoptype="field")