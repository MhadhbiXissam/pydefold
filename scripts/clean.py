import ast 
import os , glob

extra_code__ = """
import importlib , pkgutil , collections , os 
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.text_format import  Parse , MessageToString
from google.protobuf.json_format import MessageToDict , MessageToJson , ParseDict

class TypesGenerator : 
    def getDefoldTypes(self) : 
        result = dict()
        pkg_lib = importlib.import_module('defoldsdk')
        for elem in dir(pkg_lib) : 
            may_msg = pkg_lib.__getattribute__(elem)
            if type(may_msg).__name__ == 'MessageMeta' : 
                result[may_msg.__name__] = may_msg
        return collections.namedtuple('defoldsdk' , result.keys() )(**result)
sdk = TypesGenerator().getDefoldTypes()
__all__ = ["sdk"]
"""



class LocalImportFixer(ast.NodeTransformer):
	def __init__(self,pydefold_folder) : 
		self.pydefold_folder = os.path.basename(pydefold_folder)
		exxluded_folders = ['proto' , 'google']
		self.interst_folders = [	os.path.basename(f)	for f in glob.glob(os.path.join(self.pydefold_folder,"*")) if os.path.isdir(f) and not  os.path.basename(f) in exxluded_folders ]

	def visit_ImportFrom(self, node):
		if  node.module in self.interst_folders:
			node.module = f"{self.pydefold_folder}.{node.module}" 
		return node



def cleanModule(root = "defoldsdk") : 
    module_name = os.path.basename(root)
    subfolders = [os.path.join(dp, d) for dp, dn, filenames in os.walk(root) for d in dn if not (os.path.basename(d).startswith("__") and os.path.basename(d).endswith("__"))]
    for subfolder in subfolders : 
        pb2_files = glob.glob(os.path.join(subfolder,"*_pb2.py"))
        import_code = "\n".join(f'from .{os.path.basename(f).removesuffix(".py")} import *' for f in pb2_files)
        print(import_code , file=open(os.path.join(subfolder,"__init__.py"),"w"))
        submodule = os.path.basename(subfolder)
        for pb2_file in pb2_files : 
            pyfile_content = open(pb2_file).read()
            ast_tree = ast.parse(pyfile_content)
            localImportFixer = LocalImportFixer(root)
            modified_tree  = localImportFixer.visit(ast_tree)
            print(ast.unparse(modified_tree) , file = open(pb2_file,"w"))
    all_submodules = [os.path.basename(subfolder) for  subfolder in subfolders ] + [os.path.basename(f).removesuffix(".py") for f in glob.glob(os.path.join(root,"*_pb2.py"))]
    all_submodules = "\n".join(f"from .{submodule} import *" for submodule in all_submodules)
    print(all_submodules + f"\n{extra_code__}" , file= open(os.path.join(root,"__init__.py"),"w"))








cleanModule()