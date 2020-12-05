
"""
 * @author nhphung
"""
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List, Tuple
from AST import * 
from Visitor import *
from StaticError import *
from functools import *

class Type(ABC):
    __metaclass__ = ABCMeta
    pass
class Prim(Type):
    __metaclass__ = ABCMeta
    pass
class IntType(Prim):
    pass
class FloatType(Prim):
    pass
class StringType(Prim):
    pass
class BoolType(Prim):
    pass
class VoidType(Type):
    pass
class Unknown(Type):
    pass

@dataclass
class ArrayType(Type):
    dimen:List[int]
    eletype: Type

@dataclass
class MType:
    intype:List[Type]
    restype:Type

@dataclass
class Symbol:
    name: str
    mtype:Type

class Environment:
    def __init__(self):
        self.current_env = '',
        self.env = {}
        self.list_env = []
    
    def add_env(self, new_env):
        self.current_env = new_env
        self.env[new_env] = {
            'list_decl' : [],
        }
        self.list_env.append(new_env)
    
    def get_list_decl(self):
        index_current_env = self.list_env.index(self.current_env)
        list_decl = []
        for index_env in range(0, index_current_env + 1):
            env_name = self.list_env[index_env]
            for item in self.env[env_name]['list_decl']:
                list_decl.append(item)
        return reversed(list_decl)
    
    def get_list_decl_current_env(self):
        return self.env[self.current_env]['list_decl']
    
    def set_type_decl(self, name, new_type):
        list_decl = self.env[self.current_env]['list_decl']
        for decl in list_decl:
            if decl['name'] == name:
                decl['type'] = new_type

    def add_param_decl(self, list_param):
        self.env[self.current_env]['list_param'] = list_param

    def get_current_env(self):
        return self.current_env
    
    def set_current_env(self, env):
        self.current_env = env
    
    def get_list_param_current_env(self):
        try:
            list_param = self.env[self.current_env]['list_param']
            return list_param
        except:
            return []

    def get_param_decl(self, name):
        list_param = self.env[name]['list_param']
        return list_param

    def add_decl(self, new_decl):
        self.env[self.current_env]['list_decl'].append(new_decl)
    
    def get_type_decl(self, name_decl):
        list_decl = self.get_list_decl()
        for decl in list_decl:
            if decl['name'] == name_decl:
                return decl['type']
        
        return 'none'

class StaticChecker(BaseVisitor):
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = [
Symbol("int_of_float",MType([FloatType()],IntType())),
Symbol("float_of_int",MType([IntType()],FloatType())),
Symbol("int_of_string",MType([StringType()],IntType())),
Symbol("string_of_int",MType([IntType()],StringType())),
Symbol("float_of_string",MType([StringType()],FloatType())),
Symbol("string_of_float",MType([FloatType()],StringType())),
Symbol("bool_of_string",MType([StringType()],BoolType())),
Symbol("string_of_bool",MType([BoolType()],StringType())),
Symbol("read",MType([],StringType())),
Symbol("printLn",MType([],VoidType())),
Symbol("printStr",MType([StringType()],VoidType())),
Symbol("printStrLn",MType([StringType()],VoidType()))]

    def check_re_declare(self, env, name): 
        list_decl = env.get_list_decl_current_env()
        list_param = env.get_list_param_current_env()
        for decl in list_decl:
            if decl['name'] == name:
                return True
        for decl in list_param:
            if decl['name'] == name:
                return True
        return False

    def check_un_declare(self, env, name):
        list_decl = env.get_list_decl()
        for decl in list_decl:
            if decl['name'] == name:
                return False
        
        return True

    def check_type_mismatch_in_expression(self, env, lhs, rhs):
        if lhs['type'] != rhs['type']:
            return True
        else:
            return False
   
    def check(self):
        return self.visit(self.ast,self.global_envi)

    def visitProgram(self,ast, c):
        env = Environment()
        env.add_env('program')
        [self.visit(x,env) for x in ast.decl]

    
    def visitVarDecl(self, ast, c):
        id = self.visit(ast.variable, c)
        type_decl = self.visit(ast.varInit, c) if ast.varInit else {
            'type': 'none'
        }

        if self.check_re_declare(c, id['name']):
            raise Redeclared(ast, id['name'])

        c.add_decl({
            'name': id['name'],
            'type': type_decl['type']
        })
        return {
            'name': id['name'],
            'type': type_decl['type']
        }
    
    def visitFuncDecl(self, ast, c):
        id = self.visit(ast.name, c)
        current_env = c.get_current_env()

        if self.check_re_declare(c, id['name']):
            raise Redeclared(ast, id['name'])
        
        c.add_decl({
            'name': id['name'],
            'type': 'Function'
        })

        c.add_env(id['name'])

        param_list = list(map(lambda x: self.visit(x, c), ast.param))
        c.add_param_decl(param_list)

        # visit list decl
        list(map(lambda x: self.visit(x, c), ast.body[0]))

        # visit list statement
        list(map(lambda x: self.visit(x, c), ast.body[1]))

        c.set_current_env(current_env)

    def visitAssign(self, ast, c):
        lhs = self.visit(ast.lhs, c)
        rhs = self.visit(ast.rhs, c)

        type_lhs = lhs['type']
        type_rhs = rhs['type']

        if self.check_un_declare(c, lhs['name']):
            raise Undeclared(ast, lhs['name'])
            
        if (type_lhs == 'none') and (type_rhs == 'none'):
            raise TypeCannotBeInferred(ats)
        elif (type_lhs == 'none') and (type_rhs != 'none'):
            lhs_id['type'] = type_rhs
        elif (type_lhs != 'none') and (type_rhs == 'none'):
            rhs_exp['type'] = type_lhs
        elif (type_lhs != 'none') and (type_rhs != 'none'):
            if type_lhs != type_rhs:
                raise TypeMismatchInStatement(ast)
        

    def visitBinaryOp(self, ast, c):
        pass
    
    def visitUnaryOp(self, ast, c):
        pass

    def visitCallExpr(self, ast, c):
        pass

    def visitIf(self, ast, c):
        pass

    def visitFor(self, ast, c):
        pass

    def visitBreak(self, ast, c):
        pass

    def visitContinue(self, ast, c):
        pass

    def visitReturn(self, ast, c):
        pass

    def visitDowhile(self, ast, c):
        pass

    def visitWhile(self, ast, c):
        pass

    def visitCallStmt(self, ast, c):
        pass

    def visitId(self, ast, c):
        return {
            'name': ast.name,
            'type': c.get_type_decl(ast.name)
        }

    def visitArrayCell(self, ast, c):
        pass
    
    def visitIntLiteral(self, ast, c):
        return {
            'type': 'IntType'
        }

    def visitFloatLiteral(self, ast, c):
        return {
            'type': 'FloatType'
        }

    def visitStringLiteral(self, ast, c):
        pass

    def visitBooleanLiteral(self, ast, c):
        pass

    def visitArrayLiteral(self, ast, c):
        pass





        