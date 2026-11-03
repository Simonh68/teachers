/* Public, read-only classroom data loader. No GitHub API or credentials. */
const GRADES = ['grade7','grade8','grade9','grade10','grade11','grade12'];
const cache = new Map();
export async function loadGrade(grade, {signal}={}) {
  if (!GRADES.includes(grade)) throw new Error('Unknown grade');
  if (cache.has(grade)) return cache.get(grade);
  const response = await fetch('./data/'+grade+'.json',{signal,cache:'no-cache'});
  if (!response.ok) throw new Error('Cannot load '+grade+' ('+response.status+')');
  const data=await response.json();
  if(data.schemaVersion!==1 || data.grade!==Number(grade.slice(5)) || !Array.isArray(data.materials)) throw new Error('Invalid classroom data');
  const seen=new Set();
  for(const item of data.materials){
    if(!item || typeof item.id!=='string'||typeof item.title!=='string'||typeof item.url!=='string'||typeof item.unit!=='string'||seen.has(item.id)) throw new Error('Invalid or duplicate item');
    seen.add(item.id);
    const u=new URL(item.url,location.href);
    if(!['https:','http:'].includes(u.protocol)) throw new Error('Unsupported URL');
    if(u.origin===location.origin && !u.pathname.startsWith(new URL('.',location.href).pathname)) throw new Error('Invalid local URL');
  }
  cache.set(grade,data);
  return data;
}
export function clearGradeCache(grade){cache.delete(grade);}
