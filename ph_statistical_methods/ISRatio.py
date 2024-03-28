# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:58:18 2024

@author: Karandeep.Kaur
"""

import pandas as pd
import numpy as np

from confidence_intervals import byars_lower, byars_upper
from validation import metadata_cols, ci_col, validate_data, format_args, reference_pop_checks


def calculate_ISRatio(df, observations, population, count_ref, pop_ref, group_cols = [],
                       confidence=0.95, refvalue=1, refpoptype="series",
                       metadata=True, observed_totals=None):
    
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
        
        
        refpoptype (str): whether count_ref and pop_ref have been specified as series, array or a field name from 
        data; quoted string "field" or "series" or "array"; default = "series"     
           
    
    """
    
    
    confidence, group_cols = format_args(confidence, group_cols)
    
    validate_data(df, observations,group_cols, metadata, population)
    
    df=df.rename(columns={observations: "observed"})
    
    if refpoptype =="series" or refpoptype=="array":
        

        ref= pd.DataFrame({"refcount":count_ref,"refpop":pop_ref})
        ref["Rates"]=ref["refcount"]/ref["refpop"]
        
        reference_pop_checks(df,group_cols, ref=ref)       
    
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
    
        df= df.groupby(group_cols)[["observed","expected"]].sum().reset_index()
    
        df["Value"]=df["observed"]/df["expected"]*refvalue
                                    
        
    if confidence is not None: 

            for c in confidence:
                
                df[ci_col(c, 'lower')]= df.apply(lambda y: byars_lower(y["observed"],c)/y["expected"]*refvalue,axis=1)
                df[ci_col(c, 'upper')]= df.apply(lambda y: byars_upper(y["observed"],c)/y["expected"]*refvalue,axis=1)
        
    if metadata:
        method = np.where(df["observed"] < 10, 'Exact', 'Byars')
        df = metadata_cols(df, f'indirectly standardised ratio x {refvalue}', confidence, method)


    return df