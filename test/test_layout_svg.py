import os
import shutil
from name_data import NameData
from pdf import name_tag_4760100, name_tag_4786103
from pdf.name_tag_4786103 import create
from pdf.layouts import Layout
from pdf.name_tag_layouts import getNameTagLayouts
from pdf.name_tag_type import NameTagType
import svgutils.transform as sg
from pathlib import Path
import subprocess


output_dir:str = "./name_tags/svg"


def test_create_all_name_tag_svgs():
    cleanup_folders()
    create_all_name_tag_pdfs()
    convert_all_pdfs_to_svg()
    merge_all_svgs()
    clear_base_files()


def cleanup_folders():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

def clear_base_files():
    name_tags_dir = Path(output_dir)
    pdf_files = list(name_tags_dir.rglob("base_*.*"))
    for file in pdf_files:
        os.remove(file)

def create_all_name_tag_pdfs():
    name_data = NameData(
        qr_code="kongresartikler.dk",
        image_name="",
        line_1="",
        line_2="",
        line_3="",
        line_4="",
        line_5=""
    )

    for kolonne in range(1, 6):
        setattr(name_data, f"line_{kolonne}", f"Kolonne {kolonne}")

        for nameTagType in NameTagType:

            layouts = getNameTagLayouts(nameTagType)
            for layout in layouts.layouts:
                if layout == Layout.LAYOUT_INVALID:
                    continue
                type_name: str = nameTagType.name.replace("_", "")
                file_dir = f"{output_dir}/{type_name}/{layout}"
                os.makedirs(file_dir, exist_ok=True)

                image = select_image_for_layout(layout)

                name_data.image_name = image
        
                fileName:str = f"{file_dir}/base_{layout}_{kolonne}L.pdf"

                if nameTagType == NameTagType._4786103:
                    name_tag_4786103.create(
                        fileName=fileName,
                        layout=layout,
                        nameData=name_data,
                        single_page=True
                    )
                else:
                    name_tag_4760100.create(
                        fileName=fileName,
                        layout=layout,
                        nameData=name_data,
                    )


def convert_all_pdfs_to_svg():
    name_tags_dir = Path(output_dir)
    pdf_files = list(name_tags_dir.rglob("*.pdf"))

    for pdf_file in pdf_files:
        svg_file = pdf_file.with_suffix(".svg")
        pdf_to_svg(pdf_file, svg_file)


def merge_all_svgs():
    name_tags_dir = Path(output_dir)
    svg_files = list(name_tags_dir.rglob("base_*.svg"))

    for base_svg_file in svg_files:
        output_filename = base_svg_file.name.replace("base_", "")
        output_path = base_svg_file.parent / output_filename
        merge_svg(base_svg_file, output_path)


def merge_svg(base_svg_file, output_file):

    if "4760100" in str(base_svg_file):
        baggrund = "scripts/images/4760100_baggrund.svg"
        ramme = "scripts/images/4760100_ramme.svg"
        width = "283.46457"
        height = "170.07874"

    elif "4786103" in str(base_svg_file):
        baggrund = "scripts/images/4786103_baggrund.svg"
        ramme = "scripts/images/4786103_ramme.svg"
        width = "291.96851"
        height = "243.77953"
    else:
        print(f"Unknown file pattern in {base_svg_file}, skipping.")
        return

    bg_root = sg.fromfile(baggrund).getroot()
    main_root = sg.fromfile(base_svg_file).getroot()
    frame_root = sg.fromfile(ramme).getroot()

    fig = sg.SVGFigure()
    fig.append([bg_root, main_root, frame_root])
    fig.save(output_file)

    set_document_size(output_file, width, height)

    print(f"Modified and saved: {output_file}")


def pdf_to_svg(pdf_path, svg_path):
    """Convert a PDF file to SVG using pdf2svg."""
    try:
        subprocess.run(
            ["pdf2svg", str(pdf_path), str(svg_path)],
            check=True
        )
        print(f"Converted {pdf_path} -> {svg_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {pdf_path}: {e}")
        return False


def select_image_for_layout(layout: Layout) -> str:
    if layout in (Layout.LAYOUT_2PB,
                  Layout.LAYOUT_2PT,
                  Layout.LAYOUT_2PTLQ,
                  Layout.LAYOUT_2PTRQ,
                  Layout.LAYOUT_2PBLQ,
                  Layout.LAYOUT_2PBRQ,
                  Layout.LAYOUT_3PTLQ,
                  Layout.LAYOUT_3PTRQ,
                  Layout.LAYOUT_3PBLQ,
                  Layout.LAYOUT_3PBRQ,
                  Layout.LAYOUT_3PB,
                  Layout.LAYOUT_3PT):
        return '../test/images/big.jpg'
    else:
        return '../test/images/small.jpg'



def set_document_size(svg_file, width, height):
    import xml.etree.ElementTree as ET
    tree = ET.parse(svg_file)
    root = tree.getroot()
    root.set("width", width)
    root.set("height", height)
    if "viewBox" in root.attrib:
        del root.attrib["viewBox"]
    tree.write(svg_file, encoding="utf-8", xml_declaration=True)


