import ufmt_object

oracle_db_string='SVFE_TEST_BSM/SVFE_TEST_BSM1@BSM_DEV_FE'

data_set = ufmt_object.Ufmt_Data_Set( oracle_db_string )
data_set.load_from_oracle_db()
data_set.save_to_excel('UFMT_DATA_2', '.')
