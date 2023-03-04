import sys
import traceback
import warnings

from datetime import datetime
from network_process import w3_login, iAuth
from util_process import read_data, combineFiles, clear_download_folder, pd_merging, listpdf


# Hide all warning in the tool
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings('ignore')

def main():
    try:
        global iauth

        clear_download_folder()

        # Read all DOC employee from DOC.xlsx excel
        doc_df = read_data(file_dir="\\data\\DOC.xlsx", sheetname="DOC List")

        # Read base data from BaseData.xlsx excel
        pmos_df = read_data(file_dir="\\data\\BaseData.xlsx", sheetname="PMOS")
        scf_df = read_data(file_dir="\\data\\BaseData.xlsx", sheetname="SCF")
        epf_df = read_data(file_dir="\\data\\BaseData.xlsx", sheetname="EPF")
        approval_list_df = read_data(file_dir="\\data\\BaseData.xlsx", sheetname="审批清单")

        # doc_df_list = doc_df['Staff ID'].values.tolist()
        # doc_id_temp = []
        #
        # for staffid in doc_df_list:
        #     doc_id_temp.append(str(staffid).upper())
        #
        # doc_id_df = listpdf(doc_id_temp, col_name="Staff ID")
        #
        # df_= doc_df['申请人'] +" "+ doc_id_df['Staff ID']
        #
        # name_df = pd.DataFrame(df_,columns=['申请人'])

        # Login to W3 Domain
        session = w3_login('p_weusrerob', 'rob2@SRE')

        # Get all Teams
        team_list = list(set(doc_df['Team'].values.tolist()))

        for team in team_list:


            if team != 'nan':

                print('\n')
                print("Processing Team: " + str(team))
                print("处理 " + str(team) + " 团队中...")
                print('\n')

                staff_id_list = doc_df[doc_df['Team'] == team]['Staff ID'].values.tolist()

                for staff_id in staff_id_list:

                    iauth = iAuth(session=session)

                    iauth.get_user(str(staff_id))

                    iauth.export_privilege()

                response = iauth.search_files()

                delete_list = iauth.download_file(resp_dict=response)

                iauth.delete_file(delete_list=delete_list)

            else:
                print('\n')
                print("啊！！！！！！！！！！！  是老大！！！！！！！！！！！！！")
                print("老大权限将跳过。。。")
                print('\n')


        combineFiles(template_filename="\\template\\iauth_template.xlsx",
                     result_dir="\\result\\",
                     result_filename="应用系统权限(Privilege)_" + datetime.strftime(datetime.now(), "%d%m%Y") + ".xlsx",
                     input_path="\\download\\",
                     sheet_name=["应用系统权限(Privilege)"])

        # all_iAuth_df = read_data("\\result\\应用系统权限(Privilege)_" + datetime.strftime(datetime.now(), "%d%m%Y") + ".xlsx",
        #           sheetname='应用系统权限(Privilege)')
        #
        # approval_list_df = approval_list_df.drop_duplicates(subset=['申请人','申请人所属团队', '申请人所属岗位'])

        # result_df = pd_merging(df_a=name_df, df_b=approval_list_df, left_on="申请人", right_on='申请人')

        # result_df.drop(['申请单号/ApplyNo', '申请类型/ApplyType', '权限名称/PrivilegeName', '权限层级', '授权ID/PrivilegeId',
        #                 '岗位名称/PostionName', '岗位所属部门/PositionDepartment', '1审批人/Approver', '1审层级',
        #                 '1类型/Type', '1操作结果/OperationResult', '2审批人/Approver', '2审层级', '2类型/Type', '2操作结果/OperationResult',
        #                 '3审批人/Approver', '3审层级', '3类型/Type', '3操作结果/OperationResult', '4审批人/Approver',
        #                 '4审层级', '4类型/Type', '4操作结果/OperationResult', 'Remark', '最终评审层级', '对应关系是否异常 （Y,N）',
        #                 '异常原因', 'Remark'], axis=1, inplace=True)

        # result_df.to_excel("test.xlsx", index_label=False, index=False)



    except Exception:

        print("Unfortunately, This site can’t be reached...")
        # Write into log file
        with open('error_log.txt', 'w') as f:
            f.write(traceback.format_exc())

if __name__ == '__main__':
    pass
