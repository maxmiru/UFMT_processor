# UFMT CLASS GENERATORS

ufmt_list = {
    'Ufmt_Value':(('value_id',),
                  ('value_id', 'value_type', 'value_subtype', 'value', 'description'),
                  ('Int', 'Int', 'Int', 'Str', 'Str' )),
    'Ufmt_Conversion':(('conv_key',),
                       ('conv_key', 'conv_type', 'description'),
                       ('Int', 'Int', 'Str')),
    'Ufmt_Conv_Rule':(('conv_key', 'rule_num',),
                      ('conv_key', 'rule_num', 'src_value', 'dest_value', 'next_key', 'is_default' ),
                      ('Int', 'Int', 'Str', 'Str', 'Int', 'Int')),
    'Ufmt_Condition':(('cond_id',),
                      ('cond_id', 'operator', 'value1', 'conv1', 'value2', 'conv2', 'cond1', 'cond2', 'f_strcmp', 'description'),
                      ('Int', 'Str', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Str')),
    'Ufmt_Field_Format':(('field_id',),
                         ('field_id', 'length_type', 'length', 'data_type', 'field_type', 'psymbol', 'pside', 'description'),
                         ('Int', 'Int', 'Int', 'Int', 'Int', 'Str', 'Str', 'Str')),
    'Ufmt_Format':(('format_id',),
                   ('format_id', 'format_type', 'description', 'bitmap_type'),
                   ('Int', 'Int', 'Str', 'Int')),
    'Ufmt_Field':(('format_id', 'field_no'),
                  ('format_id', 'field_no', 'f_mac', 'f_key', 'f_mandatory', 'description'),
                  ('Int', 'Int', 'Int', 'Int', 'Int', 'Str')),
    'Ufmt_Build_Rule':(('format_id', 'field_no', 'priority'),
                       ('format_id', 'field_no', 'priority', 'field_id', 'cond_id', 'value_id', 'conv_key', 'f_check', 'f_write'),
                       ('Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int', 'Int')),
    'Ufmt_Format_Select':(('formatter', 'rule_num'),
                          ('formatter', 'rule_num', 'route_type', 'service_id_in', 'trans_type_in', 'msg_type_in', 'reversal_in', 'mti', 'format_id', 'trans_type_out', 'msg_type_out', 'reversal_out', 'fIntran_in', 'acq_inst_in' ,'iss_inst_in', 'service_type_in'),
                          ('Str'      , 'Int'     , 'Str'       , 'Str'          , 'Str'          , 'Str'        , 'Str'        , 'Str', 'Int'      , 'Str'           , 'Str'         , 'Str'         , 'Str'       , 'Str'         , 'Str'       , 'Str'            )),
    }

f=open('ufmt_object2.py', 'w')
if f is None :
    exit(1)
    
for ufmt_obj in ufmt_list:
    elms = ufmt_list[ufmt_obj][1]
    keys = ufmt_list[ufmt_obj][0]
    types = ufmt_list[ufmt_obj][2]
    key_props = ["self."+i for i in keys]
    print("""
class {}(object):
""".format(ufmt_obj), file = f)
    print("    def __init__( self, {}):".format(', '.join(elms)) , file = f)
    for i in range(len(elms)):
        print("        self.{0} = To_{1}({0})".format(elms[i], types[i]) , file = f)
    print("        self.key = ( {},)".format(', '.join(key_props)), file = f)
    print("", file = f)
    
    print("    def __init__( self, prop_list):", file = f)
    for i in range(len(elms)):
        print("        self.{0} = To_{1}(prop_list[{2}])".format(elms[i], types[i], i), file = f )
    print("        self.key = ( {},)".format(', '.join(key_props)), file = f)
    print("", file = f)
    
    print("    def __list__(self ):", file = f)
    print("        return [{}]".format(', '.join([("From_" + types[i] + "(self." + elms[i] + ")") for i in range(len(elms))])), file = f)
    print("", file = f)

    print("    def get_excel_values(self ):", file = f)
    print("        return [{}]".format(', '.join([("self." + elm) for elm in elms])), file = f)
    print("", file = f)
    
"""
    def get_excel_values ( self ):
        return [ self.value_id, self.value_type, self.value_subtype, self.value, self.description ]
"""
    
for ufmt_obj in ufmt_list:
    elms = ufmt_list[ufmt_obj][1]
    
    headers = ', '.join([ "'" + elm + "'" for elm in elms]).upper()
    print("""
class {0}_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ {1} ]
        
    def new_element( self, value_list ):
        return {0}( value_list )""".format(ufmt_obj, headers), file = f )
    
    cols = ', '.join(elms).upper()
    print('''
    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into {table} ( {columns} ) Values ( {{values}} );"
        return insert_sql_fmt'''.format( table = ufmt_obj.upper(), columns = cols ), file = f)
    
    print('''
    def get_table_name( self ):
        return "{}"'''.format( ufmt_obj.upper() ), file = f)
    print("", file = f)
    
f.close()
