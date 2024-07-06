from pypdf import PaperSize, PdfReader, PdfWriter, Transformation


# The PaperSize Class — pypdf 4.3.0 documentation
# https://pypdf.readthedocs.io/en/latest/modules/PaperSize.html

def format_to_a5(pdf_file):
    writer1 = PdfWriter()
    destPage = writer1.add_blank_page(width=PaperSize.A5.height, height=PaperSize.A5.width)  # h595 w400
    reader = PdfReader(pdf_file)
    sourcePage = reader.pages[0]
    h = 0 if sourcePage.mediabox.height < 500 else -PaperSize.A5.width
    destPage.merge_transformed_page(sourcePage, Transformation().translate(0, h))
    return destPage
    # writer1.write("out.pdf")


def merge2(file, writer):
    destPage = writer.add_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)  # w595, h842

    for i in range(len(file)):
        sourcePage = format_to_a5(file[i])

        height = sourcePage.mediabox.height
        # print("高",height)

        sourcePage.scale_by(0.9)
        w = (PaperSize.A4.width - sourcePage.mediabox.width) / 2
        destPage.merge_transformed_page(sourcePage, Transformation().translate(w, 50 + i * height))


def main1(file_all):
    result_writer = PdfWriter()

    # 两两分组并调用 merge_page 函数
    for i in range(0, len(file_all), 2):
        file_pairs = file_all[i:i + 2]

        merge2(file_pairs, result_writer)
    # writer.write("out.pdf")
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
