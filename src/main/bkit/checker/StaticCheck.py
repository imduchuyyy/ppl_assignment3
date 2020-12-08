
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
import copy

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
            'list_decl' : [[]],
            'param_check': False
        }
        self.list_env.append(new_env)

    def add_sub_env(self):
        self.env[self.current_env]['list_decl'] = [[]] + self.env[self.current_env]['list_decl']

    def get_list_env(self):
        return self.list_env
    
    def get_list_decl(self):
        index_current_env = self.list_env.index(self.current_env)
        list_decl = []
        for index_env in range(0, index_current_env + 1):
            env_name = self.list_env[index_env]
            for item in self.env[env_name]['list_decl']:
                list_decl = list_decl + item
        return reversed(list_decl)
    
    def get_list_decl_current_env(self):
        return self.env[self.current_env]['list_decl'][0]
    
    # def set_type_decl(self, name, new_type):
    #     list_decl = self.env[self.current_env]['list_decl'][0]
    #     for decl in list_decl:
    #         if decl['name'] == name:
    #             decl['type'] = new_type

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
        self.env[self.current_env]['list_decl'][0].append(new_decl)
    
    def get_type_decl(self, name_decl):
        list_decl = self.get_list_decl()
        for decl in list_decl:
            if decl['name'] == name_decl:
                return decl['type']
        return 'none'

    def clone_env(self):
        return copy.deepcopy(self)

    def set_return_type(self, return_type):
        self.env[self.current_env]['type'] = return_type
    
    def get_env(self, name):
        return self.env[name]

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

        if 'main' not in env.get_list_env():
            if env.get_type_decl('main') is not 'FunctionType':
                raise NoEntryPoint()

    
    def visitVarDecl(self, ast, c):
        id = self.visit(ast.variable, c)
        type_decl = self.visit(ast.varInit, c) if ast.varInit else {
            'type': 'none'
        }

        name_variable = id['name']

        if self.check_re_declare(c, name_variable):
            if (c.env[c.current_env]['param_check']):
                raise Redeclared(Parameter(), name_variable)
            raise Redeclared(Variable(), name_variable)

        c.add_decl({
            'name': name_variable,
            'type': type_decl['type']
        })
        return {
            'name': name_variable,
            'type': type_decl['type']
        }
    
    def visitFuncDecl(self, ast, c):
        id = self.visit(ast.name, c)
        current_env = c.get_current_env()

        name_function = id['name']

        if self.check_re_declare(c, name_function):
            raise Redeclared(Function(), name_function)
        
        c.add_decl({
            'name': name_function,
            'type': 'none'
        })

        c.add_env(name_function)

        c.env[name_function]['param_check'] = True

        param_list = list(map(lambda x: self.visit(x, c), ast.param))
        c.add_param_decl(param_list)

        c.env[name_function]['param_check'] = False

        # visit list decl
        list(map(lambda x: self.visit(x, c), ast.body[0]))

        # visit list statement
        list(map(lambda x: self.visit(x, c), ast.body[1]))

        c.set_current_env(current_env)

    def visitAssign(self, ast, c):
        lhs_id = self.visit(ast.lhs, c)
        rhs_exp = self.visit(ast.rhs, c)

        if self.check_un_declare(c, lhs_id['name']):
            raise Undeclared(Identifier(), lhs_id['name'])

        type_lhs = lhs_id['type']
        type_rhs = rhs_exp['type']

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
        lhs = self.visit(ast.left, c)
        rhs = self.visit(ast.right, c)
        
        type_lhs = lhs['type']
        type_rhs = rhs['type']

        if 'StringType' in [type_lhs, type_rhs]:
            raise TypeMismatchInExpression(ast)
        elif ast.op in ['+.', '-.', '*.', '\.', '=/=', '<.', '>.', '<=.', '>=.']:
            if type_lhs != 'FloatType' or type_rhs != 'FloatType':
                raise TypeMismatchInExpression(ast)
            else:
                if ast.op in ['+.', '-.', '*.', '\.']:
                    return {
                        'type': 'FloatType'
                    }
                else:
                    return {
                        'type': 'BooleanType'
                    }
        elif ast.op in ['+', '-', '*', '\\', '%', '==', '!=', '<', '>', '<=', '>=']:
            if type_lhs != 'IntType' or type_rhs != 'IntType':
                raise TypeMismatchInExpression(ast)
            else:
                if ast.op in ['+', '-', '*', '\\', '%']:
                    return {
                        'type': 'IntType'
                    }
                else: 
                    return {
                        'type': 'BooleanType'
                    }
        elif ast.op in ['!', '&&', '||']:
            if type_lhs != 'BooleanType' or type_rhs != 'BooleanType':
                raise TypeMismatchInExpression(ast)
            else:
                return {
                    'type': 'BooleanType'
                }
        else:
            raise TypeMismatchInExpression(ast)
    
    def visitUnaryOp(self, ast, c):
        exp = self.visit(ast.body)
        type_exp = exp['type']

        if ast.op == '-':
            if type_exp != 'IntType':
                raise TypeMismatchInExpression(ast)
        elif ast.op == '-.':
            if type_exp != 'FloatType':
                raise TypeMismatchInExpression(ast)
        elif ast.op == '!':
            if type_exp != 'BooleanType':
                raise TypeMismatchInExpression(ast)
        else:
            raise TypeMismatchInExpression(ast)

    def visitCallExpr(self, ast, c):
        method = self.visit(ast.method, c)
        param_send = []

        for param in ast.param:
            param_send.append(self.visit(param, c))

        method_name = method['name']
        
        if self.check_un_declare(c, method_name):
            raise Undeclared(Function(), method_name)

        param_list = c.get_param_decl(method_name)

        if len(param_send) != len(param_list):
            raise TypeMismatchInStatement(ast)

        for index in range(0, len(param_list)):
            if param_send[index]['type'] != param_list[index]['type']:
                raise TypeMismatchInStatement(ast)

        return c.get_env(method_name)

    def visitIf(self, ast, c):
        for item in ast.ifthenStmt:
            expr = self.visit(item[0], c)
            if expr['type'] != 'BooleanType':
                raise TypeMismatchInStatement(ast)
            new_env = c.clone_env()
            new_env.add_sub_env()
            for var_decl in item[1]:
                self.visit(var_decl, new_env)
            for stmt in item[2]:
                self.visit(stmt, new_env)
        new_env_else_stmt = c.clone_env()
        new_env_else_stmt.add_sub_env()
        if ast.elseStmt:
            for var_decl in ast.elseStmt[0]:
                self.visit(var_decl, new_env_else_stmt)
            for stmt in ast.elseStmt[1]:
                self.visit(stmt, new_env_else_stmt)

    def visitFor(self, ast, c):
        index_for = self.visit(ast.idx1, c)
        expr1 = self.visit(ast.expr1, c)
        expr2 = self.visit(ast.expr2, c)
        expr3 = self.visit(ast.expr3, c)

        if index_for['type'] != 'IntType' or expr1['type'] != 'IntType' or expr2['type'] != 'BooleanType' or expr3['type'] != 'IntType':
            raise TypeMismatchInStatement(ast)
        new_env = c.clone_env()
        new_env.add_sub_env()
        for var_decl in ast.loop[0]:
            self.visit(var_decl, new_env)
        for stmt in ast.loop[1]:
            self.visit(stmt, new_env)

    def visitBreak(self, ast, c):
        pass

    def visitContinue(self, ast, c):
        pass

    def visitReturn(self, ast, c):
        return_expr = self.visit(ast.expr, c)
        c.set_return_type(return_expr['type'])

    def visitDowhile(self, ast, c):
        exp = self.visit(ast.exp, c)
        if exp['type'] != 'BooleanType':
            raise TypeMismatchInStatement(ast)
        new_env = c.clone_env()
        new_env.add_sub_env()
        for var_decl in ast.sl[0]:
            self.visit(var_decl, new_env)
        for stmt in ast.sl[1]:
            self.visit(stmt, new_env)
        

    def visitWhile(self, ast, c):
        exp = self.visit(ast.exp, c)
        if exp['type'] != 'BooleanType':
            raise TypeMismatchInStatement(ast)
        new_env = c.clone_env()
        new_env.add_sub_env()
        for var_decl in ast.sl[0]:
            self.visit(var_decl, new_env)
        for stmt in ast.sl[1]:
            self.visit(stmt, new_env)

    def visitCallStmt(self, ast, c):
        method = self.visit(ast.method, c)
        param_send = []

        for param in ast.param:
            param_send.append(self.visit(param, c))

        method_name = method['name']
        
        if self.check_un_declare(c, method_name):
            raise Undeclared(Function(), method_name)

        param_list = c.get_param_decl(method_name)

        if len(param_send) != len(param_list):
            raise TypeMismatchInStatement(ast)

        for index in range(0, len(param_list)):
            if param_send[index]['type'] != param_list[index]['type']:
                raise TypeMismatchInStatement(ast)

        return c.get_env(method_name)

    def visitId(self, ast, c):
        for item in c.get_list_decl():
            if item['name'] == ast.name:
                return item
        return {
            'name': ast.name,
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
        return {
            'type': 'StringType'
        }

    def visitBooleanLiteral(self, ast, c):
        return {
            'type': 'BooleanType'
        }

    def visitArrayLiteral(self, ast, c):
        array_type = 'none'
        for item in ast.value:
            value = self.visit(item, c)
            if array_type == 'none':
                array_type = value['type']
                continue
            if array_type != value['type']:
                raise TypeMismatchInExpression(ast)
        return
        return 





        