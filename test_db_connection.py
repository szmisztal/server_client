from data_utils import DataUtils


data = DataUtils()
data.test_db_connection_with_close_conn_after_every_query(10000)
data.test_db_connection_with_close_conn_after_all_query(10000)




