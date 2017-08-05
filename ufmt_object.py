#!python3
'''
This module define classes that are used by ufmt_data_processor
'''

import os, openpyxl, logging, sys, re, csv
from enum import IntEnum
try:
    import cx_Oracle
except Exception:
    logging.warn('Oracle import/export is not supported')

#configuration
oracle_db_string='SVFE_TEST_BSM/SVFE_TEST_BSM1@BSM_DEV_FE'

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
    BITFIELD = 8
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
class Operand_Type(IntEnum):
    CURRENT = 0
    TAG = 1
    STRING = 2
    NUMBER = 3
#enum constants - end
    
#Convert functions - start
def To_Int( ext_string ):
    try:
        return int( ext_string )
    except Exception:
        return None

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

class Complex_Value(object):
    def __init__ ( self, value, ufmt_values, ufmt_convs ):
        if value[0].isdigit():
            self.separator = ''
            join_str = value
        else:
            self.separator = value[0]
            join_str = value[1:]
        val_conv_pairs = join_str.split(',')
        self.values = []
        self.convs = []
        for pair in val_conv_pairs:
            tokens = pair.split(':')
            value_id = int(tokens[0])
            if len(tokens) > 1:
                conv_key = int(tokens[1])
            else:
                conv_key = None
            u_value = ufmt_values.get( (value_id, ))
            if u_value is None:
                raise ValueError('Invalid value id {}'.format(value_id))
            u_conv = ufmt_convs.get( (conv_key, ))
            self.values.append( u_value )
            self.convs.append( u_conv )
            #print( 'value_id = {}, conv_key = {}'.format(value_id, conv_key ) )
            #print( u_value )
            #print( u_conv )
            
    def __str__ ( self ):
        pairs = []
        for i in range( len ( self.values )):
            s = str(self.values[i].value_id)
            if self.convs[i] is not None:
                s += ':' + str(self.convs[i].conv_key)
            pairs.append(s)
        s = self.separator + ','.join( pairs )
        return s

    def show_details ( self, indent = 0 ):
        tabs = '\t'*indent
        print( '{}Separator="{}"'.format( tabs, self.separator ) )
        for i in range( len ( self.values ) ):
            print( '{}{}'.format( tabs, self.values[i] ))
            if self.convs[i] is not None:
                print( '{}{}'.format(tabs, self.convs[i] ) )

class Bitfield_Value(object):
    def __init__ ( self, raw_value, ufmt_values ):
        value_ids = raw_value.split('.')
        if len(value_ids) != 2:
            raise ValueError('Invalid bit-field value format')
        self.value = ufmt_values.get( (int(value_ids[0]),) )
        self.bit_value = ufmt_values.get( (int(value_ids[1]),) )
        
    def __str__ ( self ):
        return '{}.{}'.format( self.value.value_id, self.bit_value.value_id )
    
    def show_details ( self, indent = 0 ):
        tabs = '\t'*indent
        print( '{}Value: {}'.format( tabs, self.value ))
        print( '{}Bit: {}'.format( tabs, self.bit_value ) )
        
class Arithmetic_Operand ( object ):
    def __init__ ( self, operand_str, ufmt_values, ufmt_convs ):
        if operand_str == '{-1}':
            self.type = Operand_Type.CURRENT
        elif (operand_str[0], operand_str[-1]) == ('{', '}'):
            self.type = Operand_Type.TAG
            tokens = operand_str[1:-1].split(':')
            value_id = int(tokens[0])
            if len(tokens) > 1:
                conv_key = int(tokens[1])
            else:
                conv_key = None
            self.value = ufmt_values.get( (value_id, ))
            self.conv = ufmt_convs.get( (conv_key, ))
        elif (operand_str[0], operand_str[-1]) == ('"', '"'):
            self.type = Operand_Type.STRING
            self.string = operand_str[1:-1]
        else:
            self.type = Operand_Type.NUMBER
            self.number = int(operand_str)
            
    def __str__ ( self ):
        if self.type == Operand_Type.CURRENT:
            return '{-1}'
        if self.type == Operand_Type.TAG:
            value_id = str(self.value.value_id)
            if self.conv is None:
                with_conv_key = ''
            else:
                with_conv_key = ':' + str(self.conv.conv_key)
            return '{%s%s}' % (value_id, with_conv_key )
        if self.type == Operand_Type.STRING:
            return '"%s"' % self.string
        if self.type == Operand_Type.NUMBER:
            return str(self.number)

    def show_details ( self, indent = 0):
        tabs = '\t'*indent
        print( '{}Type: {}'.format( tabs, self.type))
        if self.type == Operand_Type.TAG:
            print ('{}{}'.format( tabs, self.value ) )
            if self.conv is not None:
                print ('{}{}'.format( tabs, self.conv ) )
        elif self.type == Operand_Type.STRING:
            print ('{}"{}"'.format( tabs, self.string ))
        elif self.type == Operand_Type.NUMBER:
            print ('{}{}'.format( tabs, self.number ))
               
class Arithmetic_Conv_Rule ( object ):    
    def extract_operand( string ):
        po_tag = re.compile( '^(\{-?\d+\})' )
        po_tag2 = re.compile( '^(\{-?\d+:\d+\})' )
        po_str = re.compile( '^("\w+")' )
        po_num = re.compile( '^(-?\d+)' )
        for po in ( po_tag, po_tag2, po_str, po_num ):
            mo = po.match( string )
            if mo is not None:
                return mo.group(1)
        return None
    
    def __init__ ( self, raw_dest_value, ufmt_values, ufmt_convs ):
        opers = ('+','-','*','/','%','&')
        operand1 = Arithmetic_Conv_Rule.extract_operand ( raw_dest_value )
        if operand1 is None:
            #print( raw_dest_value )
            raise ValueError('1st operand is not found')
        remain_dest_value = raw_dest_value[len(operand1):]
        self.operator = remain_dest_value[0]
        if self.operator not in ('+','-','*','/','%','&'):
            #print( raw_dest_value )
            raise ValueError('Invalid operator %s' % self.operator )
        remain_dest_value = remain_dest_value[1:]
        operand2 = Arithmetic_Conv_Rule.extract_operand ( remain_dest_value )
        if operand2 is None:
            #print( raw_dest_value )
            #raise ValueError('2nd operand is not found')        
            operand2 = '""'
            
        self.operands = [ None ] * 2
        self.operands[0] = Arithmetic_Operand( operand1, ufmt_values, ufmt_convs )
        self.operands[1] = Arithmetic_Operand( operand2, ufmt_values, ufmt_convs )
            
    def __str__ ( self ):
        return self.operator.join( [ str( operand ) for operand in self.operands ] )

    def show_details ( self, indent = 0):
        tabs = '\t'*indent
        print ( '{}Oprand 1:'.format ( tabs ) )
        self.operands[0].show_details( indent + 1 )
        print ( '{}Operator = "{}"'.format ( tabs, self.operator ))
        print ( '{}Oprand 2:'.format ( tabs ) )
        self.operands[1].show_details( indent + 1 )
        
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
        return [From_Int(self.value_id), From_Int(self.value_type.value), From_Int(self.value_subtype.value), From_Str(self.get_raw_value()), From_Str(self.description)]

    def get_excel_values(self ):
        return [self.value_id, self.value_type.value, self.value_subtype.value, self.get_raw_value(), self.description]

    def __str__( self ):
        s = 'Value #{}: type {}, subtype {}, desc "{}", value "{}"'
        s = s.format( self.value_id, self.value_type.name, self.value_subtype.name, self.description, self.get_raw_value() )
        return s

    def validate( self, ufmt_data_set ):
        try:
            if self.value_type is Value_Type.COMPLEX:
                self.value = Complex_Value ( self.value, ufmt_data_set.values, ufmt_data_set.conversions )
            elif self.value_type is Value_Type.BITFIELD:
                self.value = Bitfield_Value ( self.value, ufmt_data_set.values )
            elif self.value_type is Value_Type.FMT:
                self.value = ufmt_data_set.formats.get( ( int(self.value), ))
            elif self.value_type in ( Value_Type.LOCAL, Value_Type.MONEYFLD, Value_Type.PMT, Value_Type.UMF ):
                self.value = int( self.value )
            elif self.value_type is Value_Type.CONST:
                if self.value_subtype in (Value_Subtype.INT, Value_Subtype.LONG_LONG ):
                    self.value = int( self.value )
                elif self.value_subtype in ( Value_Subtype.FLOAT, Value_Subtype.FLOAT_IP ):
                    self.value = float( self.value )
        except Exception as e:
            #logging.error( )
            print( 'Invalid value {}, error {}'.format( self.value_id, e ) )
            
    def get_raw_value( self ):
        if self.value is None:
            return ''
        if self.value_type is Value_Type.FMT and isinstance( self.value, Ufmt_Format ):
            return str(self.value.format_id)
        return str(self.value)
    
    def show_details( self, indent = 0 ):
        tabs = '\t'*indent
        print ( '{}{}'.format( tabs, self ) )
        if self.value_type is Value_Type.COMPLEX and isinstance( self.value, Complex_Value ) :
            self.value.show_details( indent + 1 )
        elif self.value_type is Value_Type.BITFIELD and isinstance( self.value, Bitfield_Value ) :
            self.value.show_details( indent + 1 )
        elif self.value_type is Value_Type.FMT and isinstance( self.value, Ufmt_Format ):
            self.value.show_details( indent + 1 )

    def change_key ( self, new_value_id ):
        self.value_id = new_value_id
        self.key = ( self.value_id,)
        
class Ufmt_Conversion(object):

    def __init__( self, conv_key, conv_type, description):
        self.__init__ ( (conv_key, conv_type, description) )
        
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

    def show_details ( self, indent = 0 ):
        tabs = '\t' * indent
        print ( '{}{}'.format( tabs, self ) )
        tabs += '\t'
        for conv_rule in self.conv_rules.values():
            print ( '{}{}'.format( tabs, conv_rule ) )

    def change_key ( self, new_conv_key, conv_rules ):
        old_conv_key = self.conv_key
        self.conv_key = new_conv_key
        self.key = ( self.conv_key,)
        for rule_num in self.conv_rules:
            conv_rules.change_key( (old_conv_key, rule_num), (new_conv_key, rule_num ) )
        
class Ufmt_Conv_Rule(object):

    def __init__( self, conv_key, rule_num, src_value, dest_value, next_key, is_default):
        self.__init__ ( (conv_key, rule_num, src_value, dest_value, next_key, is_default) )
        
    def __init__( self, prop_list):
        self.conv_key = To_Int(prop_list[0])
        self.rule_num = To_Int(prop_list[1])
        self.src_value = To_Str(prop_list[2])
        self.dest_value = To_Str(prop_list[3])
        self.next_key = To_Int(prop_list[4])
        self.is_default = To_Int(prop_list[5])
        self.key = ( self.conv_key, self.rule_num,)
        self.conv = None
        self.next_conv = None

    def get_conv_key( self ):
        if self.conv is not None:
            return self.conv.conv_key
        else:
            return self.conv_key

    def get_next_key( self ):
        if self.next_conv is not None:
            return self.next_conv.conv_key
        else:
            return self.next_key
        
    def __list__(self ):
        return [From_Int(self.get_conv_key()),
                From_Int(self.rule_num),
                From_Str(self.src_value),
                From_Str(self.get_raw_dest_value()),
                From_Int(self.get_next_key()),
                From_Int(self.is_default)]

    def get_excel_values(self ):
        return [self.get_conv_key(),
                self.rule_num,
                self.src_value,
                self.get_raw_dest_value(),
                self.get_next_key(),
                self.is_default]

    def link ( self, convs ):
        self.conv = convs.get( ( self.conv_key, ) )
        if self.next_key is not None:
            self.next_conv = convs.get( ( self.next_key,) )
        else:
            self.next_conv = None
        
    def __str__( self ):
        s = 'Conversion #{}, rule#{}: src "{}", dest "{}"'
        s = s.format( self.get_conv_key(), self.rule_num, self.src_value, self.dest_value)
        if self.is_default == 1:
            s = s + ', default'
        if self.next_key is not None:
            s = s + ', next key #{}'.format( self.next_key )
        return s

    def validate( self, ufmt_data_set ):
        try:
            if self.conv.conv_type is Conv_Type.ARITHMETIC:
                self.dest_value = Arithmetic_Conv_Rule ( self.dest_value, ufmt_data_set.values, ufmt_data_set.conversions )
        except Exception as e:
            print('Invalid conv key {},{}, error "{}"'.format( self.get_conv_key(), self.rule_num, e ) )
            
    def get_raw_dest_value( self ):
        return str(self.dest_value)
    
    def show_details( self, indent = 0 ):
        tabs = '\t' * indent
        print ( '{}{}'.format( tabs, self.conv ) )
        print ( '{}{}'.format( tabs, self ) )
        if self.conv.conv_type is Conv_Type.ARITHMETIC and isinstance( self.dest_value, Arithmetic_Conv_Rule ):
            print ( '{}Destination Arimetic Operation'.format (tabs ))
            self.dest_value.show_details( indent + 1)

    def change_key ( self, new_key ):
        ( self.conv_key, self.rule_num ) = new_key
        self.key = new_key
        
class Ufmt_Condition(object):

    def __init__( self, cond_id, operator, value1, conv1, value2, conv2, cond1, cond2, f_strcmp, description):
        self.__init__( ( cond_id, operator, value1, conv1, value2, conv2, cond1, cond2, f_strcmp, description ) )
        
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
        self.value1 = None
        self.value2 = None
        self.conv1 = None
        self.conv2 = None
        self.cond1 = None
        self.cond2 = None
        
    def __list__(self ):
        return [From_Int(self.cond_id),
                From_Str(self.operator),
                From_Int(self.get_value_id1()),
                From_Int(self.get_conv_key1()),
                From_Int(self.get_value_id2()),
                From_Int(self.get_conv_key2()),
                From_Int(self.get_cond_id1()),
                From_Int(self.get_cond_id2()),
                From_Int(self.f_strcmp),
                From_Str(self.description)]

    def get_excel_values(self ):
        return [self.cond_id,
                self.operator,
                self.get_value_id1(),
                self.get_conv_key1(),
                self.get_value_id2(),
                self.get_conv_key2(),
                self.get_cond_id1(),
                self.get_cond_id2(),
                self.f_strcmp,
                self.description]

    def link ( self, values, convs, conds ):
        self.value1 = values.get( ( self.value_id1, ) )
        self.value2 = values.get( ( self.value_id2, ) )
        self.conv1 = convs.get( ( self.conv_key1, ) )
        self.conv2 = convs.get( ( self.conv_key2, ) )
        self.cond1 = conds.get( ( self.cond_id1, ) )
        self.cond2 = conds.get( ( self.cond_id2, ) )

    def get_value_id1( self ):
        if self.value1 is not None:
            return self.value1.value_id
        else:
            return self.value_id1

    def get_value_id2( self ):
        if self.value2 is not None:
            return self.value2.value_id
        else:
            return self.value_id2

    def get_cond_id1( self ):
        if self.cond1 is not None:
            return self.cond1.cond_id
        else:
            return self.cond_id1

    def get_cond_id2( self ):
        if self.cond2 is not None:
            return self.cond2.cond_id
        else:
            return self.cond_id2

    def get_conv_key1( self ):
        if self.conv1 is not None:
            return self.conv1.conv_key
        else:
            return self.conv_key1

    def get_conv_key2( self ):
        if self.conv2 is not None:
            return self.conv2.conv_key
        else:
            return self.conv_key2
                
    def __str__( self ):
        if self.operator in ('&', '|', '!'):
            operand1 = 'cond {}'.format( self.get_cond_id1() )
            operand2 = 'cond {}'.format( self.get_cond_id2() )
        else:
            operand1 = 'value {}'.format( self.get_value_id1() )
            if self.get_conv_key1() is not None:
                operand1 = operand1 + ' : conv {}'.format( self.get_conv_key1() )
            operand2 = 'value {}'.format( self.get_value_id1() )
            if self.get_conv_key2() is not None:
                operand2 = operand2 + ' : conv {}'.format( self.get_conv_key2() )
                
        s = 'Condition #{}:'.format( self.cond_id )
        if self.operator == '!':
            s += ' {} {}'.format( self.operator, operand1 )
        else:
            s += ' {} {} {}'.format ( operand1, self.operator, operand2 )

        s += ', desc "{}"'.format( self.description )
        return s

    def change_key ( self, new_cond_id ):
        self.cond_id = new_cond_id
        self.key = ( self.cond_id,)
        
class Ufmt_Field_Format(object):

    def __init__( self, field_id, length_type, length, data_type, field_type, psymbol, pside, description):
        self.__init__ ( (field_id, length_type, length, data_type, field_type, psymbol, pside, description) )

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

    def change_key ( self, new_field_id ):
        self.field_id = new_field_id
        self.key = ( self.field_id,)
        
class Ufmt_Format(object):

    def __init__( self, format_id, format_type, description, bitmap_type):
        '''
        self.format_id = To_Int(format_id)
        self.format_type = Format_Type ( To_Int(format_type) )
        self.description = To_Str(description)
        self.bitmap_type = Bitmap_Type ( To_Int(bitmap_type) )
        self.key = ( self.format_id,)

        self.fields = dict()
        '''
        self.__init__ ( (format_id, format_type, description, bitmap_type) )
        
    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.format_type = Format_Type ( To_Int(prop_list[1]) )
        self.description = To_Str(prop_list[2])
        self.bitmap_type = Bitmap_Type ( To_Int(prop_list[3]) )
        self.key = ( self.format_id,)

        self.fields = dict()
        
    def __list__(self ):
        return [From_Int(self.format_id),
                From_Int(self.format_type.value),
                From_Str(self.description),
                From_Int(self.bitmap_type.value)]

    def get_excel_values(self ):
        return [self.format_id,
                self.format_type.value,
                self.description,
                self.bitmap_type.value]

    def __str__( self ):
        s = 'Format #{}: type {}, bitmap type {}, desc "{}"'
        s = s.format( self.format_id, self.format_type.name, self.bitmap_type.name, self.description )
        return s

    def add_to_fields ( self, field ):
        if field.format_id == self.format_id:
            self.fields[ field.field_no ] = field

    def show_details ( self, indent = 0 ):
        tabs = '\t' * indent
        print ( '{}{}'.format( tabs, self ) )
        tabs1 = '\t' * (indent + 1)
        tabs2 = '\t' * (indent + 2)
        tabs3 = '\t' * (indent + 3)
        for field in self.fields.values():
            print ( '{}{}'.format ( tabs1, field ) )
            for rule in field.build_rules.values():
                s = '{}{}'.format ( tabs2, rule )
                s += '\n{}{}'.format ( tabs3, rule.field_format )
                if rule.cond is not None:
                    s += '\n{}{}'.format ( tabs3, rule.cond )
                s += '\n{}{}'.format ( tabs3, rule.value )
                if rule.conv is not None:
                    s += '\n{}{}'.format ( tabs3, rule.conv )
                print ( s )

    def change_key ( self, new_format_id, fields, build_rules ):
        old_format_id = self.format_id
        self.format_id = new_format_id
        self.key = ( self.format_id,)
        for field_no in self.fields:
            fields.change_key ( ( old_format_id, field_no ), ( new_format_id, field_no ), build_rules )
            
class Ufmt_Field(object):

    def __init__( self, format_id, field_no, f_mac, f_key, f_mandatory, description):
        '''
        self.format_id = To_Int(format_id)
        self.field_no = To_Int(field_no)
        self.f_mac = To_Int(f_mac)
        self.f_key = To_Int(f_key)
        self.f_mandatory = To_Int(f_mandatory)
        self.description = To_Str(description)
        self.key = ( self.format_id, self.field_no,)

        self.build_rules = dict()
        '''
        self.__init__ ( ( format_id, field_no, f_mac, f_key, f_mandatory, description ) )
        
    def __init__( self, prop_list):
        self.format_id = To_Int(prop_list[0])
        self.field_no = To_Int(prop_list[1])
        self.f_mac = To_Int(prop_list[2])
        self.f_key = To_Int(prop_list[3])
        self.f_mandatory = To_Int(prop_list[4])
        self.description = To_Str(prop_list[5])
        self.key = ( self.format_id, self.field_no,)
        self.build_rules = dict()
        self.format = None

    def get_format_id ( self ):
        if self.format is not None:
            return self.format.format_id
        else:
            return self.format_id
        
    def __list__(self ):
        return [From_Int(self.get_format_id()),
                From_Int(self.field_no),
                From_Int(self.f_mac),
                From_Int(self.f_key),
                From_Int(self.f_mandatory),
                From_Str(self.description)]

    def get_excel_values(self ):
        return [self.get_format_id(),
                self.field_no,
                self.f_mac,
                self.f_key,
                self.f_mandatory,
                self.description]

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
        s = s.format( self.get_format_id(), self.field_no, mac, key, mand, self.description )
        return s

    def add_to_build_rules ( self, build_rule ):
        if ( build_rule.get_format_id(), build_rule.field_no ) == self.key:
            self.build_rules[ build_rule.priority ] = build_rule

    def show_details ( self, indent = 0 ):
        tabs = '\t' * indent
        print ( '{}{}'.format( tabs, self ) )
        print ( '{}{}'.format( tabs, self.format ) )
        tabs1 = '\t' * ( indent + 1 )
        tabs2 = '\t' * ( indent + 2 )
        for rule in self.build_rules.values():
            s = '{}{}'.format( tabs1, rule )
            s += '\n{}{}' .format( tabs2, rule.field_format )
            if rule.cond is not None:
                s += '\n{}{}'.format( tabs2, rule.cond )
            s += '\n{}{}'.format( tabs2, rule.value )
            if rule.conv is not None:
                s += '\n{}{}'.format( tabs2, rule.conv )
            print ( s )

    def change_key ( self, new_key, build_rules ):
        old_key = self.key
        self.key = new_key
        ( self.format_id, self.field_no,) = new_key
        for priority in self.build_rules:
            build_rules.change_key( (old_key[0], old_key[1], priority), (new_key[0], new_key[1], priority ) )

class Ufmt_Build_Rule(object):

    def __init__( self, format_id, field_no, priority, field_id, cond_id, value_id, conv_key, f_check, f_write):
        self.__init__ ( (format_id, field_no, priority, field_id, cond_id, value_id, conv_key, f_check, f_write) )
        
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
        self.field = None
        self.field_format = None
        self.cond = None
        self.conv = None
        self.value = None
        
    def get_value_id( self ):
        if self.value is not None:
            return self.value.value_id
        else:
            return self.value_id

    def get_format_id( self ):
        if self.field is not None:
            return self.field.get_format_id()
        else:
            return self.format_id

    def get_cond_id( self ):
        if self.cond is not None:
            return self.cond.cond_id
        else:
            return self.cond_id

    def get_field_id( self ):
        if self.field_format is not None:
            return self.field_format.field_id
        else:
            return self.field_id

    def get_conv_key( self ):
        if self.conv is not None:
            return self.conv.conv_key
        else:
            return self.conv_key
        
    def __list__(self ):
        return [From_Int(self.get_format_id()),
                From_Int(self.field_no),
                From_Int(self.priority),
                From_Int(self.get_field_id()),
                From_Int(self.get_cond_id()),
                From_Int(self.get_value_id()),
                From_Int(self.get_conv_key()),
                From_Int(self.f_check),
                From_Int(self.f_write)]

    def get_excel_values(self ):
        return [self.get_format_id(),
                self.field_no,
                self.priority,
                self.get_field_id(),
                self.get_cond_id(),
                self.get_value_id(),
                self.get_conv_key(),
                self.f_check,
                self.f_write]

    def link( self, fields, field_formats, conds, convs, values ):
        self.field = fields.get( ( self.format_id, self.field_no, ) )
        self.field_format = field_formats.get ( ( self.field_id, ) )
        self.cond = conds.get( (self.cond_id, ) )
        self.conv = convs.get( (self.conv_key, ) )
        self.value = values.get( (self.value_id, ) )
        
    def __str__ ( self ):
        s = 'Format #{}, field #{}, rule #{}: field format {}, cond {}, value {}, conv {}, check {}, write {}'
        s = s.format( self.get_format_id(), self.field_no, self.priority, self.get_field_id(), self.get_cond_id(),
                      self.get_value_id(), self.get_conv_key(), self.f_check, self.f_write )
        return s

    def show_details ( self, indent = 0 ):
        tabs = '\t' * indent
        print ( '{}{}'.format( tabs, self) )
        print ( '{}{}'.format( tabs, self.field.format ) )
        print ( '{}{}'.format( tabs, self.field ) )
        print ( '{}{}'.format( tabs, self.field_format ) )
        if self.cond is not None:
            print ( '{}{}'.format( tabs, self.cond ) )
        print ( '{}{}'.format( tabs, self.value ) )
        if self.conv is not None:
            print ( '{}{}'.format( tabs, self.conv ) )

    def change_key ( self, new_key ):
        ( self.format_id, self.field_no, self.priority,) = new_key
        self.key = new_key
        
class Ufmt_Format_Select(object):

    def __init__( self, formatter, rule_num, route_type, service_id_in, trans_type_in, msg_type_in, reversal_in,
                  mti, format_id, trans_type_out, msg_type_out, reversal_out, fIntran_in, acq_inst_in, iss_inst_in, service_type_in):
        '''
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
        '''
        self.__init__ ( (formatter, rule_num, route_type, service_id_in, trans_type_in, msg_type_in, reversal_in,
                         mti, format_id, trans_type_out, msg_type_out, reversal_out, fIntran_in, acq_inst_in, iss_inst_in, service_type_in) )
        
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
        self.format = None
        
    def get_format_id ( self ):
        if self.format is not None:
            return self.format.format_id
        else:
            return self.format_id
        
    def __list__(self ):
        return [From_Str(self.formatter),
                From_Int(self.rule_num),
                From_Str(self.route_type),
                From_Str(self.service_id_in),
                From_Str(self.trans_type_in),
                From_Str(self.msg_type_in),
                From_Str(self.reversal_in),
                From_Str(self.mti),
                From_Int(self.get_format_id()),
                From_Str(self.trans_type_out),
                From_Str(self.msg_type_out),
                From_Str(self.reversal_out),
                From_Str(self.fintran_in),
                From_Str(self.acq_inst_in),
                From_Str(self.iss_inst_in),
                From_Str(self.service_type_in)]

    def get_excel_values(self ):
        return [self.formatter,
                self.rule_num,
                self.route_type,
                self.service_id_in,
                self.trans_type_in,
                self.msg_type_in,
                self.reversal_in,
                self.mti,
                self.get_format_id(),
                self.trans_type_out,
                self.msg_type_out,
                self.reversal_out,
                self.fintran_in,
                self.acq_inst_in,
                self.iss_inst_in,
                self.service_type_in]

    def link ( self, formats ):
        self.format = formats.get( ( self.format_id, ) )

    def __str__ ( self ):
        s1 = '(type {}, MTI {}, service id {}, service type {}, trans type {}, msg type {}, reversal {}, fintran {}, acq inst {}, iss inst {})'
        s1 = s1.format( self.route_type, self.mti, self.service_id_in, self.service_type_in,
                        self.trans_type_in, self.msg_type_in, self.reversal_in, self.fintran_in, self.acq_inst_in, self.iss_inst_in )
        s2 = '(format {}, trans type {}, msg type {}, reversal {})'
        s2 = s2.format( self.get_format_id(), self.trans_type_out, self.msg_type_out, self.reversal_out )
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
        keys = list(self.set.keys())
        keys.sort()
        for key in keys:
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
        keys = list(self.set.keys())
        keys.sort()
        for key in keys:
            col_num = 1
            for value in self.set[key].get_excel_values():
                sheet.cell(row = row_num, column = col_num).value = value
                col_num=col_num+1
            row_num=row_num+1

    def get_oracle_select_query( self ):
        return 'SELECT {} FROM {}'.format( ','.join( self.headers ), self.get_table_name() )
    
    def load_from_oracle_db ( self, conn ):
        statement = self.get_oracle_select_query()
        cursor = conn.cursor().execute( statement )
        for row in cursor:        
            data_record = [''] * len(row)
            for i in range( len(row) ):
                if row[i] == None:
                    data_record[i] = ''
                else:
                    data_record[i] = str(row[i])
            
            logging.debug ( data_record )
            elm = self.new_element(data_record)
            self.set[elm.key] = elm
            
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

    def validate( self, ufmt_data_set ):
        for elm in self.set.values():
            elm.validate ( ufmt_data_set )

    def change_key ( self, old_value_id, new_value_id ):
        old_key = ( old_value_id, )
        new_key = ( new_value_id, )
        if new_key in self.set:
            raise KeyError('{} already exists'.format(new_value_id) )
        value = self.set.pop( old_key )
        value.change_key ( new_value_id )
        self.set[new_key] = value
       
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

    def change_key ( self, old_conv_key, new_conv_key, conv_rules ):
        old_key = ( old_conv_key, )
        new_key = ( new_conv_key, )
        if new_key in self.set:
            raise KeyError('Conversion key {} already exists'.format(new_conv_key) )
        conv = self.set.pop( old_key )
        conv.change_key ( new_conv_key, conv_rules )
        self.set[new_key] = conv

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
            
    def validate( self, ufmt_data_set ):
        for elm in self.set.values():
            elm.validate ( ufmt_data_set )

    def change_key ( self, old_key, new_key ):
        if new_key in self.set:
            raise KeyError('Key {} already exists'.format(new_key) )
        elm = self.set.pop( old_key )
        elm.change_key ( new_key )
        self.set[new_key] = elm        
    
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

    def change_key ( self, old_cond_id, new_cond_id ):
        old_key = ( old_cond_id, )
        new_key = ( new_cond_id, )
        if new_key in self.set:
            raise KeyError('Condition ID {} already exists'.format(new_cond_id) )
        cond = self.set.pop( old_key )
        cond.change_key ( new_cond_id )
        self.set[new_key] = cond
        
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

    def change_key ( self, old_field_id, new_field_id ):
        old_key = ( old_field_id, )
        new_key = ( new_field_id, )
        if new_key in self.set:
            raise KeyError('Field Format ID {} already exists'.format(new_field_id) )
        field_format = self.set.pop( old_key )
        field_format.change_key ( new_field_id )
        self.set[new_key] = field_format

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

    def change_key ( self, old_format_id, new_format_id, fields, build_rules ):
        old_key = ( old_format_id, )
        new_key = ( new_format_id, )
        if new_key in self.set:
            raise KeyError('Format ID {} already exists'.format(new_format_id) )
        u_format = self.set.pop( old_key )
        u_format.change_key ( new_format_id, fields, build_rules )
        self.set[new_key] = u_format
        
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

    def change_key ( self, old_key, new_key, build_rules ):
        if new_key in self.set:
            raise KeyError('Key {} already exists'.format(new_key) )
        elm = self.set.pop( old_key )
        elm.change_key ( new_key, build_rules )
        self.set[new_key] = elm        
            
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

    def change_key ( self, old_key, new_key ):
        if new_key in self.set:
            raise KeyError('Key {} already exists'.format(new_key) )
        elm = self.set.pop( old_key )
        elm.change_key ( new_key )
        self.set[new_key] = elm
        
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
    def __init__ ( self, ora_db_str = None ):
        self.values = Ufmt_Value_Set()
        self.conversions = Ufmt_Conversion_Set()
        self.conv_rules = Ufmt_Conv_Rule_Set()
        self.conditions = Ufmt_Condition_Set()
        self.field_formats = Ufmt_Field_Format_Set()
        self.formats = Ufmt_Format_Set()
        self.fields = Ufmt_Field_Set()
        self.build_rules = Ufmt_Build_Rule_Set()
        self.format_selects = Ufmt_Format_Select_Set()
        if ora_db_str is None:
            self.ora_db_str = oracle_db_string
        else:
            self.ora_db_str = ora_db_str
            
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

    def load_from_oracle_db ( self ):
        try:
            conn = cx_Oracle.connect( self.ora_db_str )
        except Exception:
            logging.error("Can't connect to DB")
            return
        self.values.load_from_oracle_db ( conn )
        self.conversions.load_from_oracle_db ( conn )
        self.conv_rules.load_from_oracle_db ( conn )
        self.conditions.load_from_oracle_db ( conn )
        self.field_formats.load_from_oracle_db ( conn )
        self.formats.load_from_oracle_db ( conn )
        self.fields.load_from_oracle_db ( conn )
        self.build_rules.load_from_oracle_db ( conn )
        self.format_selects.load_from_oracle_db ( conn )
        conn.close()
        
    def link( self ):
        self.conv_rules.link( self.conversions )
        self.conditions.link( self.values, self.conversions, self.conditions )
        self.fields.link( self.formats )
        self.build_rules.link( self.fields, self.field_formats, self.conditions, self.conversions, self.values ) 
        self.format_selects.link ( self.formats )
        self.values.validate ( self )
        self.conv_rules.validate ( self )

    def change_conv_key ( self, old, new ):
        self.conversions.change_key ( old, new, self.conv_rules )

    def change_value_id ( self, old, new ):
        self.values.change_key ( old, new )

    def change_cond_id ( self, old, new ):
        self.conditions.change_key ( old, new )

    def change_format_id ( self, old, new ):
        self.formats.change_key ( old, new, self.fields, self.build_rules )

    def change_field_format_id ( self, old, new ):
        self.field_formats.change_key ( old, new )
    
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
    
if __name__ == '__main__':
    #test13()
    #test14()
    test15()
    print('Warning! This is a module, please don\'t execute it directly!')
    
    
