"""Create two independent static pages from the combined report builder."""
import json
import re
import shutil
from html import escape
from pathlib import Path


def split_pages(html, manifest, built, hnn_root, stream_root):
    style = re.search(r'<style>.*?</style>', html, re.S).group(0)
    source_root = hnn_root / 'results_page/sources'
    # Capture bytes before replacing manifests in either destination.
    contents = {m['file']: (source_root / m['file']).read_bytes() for m in manifest}
    projects = [
        ('neurotwin', 'NeuroTwinBench', hnn_root,
         'Can spike activity reveal known synaptic wiring?',
         [('ROC-AUC', 'Ranks real connections above absent candidate pairs. Chance is 0.5; AUC is not reconstruction accuracy.'),
          ('Average precision', 'Precision–recall summary, stored as pr_auc. The random reference is approximately edge prevalence (~0.30).'),
          ('Jitter', 'Spikes move independently by up to ±50 ms, clipped within each recording segment. Spike counts are retained; slow activity structure is approximately retained. The model is refitted.'),
          ('Spearman correlation', 'Agreement in connection-strength ordering. Used in synthetic calibration, not interchangeable with edge AUC.'),
          ('Conditional intervals', 'Neuron resampling with the fitted models held fixed. These exclude refitting uncertainty and are not independent-circuit confidence intervals.')]),
        ('streamglm', 'StreamGLM', stream_root,
         'Efficient population GLM fitting: prediction, recovery, memory and runtime.',
         [('Bits per spike', 'Held-out log-likelihood gain per spike relative to the stated baseline. Positive is better; this is not a percentage.'),
          ('Filter correlation', 'Pearson correlation of reconstructed filter values, including self-history in the tuned benchmark. Not an edge-detection AUC.'),
          ('Low rank', 'Represents interactions through fewer shared patterns. Helps when the assumption matches the data and can hurt when it does not.'),
          ('Peak RSS', 'Peak resident process memory. Lower is better for the same workload; timing and measurement boundaries matter.'),
          ('Convergence gate', 'An independent gradient check used for candidate eligibility. Optimizer success alone is not equivalent to passing the strict gate.')]),
    ]
    for key, title, root, intro, terms in projects:
        dest = root / 'results_page'
        sources = dest / 'sources'
        sources.mkdir(parents=True, exist_ok=True)
        records = [m for m in manifest if m['file'].startswith('streamglm_') == (key == 'streamglm')]
        for m in records:
            (sources / m['file']).write_bytes(contents[m['file']])
        # Only remove known generated report copies belonging to the other page.
        for m in manifest:
            if m not in records and (sources / m['file']).exists():
                (sources / m['file']).unlink()
        section = re.search(r'<section id="'+key+r'">.*?</section>', html, re.S).group(0)
        glossary = ''.join('<dt><strong>'+escape(t)+'</strong></dt><dd>'+escape(d)+'</dd>' for t,d in terms)
        links = ''.join('<li><a href="sources/'+escape(m['file'])+'">'+escape(m['file'])+'</a></li>' for m in records)
        page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+' — Results</title>'+style+'</head><body><main>'
        page += '<header><div class="meta">RESEARCH RESULTS · STATIC SNAPSHOT</div><h1>'+title+'</h1><p>'+intro+'</p><p class="meta">Built '+escape(built)+' · Positive findings and limitations</p><nav aria-label="Page sections"><a href="#'+key+'">Results</a><a href="#terms">Reading the scores</a><a href="#sources">Source records</a><a href="../RESULTS_REPORT.md">Written report</a><a href="../SIMULATIONS.md">Run guide</a></nav></header>'
        page += section+'<section id="terms"><h2>Reading the scores</h2><dl>'+glossary+'</dl></section>'
        page += '<section id="sources"><h2>'+title+' source records</h2><p>Compact copies of the evidence used on this page. Raw recordings and feature caches are not included.</p><ul class="source-list">'+links+'</ul><p><a href="sources/manifest.json">Source manifest</a></p></section><footer>Plain HTML and CSS. No external dependencies. Saved checkpoints do not establish that a process is running.</footer></main></body></html>'
        (dest / 'index.html').write_text(page)
        (sources / 'manifest.json').write_text(json.dumps({'project':title,'built_utc':built,'sources':records},indent=2))
        print(dest / 'index.html')
