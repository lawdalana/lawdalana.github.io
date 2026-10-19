"""Original non-documentary SVG illustrations for the travel reading draft."""
import html
import re
from pathlib import Path


def write_illustration(item: dict, sources: dict[str, dict], root: Path) -> dict:
    identity = item['id']
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', identity):
        raise ValueError('unsafe item identifier for image filename')
    kind = item.get('category', 'guide')
    key = identity.lower()
    green, red, gold = '#224d3e', '#ad4230', '#b4985c'
    if kind == 'restaurants':
        scene = f'''<ellipse cx="550" cy="720" rx="330" ry="100" fill="{gold}" opacity=".3"/><ellipse cx="550" cy="640" rx="320" ry="145" fill="{green}"/><path d="M230 635 Q260 920 550 920 Q840 920 870 635" fill="{green}"/><ellipse cx="550" cy="630" rx="280" ry="115" fill="{red}"/><path d="M330 580 Q530 760 780 590 M350 650 Q540 500 760 650 M400 545 Q540 720 690 550" fill="none" stroke="#e9d7a6" stroke-width="25" stroke-linecap="round"/><path d="M900 340 L660 660 M945 375 L710 690" stroke="{gold}" stroke-width="18"/><path d="M430 475 Q350 350 445 270 M560 450 Q470 320 565 235" fill="none" stroke="{gold}" stroke-width="12" opacity=".7"/>'''
    elif 'panda' in key:
        scene = f'''<g stroke="{green}" stroke-width="12" fill="none"><path d="M200 920 L280 260 M880 930 L800 270"/><path d="M260 440 L170 370 M245 570 L350 510 M830 460 L920 350 M850 650 L750 550"/></g><ellipse cx="550" cy="760" rx="230" ry="200" fill="{green}"/><ellipse cx="550" cy="700" rx="175" ry="170" fill="#fbf5e8"/><circle cx="400" cy="390" r="75" fill="{green}"/><circle cx="700" cy="390" r="75" fill="{green}"/><ellipse cx="550" cy="510" rx="210" ry="175" fill="#fbf5e8" stroke="{green}" stroke-width="9"/><ellipse cx="465" cy="500" rx="49" ry="67" transform="rotate(30 465 500)" fill="{green}"/><ellipse cx="635" cy="500" rx="49" ry="67" transform="rotate(-30 635 500)" fill="{green}"/><circle cx="470" cy="490" r="13" fill="white"/><circle cx="630" cy="490" r="13" fill="white"/><ellipse cx="550" cy="575" rx="30" ry="20" fill="{green}"/>'''
    elif any(word in key for word in ('qingcheng','mountain')):
        scene = f'''<circle cx="770" cy="350" r="90" fill="{red}" opacity=".8"/><path d="M90 870 L350 330 L560 700 L710 430 L1020 900Z" fill="{green}"/><path d="M170 860 L360 430 L400 580 L520 820 M620 850 L720 550 L820 820" fill="none" stroke="{gold}" stroke-width="9"/><path d="M450 1000 Q700 900 530 800 Q430 710 560 650" fill="none" stroke="#f4efe3" stroke-width="28"/>'''
    elif 'dujiang' in key:
        scene = f'''<path d="M480 250 Q300 440 520 620 Q700 800 480 990 M565 250 Q390 440 600 610 Q790 800 570 990" stroke="{green}" stroke-width="48" fill="none"/><path d="M530 580 Q750 540 990 700" stroke="{gold}" stroke-width="34" fill="none"/><path d="M565 600 L495 675 L540 710" fill="{red}"/><text x="120" y="430" font-family="serif" font-size="27" fill="{green}">YUZUI</text><text x="670" y="530" font-family="serif" font-size="27" fill="{green}">FEISHAYAN</text><text x="650" y="860" font-family="serif" font-size="27" fill="{green}">BAOPINGKOU</text>'''
    else:
        scene = f'''<circle cx="810" cy="360" r="80" fill="{red}"/><path d="M150 520 Q310 520 390 390 L710 390 Q790 520 950 520 L860 560 L240 560Z" fill="{green}"/><path d="M250 730 L250 570 L850 570 L850 730 M170 750 L930 750" fill="none" stroke="{green}" stroke-width="24"/><path d="M330 570 L330 730 M460 570 L460 730 M640 570 L640 730 M770 570 L770 730" stroke="{gold}" stroke-width="20"/><path d="M200 820 Q400 760 550 840 Q700 920 920 810" stroke="{green}" stroke-width="10" fill="none"/><path d="M150 900 Q400 840 550 920 Q750 1000 980 910" stroke="{gold}" stroke-width="8" fill="none"/>'''
    if 'sanxingdui' in key:
        scene=f'<path d="M250 430 L400 360 L700 360 L850 430 L810 780 L650 860 L450 860 L290 780Z" fill="{green}"/><path d="M280 490 L470 450 L510 550 L290 570 M820 490 L630 450 L590 550 L810 570" fill="{gold}"/><path d="M510 460 L550 630 L590 460 M420 720 Q550 810 680 720" fill="none" stroke="{gold}" stroke-width="24"/><path d="M250 500 L170 460 L170 700 L290 650 M850 500 L930 460 L930 700 L810 650" fill="{green}"/><circle cx="390" cy="515" r="25" fill="{red}"/><circle cx="710" cy="515" r="25" fill="{red}"/>'
    elif 'leshan' in key:
        scene=f'<path d="M120 900 L210 400 L380 300 L520 390 L750 300 L950 460 L1010 920Z" fill="{green}"/><ellipse cx="550" cy="720" rx="230" ry="170" fill="{gold}"/><rect x="420" y="510" width="260" height="250" rx="100" fill="{gold}"/><circle cx="550" cy="430" r="90" fill="{gold}"/><path d="M330 680 L430 800 L470 930 M770 680 L670 800 L630 930" stroke="{gold}" stroke-width="65" fill="none"/><path d="M90 1000 Q400 920 550 980 Q800 1030 1010 950" stroke="{red}" stroke-width="14" fill="none"/>'
    elif 'park' in key or 'huanhua' in key:
        scene=f'<ellipse cx="550" cy="810" rx="410" ry="110" fill="{gold}" opacity=".5"/><path d="M170 780 Q550 480 930 780" stroke="{green}" stroke-width="50" fill="none"/><path d="M180 700 Q550 410 920 700" stroke="{green}" stroke-width="12" fill="none"/><path d="M240 680 L240 760 M400 590 L400 670 M700 590 L700 670 M860 680 L860 760" stroke="{green}" stroke-width="12"/><path d="M190 390 L190 650 M900 390 L900 650" stroke="{green}" stroke-width="25"/><circle cx="190" cy="370" r="100" fill="{green}"/><circle cx="900" cy="370" r="100" fill="{green}"/><path d="M230 940 Q500 870 850 940" stroke="{red}" stroke-width="10" fill="none"/>'
    elif 'museum' in key:
        windows=''.join(f'<rect x="{280+i*105}" y="{500+j*110}" width="60" height="65" fill="#e7dfc9"/>' for i in range(5) for j in range(3))
        scene=f'<path d="M180 460 L460 310 L910 400 L910 880 L180 880Z" fill="{green}"/>{windows}<path d="M130 920 L960 920" stroke="{gold}" stroke-width="30"/>'
    elif any(word in key for word in ('mi-xun','teahouse')):
        scene=f'<ellipse cx="550" cy="850" rx="330" ry="65" fill="{gold}"/><path d="M310 500 Q550 420 720 530 L720 700 Q530 850 320 690Z" fill="{green}"/><path d="M720 530 Q950 440 840 650 L720 700" fill="none" stroke="{green}" stroke-width="45"/><path d="M320 560 Q180 530 170 400 L210 400 Q220 470 360 490" fill="{green}"/><ellipse cx="520" cy="500" rx="220" ry="45" fill="{gold}"/><path d="M510 310 Q430 230 520 200" fill="none" stroke="{red}" stroke-width="14"/>'
    elif any(word in key for word in ('chunxi','ifs')):
        scene=f'<rect x="200" y="500" width="700" height="450" fill="{green}"/><path d="M260 550 L260 900 M400 550 L400 900 M540 550 L540 900 M680 550 L680 900 M820 550 L820 900 M220 650 L880 650 M220 780 L880 780" stroke="{gold}" stroke-width="8"/><ellipse cx="560" cy="465" rx="150" ry="120" fill="#fbf5e8"/><circle cx="450" cy="360" r="50" fill="{green}"/><circle cx="670" cy="360" r="50" fill="{green}"/><ellipse cx="560" cy="415" rx="130" ry="100" fill="#fbf5e8"/><ellipse cx="510" cy="410" rx="28" ry="40" fill="{green}"/><ellipse cx="610" cy="410" rx="28" ry="40" fill="{green}"/><ellipse cx="560" cy="465" rx="18" ry="14" fill="{green}"/>'
    label = identity.replace('-', ' ').replace('_',' ').upper()
    lines = [label[i:i+32] for i in range(0,len(label),32)]
    text = ''.join(f'<text x="85" y="{150+i*42}" font-family="serif" font-size="35" letter-spacing="2" fill="{green}">{html.escape(line)}</text>' for i,line in enumerate(lines[:2]))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 1100" width="1100" height="1100"><title>Original conceptual illustration: {html.escape(identity)}</title><rect width="1100" height="1100" fill="#e7dfc9"/><rect x="30" y="30" width="1040" height="1040" rx="3" fill="none" stroke="{gold}" stroke-width="2"/>{text}<g opacity=".95">{scene}</g><text x="85" y="1030" font-family="serif" font-size="20" letter-spacing="2" fill="{green}">ORIGINAL ILLUSTRATION · NOT A PHOTOGRAPH</text></svg>'''
    relative = Path('slides/chengdu/images') / (identity + '-illustration.svg')
    target = root / relative
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(svg,encoding='utf-8')
    source = next((sources[s]['url'] for s in item.get('source_ids',[]) if s in sources),'https://www.panda.org.cn/en/')
    return {'id': identity+'-illustration', 'path': str(relative), 'kind':'diagram',
        'subject':item.get('name',{}), 'meaningful':True, 'width':1100, 'height':1100,
        'creator':'Original conceptual illustration by Hermes', 'license':'CC0-1.0',
        'license_url':'https://creativecommons.org/publicdomain/zero/1.0/',
        'source_url':source, 'source_role':'concept reference, not source photograph',
        'modifications':'Original SVG shapes; display may crop margins', 'illustrative':True,
        'disclosure':{'th':'ภาพวาดแนวคิดประกอบ ไม่ใช่ภาพถ่ายสถานที่หรืออาหารจริง',
                      'zh-Hans':'概念插画，非景点或菜品实拍。'}}
