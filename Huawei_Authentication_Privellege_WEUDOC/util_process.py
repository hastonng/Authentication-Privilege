import os
import sys
import time
import traceback

import openpyxl
import pandas as pd
import shutil

from tqdm import tqdm


def clear_download_folder():

    shutil.rmtree(path=get_working_path() + "\\download\\")
    os.mkdir(get_working_path() + "\\download\\")


# Get the working path of the Project
def get_working_path():
    """
    Get the working path of the directory
    :return application_path: String
    """
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    return application_path


def read_data(file_dir, sheetname):
    """
    Read all required data from Data Excel
    从数据Excel中读取所有必需的数据

    DOC.xlsx
    BaseData.xlsx

    :return doc_df: DataFrame
    """

    try:
        df = pd.read_excel(get_working_path() + file_dir, engine='openpyxl', sheet_name=sheetname)

        return df

    except Exception:

        print(traceback.format_exc())

        time.sleep(9999)

def write_data(resp, result_dir, filename):
    """
    Write FileObject into Excel.

    :param filename:
    :type filename:
    :param result_dir:
    :type result_dir:
    :param resp: requests.Response
    :return: null
    """
    # Write response bytes into Excel file '.xlsx'

    for i in tqdm(range(0,1)):
        time.sleep(0.1)
        with open(result_dir + filename + ".xlsx", 'wb') as f:
            f.write(resp.content)

            f.close()

    print("Successfully Downloaded: " + filename)
    print("\n")


def combineFiles(template_filename, result_dir, result_filename, input_path, sheet_name: list):
    """
    Function for combining Excel files into one Excel file, including all the wanted Excel sheet.
    将Excel文件合并为一个Excel文件，包括所有需要的 Excel表。

    :param template_filename:   The Template file to be combine 要合并的模板文件名   :String
    :param result_dir:      The result directory of path 路径的结果目录        :String
    :param result_filename: Filename for the combined file 合并文件的文件名     :String
    :param input_path:       Path that reads the input files 读取输入文件的路径  :String
    :param sheet_name:      List of sheets to be combine 待合并的图纸列表      :List

    :return: None
    """

    # Read template file
    template_workbook = openpyxl.load_workbook(get_working_path() + template_filename)

    xl_name_list = []

    # Open all files in the folder
    for filename in os.listdir(get_working_path() + input_path):
        with open(os.path.join(get_working_path() + input_path, filename), 'r') as f:  # open in readonly mode
            xl_name_list.append(f.name)

    # Append all df into one Excel
    for name in xl_name_list:

        for sheets in sheet_name:
            template_worksheet = template_workbook[sheets + "_Template"]
            df_list = pd.read_excel(name, sheet_name=sheets, engine='openpyxl').values.tolist()

            for rows in df_list:
                template_worksheet.append(rows)

    template_worksheet = template_workbook['应用系统权限(Privilege)_Template']
    template_worksheet.title = "应用系统权限(Privilege)"

    # Save the template into the directory
    template_workbook.save(get_working_path() + result_dir + result_filename)

def pd_merging(df_a, df_b, left_on, right_on):

    merged_pd = pd.merge(df_a, df_b, left_on=left_on, right_on=right_on, how='left')

    return merged_pd


def listpdf(list_a, col_name):

    return pd.DataFrame(list_a,columns=[col_name])