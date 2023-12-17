from db_utils.db_func import *
from file_proccesing.file_transform import trans_file
import os

directory = 'vdb_langchain_doc_small'  # Замените это строкой со своим путем к директории

if os.path.isdir(directory):
    print('База уже есть')
    vectordb = get_db()
    print_db(vectordb)
else:
    print('База создается')
    vectordb = create_db()

#vectordb = get_db()
# print_db(vectordb)
#
#
#  # указываем путь к директории
# directory = "data"
# # получаем список файлов в директории
# file_list = os.listdir(directory)
#
#
# # # выводим имена всех файлов
# # for file_name in file_list:
# #     name = directory + '/' + file_name
# #     print(name)
# #     add_file_to_db(vectordb, name)
