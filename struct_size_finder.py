from pycparser import c_ast

import ast_generator
from helpers import submission_dir


class StructVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.structs = []

    def visit_Struct(self, node):
        if node.name:

            if node.decls:
                self.structs.append(node)

    def visit_Typedef(self, node):
        if isinstance(node.type, c_ast.Struct):
            if node.decls:
                self.structs.append(node)
            # print(node)


def find_struct_sizes(ast) -> dict:
    """
    Finds and returns the size of a struct based on the datatypes of the contents of the struct.
    Represents the size of a struct if you were to malloc one
    """
    types = {
        'char': 1,
        'short': 2,
        'int': 4,
        'long': 8,
        'long long': 8,
        'unsigned char': 1,
        'unsigned short': 2,
        'unsigned int': 4,
        'unsigned long': 8,
        'unsigned long long': 8,
        'float': 4,
        'double': 8,
        'long double': 16,
        '_Bool': 1,
        'wchar_t': 4,
        'size_t': 8,
        'ptrdiff_t': 8
    }



    visitor = StructVisitor()
    visitor.visit(ast)

    struct_dict = {
        'count': len(visitor.structs),
        'sizes': []
    }

    for struct in visitor.structs:
        size = 0
        for decl in struct.decls:
            if isinstance(decl.type, c_ast.PtrDecl):
                size += 4
            elif isinstance(decl.type, c_ast.TypeDecl):
                if isinstance(decl.type.type, c_ast.IdentifierType):
                    name = " ".join(decl.type.type.names)
                    size += types[name]
                else:
                    print("This should not happen!")
            elif isinstance(decl.type, c_ast.ArrayDecl):
                contents_type = decl.type

                array_size = 1
                while isinstance(contents_type, c_ast.ArrayDecl):
                    array_size *= int(contents_type.dim.value)

                    contents_type = contents_type.type

                array_size *= types[" ".join(contents_type.type.names)]

                size += array_size
            else:
                print("ELSE")
                # print(decl.type)
        struct_dict['sizes'].append((struct.name, size))

    print(struct_dict)

    return struct_dict


if __name__ == "__main__":
    ast_generator.find_structs(submission_dir + "/BaseFilters.c")