from xml.dom.minidom import parse
import xml.dom.minidom

src_path = 'public/sitemap.xml'
dest_path = 'public/sitemap_baidu.txt'

sitemap_baidu = open(dest_path, mode='w', encoding='utf-8')

dom_tree = xml.dom.minidom.parse(src_path)
element = dom_tree.documentElement
for url in element.getElementsByTagName('url'):
    loc = url.childNodes[1]
    loc_data = loc.childNodes[0].data.replace(' ', '').replace('\n', '').replace('\t', '')
    sitemap_baidu.write(loc_data[loc_data.find('https'):] + '\n')

sitemap_baidu.close()
