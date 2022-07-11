import pandas as pd
import numpy as np
import pdb
from InfomineCleaner import *

'''MER data procesing'''


MERSummary = pd.read_excel('MERSummaryAll Wk 20.xlsx')
EMPS = pd.read_excel('EMPSWk20.xlsx')
PDTD = pd.read_excel('PlantDowntimeDetail Wk 20.xlsx')

'''fleet desc import'''
fleetdesc = pd.read_json('fleetdesc.json')
fleetdesc.rename(columns={'Unit no':'Unit'},inplace=True)



'''Assign functions to variables'''
MERclean = MERcleaner(MERSummary)
EMPSclean = EMPScleaner(EMPS)
PDTDclean = PDTDcleaner(PDTD,fleetdesc)

'''Combined MER & EMPS'''
Combined_MER_EMPS = pd.merge(MERclean,EMPSclean, on = 'Unit', how = 'outer')

'''Attaching fleet desc'''
Complete_df = fleet_desc_combined(Combined_MER_EMPS,fleetdesc)



'''Gather all required variables'''
PWT = Complete_df.groupby(['fleet desc'])['PWT\n(00)'].sum() #F
SWT = Complete_df.groupby(['fleet desc'])['SWT\n(01)'].sum() #G
IODOn = Complete_df.groupby(['fleet desc'])['IOD-On\n(04)'].sum() #H
IODOff = Complete_df.groupby(['fleet desc'])['IOD-Off\n(04)'].sum() #I
EODOn = Complete_df.groupby(['fleet desc'])['EOD-On\n(05)'].sum() #J
EODOff = Complete_df.groupby(['fleet desc'])['EOD-Off\n(05)'].sum() #K
PDAM = Complete_df.groupby(['fleet desc'])['PDAM\n08020\n09020'].sum() #T
PMD = Complete_df.groupby(['fleet desc'])['PMD\n(08)'].sum() #L
UMD = Complete_df.groupby(['fleet desc'])['UMD\n(09)'].sum() #M
EngOn = Complete_df.groupby(['fleet desc'])['Total\nEng On\n(SMU Hrs)'].sum() #V
nFail = Complete_df.groupby(['fleet desc'])['Number of\nFailures\nPeriod'].sum() #W
MTBF_period = Complete_df.groupby(['fleet desc'])['MTBF\nPeriod'].sum() #X
MTTRF_period = Complete_df.groupby(['fleet desc'])['MTTR-F\nPeriod'].sum() #Y1