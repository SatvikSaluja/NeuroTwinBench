"""Restartable sequential execution of the explicit pending-work manifest."""
import fcntl,json,os,signal,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from experiments.run_handoff import ROOT,RUN,run_step,variant,report
from neurotwinbench.reporting import write_json

def main():
 os.chdir(ROOT);RUN.mkdir(parents=True,exist_ok=True)
 lock=(RUN/'runner.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 def stop(*_):raise RuntimeError('pending runner interrupted')
 signal.signal(signal.SIGTERM,stop)
 manifest=RUN/'pending_manifest.json';ledger_path=RUN/'pending_ledger.json'
 ledger=json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
 try:
  while True:
   tasks=json.loads(manifest.read_text())['tasks']
   pending=[t for t in tasks if ledger.get(t['name'],{}).get('status')!='DONE']
   if not pending:break
   task=pending[0];name=task['name'];started=time.time()
   write_json(RUN/'pending_status.json',{'status':'RUNNING','task':name,'pid':os.getpid(),'updated_unix':time.time(),'completed':len([v for v in ledger.values() if v['status']=='DONE']),'total':len(tasks)})
   if task.get('variant'):variant(task['variant'],task.get('conn_seed',3))
   else:run_step(name,task['args'])
   ledger[name]={'status':'DONE','seconds':time.time()-started,'task':task,'updated_unix':time.time()}
   write_json(ledger_path,ledger)
  report()
  write_json(RUN/'status.json',{'status':'DONE','scope':'pending manifest; inspect convergence and controls','updated_unix':time.time()})
  write_json(RUN/'pending_status.json',{'status':'DONE','updated_unix':time.time()})
 except BaseException as exc:
  write_json(RUN/'pending_status.json',{'status':'FAILED','error':repr(exc),'updated_unix':time.time()})
  write_json(RUN/'status.json',{'status':'FAILED','error':repr(exc),'updated_unix':time.time()})
  raise

if __name__=='__main__':main()
