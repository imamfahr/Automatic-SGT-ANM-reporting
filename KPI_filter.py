from InfomineCleaner import *
from MERprocessing import *

'''Do the math'''
MA = ((PWT+SWT+IODOn+IODOff+EODOn+EODOff+PDAM)/(PWT+SWT+IODOn+IODOff+EODOn+EODOff+PDAM+PMD+UMD-PDAM).replace({0:np.nan})).fillna(0)
MTBF =(EngOn/(nFail).replace({0:np.nan})).fillna(EngOn)
MTTR = ((MTTRF_period)/(nFail).replace({0:np.nan})).fillna(nFail*MTBF_period)

KPI_all_this_week = KPI_filter_frame(MA,MTBF,MTTR)



'''MA processing'''
red_MA_this_week = KPI_all_this_week['MA'][KPI_all_this_week['MA']<0.9].dropna()
MA_df = PDTDclean[PDTDclean['fleet desc'].isin(red_MA_this_week.index)]
MA_df['MA Anomali']= MA_df['Unit']+' '+MA_df['Reported Fault/Job Description']+' ('+MA_df['Period\nEvent\nMaint.\nDuration'].values.astype(str)+" Hours)"

'''MTBF processing'''
red_MTBF_this_week = KPI_all_this_week['MTBF'][KPI_all_this_week['MTBF']<100].dropna()
MTBF_df = PDTDclean[PDTDclean['fleet desc'].isin(red_MTBF_this_week.index)]

'''MTTRF processing'''
red_MTTR_this_week = KPI_all_this_week['MTTR'][KPI_all_this_week['MTTR']>6].dropna()
MTTR_df = PDTDclean[PDTDclean['fleet desc'].isin(red_MTTR_this_week.index)]
MTTR_df['Period\nEvent\nMaint.\nDuration'] = MTTR_df['Period\nEvent\nMaint.\nDuration'].apply(lambda x: round(x,2))
MTTR_df['MTTR Anomali']= MTTR_df['Unit']+' '+MTTR_df['Description of Repair']+' ('+MTTR_df['Period\nEvent\nMaint.\nDuration'].values.astype(str)+" Hours)"



