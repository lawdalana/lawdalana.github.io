"""Command-line validation and explicitly contained local preview generation."""
import argparse
import json
from pathlib import Path
from .model import load_dataset
from .validation import validate_dataset
from .asset_validation import validate_assets
from .render import build_deck,build_preview


def main():
    root=Path(__file__).resolve().parents[2]
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','preview','build'])
    parser.add_argument('--publication',action='store_true')
    parser.add_argument('--output',type=Path,default=root/'_reports/chengdu-slides/draft')
    args=parser.parse_args();directory=root/'_data/chengdu_slides'
    try:
        if args.command=='validate':
            data=load_dataset(directory)
            result=validate_dataset(data,publication=args.publication)+validate_assets(data,root)
            print(json.dumps({'valid':not result,'publication':args.publication,'findings':result},ensure_ascii=False,indent=2))
            return 1 if result else 0
        result=build_preview(directory,root,args.output) if args.command=='preview' else build_deck(directory,root)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,KeyError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False));return 1


if __name__=='__main__':raise SystemExit(main())
