"""Build a portable, evidence-linked HTML snapshot; never launches experiments."""
from pathlib import Path
from datetime import datetime, timezone
from statistics import mean
from html import escape
import argparse
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stream-root', type=Path, default=Path('/home/satvik/side_project'))
    args = parser.parse_args()
    out = ROOT / 'results_page'
    sources = out / 'sources'
    sources.mkdir(parents=True, exist_ok=True)
    manifest = []

    def source(path, name):
        path = Path(path)
        shutil.copyfile(path, sources / name)
        manifest.append({'file': name, 'original': str(path), 'modified_utc': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()})
        return json.loads(path.read_text()) if path.suffix == '.json' else None

    def link(name, label='Source report'):
        return f'<a href="sources/{escape(name)}">{escape(label)}</a>'

    def table(headers, rows, caption):
        return '<div class="scroll"><table><caption>'+escape(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+escape(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

    topology = []
    for p in sorted((ROOT/'results/phase2').glob('topology_*/report.json')) + sorted((ROOT/'results/phase2_full').glob('topology_*/report.json')):
        r = json.loads(p.read_text())
        if r.get('status') == 'DONE' and r.get('controls'):
            name = p.parent.name+'.json'
            source(p, name)
            topology.append((r, name))
    top_tables = ''
    for layer in ['L2','L5']:
        rows = []
        for r, name in topology:
            key = f'{layer}_pyramidal->{layer}_pyramidal'
            controls = r['controls']
            s = controls[0]['scores'][key]
            null = [c['scores'][key]['control']['roc_auc'] for c in controls]
            intervals = [c['scores'][key]['paired_uncertainty']['auc_difference_interval95'] for c in controls]
            rows.append([link(name, 'C'+str(r['conn_seed'])), f"{r['duration_s']:,.0f}", f"{s['original']['roc_auc']:.3f}", f'{min(null):.3f}–{max(null):.3f}', f"{s['original']['pr_auc']:.3f}", f"{s['original']['prevalence']:.3f}", f"{s['distance_control']['roc_auc']:.3f}", 'Yes' if all(c['converged'] for c in controls) else 'No', 'Yes' if all(i[0] > 0 for i in intervals) else 'No'])
        top_tables += f'<h3>{layer} recurrent edges</h3>'+table(['Circuit','Duration (s)','GLM ROC-AUC ↑','Jitter AUC range','Average precision ↑','Edge prevalence','Distance AUC','All fits converge','AUC advantage interval > 0 for every null'],rows,'All completed independent Phase 2 topology reports found at build time. Jitter range includes all three controls.')

    cal = []
    for p in sorted((ROOT/'results/calibration5').glob('seed*/calibration*.json')):
        cal.append(source(p,'calibration5_'+p.parent.name+'.json')['results'])
    calibration = table(['Method','Mean strength-rank correlation ↑'], [[escape(k),f"{mean(r[k]['weight_spearman'] for r in cal):.3f}"] for k in cal[0]], 'Three synthetic GLM seeds; five temporal basis functions. These are correlations, not edge-detection AUCs.')
    location = source(ROOT/'results/phase2_long/location_s3_1280s/report.json','location.json')['apical_minus_basal']
    shared = source(ROOT/'results/phase2_full/shared_c11_2560s/report.json','shared.json')['observed_vs_hidden']['L2_pyramidal->L2_pyramidal']

    selected = source(args.stream_root/'artifacts/v6/tuned/selected.json','streamglm_selected.json')
    source(args.stream_root/'artifacts/v6/tuned/report.md','streamglm_tuning_report.md')
    source(args.stream_root/'artifacts/v6/tuned/protocol.json','streamglm_tuning_protocol.json')
    source(args.stream_root/'artifacts/v6/failure_audit/README.md','streamglm_failure_audit.md')
    model_tables = ''
    for family, title in [('lowrank','When the generating network is low rank'),('permutation_fullrank','When the generating network is full rank')]:
        rows=[]
        for n in [64,128]:
            for backend,label in [('dense','StreamGLM dense'),('lowrank','StreamGLM low rank'),('nemos','NeMoS')]:
                rs=[r for r in selected if r['family']==family and r['neurons']==n and r['backend']==backend]
                rows.append([n,label,f"{mean(r['evaluation']['test']['gain_bits_per_spike'] for r in rs):.6f}", f"{mean(r['evaluation']['filter_correlation'] for r in rs):.3f}"])
        model_tables += '<h3>'+title+'</h3>'+table(['Neurons','Model','Test gain (bits/spike) ↑','Filter correlation ↑'],rows,'Mean over two seeds (31, 47); 60/20/20 chronological split; settings selected on validation data among fits passing the gradient gate.')
    performance=source(args.stream_root/'artifacts/v7/length_scaling/results.json','streamglm_length_scaling.json')
    source(args.stream_root/'artifacts/v7/extended_dense/protocol.json','streamglm_timing_protocol.json')
    rows=[]
    for r in performance:
        rows.append([r['bins'],escape(r['family'].replace('permutation_','')), 'StreamGLM' if r['backend']=='streamglm' else 'NeMoS',f"{r['fits'][0]['fit_seconds']:.3f}", f"{r['fits'][1]['fit_seconds']:.3f}",f"{r['peak_rss_gib']:.3f}"])
    timing=table(['Bins','Data family','Backend','First fit (s) ↓','Repeat fit (s) ↓','Peak RSS (GiB) ↓'],rows,'64 neurons, seed 31; all listed executions passed the gradient gate. Fixed-configuration pilot, not a universal speed comparison.')
    real=source(args.stream_root/'artifacts/v4/release_report.json','streamglm_release_report.json')['real_data']
    real_table=table(['Retained neurons','Selected rank','Test gain over self-history (bits/spike) ↑','Peak RSS (GiB)'],[[r['retained_units'],r['selected_rank'],f"{r['test_gain_over_self_history_bits_per_spike']:.4f}",f"{r['peak_rss_gib']:.3f}"] for r in real],'Allen VISp, 300-second cohorts from the same session; not independent-session replications.')
    states=[]
    process_lines = subprocess.check_output(['ps', '-eo', 'comm=,args='], text=True).splitlines()
    for p in sorted((ROOT/'results/phase2_full').glob('topology_*/status.json')):
        if (p.parent/'report.json').exists(): continue
        s=source(p,p.parent.name+'_checkpoint.json')
        active = any(line.split()[0].startswith('python') and 'phase2_studies.py' in line and p.parent.name in line for line in process_lines if line.split())
        states.append(escape(p.parent.name)+f": INCOMPLETE — {'runner detected' if active else 'no runner detected at page build'}. Last saved simulation checkpoint: chunk {s.get('chunk','?')}/{s.get('total','?')}. No completed report or new recovery score. Status is a snapshot, not live monitoring.")
    coupled=list((args.stream_root/'artifacts/v8').glob('coupled1000*/report.json'))
    for p in coupled: source(p,'streamglm_'+p.parent.name+'.json')
    now=datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
    html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NeuroTwinBench &amp; StreamGLM — Results</title>
<meta name="description" content="Verified experimental results, controls, failures and limitations for NeuroTwinBench and StreamGLM.">
<style>
:root{color-scheme:light;--ink:#1e2933;--muted:#53616c;--rule:#dce2e6;--accent:#175b49}*{box-sizing:border-box}body{margin:0;background:#fafbf9;color:var(--ink);font:16px/1.65 system-ui,sans-serif}main{max-width:1140px;margin:auto;padding:42px 24px 64px}header{border-bottom:2px solid var(--ink);padding-bottom:24px}h1{font-size:clamp(1.8rem,4vw,2.7rem);line-height:1.2;margin:8px 0 16px;letter-spacing:-.035em}h2{font-size:1.65rem;margin:0 0 8px}h3{font-size:1.1rem;margin:28px 0 8px}p{max-width:850px}a{color:#165e79;text-underline-offset:3px}nav{display:flex;gap:22px;flex-wrap:wrap;margin-top:22px}.meta,small,caption{color:var(--muted);font-size:.88rem}section{padding:34px 0;border-bottom:1px solid var(--rule);scroll-margin-top:20px}.verdict{border-left:3px solid var(--accent);padding:9px 18px;background:#eef5f0;margin:18px 0}.limit{border-left-color:#976722;background:#faf3e8}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:.9rem;margin:14px 0 22px;font-variant-numeric:tabular-nums}caption{text-align:left;margin-bottom:10px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule);vertical-align:top}th{background:#edf0ed;white-space:normal}td{white-space:nowrap}details{margin:20px 0}summary{cursor:pointer;font-weight:600}li{margin:7px 0}.source-list{columns:2;overflow-wrap:anywhere}footer{font-size:.88rem;color:var(--muted);padding-top:22px}@media(max-width:650px){main{padding:24px 16px}.source-list{columns:1}th,td{padding:8px}section{padding:26px 0}}@media print{body{background:white}main{max-width:none;padding:0}.scroll{overflow:visible}table{font-size:8pt}nav{display:none}details>*{display:block}.source-list{columns:1}}
</style></head><body><main>
<header><div class="meta">RESEARCH RESULTS · STATIC EVIDENCE SNAPSHOT</div><h1>NeuroTwinBench &amp; StreamGLM</h1><p>Can spikes reveal neural wiring? Can we fit the models efficiently? Two related projects, with different success criteria.</p><p class="meta">Built '''+now+''' · Recorded outcomes, including negative results · No live job controls</p><nav aria-label="Page sections"><a href="#neurotwin">NeuroTwinBench</a><a href="#streamglm">StreamGLM</a><a href="#terms">Reading the scores</a><a href="#sources">Source files</a></nav></header>
<section><h2>What each project contributes</h2><p><strong>NeuroTwinBench</strong> simulates circuits with known wiring, fits a population GLM to spikes, and checks whether inferred coupling identifies actual edges. <strong>StreamGLM</strong> implements chunked GLM fitting and optional low-rank coupling to reduce computational demands. Both use spike data; these experiments do not infer wiring from EEG.</p></section>
<section id="neurotwin"><h2>NeuroTwinBench</h2><p>70-neuron HNN circuits; recurrent L2 and L5 excitatory projections thinned to connection probability 0.3. Fits use 1 ms bins, a 25 ms history, five basis functions, float64 and ridge 0.001.</p>
<div class="verdict"><strong>Positive finding:</strong> completed circuits show L2 edge ranking above all three jitter controls. Best completed L2 ROC-AUC: 0.807 (C12). This supports selective recovery within the tested simulation design.</div>
<div class="verdict limit"><strong>Boundary:</strong> L5 ROC-AUC advantages remain weak. Beating jitter and a distance-only baseline does not prove that every inferred influence is a direct synapse or eliminate every spatial/common-input confound.</div>'''+top_tables+'''
<p class="meta">Intervals resample neurons, keeping fitted models and circuits fixed. They exclude refitting uncertainty and are not confidence intervals over independent circuits. C15 has five times the recording duration of C11–C13; differences between their scores cannot isolate a duration effect. Only eligible, evaluable pairs within the modeled delay window are scored.</p>
<h3>Calibration: can the estimator recover a known GLM?</h3>'''+calibration+'''<p>Strong synthetic recovery supports the implementation under matched model assumptions. Population and pairwise GLMs perform similarly here; it does not establish a large population-model advantage.</p>
<h3>Other findings</h3><ul><li><strong>Dendritic location:</strong> mean paired coupling-area contrast '''+f"{location['mean_paired_area_difference']:.3f}"+''', conditional 95% interval '''+str([round(v,3) for v in location['conditional_node_interval95']])+''', across '''+str(location['n_pairs'])+''' pairs. A circuit-wide location swap changes inferred coupling; this is not a single-synapse causal effect. '''+link('location.json')+'''</li><li><strong>Shared input:</strong> observing versus hiding the specified shared drive changes L2 AUC by '''+f"{shared['paired_uncertainty']['auc_difference']:+.6f}"+'''. This construction shows no improvement from observing the drive; it does not establish that common input is generally harmless. '''+link('shared.json')+'''</li><li><strong>Dense-network limitation:</strong> distance-dependent weight ranks confound strength recovery with geometry. Sparse topology supplies meaningful absent-edge controls.</li><li><strong>Not established:</strong> whole-circuit reconstruction, 270-neuron generalization, or reliable fine-latency recovery.</li></ul>
<details><summary>Incomplete experiment checkpoints</summary><ul>'''+''.join('<li>'+s+'</li>' for s in states)+'''</ul></details></section>
<section id="streamglm"><h2>StreamGLM</h2><p>A JAX fitting implementation that processes history features in chunks, with dense and low-rank coupling options. It predicts expected spike counts/rates and estimates coupling filters. NeMoS is the reference comparison, not an engine invoked separately for each neuron by this project.</p>
<div class="verdict"><strong>Positive finding:</strong> low-rank fits improve held-out prediction and filter recovery on low-rank synthetic networks. The recorded memory pilots also favor StreamGLM.</div><div class="verdict limit"><strong>Boundary:</strong> low-rank fits lose on full-rank synthetic networks. NeMoS is faster in some repeat-fit comparisons. Neither memory savings nor predictive improvement establishes anatomical recovery.</div>'''+model_tables+'''
<p class="meta">Bits/spike are gains over a constant-rate baseline trained on the training split. Filter correlations are Pearson correlations including diagonal/self-history terms, not off-diagonal edge AUC. Two seeds are exploratory evidence. Low-rank and full models are different hypothesis classes.</p><p>'''+link('streamglm_selected.json','All selected fits')+' · '+link('streamglm_tuning_protocol.json','Selection protocol')+'''</p>
<details><summary>Failures and convergence — retained in the comparison</summary><p>The original 256 tuning candidates included 188 gradient-gate passes, 46 completed without passing the gate, 21 numerical failures and one timeout. The timeout retry completed but still failed the convergence gate. All 24 selected model results were available. Failed candidates were not eligible for selection; they remain part of the accounting.</p><p>Factorized models use a gradient gate in factor coordinates. Search budgets and solver configurations differ; the tuning timings are not a pure implementation-speed benchmark. '''+link('streamglm_tuning_report.md','Full tuning report')+' · '+link('streamglm_failure_audit.md','Failure audit')+'''</p></details>
<h3>Runtime and memory: wins and losses</h3>'''+timing+'''<p>These compare StreamGLM SciPy L-BFGS-B with NeMoS native LBFGS. First-fit timings include feature creation and compilation; repeats reuse caches, including NeMoS’s design. Imports and validation checks are excluded. The host is shared. These measurements do not establish superiority over all NeMoS solvers or its streaming capabilities.</p>
<h3>Real spikes: held-out prediction</h3>'''+real_table+'''<p>Coupling improves test prediction over a self-history baseline in these cohorts. Real recordings have no synaptic answer key, so these gains do not validate anatomical connectivity. The report’s optimizer-success flags do not imply the later strict 1e-5 gradient gate: selected gradient norms were approximately 1.07e-4 and 3.58e-4.</p>
<h3>What remains unresolved</h3><p>A 1,000-neuron independent-spike stress test demonstrates fitting feasibility, not planted connectivity recovery. '''+('No completed coupled-1,000-neuron report was found in the checked v8 experiment directories.' if not coupled else 'Coupled-1,000-neuron reports are included in the source bundle; their results require separate review before a headline claim.')+''' Broader recording/session replication and an equivalent streaming-versus-streaming NeMoS comparison remain needed before general performance claims.</p></section>
<section id="terms"><h2>Reading the scores</h2><dl><dt><strong>ROC-AUC</strong></dt><dd>How often a true edge ranks above a non-edge, with ties receiving half credit. Chance is 0.5. An AUC of 0.807 is not 80.7% reconstruction accuracy.</dd><dt><strong>Average precision (stored as pr_auc)</strong></dt><dd>A precision–recall summary; its random-ranking reference is approximately the edge prevalence. It is not the trapezoidal area under a plotted PR curve.</dd><dt><strong>Jitter</strong></dt><dd>Each spike is shifted randomly within ±50 ms and clipped to its segment boundaries. Counts are preserved and slow rate patterns approximately retained, while precise timing is disrupted. The same GLM is refit to each control.</dd><dt><strong>Spearman ρ versus filter correlation</strong></dt><dd>NeuroTwinBench calibration uses strength-rank correlation. StreamGLM’s synthetic comparison uses Pearson correlation of filter values. Neither is an edge AUC.</dd><dt><strong>Bits per spike</strong></dt><dd>Held-out log-likelihood improvement normalized by spikes. Positive values favor the tested model over the stated baseline; they are not percentages.</dd><dt><strong>Low rank</strong></dt><dd>Describes many pairwise interactions through fewer shared patterns. Helpful when this matches the underlying structure; potentially restrictive when it does not.</dd></dl></section>
<section id="sources"><h2>Evidence and reproducibility</h2><p>Report copies are bundled with this page so links work offline and when the folder is hosted. This is a selected evidence summary, not the complete raw spike/model archive. No simulations are started or changed by building the page.</p><ul class="source-list">'''+''.join('<li>'+link(m['file'],m['file'])+'</li>' for m in manifest)+'''</ul><p><a href="sources/manifest.json">Source manifest and snapshot time</a></p></section><footer>Plain HTML and CSS · No trackers, external fonts or JavaScript dependencies · Rebuild using scripts/build_results_page.py</footer></main></body></html>'''
    (out/'index.html').write_text(html)
    (sources/'manifest.json').write_text(json.dumps({'built_utc':now,'sources':manifest},indent=2))
    from split_results_pages import split_pages
    split_pages(html, manifest, now, ROOT, args.stream_root)

if __name__ == '__main__':
    main()
