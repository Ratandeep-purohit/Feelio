import zipfile
import xml.etree.ElementTree as ET
import sys

def extract_text(doc_path):
    try:
        with zipfile.ZipFile(doc_path) as docx:
            xml_content = docx.read('word/document.xml')
        tree = ET.XML(xml_content)
        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        texts = []
        for paragraph in tree.findall('.//w:p', namespace):
            texts.append(''.join(node.text for node in paragraph.findall('.//w:t', namespace) if node.text))
        return '\n'.join(texts)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    doc_path = sys.argv[1]
    print(extract_text(doc_path))
