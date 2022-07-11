import pandas as pd
import numpy as np
import pdb


'''
MER Processing

'''
def MERcleaner(MERSummary):
    MERSummary.drop(MERSummary.columns[[0,1]],axis=1,inplace=True)
    MERSummary.dropna(inplace=True)
    MERSummary.reset_index(drop=True,inplace=True)
    MERSummary.columns = MERSummary.iloc[0]
    MERSummary.drop(0,inplace=True)
    indexNames = MERSummary[(MERSummary['Unit']=='OEM Totals')|(MERSummary['Unit']=='Class Total')|(MERSummary['Unit']=='Report Total')].index
    MERSummary.drop(indexNames, inplace = True)
    return MERSummary

'''
EMPS Processing

'''
def EMPScleaner(EMPS):
    EMPS.drop(EMPS.columns[[0]],axis=1,inplace=True)
    EMPS.dropna(inplace=True)
    EMPS.reset_index(drop=True,inplace=True)
    EMPS.columns = EMPS.iloc[0]
    EMPS.drop(0,inplace=True)
    EMPS.rename(columns = {'Unit\nNumber':'Unit'},inplace=True)
    indexNames2 = EMPS[(EMPS['Unit']=='OEM Totals')|(EMPS['Unit']=='Class Total')|(EMPS['Unit']=='Report Total')].index
    EMPS.drop(indexNames2,inplace=True)
    return EMPS

'''Processing PDTD'''
def PDTDcleaner(PDTD,fleetdesc):
    PDTD.dropna(thresh=3,inplace=True) #masih PR ya
    PDTD.reset_index(drop=True,inplace=True)
    PDTD.columns = PDTD.iloc[0]
    PDTD.drop(0,inplace=True)
    PDTD.rename(columns = {'Unit No.' : 'Unit'},inplace=True)
    PDTD_complete = pd.merge(PDTD, fleetdesc, on='Unit', how='inner')
    PDTD_complete['Period\nEvent\nMaint.\nDuration'] =  PDTD_complete['Period\nEvent\nMaint.\nDuration'].apply(lambda x: round(x,2))
    return PDTD_complete


'''fleet desc combination'''

def fleet_desc_combined(combined,fleetdesc):

    '''Combine fleet desc & combined'''
    All_KPI = pd.merge(combined,fleetdesc,on='Unit', how='outer')
    All_KPI.drop(columns=['Check','Column7','Column8'],inplace=True)
    All_KPI.dropna(thresh=24, inplace=True)

    '''round selected column'''
    All_KPI['PMD\n(08)'] = All_KPI['PMD\n(08)'].apply(lambda x: round(x,2))
    All_KPI['UMD\n(09)'] = All_KPI['UMD\n(09)'].apply(lambda x: round(x,2))
    All_KPI['Total\nEngine On\nPeriod'] =  All_KPI['Total\nEngine On\nPeriod'].apply(lambda x: round(x,2))
    All_KPI['PDAM\n08020\n09020'] =  All_KPI['PDAM\n08020\n09020'].apply(lambda x: round(x,2))

    return All_KPI

'''KPI filter frame'''

def KPI_filter_frame(MA,MTBF,MTTR):

    '''Combined all KPI'''
    Anomali_db = pd.merge(MA.to_frame(),MTBF.to_frame(), on='fleet desc', how= 'outer')
    complete_anomali = pd.merge(Anomali_db, MTTR.to_frame(), on='fleet desc', how= 'outer')
    complete_anomali.rename(columns = {'0_x':'MA','0_y':'MTBF'},inplace=True)
    complete_anomali.columns = ['MA','MTBF','MTTR']

    '''round by 2 decimals'''
    complete_anomali['MTBF'] = complete_anomali['MTBF'].apply(lambda x: round(x,2))
    complete_anomali['MTTR'] = complete_anomali['MTTR'].apply(lambda x: round(x,2))

    '''drop zeros'''
    complete_KPI = complete_anomali.loc[~(complete_anomali==0).all(axis=1)]

    return complete_KPI