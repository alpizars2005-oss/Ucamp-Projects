"""Añade enlaces al índice sin reescribir entregas históricas."""
from pathlib import Path
import hashlib
import json
import platform
import zipfile

B = Path(__file__).resolve().parents[1]
R = B.parents[1]
MARKER = '## Semana 4 — Simulación de Sprint e Incremento'
updates = {
    R/'README.md': '\n\n'+MARKER+'\n\nMochi Monchi incorpora un incremento local de pedidos e inventario, con simulación Scrum, pruebas y ambas plantillas de entrega.\n\n[Proyecto y ejecución](Retos_M5/Semana4_SCRUM/) · [Observaciones](Retos_M5/Semana4_SCRUM/Observaciones_del_Sprint.md) · [Documentos finales](Retos_M5/Semana4_SCRUM/documentos/)\n',
    R/'Retos_M5/README.md': '\n\n'+MARKER+'\n\nLa Semana 4 continúa las diez historias del MVP de Semana 3. Incluye Planning, cinco Daily virtuales, Review, Retrospective, DoR/DoD, aprendizajes y un incremento ejecutable local. La simulación individual se distingue de las pruebas técnicas reales y de la validación comercial pendiente.\n\n[Guía y código](Semana4_SCRUM/) · [Observaciones](Semana4_SCRUM/Observaciones_del_Sprint.md) · [Plantillas Semanas 2 y 4](Semana4_SCRUM/documentos/) · [Capturas y resultados](Semana4_SCRUM/evidencias/)\n\nA diferencia de las semanas documentales anteriores, esta entrega incorpora código ejecutable: 44 pruebas de lógica/API y nueve comprobaciones visuales reproducibles. El registro de navegador identifica el modo de ejecución exacto; no acredita dispositivos físicos ni uso productivo.\n',
    R/'PLAN.md': '\n\n---\n\n'+MARKER+'\n\nFecha: 2026-09-30. Continuar Mochi Monchi y US-01–US-10 sin alterar ejercicios previos. Separar responsabilidades simuladas y evidencia técnica. Implementar un servidor local de biblioteca estándar, interfaz de navegador y SQLite; verificar transacciones, validación, persistencia, idempotencia y concurrencia. Completar la plantilla oficial de Semana 4, recuperar Semana 2 y consolidar PDF, código y capturas.\n\nValidación: suite de 44 casos, comprobación visual de nueve escenarios, compilación y revisión de documentos. Los timeboxes y jornadas son virtuales; todos los datos de negocio son sintéticos. No se incorpora nube, cobros o funcionalidades de Release 2.\n\nPublicación: cambios limitados a Semana4_SCRUM, este registro, índices y un workflow específico de comprobación/documentación. El workflow sólo publica resultados tras pasar pruebas; no utiliza force push ni cambia ejercicios históricos. Revertir los commits de esta entrega permite retirar el incremento sin tocar semanas anteriores.\n'
}
for path, addition in updates.items():
    if not path.exists():
        # Permite generar el paquete aislado, sin crear índices raíz falsos.
        continue
    original = path.read_text(encoding='utf-8')
    if MARKER not in original:
        path.write_text(original.rstrip()+addition,encoding='utf-8')

(B/'documentos/README.md').write_text('''# Documentos de entrega

- [Consolidado PDF: Semanas 2 y 4](UCAMP_SCRUM_Consolidado.pdf)
- Semana 2: [Word](UCAMP_SCRUM_Semana2_Mochi_Monchi.docx) · [PDF](UCAMP_SCRUM_Semana2_Mochi_Monchi.pdf)
- Semana 4: [Word](UCAMP_SCRUM_Semana4_Mochi_Monchi.docx) · [PDF](UCAMP_SCRUM_Semana4_Mochi_Monchi.pdf)

La Semana 2 recupera la plantilla completada previamente; la Semana 4 conserva los campos de la plantilla oficial y añade eventos, resultados y capturas. La versión pública usa Angel Alfredo y no distribuye archivos de fuentes. Los datos son sintéticos. Revisar las reflexiones personales antes de subir a Community.
''',encoding='utf-8')
manifest = {'python':platform.python_version(),'platform':platform.platform(),'files':{}}
for path in sorted(B.rglob('*')):
    if not path.is_file() or any(part in path.parts for part in ('__pycache__','data','documentos','evidencias')):continue
    manifest['files'][path.relative_to(B).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
(B/'evidencias/manifest_fuentes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
