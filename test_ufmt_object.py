# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 22:32:39 2017

@author: Minh Mai Xuan
"""
from ufmt_object import *

def test1():
    data_set = Ufmt_Data_Set()
    data_set.load_from_sql()
    data_set.export_to_sql()

def test2():
    file_name = 'UFMT_DATA'
    file_path = os.path.join( 'Data', 'Excel', file_name + '.xlsx' )
    wb = openpyxl.load_workbook ( file_path)
    value_set = Ufmt_Value_Set()
    value_set.load_from_excel( wb, 'UFMT_VALUE' )
    value_set.save_to_excel( wb, 'UFMT_VALUE')
    file_name = 'UFMT_DATA_1'
    file_path = os.path.join( 'Data', 'Excel', file_name + '.xlsx' )
    wb.save( file_path )

def test3():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel( 'UFMT_DATA' )
    data_set.save_to_excel( 'UFMT_DATA_1' )

def test4():
    data_set = Ufmt_Data_Set()
    data_set.load_from_sql()
    data_set.save_to_excel('UFMT_DATA_2')
    del data_set
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA_2')
    data_set.export_to_sql()

def test5():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    data_set.export_to_sql( )

def test6():
    data_set = Ufmt_Data_Set()
    data_set.load_from_sql('.')
    data_set.save_to_excel('UFMT_DATA', '.')

def test7():
    data_set = Ufmt_Data_Set()
    data_set.load_from_sql()
    data_set.build_rules.link( data_set.fields, data_set.field_formats, data_set.conditions, data_set.conversions, data_set.values )
    rule = data_set.build_rules.get( (4, 3, 3) )
    #rule.link( data_set.fields, data_set.field_formats, data_set.conditions, data_set.conversions, data_set.values )
    print(rule.value.__list__() )
    print(rule.field.__list__() )
    print(rule.field_format.__list__())
    print(rule.cond.__list__())
    print(rule.conv.__list__())

def test8():
    data_set = Ufmt_Data_Set()
    data_set.load_from_sql()
    data_set.link()
    cond = data_set.conditions.get( (10, ))
    print( cond.__list__())
    if cond.value1 is not None:
        print( cond.value1.__list__())  
    if cond.value2 is not None:
        print( cond.value2.__list__())  
    if cond.conv1 is not None:
        print( cond.conv1.__list__())  
    if cond.conv2 is not None:
        print( cond.conv2.__list__())  
    if cond.cond1 is not None:
        print( cond.cond1.__list__())
    if cond.cond2 is not None:
        print( cond.cond2.__list__())

def test9():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    rule = data_set.build_rules.get( (4, 3, 3) )
    rule.show_details()
    field = data_set.fields.get ( (4, 3 ))
    field.show_details()
    fmt = data_set.formats.get ( (4, ))
    fmt.show_details()
    conv = data_set.conversions.get( (20, ))
    conv.show_details()

def test10():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    rule = data_set.build_rules.get( (4, 3, 3) )
    rule.show_details()
    data_set.values.get((93,)).show_details()
    data_set.values.get((289,)).show_details()
    data_set.export_to_sql()

def test11():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    rule = data_set.conv_rules.get ((112, 1))
    #ari_rule = Arithmetic_Conv_Rule( rule.dest_value, data_set.values, data_set.conversions )
    print(rule)
    rule.show_details()

def test12():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    data_set.values.get((304,)).show_details()
    data_set.values.get((324,)).show_details()
    data_set.export_to_sql()

def test13():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    data_set.change_value_id ( 3, 363 )
    data_set.change_format_id ( 2, 10 )
    data_set.change_cond_id ( 20, 95 )
    data_set.change_field_format_id ( 24, 46 )
    data_set.change_conv_key ( 1, 165 )
    #print( data_set.conv_rules.get ( (165, 1) ))
    print ( data_set.build_rules.get( (10,1,1) ) )
    print ( data_set.fields.get( (10,1)))
    data_set.save_to_excel('UFMT_DATA_2')
    data_set.export_to_sql()
    
def test14():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA_2')
    data_set.link()
    data_set.change_value_id ( 363, 3 )
    data_set.change_format_id ( 10, 2 )
    data_set.change_cond_id ( 95, 20 )
    data_set.field_formats.change_key ( 46, 24 )
    data_set.change_conv_key ( 165, 1 )
    data_set.export_to_sql()

def test15():
    data_set = Ufmt_Data_Set()
    data_set.load_from_oracle_db()
    data_set.link()
    print(data_set.values.get((12,)))
    print(data_set.conv_rules.get((1,1)))
    data_set.save_to_excel('UFMT_DATA_2')

def test16():
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA_2')
    data_set.link()
    print( data_set.values.get( (10,)))
    
def test_17():
    '''
    Adding new values, conditions and field formats into existing UFMT data set
    '''
    data_set = Ufmt_Data_Set()
    data_set.load_from_excel('UFMT_DATA')
    data_set.link()
    
    elms = data_set.values
    new_value = [None, 1, 0, '99', 'TEST1']
    data_set.values.add( new_value )
    new_value = [100, 1, 0, '99', 'TEST2']
    data_set.values.add( new_value )
    new_value = [100, 1, 0, '99', 'TEST3']
    data_set.values.add( new_value )
    data_set.save_to_excel('UFMT_DATA_2')

    new_cond = ['', '=', '224', '', '361',  '', '', '', '1', 'TEST1']
    data_set.conditions.add( new_cond )
    new_cond = ['100', '=', '224', '', '361',  '', '', '', '1', 'TEST2']
    data_set.conditions.add( new_cond )
    new_cond = ['100', '=', '224', '', '361',  '', '', '', '1', 'TEST3']
    data_set.conditions.add( new_cond )
    
    elms = data_set.field_formats
    new_elm = ['', '0', '16', '0', '0', ' ', 'R', 'TEST1']
    elms.add(new_elm)
    new_elm = ['50', '0', '16', '0', '0', ' ', 'R', 'TEST2']
    elms.add(new_elm)
    new_elm = ['50', '0', '16', '0', '0', ' ', 'R', 'TEST3']
    elms.add(new_elm)
    
    data_set.save_to_excel('UFMT_DATA_2')
    
if __name__ == '__main__':
    test_17()
    