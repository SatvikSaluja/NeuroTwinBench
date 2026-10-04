"""Sequential corrected-study runner using the shared HNN process-group guard."""
import fcntl,json,os,signal,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiments.run_handoff import ROOT,RUN,run_step
from neurotwinbench.reporting import write_json

def main():
    os.chdir(ROOT);folder=ROOT/'results/phase2';folder.mkdir(parents=True,exist_ok=True)
    lock=(RUN/'runner.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    def stop(*_):raise RuntimeError('phase2 interrupted; restart reuses complete chunks and fitted parameters')
    signal.signal(signal.SIGTERM,stop)
    manifest=json.load(open(folder/'manifest.json'));ledger_path=folder/'ledger.json'
    ledger=json.load(open(ledger_path)) if ledger_path.exists() else {}
    try:
        for task in manifest['tasks']:
            if ledger.get(task['name'],{}).get('status')=='DONE':continue
            write_json(folder/'status.json',{'status':'RUNNING','pid':os.getpid(),'task':task['name'],'completed':len(ledger),'total':len(manifest['tasks']),'updated_unix':time.time()})
            start=time.time();run_step(task['name'],task['args'])
            ledger[task['name']]={'status':'DONE','seconds':time.time()-start};write_json(ledger_path,ledger)
        write_json(folder/'status.json',{'status':'DONE','completed':len(ledger),'updated_unix':time.time(),'note':'execution complete; inspect convergence and uncertainty before claims'})
        write_json(RUN/'status.json',{'status':'DONE','scope':'phase2','updated_unix':time.time()})
    except BaseException as exc:
        write_json(folder/'status.json',{'status':'FAILED','error':repr(exc),'updated_unix':time.time()});write_json(RUN/'status.json',{'status':'FAILED','scope':'phase2','error':repr(exc),'updated_unix':time.time()});raise
if __name__=='__main__':main()
