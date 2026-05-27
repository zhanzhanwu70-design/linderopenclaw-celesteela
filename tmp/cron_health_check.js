const fs=require('fs');
const jobs=JSON.parse(fs.readFileSync('/home/node/.openclaw/cron/jobs.json','utf8')).jobs;
const states=JSON.parse(fs.readFileSync('/home/node/.openclaw/cron/jobs-state.json','utf8')).jobs;
const now=Date.parse('2026-05-26T12:30:00Z');
function dt(ms){return ms?new Date(ms).toISOString():'-'}
function periodMs(schedule){
 if(!schedule) return null;
 if(schedule.kind==='interval') return schedule.everyMs||schedule.intervalMs||null;
 if(schedule.kind==='cron'){
  const e=(schedule.expr||'').trim().split(/\s+/);
  const sec = e.length===6?e[0]:null;
  const min = e.length===6?e[1]:e[0];
  const hour = e.length===6?e[2]:e[1];
  if(sec && sec.startsWith('*/')) return Number(sec.slice(2))*1000;
  if(min && min.startsWith('*/')) return Number(min.slice(2))*60_000;
  if(hour && hour.startsWith('*/')) return Number(hour.slice(2))*3600_000;
  return null;
 }
 return null;
}
const rows=[]; const probs=[];
for(const j of jobs){
 const s=states[j.id]?.state||{};
 const enabled=j.enabled!==false;
 const runFile=`/home/node/.openclaw/cron/runs/${j.id}.jsonl`;
 let tail=''; try{ const txt=fs.readFileSync(runFile,'utf8').trim(); const lines=txt?txt.split(/\n/):[]; tail=lines.slice(-1)[0]||'';}catch{}
 let issues=[];
 if(enabled && !states[j.id]) issues.push('missing-state');
 if(enabled && (s.consecutiveErrors||0)>0) issues.push(`consecutiveErrors=${s.consecutiveErrors}`);
 if(enabled && s.lastRunStatus && s.lastRunStatus!=='ok') issues.push(`lastRunStatus=${s.lastRunStatus}`);
 if(enabled && s.lastStatus && !['ok','running'].includes(s.lastStatus)) issues.push(`lastStatus=${s.lastStatus}`);
 if(enabled && (s.consecutiveSkipped||0)>0) issues.push(`consecutiveSkipped=${s.consecutiveSkipped}`);
 if(enabled && s.lastDeliveryStatus && !['not-requested','delivered'].includes(s.lastDeliveryStatus)) issues.push(`delivery=${s.lastDeliveryStatus}`);
 const per=periodMs(j.schedule);
 if(enabled && s.lastRunAtMs && per && now-s.lastRunAtMs > per*2.5 + (j.schedule?.staggerMs||0)) issues.push(`stale-last-run ${Math.round((now-s.lastRunAtMs)/60000)}m ago`);
 if(enabled && s.nextRunAtMs && s.nextRunAtMs < now-10*60_000 && !s.runningAtMs) issues.push(`overdue-next ${Math.round((now-s.nextRunAtMs)/60000)}m`);
 if(enabled && s.runningAtMs && now-s.runningAtMs > 60*60_000) issues.push(`stuck-running ${Math.round((now-s.runningAtMs)/60000)}m`);
 if(issues.length) probs.push({j,s,issues,tail});
 rows.push({id:j.id,name:j.name,enabled,schedule:j.schedule,lastStatus:s.lastStatus,lastRunStatus:s.lastRunStatus,consecutiveErrors:s.consecutiveErrors||0,consecutiveSkipped:s.consecutiveSkipped||0,lastRun:dt(s.lastRunAtMs),nextRun:dt(s.nextRunAtMs),runningAt:dt(s.runningAtMs),delivery:s.lastDeliveryStatus||'',issues:issues.join('; ')});
}
console.log(JSON.stringify({now:dt(now), total:jobs.length, enabled:jobs.filter(j=>j.enabled!==false).length, disabled:jobs.filter(j=>j.enabled===false).length, problems:probs.length, rows, problemDetails:probs.map(p=>({id:p.j.id,name:p.j.name,schedule:p.j.schedule,state:p.s,issues:p.issues,tail:p.tail}))},null,2));
