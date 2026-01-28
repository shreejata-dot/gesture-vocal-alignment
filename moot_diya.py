import pandas as pd, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('folder', type=str)
args = parser.parse_args()

mods = ['facial expression', 'hand', 'head', 'leg', 'face', 'vocal', 'gaze', 'body']
partner = ['response']

repertoire = {k:set() for k in mods}

output = pd.DataFrame(columns=[
    'file', 'seqid', 'duration',
    'seq_length', 'seq_length_focal', 'seq_length_partner',
    'num_units', 'num_units_focal', 'num_units_partner', 'num_diff_units',
    'tot_focal_combi', 'focal_combi', 'partner_combi', 'inter_indiv_overlap',
    'prop_focal_states', 'prop_partner_states'
    ] + [mod+'_seq' for mod in mods])

for f in os.listdir(args.folder):
    if f.endswith('txt'):
        df = pd.read_csv(args.folder+'/'+f, delimiter='\t', skiprows=1)
        df.rename(columns={'temps de fin - ss.msec':'end time', 'Temps de départ - ss.msec': 'start time', 'gesture in sequence':'sequence', 'legs':'leg'}, inplace=True)
    else:
        print('Format not supported for '+f)
        continue
    for mod in mods:
        if not mod in df.columns:
            df[mod] = None
        elif not df[mod].isna().all():
            df[mod] = df[mod].str.replace(' ','')
            df[mod] = df[mod].str.split(':').str[0]
            for e in df[mod].dropna().unique():
                repertoire[mod].add(e.upper())
    for s, grp in df.groupby('sequence'):
        temp = {}
        temp['file'] = f
        temp['seqid'] = s
        temp['duration'] = float(grp.iloc[-1]['end time'] - grp.iloc[0]['start time'])
        temp['seq_length'] = sum([grp[mod].isna().diff().sum()/2 for mod in mods + partner]) 
        temp['seq_length_focal'] = sum([grp[mod].isna().diff().sum()/2 for mod in mods])
        temp['seq_length_partner'] = sum([grp[mod].isna().diff().sum()/2 for mod in partner])
        temp['num_units'] = sum([grp[mod].dropna().nunique() for mod in mods + partner])
        temp['num_units_focal'] = sum([grp[mod].dropna().nunique() for mod in mods])
        temp['num_units_partner'] = sum([grp[mod].dropna().nunique() for mod in partner])
        temp['num_diff_units'] = pd.concat([grp[mod].dropna() for mod in mods + partner]).nunique()
        temp['tot_focal_combi'] = sum([len(r[mods].dropna()) > 1 for i, r in grp.iterrows()]) / len(grp)
        temp['focal_combi'] = sum([len(r[mods].dropna()) > 1 for i, r in grp.iterrows()]) / len(grp[mods].dropna(how='all'))
        temp['partner_combi'] = sum([len(r[partner].dropna()) > 1 for i, r in grp.iterrows()]) / len(grp[partner].dropna(how='all')) if len(grp[partner].dropna(how='all'))>0 else 0
        temp['inter_indiv_overlap'] = sum([r[mods].dropna().any() and r[partner].dropna().any() for i, r in grp.iterrows()]) / len(grp)
        temp['prop_focal_states'] = len(grp[mods].dropna(how='all')) / len(grp)
        temp['prop_partner_states'] = len(grp[partner].dropna(how='all')) / len(grp)
        for mod in mods + partner:
            temp[mod+'_seq'] = "-".join(grp[mod].dropna())

        for i, r in grp[~grp['response'].isna()].iterrows():
            if i == grp.index[0]:
                continue
            for mod in mods:
                if not pd.isna(grp.loc[i-1, mod]):
                    temp['preresp_'+mod+'_'+grp.loc[i-1, mod]] = True
        for c in temp:
            if c not in output.columns:
                output[c] = None
        output.loc[len(output)] = temp

output.to_csv('output.csv', index=False)

compositions = {}
for mod in mods:
    print(f"In mod {mod}, found {repertoire[mod]}\n")
    for unit in repertoire[mod]:
        compositions[f'{mod}_contains_{unit}'] = output[mod+'_seq'].str.contains(unit).to_list()
output = pd.concat([output, pd.DataFrame(compositions)], axis=1)
output.to_csv('output_and_composition.csv', index=False)