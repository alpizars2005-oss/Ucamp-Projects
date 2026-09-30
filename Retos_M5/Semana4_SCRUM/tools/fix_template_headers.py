"""Corrige el recorte de los subtítulos en las plantillas oficiales exportadas.

Los cuadros de texto traían 7.2 pt de margen superior e inferior dentro
de una altura de 15.7 pt. Se conservan texto, posición, logos y colores.
Arial evita depender de la fuente incrustada en el documento original.
"""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from lxml import etree

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
}


def repair(path: Path) -> None:
    """Normaliza sólo la tipografía y los márgenes de texto del encabezado."""
    with ZipFile(path) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    changed = False
    for name, data in members.items():
        if not (name.startswith('word/header') and name.endswith('.xml')):
            continue
        root = etree.fromstring(data)
        for shape in root.findall('.//wps:wsp', NS):
            if not shape.findall('.//w:t', NS):
                continue
            for fonts in shape.findall('.//w:rFonts', NS):
                for attribute in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                    key = '{' + NS['w'] + '}' + attribute
                    if fonts.get(key) != 'Arial':
                        fonts.set(key, 'Arial')
                        changed = True
            body = shape.find('wps:bodyPr', NS)
            if body is not None:
                for attribute in ('tIns', 'bIns'):
                    if body.get(attribute) != '0':
                        body.set(attribute, '0')
                        changed = True
        members[name] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    if changed:
        temporary = path.with_suffix('.tmp')
        with ZipFile(temporary, 'w', compression=ZIP_DEFLATED) as archive:
            for name, data in members.items():
                archive.writestr(name, data)
        temporary.replace(path)
    print(f'{path.name}: encabezado sin márgenes verticales internos')


if __name__ == '__main__':
    templates = Path(__file__).resolve().parent / 'templates'
    for filename in ('Semana2_completada.docx', 'Semana4_base.docx'):
        repair(templates / filename)
