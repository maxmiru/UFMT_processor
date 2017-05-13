import ufmt_object

data_set = ufmt_object.Ufmt_Data_Set()
data_set.load_from_sql('.')
data_set.save_to_excel('UFMT_DATA', '.')
