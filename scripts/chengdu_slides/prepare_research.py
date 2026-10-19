"""Transform sourced researcher output into an explicitly unapproved illustrated draft."""
import argparse
import copy
import json
from pathlib import Path
from string import Formatter
from decimal import Decimal
from .illustrations import write_illustration
from .evidence import evaluate_gift
from .model import PARTS

LANGS=('th','zh-Hans')


def _paginate_unit(unit: dict, *, community: bool = False) -> list[dict]:
    """Keep translation bullet boundaries identical; split dense pages, not fonts."""
    count=len(unit['body']['th'])
    if count!=len(unit['body']['zh-Hans']):
        raise ValueError('bilingual bullet boundaries differ for '+unit['id'])
    limit=2 if community else 4
    chunk=2 if community else 3
    if count<=limit:
        return [unit]
    offsets=list(range(0,count,chunk));result=[]
    for index,offset in enumerate(offsets):
        part=copy.deepcopy(unit)
        part['id']=unit['id'] if index==0 else unit['id']+'-part-'+str(index+1)
        part['original_unit_id']=unit['id']
        part['body']={lang:unit['body'][lang][offset:offset+chunk] for lang in LANGS}
        part['title']={lang:unit['title'][lang]+' · '+str(index+1)+'/'+str(len(offsets)) for lang in LANGS}
        part['fact_ids']=sorted({name for line in part['body']['th'] for _,name,_,_ in Formatter().parse(line) if name is not None})
        result.append(part)
    return result


def prepare_report(report: dict, root: Path, meta: dict) -> dict:
    data={'meta':copy.deepcopy(meta),'sources':copy.deepcopy(report['sources']),
          'attractions':copy.deepcopy(report.get('attractions',[])),
          'restaurants':copy.deepcopy(report.get('restaurants',[])),
          'gifts':[],'assets':[],'support':[]}
    data['meta']['status']='research_incomplete'
    community_policy=meta.get('gift_policy')=='community_curated'
    if community_policy:
        data['gifts']=copy.deepcopy(report.get('gifts',[]))
    sources={s['id']:s for s in data['sources']}
    for category in ('attractions','restaurants','gifts'):
        for item in data[category]:
            if category=='gifts':
                assessment=evaluate_gift(item,sources,Decimal('30'),policy=meta.get('gift_policy','verified_market'))
                if not assessment['qualified']:
                    raise ValueError(item['id']+': '+'; '.join(assessment['reasons']))
            item['stage']='sourced_draft'
            asset=write_illustration(item,sources,root)
            data['assets'].append(asset)
            paginated=[]
            for unit in item['units']:
                unit['asset_id']=asset['id']
                unit['alt']={'th':'ภาพวาดแนวคิดประกอบ '+item['name']['th']+' ไม่ใช่ภาพถ่ายสถานที่ อาหาร หรือสินค้าจริง',
                             'zh-Hans':item['name']['zh-Hans']+'概念插画，非景点、菜品或商品实拍。'}
                paginated.extend(_paginate_unit(unit,community=category=='gifts' and community_policy))
            item['units']=paginated
    font_sources={'Kanit':('TravelDisplay','kanit'),
                  'NotoSansThai':('TravelThai','notosansthai'),
                  'NotoSerifSC':('TravelChinese','notoserifsc')}
    for family,(filename,slug) in font_sources.items():
        folder=root/'slides/chengdu/fonts'
        actual=filename+'.woff2' if (folder/(filename+'.woff2')).exists() else filename+'.ttf'
        if not (folder/actual).exists():
            continue
        data['assets'].append({'id':'font-'+family,'kind':'font','path':'slides/chengdu/fonts/'+actual,
             'creator':'Google Fonts project contributors','license':'SIL Open Font License 1.1',
             'license_url':'https://openfontlicense.org/','source_url':'https://github.com/google/fonts/tree/main/ofl/'+slug,
             'modifications':'Locally generated WOFF2; Chinese glyph subset with derivative family name; original OFL notice retained' if actual.endswith('.woff2') else 'Downloaded TTF, unmodified',
             'license_path':'slides/chengdu/fonts/'+family+'_OFL.txt'})
    reference_ids=['panda-official'] if 'panda-official' in sources else [s['id'] for s in data['sources'][:1]]
    guide={'id':'chengdu-guide','category':'guide','name':{'th':'อ่านก่อนเปิดคู่มือ','zh-Hans':'阅读说明'},'source_ids':reference_ids}
    illustration=write_illustration(guide,sources,root)
    data['assets'].append(illustration)
    common={'asset_id':illustration['id'],'source_ids':reference_ids,'fact_ids':[],'facts':{},
            'alt':{'th':'ภาพวาดแนวคิดประกอบคู่มือเฉิงตู ไม่ใช่ภาพถ่ายสถานที่จริง','zh-Hans':'成都指南概念插画，非景点实拍。'}}
    units=[('guide-cover','guide',
            {'th':'เฉิงตู: เที่ยว กิน และเลือกของฝากอย่างมีข้อมูล','zh-Hans':'成都：景点、美食与有据可查的伴手礼'},
            {'th':['ฉบับร่างเพื่ออ่านและตรวจข้อมูล ยังไม่ใช่คำแนะนำซื้อของฝากที่ผ่านเกณฑ์ทั้งหมด',
                   'สถานที่เที่ยวและร้านอาหารแยกหน้าแนะนำกับหน้าวางแผน: ไทยตามด้วยจีนตัวย่อของเนื้อหาเดียวกัน',
                   'แต่ละหน้ามีลิงก์แหล่งข้อมูล และระบุข้อจำกัดของเวลาเปิด ราคา และการเดินทางตามที่ตรวจได้',
                   'ภาพทุกหน้าเป็นภาพวาดแนวคิดที่สร้างขึ้น ไม่ใช่ภาพถ่ายยืนยันว่าสถานที่หรืออาหารจริงหน้าตาเช่นนั้น'],
             'zh-Hans':['本稿用于阅读和核查资料，尚不是满足全部证据条件的伴手礼购买推荐。',
                        '景点和餐厅各有介绍页与实用规划页：泰文页后紧接内容对应的简体中文页。',
                        '页面附信息来源链接；营业时间、价格和交通均保留核查时发现的限制。',
                        '所有配图均为原创概念插画，不是证明景点或菜品真实外观的照片。']}),
           ('guide-controls','guide',
            {'th':'วิธีอ่านและใช้คู่มือนี้','zh-Hans':'如何阅读与使用'},
            {'th':['ใช้ลูกศรซ้าย–ขวา ปุ่มก่อนหน้า–ถัดไป หรือปัดแนวนอนเพื่อเปลี่ยนหน้า; สารบัญเลือกหน้าได้โดยตรง',
                   'ปุ่มไทย / 中文 สลับเฉพาะภาษาของหน้าปัจจุบัน ไม่ข้ามไปยังคนละรายการ',
                   'บนมือถือใช้ปุ่มอ่าน / 阅读 เพื่อเปลี่ยนเป็นบทความเรียงยาวและอ่านตัวอักษรขนาดปกติ',
                   'คำแนะนำระยะเวลา งบ และการจัดกลุ่มเส้นทางเป็นแนวทางวางแผน ไม่ใช่คำยืนยันราคาเปิดขายหรือเวลาคิวสด'],
             'zh-Hans':['可用左右方向键、前后按钮或横向滑动换页，也可通过目录直接选择页面。',
                        '“ไทย / 中文”只切换当前内容的语言，不会跳到另一条目。',
                        '手机上可点“อ่าน / 阅读”切换为连续文章，以正常字号阅读。',
                        '游览时长、预算和路线分组属于规划建议，不保证实时售价或排队时长。']}),
           ('guide-gift-status','guide',
            {'th':'ของฝาก: ยังไม่ผ่านหลักฐานเงื่อนไขซื้อ','zh-Hans':'伴手礼：购买条件证据尚未达标'},
            {'th':['ยังไม่มีรายการที่ยืนยันครบทั้งสินค้า/ขนาดเดียวกัน ช่องทางซื้อที่ใช้ได้ และเงื่อนไขความคุ้มค่าตามเกณฑ์',
                   'หน้าค้น Shopee ที่ไม่แสดงผลสินค้าหรือเข้าไม่ได้ ไม่ได้พิสูจน์ว่าไม่มีสินค้านั้นขาย',
                   'ราคาหน้าเว็บที่ถูกกว่าแต่หมดสต็อก รุ่นไม่ตรง หรือยังไม่รวมค่าใช้จ่ายที่เกี่ยวข้อง ไม่ถือเป็นส่วนต่างราคาที่ซื้อได้จริง',
                   'จึงเว้นหมวดของฝากที่ผ่านเกณฑ์ไว้ก่อน ไม่เติมสินค้าทั่วไปหรือราคาเดาเพื่อทำจำนวนให้ครบ'],
             'zh-Hans':['目前没有条目同时核实同型号/规格、可用购买渠道及满足门槛的实际价格优势。',
                        'Shopee搜索页不展示商品或无法访问，并不能证明该商品没有销售。',
                        '更低的网页标价若缺货、型号不一致或尚未计入相关费用，不能视为实际可购买的价差。',
                        '因此暂不列入已达标伴手礼，不用普通商品或猜测价格凑足数量。']})]
    if community_policy:
        units[0][3]['th'][0]='ข้อมูลเที่ยวและกินประกอบการวางแผน ส่วนของฝากคัดจากความเห็นผู้เดินทาง ไม่ใช่รายการรับรองราคาหรือสต็อกสด'
        units[0][3]['zh-Hans'][0]='景点与餐饮信息用于规划；伴手礼依据旅行者意见筛选，不是实时价格或库存认证清单。'
        units[2]=('guide-gift-status','guide',
                  {'th':'ของฝาก: คัดจากความเห็นชุมชน','zh-Hans':'伴手礼：社区意见筛选'},
                  {'th':['รวมคำแนะนำและเหตุผลที่ไม่คุ้มซื้อจากกระทู้หรือคอมเมนต์จริง แล้วคัดเป็นตัวเลือก ไม่ใช่คำรับรองของร้านค้า',
                         'คำว่าในไทยมีขายหรือซื้อจีนคุ้มกว่าเป็นความเห็น ณ เวลาที่โพสต์ ไม่ยืนยันราคาหรือสต็อกของ Shopee และ Lazada ในปัจจุบัน',
                         'วันที่เก่า แหล่งเดียว หรือข้อความที่อ่านได้เพียงบางส่วนจะระบุข้อจำกัด ไม่เรียกว่าเป็นฉันทามติของนักท่องเที่ยวทั้งหมด',
                         'ก่อนซื้อให้เทียบรุ่น คุณภาพ น้ำหนักและการหิ้วกลับ พร้อมตรวจข้อกำหนดนำเข้าไทย ไม่สมมติว่าทุกชิ้นถูกกว่าหรือไม่มีขายออนไลน์'],
                   'zh-Hans':['汇集真实帖文或评论中的推荐与不值得购买理由，再筛成选项，不代表商家保证。',
                              '泰国有售或在中国更划算均为发帖时的观点，不确认Shopee或Lazada当前的价格与库存。',
                              '旧资料、单一讨论或只能读取节选的来源会标明限制，不宣称代表所有游客共识。',
                              '购买前比较型号、品质、重量和携带条件，并核对泰国入境要求；不假定每件都更便宜或网购不到。']})
    for identity,kind,title,body in units:
        unit=copy.deepcopy(common);unit.update({'id':identity,'kind':kind,'title':title,'body':body})
        data['support'].append(unit)
    return data


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report',type=Path)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    args=parser.parse_args();root=args.root.resolve()
    directory=root/'_data/chengdu_slides'
    meta=json.loads((directory/'meta.json').read_text())
    data=prepare_report(json.loads(args.report.read_text()),root,meta)
    for name in PARTS:
        (directory/(name+'.json')).write_text(json.dumps(data[name],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':data['meta']['status'],'counts':{k:len(data[k]) for k in ('attractions','restaurants','gifts')},'assets':len(data['assets'])},ensure_ascii=False))


if __name__=='__main__':main()
