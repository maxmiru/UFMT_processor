import ufmt_object

data_set = ufmt_object.Ufmt_Data_Set()
data_set.load_from_excel('UFMT_DATA', '.')
data_set.export_to_sql( '.' )
