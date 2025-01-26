from pypdf import PaperSize, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

# The PaperSize Class — pypdf 4.3.0 documentation
# https://pypdf.readthedocs.io/en/latest/modules/PaperSize.html

def format_to_a5(pdf_file):
    writer1 = PdfWriter()
    destPage = writer1.add_blank_page(width=PaperSize.A5.height, height=PaperSize.A5.width)  # h595 w420
    # print(f"a5尺寸: 【高：{PaperSize.A5.height}】\t宽：{PaperSize.A5.width}")
    reader = PdfReader(pdf_file)
    sourcePage = reader.pages[0]
    # print(f"原始页面尺寸: 【高：{sourcePage.mediabox.height}】\t宽：{sourcePage.mediabox.width}  ")
    if 420 < sourcePage.mediabox.height < 550:
        # scale_rate = sourcePage.mediabox.height / PaperSize.A5.height
        scale_rate = 420 / sourcePage.mediabox.height
        # print(f"缩放比例:{scale_rate}")
        sourcePage.scale_by(scale_rate )
    h = 0 if sourcePage.mediabox.height < 550 else -PaperSize.A5.width
    w = (PaperSize.A5.height - sourcePage.mediabox.width) / 2
    # destPage.merge_transformed_page(sourcePage, Transformation().translate(0, h))
    destPage.merge_translated_page(sourcePage, w, h)
    return destPage
    # writer1.write("out.pdf")


def merge2(file, writer):
    destPage = writer.add_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)  # w595, h842

    for i in range(len(file)):
        sourcePage = format_to_a5(file[i])
        # print(f"[merge2]原始页面尺寸: 【高：{sourcePage.mediabox.height}】\t宽：{sourcePage.mediabox.width}  ")

        height = sourcePage.mediabox.height
        # print("高",height)

        sourcePage.scale_by(0.9)
        w = (PaperSize.A4.width - sourcePage.mediabox.width) / 2
        # destPage.merge_transformed_page(sourcePage, Transformation().translate(w, 50 + i * height))
        destPage.merge_translated_page(sourcePage, w+10, (1 - i) * height)


# 创建一个新的 PDF 页面，并在中间画一条横线
def create_line_page():
    A4_WIDTH, A4_HEIGHT = PaperSize.A4.width, PaperSize.A4.height
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(A4_WIDTH, A4_HEIGHT))

    # 计算中间位置的 Y 坐标
    middle_y = A4_HEIGHT / 2

    # 画一条横线
    can.setStrokeColorRGB(0.5, 0.5, 0.5)  # 设置线条颜色为黑色
    can.setLineWidth(0.3)  # 设置线条宽度
    can.line(0, middle_y, A4_WIDTH, middle_y)  # 从 (50, middle_y) 到 (A4_WIDTH - 50, middle_y)

    can.save()  # 保存绘制的内容

    # 将内容写入 BytesIO 对象
    packet.seek(0)
    return packet

def main1(file_all):
    result_writer = PdfWriter()

    # 两两分组并调用 merge_page 函数
    for i in range(0, len(file_all), 2):
        file_pairs = file_all[i:i + 2]

        merge2(file_pairs, result_writer)
    # writer.write("out.pdf")

    # 打开现有的 PDF 文件
    # reader = PdfReader("input.pdf")
    writer = PdfWriter()

    # 遍历每一页
    for page in result_writer.pages:
        # 创建一个包含横线的新页面
        line_page_packet = create_line_page()
        line_page = PdfReader(line_page_packet).pages[0]

        # 将横线页面合并到原始页面
        page.merge_page(line_page)

        # 将修改后的页面添加到 PdfWriter
        writer.add_page(page)
    return result_writer


def get_user_confirmation(prompt, default="yes"):
    while True:
        response = input(prompt).lower().strip()
        if response == "" and default is not None:
            return default == "yes"
        elif response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("请输入 'yes' 或 'no'（直接回车默认为 'yes'）")


def get_valid_path():
    while True:
        path_input = input("请输入文件夹路径：")
        path = Path(path_input)
        if not path.exists():
            print("输入的路径不存在，请重新输入。")
        elif not path.is_dir():
            print("输入的路径不是一个文件夹，请重新输入。")
        else:
            return path


if __name__ == '__main__':
    from pathlib import Path

    exec_path = get_valid_path()
    file_all = [file for file in exec_path.iterdir() if file.suffix.lower() == '.pdf']

    if not file_all:
        print("在指定文件夹中没有找到PDF文件。")
        exit()

    merged_pdf = main1(file_all)
    output_file = exec_path / "合并.pdf"

    if output_file.exists():
        if get_user_confirmation(f"文件 '{output_file}' 已存在。是否替换？ (Y/n) "):
            print(f"正在替换文件 '{output_file}'")
            merged_pdf.write(str(output_file))
        else:
            print("操作已取消")
    else:
        print(f"正在创建文件 '{output_file}'")
        merged_pdf.write(str(output_file))
