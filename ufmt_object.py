#!python3
'''
This module define classes that are used by ufmt_data_processor
'''

import os, openpyxl, logging, sys, re, csv

def Int( string ):
    if not string.isdecimal():
        return None
    return int(string)

class Ufmt_Value(object):

    def __init__( self, value_id, value_type, value_subtype, value, description):
        self.value_id = Int(value_id)
        self.value_type = Int(value_type)
        self.value_subtype = Int(value_subtype)
        self.value = str(value)
        self.description = str(description)
        self.key = ( self.value_id,)

    def __init__( self, prop_list):
        self.value_id = Int(prop_list[0])
        self.value_type = Int(prop_list[1])
        self.value_subtype = Int(prop_list[2])
        self.value = str(prop_list[3])
        self.description = str(prop_list[4])
        self.key = ( self.value_id,)

    def __list__(self ):
        return [self.value_id, self.value_type, self.value_subtype, self.value, self.description]


class Ufmt_Conversion(object):

    def __init__( self, conv_key, conv_type, description):
        self.conv_key = Int(conv_key)
        self.conv_type = Int(conv_type)
        self.description = str(description)
        self.key = ( self.conv_key,)

    def __init__( self, prop_list):
        self.conv_key = Int(prop_list[0])
        self.conv_type = Int(prop_list[1])
        self.description = str(prop_list[2])
        self.key = ( self.conv_key,)

    def __list__(self ):
        return [self.conv_key, self.conv_type, self.description]


class Ufmt_Conv_Rule(object):

    def __init__( self, conv_key, rule_num, src_value, dest_value, next_key, is_default):
        self.conv_key = Int(conv_key)
        self.rule_num = Int(rule_num)
        self.src_value = Int(src_value)
        self.dest_value = Int(dest_value)
        self.next_key = Int(next_key)
        self.is_default = Int(is_default)
        self.key = ( self.conv_key, self.rule_num,)

    def __init__( self, prop_list):
        self.conv_key = Int(prop_list[0])
        self.rule_num = Int(prop_list[1])
        self.src_value = Int(prop_list[2])
        self.dest_value = Int(prop_list[3])
        self.next_key = Int(prop_list[4])
        self.is_default = Int(prop_list[5])
        self.key = ( self.conv_key, self.rule_num,)

    def __list__(self ):
        return [self.conv_key, self.rule_num, self.src_value, self.dest_value, self.next_key, self.is_default]


class Ufmt_Condition(object):

    def __init__( self, cond_id, operator, value1, conv1, value2, conv2, cond1, cond2, f_strcmp, description):
        self.cond_id = Int(cond_id)
        self.operator = str(operator)
        self.value1 = Int(value1)
        self.conv1 = Int(conv1)
        self.value2 = Int(value2)
        self.conv2 = Int(conv2)
        self.cond1 = Int(cond1)
        self.cond2 = Int(cond2)
        self.f_strcmp = Int(f_strcmp)
        self.description = str(description)
        self.key = ( self.cond_id,)

    def __init__( self, prop_list):
        self.cond_id = Int(prop_list[0])
        self.operator = str(prop_list[1])
        self.value1 = Int(prop_list[2])
        self.conv1 = Int(prop_list[3])
        self.value2 = Int(prop_list[4])
        self.conv2 = Int(prop_list[5])
        self.cond1 = Int(prop_list[6])
        self.cond2 = Int(prop_list[7])
        self.f_strcmp = Int(prop_list[8])
        self.description = str(prop_list[9])
        self.key = ( self.cond_id,)

    def __list__(self ):
        return [self.cond_id, self.operator, self.value1, self.conv1, self.value2, self.conv2, self.cond1, self.cond2, self.f_strcmp, self.description]


class Ufmt_Field_Format(object):

    def __init__( self, field_id, length_type, length, data_type, field_type, psymbol, pside, description):
        self.field_id = Int(field_id)
        self.length_type = Int(length_type)
        self.length = Int(length)
        self.data_type = Int(data_type)
        self.field_type = Int(field_type)
        self.psymbol = str(psymbol)
        self.pside = str(pside)
        self.description = str(description)
        self.key = ( self.field_id,)

    def __init__( self, prop_list):
        self.field_id = Int(prop_list[0])
        self.length_type = Int(prop_list[1])
        self.length = Int(prop_list[2])
        self.data_type = Int(prop_list[3])
        self.field_type = Int(prop_list[4])
        self.psymbol = str(prop_list[5])
        self.pside = str(prop_list[6])
        self.description = str(prop_list[7])
        self.key = ( self.field_id,)

    def __list__(self ):
        return [self.field_id, self.length_type, self.length, self.data_type, self.field_type, self.psymbol, self.pside, self.description]


class Ufmt_Format(object):

    def __init__( self, format_id, format_type, description):
        self.format_id = Int(format_id)
        self.format_type = Int(format_type)
        self.description = str(description)
        self.key = ( self.format_id,)

    def __init__( self, prop_list):
        self.format_id = Int(prop_list[0])
        self.format_type = Int(prop_list[1])
        self.description = str(prop_list[2])
        self.key = ( self.format_id,)

    def __list__(self ):
        return [self.format_id, self.format_type, self.description]


class Ufmt_Field(object):

    def __init__( self, format_id, field_no, f_mac, f_key, f_mandatory, description):
        self.format_id = Int(format_id)
        self.field_no = Int(field_no)
        self.f_mac = Int(f_mac)
        self.f_key = Int(f_key)
        self.f_mandatory = Int(f_mandatory)
        self.description = str(description)
        self.key = ( self.format_id, self.field_no,)

    def __init__( self, prop_list):
        self.format_id = Int(prop_list[0])
        self.field_no = Int(prop_list[1])
        self.f_mac = Int(prop_list[2])
        self.f_key = Int(prop_list[3])
        self.f_mandatory = Int(prop_list[4])
        self.description = str(prop_list[5])
        self.key = ( self.format_id, self.field_no,)

    def __list__(self ):
        return [self.format_id, self.field_no, self.f_mac, self.f_key, self.f_mandatory, self.description]


class Ufmt_Build_Rule(object):

    def __init__( self, format_id, field_no, priority, field_id, cond_id, value_id, conv_key, f_check, f_write):
        self.format_id = Int(format_id)
        self.field_no = Int(field_no)
        self.priority = Int(priority)
        self.field_id = Int(field_id)
        self.cond_id = Int(cond_id)
        self.value_id = Int(value_id)
        self.conv_key = Int(conv_key)
        self.f_check = Int(f_check)
        self.f_write = Int(f_write)
        self.key = ( self.format_id, self.field_no, self.priority,)

    def __init__( self, prop_list):
        self.format_id = Int(prop_list[0])
        self.field_no = Int(prop_list[1])
        self.priority = Int(prop_list[2])
        self.field_id = Int(prop_list[3])
        self.cond_id = Int(prop_list[4])
        self.value_id = Int(prop_list[5])
        self.conv_key = Int(prop_list[6])
        self.f_check = Int(prop_list[7])
        self.f_write = Int(prop_list[8])
        self.key = ( self.format_id, self.field_no, self.priority,)

    def __list__(self ):
        return [self.format_id, self.field_no, self.priority, self.field_id, self.cond_id, self.value_id, self.conv_key, self.f_check, self.f_write]


class Ufmt_Format_Select(object):

    def __init__( self, formatter, rule_num, route_type, service_id_in, trans_type_in, msg_type_in, reversal_in, mti, format_id, trans_type_out, msg_type_out, reversal_out, fIntran_in, acq_inst_in, iss_inst_in, service_type_in):
        self.formatter = str(formatter)
        self.rule_num = Int(rule_num)
        self.route_type = str(route_type)
        self.service_id_in = str(service_id_in)
        self.trans_type_in = str(trans_type_in)
        self.msg_type_in = str(msg_type_in)
        self.reversal_in = str(reversal_in)
        self.mti = str(mti)
        self.format_id = Int(format_id)
        self.trans_type_out = str(trans_type_out)
        self.msg_type_out = str(msg_type_out)
        self.reversal_out = str(reversal_out)
        self.fIntran_in = str(fIntran_in)
        self.acq_inst_in = str(acq_inst_in)
        self.iss_inst_in = str(iss_inst_in)
        self.service_type_in = str(service_type_in)
        self.key = ( self.formatter, self.rule_num,)

    def __init__( self, prop_list):
        self.formatter = str(prop_list[0])
        self.rule_num = Int(prop_list[1])
        self.route_type = str(prop_list[2])
        self.service_id_in = str(prop_list[3])
        self.trans_type_in = str(prop_list[4])
        self.msg_type_in = str(prop_list[5])
        self.reversal_in = str(prop_list[6])
        self.mti = str(prop_list[7])
        self.format_id = Int(prop_list[8])
        self.trans_type_out = str(prop_list[9])
        self.msg_type_out = str(prop_list[10])
        self.reversal_out = str(prop_list[11])
        self.fIntran_in = str(prop_list[12])
        self.acq_inst_in = str(prop_list[13])
        self.iss_inst_in = str(prop_list[14])
        self.service_type_in = str(prop_list[15])
        self.key = ( self.formatter, self.rule_num,)

    def __list__(self ):
        return [self.formatter, self.rule_num, self.route_type, self.service_id_in, self.trans_type_in, self.msg_type_in, self.reversal_in, self.mti, self.format_id, self.trans_type_out, self.msg_type_out, self.reversal_out, self.fIntran_in, self.acq_inst_in, self.iss_inst_in, self.service_type_in]

class Ufmt_Set (object):
    def __init__ ( self ):
        self.set = {}
        
    def new_element( self, value_list ):
        return None

    def load_from_sql ( self, file_name ):
        file_path = os.path.join( 'Data', 'SQL', file_name + '.sql' )
        file = open( file_path, 'r')
        po = re.compile( r'Insert\s+into\s+(\w+)\s*\((.*)\)\s*values\s*\((.*)\);', re.I)
        data_dict = {}
        data_table = []
        value_strings = []
        for line in file:
            mo = po.match( line )
            if mo != None and mo.group(3) != None:
                value_strings.append( mo.group(3).strip() )
        file.close()

        #print(value_strings)
        #return list(csv.reader( value_strings, 'singlequote_dialect' ))
        csv.register_dialect('singlequote_dialect', quotechar ="'")
        for rec in csv.reader( value_strings, 'singlequote_dialect' ):
            elm = self.new_element(rec)
            self.set[elm.key] = elm

    def export_to_sql ( self, file_name ):
        file_header_str = """\
Drop table {table}_BK;
Create table {table}_BK as Select * from {table};
Delete from {table};
""".format( table = self.get_table_name() )
        file_trailer_str = "\nCOMMIT;\n"
        insert_sql_fmt = self.get_insert_sql_fmt() + '\n'

        file_path = os.path.join( 'Data', 'SQL', file_name + '.sql' )
        file = open( file_path , 'w')
        file.write( file_header_str )
        for key in self.set:
            val_str = ','.join ( ["'%s'" % i for i in self.set[key].__list__() ] )
            sql_str = insert_sql_fmt.format( values = val_str )
            file.write( sql_str )

        file.write( file_trailer_str)
        file.close()        

class Ufmt_Value_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Value( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_VALUE ( VALUE_ID, VALUE_TYPE, VALUE_SUBTYPE, VALUE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_VALUE"


class Ufmt_Conversion_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Conversion( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_CONVERSION ( CONV_KEY, CONV_TYPE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_CONVERSION"


class Ufmt_Conv_Rule_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Conv_Rule( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_CONV_RULE ( CONV_KEY, RULE_NUM, SRC_VALUE, DEST_VALUE, NEXT_KEY, IS_DEFAULT ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_CONV_RULE"


class Ufmt_Condition_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Condition( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_CONDITION ( COND_ID, OPERATOR, VALUE1, CONV1, VALUE2, CONV2, COND1, COND2, F_STRCMP, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_CONDITION"


class Ufmt_Field_Format_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Field_Format( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FIELD_FORMAT ( FIELD_ID, LENGTH_TYPE, LENGTH, DATA_TYPE, FIELD_TYPE, PSYMBOL, PSIDE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FIELD_FORMAT"


class Ufmt_Format_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Format( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FORMAT"


class Ufmt_Field_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Field( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FIELD ( FORMAT_ID, FIELD_NO, F_MAC, F_KEY, F_MANDATORY, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FIELD"


class Ufmt_Build_Rule_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Build_Rule( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_BUILD_RULE ( FORMAT_ID, FIELD_NO, PRIORITY, FIELD_ID, COND_ID, VALUE_ID, CONV_KEY, F_CHECK, F_WRITE ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_BUILD_RULE"


class Ufmt_Format_Select_Set (Ufmt_Set):
    def new_element( self, value_list ):
        return Ufmt_Format_Select( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FORMAT_SELECT ( FORMATTER, RULE_NUM, ROUTE_TYPE, SERVICE_ID_IN, TRANS_TYPE_IN, MSG_TYPE_IN, REVERSAL_IN, MTI, FORMAT_ID, TRANS_TYPE_OUT, MSG_TYPE_OUT, REVERSAL_OUT, FINTRAN_IN, ACQ_INST_IN, ISS_INST_IN, SERVICE_TYPE_IN ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FORMAT_SELECT"

tables = ('UFMT_VALUE', 'UFMT_CONVERSION', 'UFMT_CONV_RULE', 'UFMT_CONDITION', 'UFMT_FIELD_FORMAT', 'UFMT_FORMAT', 'UFMT_FIELD', 'UFMT_BUILD_RULE', 'UFMT_FORMAT_SELECT' )

class Ufmt_Data_Set (object):
    def __init__ ( self ):
        self.values = Ufmt_Value_Set()
        self.conversions = Ufmt_Conversion_Set()
        self.conv_rules = Ufmt_Conv_Rule_Set()
        self.conditions = Ufmt_Condition_Set()
        self.field_formats = Ufmt_Field_Format_Set()
        self.formats = Ufmt_Format_Set()
        self.fields = Ufmt_Field_Set()
        self.build_rules = Ufmt_Build_Rule_Set()
        self.format_selects = Ufmt_Format_Select_Set()

    def load_from_sql( self ):
        self.values.load_from_sql('UFMT_VALUE')
        self.conversions.load_from_sql('UFMT_CONVERSION')
        self.conv_rules.load_from_sql('UFMT_CONV_RULE')
        self.conditions.load_from_sql('UFMT_CONDITION')
        self.field_formats.load_from_sql('UFMT_FIELD_FORMAT')
        self.formats.load_from_sql('UFMT_FORMAT')
        self.fields.load_from_sql('UFMT_FIELD')
        self.build_rules.load_from_sql('UFMT_BUILD_RULE')
        self.format_selects.load_from_sql('UFMT_FORMAT_SELECT')

    def export_to_sql( self ):
        self.values.export_to_sql('UFMT_VALUE_1')
        self.conversions.export_to_sql('UFMT_CONVERSION_1')
        self.conv_rules.export_to_sql('UFMT_CONV_RULE_1')
        self.conditions.export_to_sql('UFMT_CONDITION_1')
        self.field_formats.export_to_sql('UFMT_FIELD_FORMAT_1')
        self.formats.export_to_sql('UFMT_FORMAT_1')
        self.fields.export_to_sql('UFMT_FIELD_1')
        self.build_rules.export_to_sql('UFMT_BUILD_RULE_1')
        self.format_selects.export_to_sql('UFMT_FORMAT_SELECT_1')
        
def test():
    data_set = Ufmt_Data_Set()
    data_set.load_from_sql()
    data_set.export_to_sql()
    
if __name__ == '__main__':
    test()
    
