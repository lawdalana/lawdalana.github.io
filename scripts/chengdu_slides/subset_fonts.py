"""Build locally served, OFL-attributed WOFF2 derivatives; no network requests."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path


def main():
    from fontTools import subset
    from fontTools.ttLib import TTFont
    parser=argparse.ArgumentParser(description=__doc__)
    root=Path(__file__).resolve().parents[2]
    parser.add_argument('--source-dir',type=Path,default=root/'_reports/chengdu-slides/font-sources')
    args=parser.parse_args();args.source_dir.mkdir(parents=True,exist_ok=True)
    folder=root/'slides/chengdu/fonts'
    text=''.join(p.read_text() for p in (root/'_data/chengdu_slides').glob('*.json'))+'蜀ไทย中文อ่าน阅读สารบัญ目录'
    requested={ord(c) for c in text if not c.isspace() and not 0x0e00<=ord(c)<=0x0e7f}|set(range(32,127))
    audit=[]
    for original,derivative,should_subset in [('Kanit-Medium','TravelDisplay',False),('NotoSansThai','TravelThai',False),('NotoSerifSC','TravelChinese',True)]:
        source=args.source_dir/(original+'.ttf')
        if not source.exists():
            incoming=folder/(original+'.ttf')
            if not incoming.exists():raise FileNotFoundError('font source unavailable: '+str(source))
            shutil.copy2(incoming,source)
        font=TTFont(source,recalcTimestamp=False)
        available=set(font.getBestCmap())
        if should_subset:
            options=subset.Options();options.recalc_timestamp=False
            subsetter=subset.Subsetter(options=options)
            subsetter.populate(unicodes=requested&available)
            subsetter.subset(font)
        for record in font['name'].names:
            if record.nameID in (1,3,4,6,16):
                record.string=derivative.encode(record.getEncoding(),errors='replace')
        font.flavor='woff2';destination=folder/(derivative+'.woff2');font.save(destination);font.close()
        verified=TTFont(destination)
        if should_subset and not (requested&available)<=set(verified.getBestCmap()):
            raise ValueError('font subset lost requested supported characters')
        verified.close()
        audit.append({'source':str(source.relative_to(root)),'output':str(destination.relative_to(root)),
                      'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                      'output_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),
                      'source_bytes':source.stat().st_size,'output_bytes':destination.stat().st_size,
                      'subset':should_subset,'requested_supported_codepoints':len(requested&available),
                      'original_license_notice':'retained in *_OFL.txt; copyright/name licensing records retained'})
        original_path=folder/(original+'.ttf')
        if original_path.exists():original_path.unlink()
    target=root/'_reports/chengdu-slides/font-audit.json'
    target.write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps(audit,indent=2))


if __name__=='__main__':main()
