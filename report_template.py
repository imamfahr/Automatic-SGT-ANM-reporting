from KPI_filter import *
from MERprocessing import *
'''MA Report Template'''

MA_report = []

    
    
for i in red_MA_this_week.index:
    Scheduled_maintenance = []
    Unschedule_maintenance = []
    
    for x in MA_df[((MA_df.Activity =='08-Planned Maintenance (PMD)')|(MA_df.Activity ==',08-Planned Maintenance (PMD)'))&(MA_df['fleet desc'] ==i)&(MA_df['Period\nEvent\nMaint.\nDuration']>10.0)]['MA Anomali']:
        Scheduled_maintenance.append(x)
    
    for x in MA_df[((MA_df.Activity =='09-Unplanned Maintenance (UMD)')|(MA_df.Activity ==',09-Unplanned Maintenance (UMD)'))&((MA_df['fleet desc'] ==i)&(MA_df['Period\nEvent\nMaint.\nDuration']>10.0))]['MA Anomali']:
        Unschedule_maintenance.append(x)
    
    
    structured_MA = {
        
    
    'Fleet':i,
    'MA':red_MA_this_week[i],
    'Total Unit':Complete_df.groupby('fleet desc').count()['Unit'][i],
    'UMD total hours':round(Complete_df.groupby('fleet desc').sum()['UMD\n(09)'][i],2),
    'PMD total hours':Complete_df.groupby('fleet desc').sum()['PMD\n(08)'][i],
    'PDAM total hours':Complete_df.groupby('fleet desc').sum()['PDAM\n08020\n09020'][i],
    'Scheduled maintenance' : Scheduled_maintenance,
    'Unscheduled maintenance' : Unschedule_maintenance
    
}
    MA_report.append(structured_MA)

'''MTBF Report template'''


MTBF_report = []


for i in red_MTBF_this_week.index:
    comp_gp_issue = []
    
    '''
    filter downtime detail for only failure event 
    '''
    
    na = MTBF_df[(MTBF_df['Is Failure']=='Yes')&(MTBF_df['fleet desc'] ==i)][['Reason','System']].groupby(['Reason'],as_index=False).count().sort_values('System',ascending=False)['Reason']
    count_of_failure = MTBF_df[(MTBF_df['fleet desc'] ==i)&(MTBF_df['Is Failure']=='Yes')].count()['Is Failure']
    '''
    conditional statement for unit that has no failure
    '''
    if count_of_failure == 0:
        comp_gp_issue.append({})
    else:
        for u in na:    
            
            '''
            Create dataframe for system failure
            '''
            system_failure = MTBF_df[(MTBF_df['Is Failure']=='Yes')][['fleet desc','Reason','System','Part']].groupby(['fleet desc','Reason','System'],as_index=False).count()
            system_failure['MTBF_gp_repetitive'] = system_failure['System']+' '+system_failure['Part'].values.astype(str)+' times'
            
            '''
            Create dataframe for reason failure failure
            '''
            reason_failure = MTBF_df[(MTBF_df['fleet desc']==i) & (MTBF_df['Is Failure']=='Yes')]['Reason'].value_counts().reset_index()
            reason_failure['Reason_repetitive'] = reason_failure['index']+' '+reason_failure['Reason'].values.astype(str)+' times'

            general_comp_failure = []
            for e in reason_failure['index']:
                f = system_failure[(system_failure['fleet desc']==i)&(system_failure['Reason']==e)]['MTBF_gp_repetitive'].tolist()
                general_comp_failure.append(f)
            repetitive_issue = dict(zip(reason_failure['Reason_repetitive'],general_comp_failure))
        comp_gp_issue.append(repetitive_issue)
    
    '''
    report template per fleet model
    
    '''
    
    structured_MTBF = {
    'Fleet':i,
    'MTBF':red_MTBF_this_week[i],
    'Total Unit':Complete_df.groupby('fleet desc').count()['Unit'][i],
    'Total Hours Engine ON' : Complete_df.groupby('fleet desc').sum()['Total\nEngine On\nPeriod'][i],
    'Count of failures' : count_of_failure,
    'Failures by Comp Gp with repetitive issue' : comp_gp_issue 
    }
    
    MTBF_report.append(structured_MTBF)

'''MTTR Report Template'''

MTTR_report = []
 
    
for i in red_MTTR_this_week.index:
    Breakdown_detail = []
    
    for x in MTTR_df[(MTTR_df['Is Failure'] =='Yes')&(MTTR_df['fleet desc'] ==i)&(MTTR_df['Period\nEvent\nMaint.\nDuration'])]['MTTR Anomali']:
        Breakdown_detail.append(x)
        
    structured_MTTR = {
    'Fleet':i,
    'MTTR':red_MTTR_this_week[i],
    'Total Unit': Complete_df.groupby('fleet desc').count()['Unit'][i],
    'Hours Maintenance with Failure is Yes' : round(MTTR_df[(MTTR_df['Is Failure'] =='Yes')&(MTTR_df['fleet desc'] ==i)].sum()['Period\nEvent\nMaint.\nDuration'],2),
    'Count of Failures' : MTTR_df[(MTTR_df['Is Failure'] =='Yes')&(MTTR_df['fleet desc'] ==i)].count()['Is Failure'],
    'Detail Breakdown with Failure is Yes' : Breakdown_detail
    
}
    MTTR_report.append(structured_MTTR)
