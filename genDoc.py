from  defoldsdk import sdk 
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.text_format import  Parse , MessageToString
from google.protobuf.json_format import MessageToDict , MessageToJson , ParseDict
import inspect , os , json , sys
os.system('clear')


class SdkGenDoc : 
    PROTOBUF_TYPE_TO_PYTHON_TYPE = {
        FieldDescriptor.TYPE_DOUBLE: 'float',
        FieldDescriptor.TYPE_FLOAT: 'float',
        FieldDescriptor.TYPE_INT64: 'int',
        FieldDescriptor.TYPE_UINT64: 'int',
        FieldDescriptor.TYPE_INT32: 'int',
        FieldDescriptor.TYPE_FIXED64: 'int',
        FieldDescriptor.TYPE_FIXED32: 'int',
        FieldDescriptor.TYPE_BOOL: 'bool',
        FieldDescriptor.TYPE_STRING: 'str',
        FieldDescriptor.TYPE_BYTES: 'bytes',
        FieldDescriptor.TYPE_UINT32: 'int',
        FieldDescriptor.TYPE_ENUM: 'int',
        FieldDescriptor.TYPE_SFIXED32: 'int',
        FieldDescriptor.TYPE_SFIXED64: 'int',
        FieldDescriptor.TYPE_SINT32: 'int',
        FieldDescriptor.TYPE_SINT64: 'int',
    }

    def get_type_enums(typ ) : 
        enums = dict()
        for enum_name , enum_type in typ.DESCRIPTOR.enum_types_by_name.items() : 
            typename = typ.__class__.__name__ 
            enums[enum_name] = [
                f'{typename}.{enum_name}.{key}' 
                for key , value  in enum_type.values_by_name.items()
            ]
        return enums

    def get_fields(typ) : 
        return [property_name for property_name, field in typ.DESCRIPTOR.fields_by_name.items() ]

    def parseFiled(typ,field,name) : 
        field_type = None
        namespace = "sdk"
        innerTypes = dict()
        if field.type == field.TYPE_MESSAGE and field.label != field.LABEL_REPEATED  : # memeber type message
            field_type  = field.message_type._concrete_class.__name__ 
            if not field_type in sdk._asdict() : 
                namespace += f".{name}"
                innerTypes[field_type] = field_type
        if field.type == field.TYPE_MESSAGE and field.label == field.LABEL_REPEATED  : # memeber type list of message
            field_type = f"List[{field.message_type._concrete_class.__name__}]" 
        if field.type != field.TYPE_MESSAGE and field.label == field.LABEL_REPEATED  : # memeber type list of prirmitive_types
            field_type = f"List[{SdkGenDoc.PROTOBUF_TYPE_TO_PYTHON_TYPE.get(field.type)}]" 
        if field.type != field.TYPE_MESSAGE and field.label != field.LABEL_REPEATED  : # memeber type prirmitive
            field_type = SdkGenDoc.PROTOBUF_TYPE_TO_PYTHON_TYPE.get(field.type)

        f = {
            "name" : name , 
            "namespace" : namespace , 
            "type" : field_type , 
            "innerTypes" : innerTypes

        }
        return f 

    def parseFields(typ): 
        fields = dict()
        for name , field in typ.DESCRIPTOR.fields_by_name.items() : 
            field = typ.DESCRIPTOR.fields_by_name.get(name)
            fields[name] = SdkGenDoc.parseFiled(typ=typ , field=field , name = name)
        return fields




    def genDoc(self) : 
        sdk_types = dict()
        for typ_name, typ in sdk._asdict().items() : 
            sdk_types[typ_name] =  SdkGenDoc.parseType(typ=typ)
        json.dump(sdk_types , fp = open("sdk.json","w"), indent=4)

    def parseType(typ) : 
        info = {
            "enums" : SdkGenDoc.get_type_enums(typ) , "fields" : SdkGenDoc.parseFields(typ) 
        }
        return info

    def parseInnerType(field) : 
        print(field.name)
        fields = dict()
        for name , f in field.fields_by_name.items() : 
            name = f._concrete_class.fields_by_name.get(name)
            fields[name] = SdkGenDoc.parseFiled(typ=typ , field=f , name = name)
        print(fields)


SdkGenDoc().genDoc()