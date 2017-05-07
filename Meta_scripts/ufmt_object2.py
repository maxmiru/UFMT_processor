
class Ufmt_Value(object):

    def __init__( self, value_id, value_type, value_subtype, value, description):
        self.value_id = To_Int(value_id)
        self.value_type = To_Int(value_type)
        self.value_subtype = To_Int(value_subtype)
        self.value = To_Str(value)
        self.description = To_Str(description)
        self.key = ( self.value_id,)

    def __init__( self, prop_list):
        self.value_id = To_Int(prop_list[0])
        self.value_type = To_Int(prop_list[1])
        self.value_subtype = To_Int(prop_list[2])
        self.value = To_Str(prop_list[3])
        self.description = To_Str(prop_list[4])
        self.key = ( self.value_id,)

    def __list__(self ):
        return [From_Int(self.value_id), From_Int(self.value_type), From_Int(self.value_subtype), From_Str(self.value), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.value_id, self.value_type, self.value_subtype, self.value, self.description]


class Ufmt_Conversion(object):

    def __init__( self, conv_key, conv_type, description):
        self.conv_key = To_Int(conv_key)
        self.conv_type = To_Int(conv_type)
        self.description = To_Str(description)
        self.key = ( self.conv_key,)

    def __init__( self, prop_list):
        self.conv_key = To_Int(prop_list[0])
        self.conv_type = To_Int(prop_list[1])
        self.description = To_Str(prop_list[2])
        self.key = ( self.conv_key,)

    def __list__(self ):
        return [From_Int(self.conv_key), From_Int(self.conv_type), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.conv_key, self.conv_type, self.description]


class Ufmt_Conv_Rule(object):

    def __init__( self, conv_key, rule_num, src_value, dest_value, next_key, is_default):
        self.conv_key = To_Int(conv_key)
        self.rule_num = To_Int(rule_num)
        self.src_value = To_Str(src_value)
        self.dest_value = To_Str(dest_value)
        self.next_key = To_Int(next_key)
        self.is_default = To_Int(is_default)
        self.key = ( self.conv_key, self.rule_num,)

    def __init__( self, prop_list):
        self.conv_key = To_Int(prop_list[0])
        self.rule_num = To_Int(prop_list[1])
        self.src_value = To_Str(prop_list[2])
        self.dest_value = To_Str(prop_list[3])
        self.next_key = To_Int(prop_list[4])
        self.is_default = To_Int(prop_list[5])
        self.key = ( self.conv_key, self.rule_num,)

    def __list__(self ):
        return [From_Int(self.conv_key), From_Int(self.rule_num), From_Str(self.src_value), From_Str(self.dest_value), From_Int(self.next_key), From_Int(self.is_default)]

    def get_excel_values(self ):
        return [self.conv_key, self.rule_num, self.src_value, self.dest_value, self.next_key, self.is_default]


class Ufmt_Condition(object):

    def __init__( self, cond_id, operator, value1, conv1, value2, conv2, cond1, cond2, f_strcmp, description):
        self.cond_id = To_Int(cond_id)
        self.operator = To_Str(operator)
        self.value1 = To_Int(value1)
        self.conv1 = To_Int(conv1)
        self.value2 = To_Int(value2)
        self.conv2 = To_Int(conv2)
        self.cond1 = To_Int(cond1)
        self.cond2 = To_Int(cond2)
        self.f_strcmp = To_Int(f_strcmp)
        self.description = To_Str(description)
        self.key = ( self.cond_id,)

    def __init__( self, prop_list):
        self.cond_id = To_Int(prop_list[0])
        self.operator = To_Str(prop_list[1])
        self.value1 = To_Int(prop_list[2])
        self.conv1 = To_Int(prop_list[3])
        self.value2 = To_Int(prop_list[4])
        self.conv2 = To_Int(prop_list[5])
        self.cond1 = To_Int(prop_list[6])
        self.cond2 = To_Int(prop_list[7])
        self.f_strcmp = To_Int(prop_list[8])
        self.description = To_Str(prop_list[9])
        self.key = ( self.cond_id,)

    def __list__(self ):
        return [From_Int(self.cond_id), From_Str(self.operator), From_Int(self.value1), From_Int(self.conv1), From_Int(self.value2), From_Int(self.conv2), From_Int(self.cond1), From_Int(self.cond2), From_Int(self.f_strcmp), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.cond_id, self.operator, self.value1, self.conv1, self.value2, self.conv2, self.cond1, self.cond2, self.f_strcmp, self.description]


class Ufmt_Field_Format(object):

    def __init__( self, field_id, length_type, length, data_type, field_type, psymbol, pside, description):
        self.field_id = To_Int(field_id)
        self.length_type = To_Int(length_type)
        self.length = To_Int(length)
        self.data_type = To_Int(data_type)
        self.field_type = To_Int(field_type)
        self.psymbol = To_Str(psymbol)
        self.pside = To_Str(pside)
        self.description = To_Str(description)
        self.key = ( self.field_id,)

    def __init__( self, prop_list):
        self.field_id = To_Int(prop_list[0])
        self.length_type = To_Int(prop_list[1])
        self.length = To_Int(prop_list[2])
        self.data_type = To_Int(prop_list[3])
        self.field_type = To_Int(prop_list[4])
        self.psymbol = To_Str(prop_list[5])
        self.pside = To_Str(prop_list[6])
        self.description = To_Str(prop_list[7])
        self.key = ( self.field_id,)

    def __list__(self ):
        return [From_Int(self.field_id), From_Int(self.length_type), From_Int(self.length), From_Int(self.data_type), From_Int(self.field_type), From_Str(self.psymbol), From_Str(self.pside), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.field_id, self.length_type, self.length, self.data_type, self.field_type, self.psymbol, self.pside, self.description]


class Ufmt_Format(object):

    def __init__( self, format_id, format_type, description, bitmap_type):
        self.format_id = To_Int(format_id)
        self.format_type = To_Int(format_type)
        self.description = To_Str(description)
        self.bitmap_type = To_Int(bitmap_type)
        self.key = ( self.format_id,)

    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.format_type = To_Int(prop_list[1])
        self.description = To_Str(prop_list[2])
        self.bitmap_type = To_Int(prop_list[3])
        self.key = ( self.format_id,)

    def __list__(self ):
        return [From_Int(self.format_id), From_Int(self.format_type), From_Str(self.description), From_Int(self.bitmap_type)]

    def get_excel_values(self ):
        return [self.format_id, self.format_type, self.description, self.bitmap_type]


class Ufmt_Field(object):

    def __init__( self, format_id, field_no, f_mac, f_key, f_mandatory, description):
        self.format_id = To_Int(format_id)
        self.field_no = To_Int(field_no)
        self.f_mac = To_Int(f_mac)
        self.f_key = To_Int(f_key)
        self.f_mandatory = To_Int(f_mandatory)
        self.description = To_Str(description)
        self.key = ( self.format_id, self.field_no,)

    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.field_no = To_Int(prop_list[1])
        self.f_mac = To_Int(prop_list[2])
        self.f_key = To_Int(prop_list[3])
        self.f_mandatory = To_Int(prop_list[4])
        self.description = To_Str(prop_list[5])
        self.key = ( self.format_id, self.field_no,)

    def __list__(self ):
        return [From_Int(self.format_id), From_Int(self.field_no), From_Int(self.f_mac), From_Int(self.f_key), From_Int(self.f_mandatory), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.format_id, self.field_no, self.f_mac, self.f_key, self.f_mandatory, self.description]


class Ufmt_Build_Rule(object):

    def __init__( self, format_id, field_no, priority, field_id, cond_id, value_id, conv_key, f_check, f_write):
        self.format_id = To_Int(format_id)
        self.field_no = To_Int(field_no)
        self.priority = To_Int(priority)
        self.field_id = To_Int(field_id)
        self.cond_id = To_Int(cond_id)
        self.value_id = To_Int(value_id)
        self.conv_key = To_Int(conv_key)
        self.f_check = To_Int(f_check)
        self.f_write = To_Int(f_write)
        self.key = ( self.format_id, self.field_no, self.priority,)

    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.field_no = To_Int(prop_list[1])
        self.priority = To_Int(prop_list[2])
        self.field_id = To_Int(prop_list[3])
        self.cond_id = To_Int(prop_list[4])
        self.value_id = To_Int(prop_list[5])
        self.conv_key = To_Int(prop_list[6])
        self.f_check = To_Int(prop_list[7])
        self.f_write = To_Int(prop_list[8])
        self.key = ( self.format_id, self.field_no, self.priority,)

    def __list__(self ):
        return [From_Int(self.format_id), From_Int(self.field_no), From_Int(self.priority), From_Int(self.field_id), From_Int(self.cond_id), From_Int(self.value_id), From_Int(self.conv_key), From_Int(self.f_check), From_Int(self.f_write)]

    def get_excel_values(self ):
        return [self.format_id, self.field_no, self.priority, self.field_id, self.cond_id, self.value_id, self.conv_key, self.f_check, self.f_write]


class Ufmt_Format_Select(object):

    def __init__( self, formatter, rule_num, route_type, service_id_in, trans_type_in, msg_type_in, reversal_in, mti, format_id, trans_type_out, msg_type_out, reversal_out, fIntran_in, acq_inst_in, iss_inst_in, service_type_in):
        self.formatter = To_Str(formatter)
        self.rule_num = To_Int(rule_num)
        self.route_type = To_Str(route_type)
        self.service_id_in = To_Str(service_id_in)
        self.trans_type_in = To_Str(trans_type_in)
        self.msg_type_in = To_Str(msg_type_in)
        self.reversal_in = To_Str(reversal_in)
        self.mti = To_Str(mti)
        self.format_id = To_Int(format_id)
        self.trans_type_out = To_Str(trans_type_out)
        self.msg_type_out = To_Str(msg_type_out)
        self.reversal_out = To_Str(reversal_out)
        self.fIntran_in = To_Str(fIntran_in)
        self.acq_inst_in = To_Str(acq_inst_in)
        self.iss_inst_in = To_Str(iss_inst_in)
        self.service_type_in = To_Str(service_type_in)
        self.key = ( self.formatter, self.rule_num,)

    def __init__( self, prop_list):
        self.formatter = To_Str(prop_list[0])
        self.rule_num = To_Int(prop_list[1])
        self.route_type = To_Str(prop_list[2])
        self.service_id_in = To_Str(prop_list[3])
        self.trans_type_in = To_Str(prop_list[4])
        self.msg_type_in = To_Str(prop_list[5])
        self.reversal_in = To_Str(prop_list[6])
        self.mti = To_Str(prop_list[7])
        self.format_id = To_Int(prop_list[8])
        self.trans_type_out = To_Str(prop_list[9])
        self.msg_type_out = To_Str(prop_list[10])
        self.reversal_out = To_Str(prop_list[11])
        self.fIntran_in = To_Str(prop_list[12])
        self.acq_inst_in = To_Str(prop_list[13])
        self.iss_inst_in = To_Str(prop_list[14])
        self.service_type_in = To_Str(prop_list[15])
        self.key = ( self.formatter, self.rule_num,)

    def __list__(self ):
        return [From_Str(self.formatter), From_Int(self.rule_num), From_Str(self.route_type), From_Str(self.service_id_in), From_Str(self.trans_type_in), From_Str(self.msg_type_in), From_Str(self.reversal_in), From_Str(self.mti), From_Int(self.format_id), From_Str(self.trans_type_out), From_Str(self.msg_type_out), From_Str(self.reversal_out), From_Str(self.fIntran_in), From_Str(self.acq_inst_in), From_Str(self.iss_inst_in), From_Str(self.service_type_in)]

    def get_excel_values(self ):
        return [self.formatter, self.rule_num, self.route_type, self.service_id_in, self.trans_type_in, self.msg_type_in, self.reversal_in, self.mti, self.format_id, self.trans_type_out, self.msg_type_out, self.reversal_out, self.fIntran_in, self.acq_inst_in, self.iss_inst_in, self.service_type_in]


class Ufmt_Value_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'VALUE_ID', 'VALUE_TYPE', 'VALUE_SUBTYPE', 'VALUE', 'DESCRIPTION' ]
        
    def new_element( self, value_list ):
        return Ufmt_Value( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_VALUE ( VALUE_ID, VALUE_TYPE, VALUE_SUBTYPE, VALUE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_VALUE"


class Ufmt_Conversion_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'CONV_KEY', 'CONV_TYPE', 'DESCRIPTION' ]
        
    def new_element( self, value_list ):
        return Ufmt_Conversion( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_CONVERSION ( CONV_KEY, CONV_TYPE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_CONVERSION"


class Ufmt_Conv_Rule_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'CONV_KEY', 'RULE_NUM', 'SRC_VALUE', 'DEST_VALUE', 'NEXT_KEY', 'IS_DEFAULT' ]
        
    def new_element( self, value_list ):
        return Ufmt_Conv_Rule( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_CONV_RULE ( CONV_KEY, RULE_NUM, SRC_VALUE, DEST_VALUE, NEXT_KEY, IS_DEFAULT ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_CONV_RULE"


class Ufmt_Condition_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'COND_ID', 'OPERATOR', 'VALUE1', 'CONV1', 'VALUE2', 'CONV2', 'COND1', 'COND2', 'F_STRCMP', 'DESCRIPTION' ]
        
    def new_element( self, value_list ):
        return Ufmt_Condition( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_CONDITION ( COND_ID, OPERATOR, VALUE1, CONV1, VALUE2, CONV2, COND1, COND2, F_STRCMP, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_CONDITION"


class Ufmt_Field_Format_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'FIELD_ID', 'LENGTH_TYPE', 'LENGTH', 'DATA_TYPE', 'FIELD_TYPE', 'PSYMBOL', 'PSIDE', 'DESCRIPTION' ]
        
    def new_element( self, value_list ):
        return Ufmt_Field_Format( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FIELD_FORMAT ( FIELD_ID, LENGTH_TYPE, LENGTH, DATA_TYPE, FIELD_TYPE, PSYMBOL, PSIDE, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FIELD_FORMAT"


class Ufmt_Format_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'FORMAT_ID', 'FORMAT_TYPE', 'DESCRIPTION', 'BITMAP_TYPE' ]
        
    def new_element( self, value_list ):
        return Ufmt_Format( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FORMAT ( FORMAT_ID, FORMAT_TYPE, DESCRIPTION, BITMAP_TYPE ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FORMAT"


class Ufmt_Field_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'FORMAT_ID', 'FIELD_NO', 'F_MAC', 'F_KEY', 'F_MANDATORY', 'DESCRIPTION' ]
        
    def new_element( self, value_list ):
        return Ufmt_Field( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FIELD ( FORMAT_ID, FIELD_NO, F_MAC, F_KEY, F_MANDATORY, DESCRIPTION ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FIELD"


class Ufmt_Build_Rule_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'FORMAT_ID', 'FIELD_NO', 'PRIORITY', 'FIELD_ID', 'COND_ID', 'VALUE_ID', 'CONV_KEY', 'F_CHECK', 'F_WRITE' ]
        
    def new_element( self, value_list ):
        return Ufmt_Build_Rule( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_BUILD_RULE ( FORMAT_ID, FIELD_NO, PRIORITY, FIELD_ID, COND_ID, VALUE_ID, CONV_KEY, F_CHECK, F_WRITE ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_BUILD_RULE"


class Ufmt_Format_Select_Set (Ufmt_Set):
    def __init__ ( self ):
        super().__init__()
        self.headers = [ 'FORMATTER', 'RULE_NUM', 'ROUTE_TYPE', 'SERVICE_ID_IN', 'TRANS_TYPE_IN', 'MSG_TYPE_IN', 'REVERSAL_IN', 'MTI', 'FORMAT_ID', 'TRANS_TYPE_OUT', 'MSG_TYPE_OUT', 'REVERSAL_OUT', 'FINTRAN_IN', 'ACQ_INST_IN', 'ISS_INST_IN', 'SERVICE_TYPE_IN' ]
        
    def new_element( self, value_list ):
        return Ufmt_Format_Select( value_list )

    def get_insert_sql_fmt( self ):
        insert_sql_fmt = "Insert into UFMT_FORMAT_SELECT ( FORMATTER, RULE_NUM, ROUTE_TYPE, SERVICE_ID_IN, TRANS_TYPE_IN, MSG_TYPE_IN, REVERSAL_IN, MTI, FORMAT_ID, TRANS_TYPE_OUT, MSG_TYPE_OUT, REVERSAL_OUT, FINTRAN_IN, ACQ_INST_IN, ISS_INST_IN, SERVICE_TYPE_IN ) Values ( {values} );"
        return insert_sql_fmt

    def get_table_name( self ):
        return "UFMT_FORMAT_SELECT"

