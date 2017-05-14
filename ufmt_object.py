#!python3
'''
This module define classes that are used by ufmt_data_processor
'''

import os, openpyxl, logging, sys, re, csv
from enum import IntEnum 

#enum constants - start
class Value_Type(IntEnum):
    CONST = 0
    UMF = 1
    PMT = 2
    COMPLEX = 3
    FMT = 4
    LOCAL = 5
    ITERATOR = 6
    MONEYFLD = 7
class Value_Subtype(IntEnum):
    STR = 0
    INT = 1
    UINT = 2
    FLOAT = 3
    FLOAT_IP = 4
    LONG_LONG = 5
    BINARY = 6
class Conv_Type(IntEnum):
    REPLACE = 0
    DATEFMT = 1
    TEMPLATE = 2
    EXPFMT = 3
    ARITHMETIC = 4
    FUNCTION = 5
class Field_Length_Type(IntEnum):
    NO = 0
    LLA = 1
    LLLA = 2
    LLB = 3
    LLLB = 4
    LLLLA = 5
    LLLLB = 6
    LLH = 7
    LLLH = 8
    LH = 9
class Field_Data_Type(IntEnum):
    ASCII = 0
    BYTE = 1
    BCD = 2
    EBCDIC = 3
class Format_Type(IntEnum):
    ISO8583_87= 0
    TLV= 1
    COMPLEX= 2
    ISO8583_03= 3
class Bitmap_Type(IntEnum):
    HEX = 0
    ASCII = 1
#enum constants - end
    
#Convert functions - start
def To_Int( ext_string ):
    if not ext_string.isdecimal():
        return None
    return int(ext_string)

def To_Str( ext_string ):
    if ext_string == '':
        return None
    return ext_string

def From_Str( string ):
    if string is None:
        return ''
    return string

def From_Int ( integer ):
    if integer is None:
        return ''
    return str( integer )
#Convert functions - end

class Ufmt_Value(object):

    def __init__( self, value_id, value_type, value_subtype, value, description):
        self.value_id = To_Int(value_id)
        self.value_type = Value_Type(To_Int(value_type))
        self.value_subtype = Value_Subtype(To_Int(value_subtype))
        self.value = To_Str(value)
        self.description = To_Str(description)
        self.key = ( self.value_id,)

    def __init__( self, prop_list):
        self.value_id = To_Int(prop_list[0])
        self.value_type = Value_Type(To_Int(prop_list[1]))
        self.value_subtype = Value_Subtype(To_Int(prop_list[2]))
        self.value = To_Str(prop_list[3])
        self.description = To_Str(prop_list[4])
        self.key = ( self.value_id,)

    def __list__(self ):
        return [From_Int(self.value_id), From_Int(self.value_type.value), From_Int(self.value_subtype.value), From_Str(self.value), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.value_id, self.value_type.value, self.value_subtype.value, self.value, self.description]

    def __str__( self ):
        s = 'Value #{}: type {}, subtype {}, desc "{}", value "{}"'
        s = s.format( self.value_id, self.value_type.name, self.value_subtype.name, self.description, self.value )
        return s
    
class Ufmt_Conversion(object):

    def __init__( self, conv_key, conv_type, description):
        self.conv_key = To_Int(conv_key)
        self.conv_type = Conv_Type(To_Int(conv_type))
        self.description = To_Str(description)
        self.key = ( self.conv_key,)

        self.conv_rules = dict()
        
    def __init__( self, prop_list):
        self.conv_key = To_Int(prop_list[0])
        self.conv_type = Conv_Type(To_Int(prop_list[1]))
        self.description = To_Str(prop_list[2])
        self.key = ( self.conv_key,)

        self.conv_rules = dict()
        
    def __list__(self ):
        return [From_Int(self.conv_key), From_Int(self.conv_type.value), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.conv_key, self.conv_type.value, self.description]

    def __str__( self ):
        s = 'Conversion #{}: type {}, desc "{}"'
        s = s.format( self.conv_key, self.conv_type.name, self.description )
        return s

    def add_to_conv_rules ( self, conv_rule ):
        if conv_rule.conv_key == self.conv_key:
            self.conv_rules[ conv_rule.rule_num ] = conv_rule

    def show_details ( self ):
        print ( self )
        for conv_rule in self.conv_rules.values():
            print ( '\t%s' % str ( conv_rule ))
            
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

    def link ( self, convs ):
        self.conv = convs.get( ( self.conv_key, ) )
        if self.next_key is not None:
            self.next_conv = convs.get( ( self.next_key,) )
        
    def __str__( self ):
        s = 'Conversion #{}, rule#{}: src "{}", dest "{}"'
        s = s.format( self.conv_key, self.rule_num, self.src_value, self.dest_value)
        if self.is_default == 1:
            s = s + ', default'
        if self.next_key is not None:
            s = s + ', next key #{}'.format( self.next_key )
        return s
    
class Ufmt_Condition(object):

    def __init__( self, cond_id, operator, value1, conv1, value2, conv2, cond1, cond2, f_strcmp, description):
        self.cond_id = To_Int(cond_id)
        self.operator = To_Str(operator)
        self.value_id1 = To_Int(value1)
        self.conv_key1 = To_Int(conv1)
        self.value_id2 = To_Int(value2)
        self.conv_key2 = To_Int(conv2)
        self.cond_id1 = To_Int(cond1)
        self.cond_id2 = To_Int(cond2)
        self.f_strcmp = To_Int(f_strcmp)
        self.description = To_Str(description)
        self.key = ( self.cond_id,)

    def __init__( self, prop_list):
        self.cond_id = To_Int(prop_list[0])
        self.operator = To_Str(prop_list[1])
        self.value_id1 = To_Int(prop_list[2])
        self.conv_key1 = To_Int(prop_list[3])
        self.value_id2 = To_Int(prop_list[4])
        self.conv_key2 = To_Int(prop_list[5])
        self.cond_id1 = To_Int(prop_list[6])
        self.cond_id2 = To_Int(prop_list[7])
        self.f_strcmp = To_Int(prop_list[8])
        self.description = To_Str(prop_list[9])
        self.key = ( self.cond_id,)

    def __list__(self ):
        return [From_Int(self.cond_id), From_Str(self.operator), From_Int(self.value_id1), From_Int(self.conv_key1), From_Int(self.value_id2), From_Int(self.conv_key2), From_Int(self.cond_id1), From_Int(self.cond_id2), From_Int(self.f_strcmp), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.cond_id, self.operator, self.value_id1, self.conv_key1, self.value_id2, self.conv_key2, self.cond_id1, self.cond_id2, self.f_strcmp, self.description]

    def link ( self, values, convs, conds ):
        self.value1 = values.get( ( self.value_id1, ) )
        self.value2 = values.get( ( self.value_id2, ) )
        self.conv1 = convs.get( ( self.conv_key1, ) )
        self.conv2 = convs.get( ( self.conv_key2, ) )
        self.cond1 = conds.get( ( self.cond_id1, ) )
        self.cond2 = conds.get( ( self.cond_id2, ) )

    def __str__( self ):
        if self.operator in ('&', '|', '!'):
            operand1 = 'cond {}'.format( self.cond_id1 )
            operand2 = 'cond {}'.format( self.cond_id2 )
        else:
            operand1 = 'value {}'.format( self.value_id1 )
            if self.conv_key1 is not None:
                operand1 = operand1 + ' : conv {}'.format( self.conv_key1 )
            operand2 = 'value {}'.format( self.value_id2 )
            if self.conv_key2 is not None:
                operand2 = operand2 + ' : conv {}'.format( self.conv_key2 )
                
        s = 'Condition #{}:'.format( self.cond_id )
        if self.operator == '!':
            s += ' {} {}'.format( self.operator, operand1 )
        else:
            s += ' {} {} {}'.format ( operand1, self.operator, operand2 )

        s += ', desc "{}"'.format( self.description )
        return s
            
class Ufmt_Field_Format(object):

    def __init__( self, field_id, length_type, length, data_type, field_type, psymbol, pside, description):
        self.field_id = To_Int(field_id)
        self.length_type = Field_Length_Type(To_Int(length_type))
        self.length = To_Int(length)
        self.data_type = Field_Data_Type (To_Int(data_type))
        self.field_type = Field_Length_Type(To_Int(field_type))
        self.psymbol = To_Str(psymbol)
        self.pside = To_Str(pside)
        self.description = To_Str(description)
        self.key = ( self.field_id,)

    def __init__( self, prop_list):
        self.field_id = To_Int(prop_list[0])
        self.length_type = Field_Length_Type ( To_Int(prop_list[1]) )
        self.length = To_Int(prop_list[2])
        self.data_type = Field_Data_Type ( To_Int(prop_list[3]) )
        self.field_type = Field_Length_Type ( To_Int(prop_list[4]) )
        self.psymbol = To_Str(prop_list[5])
        self.pside = To_Str(prop_list[6])
        self.description = To_Str(prop_list[7])
        self.key = ( self.field_id,)

    def __list__(self ):
        return [From_Int(self.field_id), From_Int(self.length_type.value), From_Int(self.length), From_Int(self.data_type.value), From_Int(self.field_type.value), From_Str(self.psymbol), From_Str(self.pside), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.field_id, self.length_type.value, self.length, self.data_type.value, self.field_type.value, self.psymbol, self.pside, self.description]

    def __str__ ( self ):
        if self.psymbol is None:
            pchar = ' '
        else:
            pchar = self.psymbol

        if self.pside == 'L':
            pad = 'Left padded with "{}"'.format(pchar)          
        elif self.pside == 'R':
            pad = 'Right padded with "{}"'.format(pchar)
        else:
            pad = 'No padding'
        
        s = 'Field format #{}: length type {}, length {}, data type {}, field type {}, {}, desc "{}"'
        s = s.format( self.field_id, self.length_type.name, self.length, self.data_type.name, self.field_type.name, pad, self.description )
        return s
    
class Ufmt_Format(object):

    def __init__( self, format_id, format_type, description, bitmap_type):
        self.format_id = To_Int(format_id)
        self.format_type = Format_Type ( To_Int(format_type) )
        self.description = To_Str(description)
        self.bitmap_type = Bitmap_Type ( To_Int(bitmap_type) )
        self.key = ( self.format_id,)

        self.fields = dict()

    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.format_type = Format_Type ( To_Int(prop_list[1]) )
        self.description = To_Str(prop_list[2])
        self.bitmap_type = Bitmap_Type ( To_Int(prop_list[3]) )
        self.key = ( self.format_id,)

        self.fields = dict()
        
    def __list__(self ):
        return [From_Int(self.format_id), From_Int(self.format_type.value), From_Str(self.description), From_Int(self.bitmap_type.value)]

    def get_excel_values(self ):
        return [self.format_id, self.format_type.value, self.description, self.bitmap_type.value]

    def __str__( self ):
        s = 'Format #{}: type {}, bitmap type {}, desc "{}"'
        s = s.format( self.format_id, self.format_type.name, self.bitmap_type.name, self.description )
        return s

    def add_to_fields ( self, field ):
        if field.format_id == self.format_id:
            self.fields[ field.field_no ] = field

    def show_details ( self ):
        print ( self )
        for field in self.fields.values():
            print ( '\t%s' % str ( field ) )
            for rule in field.build_rules.values():
                s = '\t\t%s' % str ( rule )
                s += '\n\t\t\t%s' % str ( rule.field_format )
                if rule.cond is not None:
                    s += '\n\t\t\t%s' % str ( rule.cond )
                s += '\n\t\t\t%s' % str ( rule.value )
                if rule.conv is not None:
                    s += '\n\t\t\t%s' % str ( rule.conv )
                print ( s )
                
class Ufmt_Field(object):

    def __init__( self, format_id, field_no, f_mac, f_key, f_mandatory, description):
        self.format_id = To_Int(format_id)
        self.field_no = To_Int(field_no)
        self.f_mac = To_Int(f_mac)
        self.f_key = To_Int(f_key)
        self.f_mandatory = To_Int(f_mandatory)
        self.description = To_Str(description)
        self.key = ( self.format_id, self.field_no,)

        self.build_rules = dict()
        
    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.field_no = To_Int(prop_list[1])
        self.f_mac = To_Int(prop_list[2])
        self.f_key = To_Int(prop_list[3])
        self.f_mandatory = To_Int(prop_list[4])
        self.description = To_Str(prop_list[5])
        self.key = ( self.format_id, self.field_no,)

        self.build_rules = dict()
        
    def __list__(self ):
        return [From_Int(self.format_id), From_Int(self.field_no), From_Int(self.f_mac), From_Int(self.f_key), From_Int(self.f_mandatory), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.format_id, self.field_no, self.f_mac, self.f_key, self.f_mandatory, self.description]

    def link ( self, formats ):
        self.format = formats.get( ( self.format_id, ) )

    def __str__ ( self ):
        if self.f_mac == 1:
            mac = "MAC"
        else:
            mac = "No MAC"
        if self.f_key == 1:
            key = "Key"
        else:
            key = "No key"
        if self.f_mandatory == 1:
            mand = "Mandatory"
        else:
            mand = "Optional"
        s = 'Format #{}, field #{}: {}, {}, {}, desc "{}"'
        s = s.format( self.format_id, self.field_no, mac, key, mand, self.description )
        return s

    def add_to_build_rules ( self, build_rule ):
        if ( build_rule.format_id, build_rule.field_no ) == self.key:
            self.build_rules[ build_rule.priority ] = build_rule

    def show_details ( self ):
        print ( self )
        print ( self.format )
        for rule in self.build_rules.values():
            s = '\t%s' % str ( rule )
            s += '\n\t\t%s' % str ( rule.field_format )
            if rule.cond is not None:
                s += '\n\t\t%s' % str ( rule.cond )
            s += '\n\t\t%s' % str ( rule.value )
            if rule.conv is not None:
                s += '\n\t\t%s' % str ( rule.conv )
            print ( s )
            
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

    def link( self, fields, field_formats, conds, convs, values ):
        self.field = fields.get( ( self.format_id, self.field_no, ) )
        self.field_format = field_formats.get ( ( self.field_id, ) )
        self.cond = conds.get( (self.cond_id, ) )
        self.conv = convs.get( (self.conv_key, ) )
        self.value = values.get( (self.value_id, ) )
        
    def __str__ ( self ):
        s = 'Format #{}, field #{}, rule #{}: field format {}, cond {}, value {}, conv {}, check {}, write {}'
        s = s.format( self.format_id, self.field_no, self.priority, self.field_id, self.cond_id, self.value_id, self.conv_key, self.f_check, self.f_write )
        return s

    def show_details ( self ):
        print ( self )
        print ( self.field.format )
        print ( self.field )
        print ( self.field_format )
        if self.cond is not None:
            print ( self.cond )
        print ( self.value )
        if self.conv is not None:
            print ( self.conv )
        
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
        self.fintran_in = To_Str(fIntran_in)
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
        self.fintran_in = To_Str(prop_list[12])
        self.acq_inst_in = To_Str(prop_list[13])
        self.iss_inst_in = To_Str(prop_list[14])
        self.service_type_in = To_Str(prop_list[15])
        self.key = ( self.formatter, self.rule_num,)

    def __list__(self ):
        return [From_Str(self.formatter), From_Int(self.rule_num), From_Str(self.route_type), From_Str(self.service_id_in), From_Str(self.trans_type_in), From_Str(self.msg_type_in), From_Str(self.reversal_in), From_Str(self.mti), From_Int(self.format_id), From_Str(self.trans_type_out), From_Str(self.msg_type_out), From_Str(self.reversal_out), From_Str(self.fintran_in), From_Str(self.acq_inst_in), From_Str(self.iss_inst_in), From_Str(self.service_type_in)]

    def get_excel_values(self ):
        return [self.formatter, self.rule_num, self.route_type, self.service_id_in, self.trans_type_in, self.msg_type_in, self.reversal_in, self.mti, self.format_id, self.trans_type_out, self.msg_type_out, self.reversal_out, self.fintran_in, self.acq_inst_in, self.iss_inst_in, self.service_type_in]

    def link ( self, formats ):
        self.format = formats.get( ( self.format_id, ) )

    def __str__ ( self ):
        s1 = '(type {}, MTI {}, service id {}, service type {}, trans type {}, msg type {}, reversal {}, fintran {}, acq inst {}, iss inst {})'
        s1 = s1.format( self.route_type, self.mti, self.service_id_in, self.service_type_in,
                        self.trans_type_in, self.msg_type_in, self.reversal_in, self.fintran_in, self.acq_inst_in, self.iss_inst_in )
        s2 = '(format {}, trans type {}, msg type {}, reversal {})'
        s2 = s2.format( self.format_id, self.trans_type_out, self.msg_type_out, self.reversal_out )
        s = 'Formatter "{}", rule #{}: {} => {}'
        s = s.format ( self.formatter, self.rule_num, s1, s2 )
        return s
    
class Ufmt_Set (object):
    def __init__ ( self ):
        self.set = {}
        self.headers = []

    def get_headers ( self ):
        return self.headers
      
    def new_element( self, value_list ):
        return None

    def load_from_sql ( self, file_name, dir_path = None ):
        if dir_path is None:
            file_path = os.path.join( 'Data', 'SQL', file_name + '.sql' )
        else:
            file_path = os.path.join( dir_path, file_name + '.sql' )
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

    def export_to_sql ( self, file_name, dir_path = None ):
        file_header_str = """\
Drop table {table}_BK;
Create table {table}_BK as Select * from {table};
Delete from {table};

""".format( table = self.get_table_name() )
        file_trailer_str = "\nCOMMIT;\n"
        insert_sql_fmt = self.get_insert_sql_fmt() + '\n'

        if dir_path is None:
            file_path = os.path.join( 'Data', 'SQL', file_name + '.sql' )
        else:
            file_path = os.path.join( dir_path, file_name + '.sql' )
        file = open( file_path , 'w')
        file.write( file_header_str )
        for key in self.set:
            val_str = ','.join ( ["'%s'" % i for i in self.set[key].__list__() ] )
            sql_str = insert_sql_fmt.format( values = val_str )
            file.write( sql_str )

        file.write( file_trailer_str)
        file.close()        

    def load_from_excel ( self, wb, sheet_name ):
        sheet = wb.get_sheet_by_name ( sheet_name)
        
        data_table = []
        max_col = len ( self.get_headers() )
        for row in sheet.iter_rows( min_row = 4, max_row = sheet.max_row ):        
            data_record = [''] * max_col
            empty_row = True
            for i in range( max_col ):
                if row[i].value == None:
                    data_record[i] = ''
                else:
                    data_record[i] = str(row[i].value)
                    empty_row = False
            if empty_row:
                break
            
            logging.debug ( data_record )
            elm = self.new_element(data_record)
            self.set[elm.key] = elm

    def save_to_excel ( self, wb, sheet_name ):
        sheet = wb.get_sheet_by_name ( sheet_name)
        max_col = len(self.get_headers())

        #clear existing data
        for row in sheet.iter_rows( min_row = 4, max_row = sheet.max_row ):
            for i in range(max_col):
                row[i].value = None

        #write data rows
        row_num=4
        for key in self.set:
            col_num = 1
            for value in self.set[key].get_excel_values():
                sheet.cell(row = row_num, column = col_num).value = value
                col_num=col_num+1
            row_num=row_num+1

    def get( self, key ):
        return self.set.get(key)

    def __str__ ( self ):
        s = ''
        for elm in self.set.values():
            s += str(elm) + '\n'
        return s
    
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

    def link ( self, convs ):
        for elm in self.set.values():
            elm.link ( convs )

            conv = convs.get ( ( elm.conv_key, ) )
            conv.add_to_conv_rules ( elm )
            
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

    def link ( self, values, convs, conds ):
        for elm in self.set.values():
            elm.link( values, convs, conds )
            
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

    def link ( self, formats ):
        for elm in self.set.values():
            elm.link( formats )

            _format = formats.get( (elm.format_id, ) )
            _format.add_to_fields ( elm )
            
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

    def link( self, fields, field_formats, conds, convs, values ):
        for elm in self.set.values():
            elm.link( fields, field_formats, conds, convs, values )
            
            field = fields.get( ( elm.format_id, elm.field_no ) )
            field.add_to_build_rules ( elm )
            
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

    def link ( self, formats ):
        for elm in self.set.values():
            elm.link( formats )
        

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

    def load_from_sql( self, dir_path = None ):
        self.values.load_from_sql('UFMT_VALUE', dir_path )
        self.conversions.load_from_sql('UFMT_CONVERSION', dir_path )
        self.conv_rules.load_from_sql('UFMT_CONV_RULE', dir_path )
        self.conditions.load_from_sql('UFMT_CONDITION', dir_path )
        self.field_formats.load_from_sql('UFMT_FIELD_FORMAT', dir_path )
        self.formats.load_from_sql('UFMT_FORMAT', dir_path )
        self.fields.load_from_sql('UFMT_FIELD', dir_path )
        self.build_rules.load_from_sql('UFMT_BUILD_RULE', dir_path )
        self.format_selects.load_from_sql('UFMT_FORMAT_SELECT', dir_path )

    def export_to_sql( self, dir_path = None ):
        self.values.export_to_sql('UFMT_VALUE', dir_path )
        self.conversions.export_to_sql('UFMT_CONVERSION', dir_path )
        self.conv_rules.export_to_sql('UFMT_CONV_RULE', dir_path )
        self.conditions.export_to_sql('UFMT_CONDITION', dir_path )
        self.field_formats.export_to_sql('UFMT_FIELD_FORMAT', dir_path )
        self.formats.export_to_sql('UFMT_FORMAT', dir_path )
        self.fields.export_to_sql('UFMT_FIELD', dir_path )
        self.build_rules.export_to_sql('UFMT_BUILD_RULE', dir_path )
        self.format_selects.export_to_sql('UFMT_FORMAT_SELECT', dir_path )

    def load_from_excel( self, file_name, dir_path = None ):
        if dir_path is None:
            file_path = os.path.join( 'Data', 'Excel', file_name + '.xlsx' )
        else:
            file_path = os.path.join( dir_path, file_name + '.xlsx' )
        wb = openpyxl.load_workbook ( file_path)
        self.values.load_from_excel(wb, 'UFMT_VALUE')
        self.conversions.load_from_excel(wb, 'UFMT_CONVERSION')
        self.conv_rules.load_from_excel(wb, 'UFMT_CONV_RULE')
        self.conditions.load_from_excel(wb, 'UFMT_CONDITION')
        self.field_formats.load_from_excel(wb, 'UFMT_FIELD_FORMAT')
        self.formats.load_from_excel(wb, 'UFMT_FORMAT')
        self.fields.load_from_excel(wb, 'UFMT_FIELD')
        self.build_rules.load_from_excel(wb, 'UFMT_BUILD_RULE')
        self.format_selects.load_from_excel(wb, 'UFMT_FORMAT_SELECT')

    def save_to_excel( self, file_name, dir_path = None ):
        if dir_path is None:
            file_path = os.path.join( 'Data', 'Excel', file_name + '.xlsx' )
        else:
            file_path = os.path.join( dir_path, file_name + '.xlsx' )
        wb = openpyxl.load_workbook ( file_path)
        self.values.save_to_excel(wb, 'UFMT_VALUE')
        self.conversions.save_to_excel(wb, 'UFMT_CONVERSION')
        self.conv_rules.save_to_excel(wb, 'UFMT_CONV_RULE')
        self.conditions.save_to_excel(wb, 'UFMT_CONDITION')
        self.field_formats.save_to_excel(wb, 'UFMT_FIELD_FORMAT')
        self.formats.save_to_excel(wb, 'UFMT_FORMAT')
        self.fields.save_to_excel(wb, 'UFMT_FIELD')
        self.build_rules.save_to_excel(wb, 'UFMT_BUILD_RULE')
        self.format_selects.save_to_excel(wb, 'UFMT_FORMAT_SELECT')
        wb.save( file_path )

    def link( self ):
        self.conv_rules.link( self.conversions )
        self.conditions.link( self.values, self.conversions, self.conditions )
        self.fields.link( self.formats )
        self.build_rules.link( self.fields, self.field_formats, self.conditions, self.conversions, self.values ) 
        self.format_selects.link ( self.formats )
        
def test():
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
    data_set.load_from_excel('UFMT_DATA', '.')
    data_set.export_to_sql( '.' )

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
    
if __name__ == '__main__':
    test9()
    print('Warning! This is a module, please don\'t execute it directly!')
    
    
