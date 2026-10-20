"""Lossless regrouping and validated, browser-measured Thai-primary page plans."""
import copy
import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
LANGS=('th','zh-Hans')
POLICY='thai-first-measured'


def ordered_entries(data):
    placements=('after_gifts','before_attractions','before_restaurants','before_gifts')
    entries=[(None,u) for u in data.get('support',[]) if u.get('placement') not in placements]
    for category in ('attractions','restaurants','gifts'):
        entries.extend((None,u) for u in data.get('support',[]) if u.get('placement')=='before_'+category)
        entries.extend((item,u) for item in data.get(category,[]) for u in item.get('units',[]))
    entries.extend((None,u) for u in data.get('support',[]) if u.get('placement')=='after_gifts')
    return entries


def _title(text, name=''):
    text=re.sub(r'\s*·\s*\d+/\d+\s*$','',text)
    prefix=name+' · '
    return text[len(prefix):] if name and text.startswith(prefix) else text


def _regroup(units, names=None):
    groups=[]; previous=None
    for unit in units:
        titles={lang:_title(unit.get('title',{}).get(lang,''),(names or {}).get(lang,'')) for lang in LANGS}
        key=(unit.get('placement'),unit.get('kind'),tuple(titles.values()))
        if key!=previous:
            group=copy.deepcopy(unit)
            group['id']=unit.get('original_unit_id') or re.sub(r'-(?:present|part)-\d+$','',unit['id'])
            group['title']=titles; group['body']={lang:[] for lang in LANGS}
            group['legacy_ids']=[]; group['source_ids']=[]; group['fact_ids']=[]
            for field in ('continuation','original_unit_id','pagination'):group.pop(field,None)
            groups.append(group)
        group=groups[-1]
        for lang in LANGS:group['body'][lang].extend(unit['body'][lang])
        for field,values in (('legacy_ids',unit.get('legacy_ids',[unit['id']])),('source_ids',unit.get('source_ids',[])),('fact_ids',unit.get('fact_ids',[]))):
            group[field]=list(dict.fromkeys(group[field]+values))
        previous=key
    for lang in LANGS:
        if [text for unit in units for text in unit['body'][lang]] != [text for unit in groups for text in unit['body'][lang]]:
            raise ValueError('regrouping changed source text/order')
    return groups


def regroup_dataset(data):
    result=copy.deepcopy(data)
    result['meta']['pagination_policy']=POLICY
    result['meta'].pop('pagination_signature',None)
    for category in ('attractions','restaurants','gifts'):
        for item in result.get(category,[]):item['units']=_regroup(item['units'],item.get('name'))
    result['support']=_regroup(result.get('support',[]))
    return result


def layout_signature(data):
    layout=copy.deepcopy(data)
    layout.pop('pagination',None)
    layout.get('meta',{}).pop('pagination_signature',None)
    layout.get('meta',{}).pop('status',None)
    for _,unit in ordered_entries(layout):unit.pop('pagination',None)
    digest=hashlib.sha256(json.dumps(layout,ensure_ascii=False,sort_keys=True).encode())
    for relative in ('scripts/chengdu_slides/render.py','scripts/chengdu_slides/pagination.py',
                     'scripts/chengdu_slides/measure-pagination.mjs','scripts/chengdu_slides/viewport-base.css',
                     'slides/chengdu/deck.css'):
        path=ROOT/relative
        if path.is_file():digest.update(path.read_bytes())
    for asset in sorted(data.get('assets',[]),key=lambda a:a.get('id','')):
        if asset.get('kind')=='font':digest.update((ROOT/asset['path']).read_bytes())
    return digest.hexdigest()


def _range(value, start, stop):
    return (isinstance(value,list) and len(value)==2 and all(type(x) is int for x in value)
            and value[0]==start and start<value[1]<=stop)


def validate_pagination(data):
    planned=any('pagination' in unit for _,unit in ordered_entries(data))
    if not data.get('meta',{}).get('pagination_policy') and not planned:return []
    findings=[]
    def issue(path,message):findings.append({'code':'pagination','path':path,'message':message})
    if data.get('meta',{}).get('pagination_policy')!=POLICY:issue('meta/pagination_policy','missing/unknown page policy')
    if data['meta'].get('pagination_signature')!=layout_signature(data):
        issue('meta/pagination_signature','layout inputs changed; remeasure before release')
    seen=set()
    for _,unit in ordered_entries(data):
        identity=unit.get('id'); path='pagination/'+str(identity)
        if identity in seen:issue(path,'duplicate topic ID')
        seen.add(identity)
        bodies=unit.get('body',{}); n=len(bodies.get('th',[]))
        if not n or n!=len(bodies.get('zh-Hans',[])):
            issue(path,'source bilingual bullet correspondence is required');continue
        pages=unit.get('pagination')
        if not isinstance(pages,list) or not pages:issue(path,'missing measured page plan');continue
        start=0
        for page in pages:
            if not isinstance(page,dict) or not _range(page.get('th'),start,n):
                issue(path,'Thai ranges must cover each source bullet once in order');break
            end=page['th'][1]; chinese=page.get('zh-Hans')
            if not isinstance(chinese,list) or not chinese:
                issue(path,'each Thai page requires corresponding Chinese pages');break
            cursor=start
            for window in chinese:
                if not _range(window,cursor,end):
                    issue(path,'Chinese pages must partition their Thai window without gaps or duplication');break
                cursor=window[1]
            if cursor!=end:issue(path,'Chinese range does not cover its Thai page')
            start=end
        if start!=n:issue(path,'Thai plan does not cover the complete source body')
    return findings


def unit_pages(unit):
    """Each Thai window anchors one or more Chinese pages; switching uses topic ID."""
    plan=unit.get('pagination')
    if plan is None:
        for lang in LANGS:
            yield {'lang':lang,'id':unit['id']+'--'+lang,'body':unit['body'].get(lang,[]),
                   'part':1,'total':1,'primary':0,'continuation':unit.get('continuation',{})}
        return
    totals={'th':len(plan),'zh-Hans':sum(len(page['zh-Hans']) for page in plan)}
    counts={lang:0 for lang in LANGS}
    for primary,page in enumerate(plan):
        for lang,windows in (('th',[page['th']]),('zh-Hans',page['zh-Hans'])):
            for start,end in windows:
                counts[lang]+=1; part=counts[lang]
                identity=unit['id']+('-page-'+str(part) if part>1 else '')+'--'+lang
                yield {'lang':lang,'id':identity,'body':unit['body'][lang][start:end],
                       'part':part,'total':totals[lang],'primary':primary,
                       'continuation':{'part':part,'total':totals[lang]} if totals[lang]>1 else {}}


def main():
    """Regenerate measured plans locally; --write explicitly updates canonical data."""
    import argparse
    import subprocess
    from .model import load_dataset, PARTS
    from .render import render_deck
    from .validation import validate_dataset
    from .asset_validation import validate_assets
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    directory=ROOT/'_data/chengdu_slides'
    source=load_dataset(directory); data=regroup_dataset(source)
    reports=ROOT/'_reports/chengdu-thai-first'; reports.mkdir(parents=True,exist_ok=True)
    (reports/'source-before.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
    (reports/'measurement-input.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    probe=render_deck(data,measure=True).replace('<head>','<head><base href="'+(ROOT/'slides/chengdu').as_uri()+'/">',1)
    (reports/'probe.html').write_text(probe,encoding='utf-8')
    subprocess.run(['node','scripts/chengdu_slides/measure-pagination.mjs',str(reports/'measurement-input.json'),str(reports/'probe.html'),str(reports/'measured.json')],cwd=ROOT,check=True)
    measured=json.loads((reports/'measured.json').read_text())
    measured['meta']['pagination_signature']=layout_signature(measured)
    findings=validate_pagination(measured)+validate_dataset(measured,publication=True)+validate_assets(measured,ROOT)
    if findings:raise ValueError(json.dumps(findings,ensure_ascii=False))
    for category in ('attractions','restaurants','gifts'):
        for before,after in zip(source[category],measured[category]):
            for lang in LANGS:
                if [t for u in before['units'] for t in u['body'][lang]] != [t for u in after['units'] for t in u['body'][lang]]:
                    raise ValueError('entry text/order changed: '+before['id'])
            for key in ('facts','details','identity_key','purchase_evidence'):
                if before.get(key)!=after.get(key):raise ValueError('entry evidence changed: '+before['id'])
    (reports/'measured.json').write_text(json.dumps(measured,ensure_ascii=False,indent=2)+'\n')
    if args.write:
        for name in PARTS:(directory/(name+'.json')).write_text(json.dumps(measured[name],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'canonical_written':args.write,'source_text_and_evidence_preserved':True,'signature':measured['meta']['pagination_signature']}))


if __name__=='__main__':main()
