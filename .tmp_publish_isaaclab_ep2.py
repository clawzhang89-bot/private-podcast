import datetime as dt
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
NS_ITUNES="http://www.itunes.com/dtds/podcast-1.0.dtd"
NS_CONTENT="http://purl.org/rss/1.0/modules/content/"
NS_ATOM="http://www.w3.org/2005/Atom"
ET.register_namespace("itunes", NS_ITUNES)
ET.register_namespace("content", NS_CONTENT)
ET.register_namespace("atom", NS_ATOM)
pages_base="https://clawzhang89-bot.github.io/private-podcast"
slug="2026-04-07-isaac-lab-articulation-joint-actuator-single-male"
title="Isaac Lab 基础概念专题：Articulation、Joint 与 Actuator"
summary="一段偏技术向、适合开发者收听的中文长音频，系统讲解 Isaac Lab 中 articulation、joint、actuator 的层次关系，以及它们如何进入控制与训练流程。"
root_dir=Path("/Users/admin/.openclaw/workspace/private-podcast")
mp3=root_dir/"episodes"/f"{slug}.mp3"
feed=root_dir/"feed.xml"
out=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(mp3)], text=True).strip()
seconds=int(round(float(out)))
duration=f"{seconds//60:02d}:{seconds%60:02d}" if seconds<3600 else f"{seconds//3600:02d}:{(seconds%3600)//60:02d}:{seconds%60:02d}"
pub_date=dt.datetime.now(dt.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
size=mp3.stat().st_size
tree=ET.parse(feed)
root=tree.getroot()
channel=root.find("channel")
for item in list(channel.findall("item")):
    guid=item.find("guid")
    if guid is not None and guid.text==slug:
        channel.remove(item)
item=ET.Element("item")
ET.SubElement(item,"title").text=title
ET.SubElement(item,"link").text=f"{pages_base}/episodes/{slug}.mp3"
ET.SubElement(item,"description").text=summary
ET.SubElement(item,f"{{{NS_CONTENT}}}encoded").text=summary
ET.SubElement(item,f"{{{NS_ITUNES}}}author").text="Evan"
ET.SubElement(item,f"{{{NS_ITUNES}}}summary").text=summary
ET.SubElement(item,f"{{{NS_ITUNES}}}duration").text=duration
ET.SubElement(item,f"{{{NS_ITUNES}}}episodeType").text="full"
ET.SubElement(item,f"{{{NS_ITUNES}}}explicit").text="false"
ET.SubElement(item,"pubDate").text=pub_date
ET.SubElement(item,"guid", {"isPermaLink":"false"}).text=slug
ET.SubElement(item,"enclosure", {"url":f"{pages_base}/episodes/{slug}.mp3","length":str(size),"type":"audio/mpeg"})
items=channel.findall("item")
insert_at=list(channel).index(items[0]) if items else len(list(channel))
channel.insert(insert_at,item)

def indent(elem, level=0):
    i="\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text=i+"  "
        for child in elem:
            indent(child, level+1)
        if not child.tail or not child.tail.strip():
            child.tail=i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail=i
indent(root)
tree.write(feed, encoding="utf-8", xml_declaration=True)
print(duration)
