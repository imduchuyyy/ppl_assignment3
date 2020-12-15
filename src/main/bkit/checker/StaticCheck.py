
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
        self.list_function_decl = []
    
    def add_env(self, new_env):
        self.current_env = new_env
        self.env[new_env] = {
            'list_decl' : [[]],
            'param_check': False,
            'type': Unknown(),
            'list_param': []
        }
        self.list_env.append(new_env)

    def add_sub_env(self):
        self.env[self.current_env]['list_decl'] = [[]] + self.env[self.current_env]['list_decl']
    
    def delete_sub_env(self):
        self.env[self.current_env]['list_decl'] = self.env[self.current_env]['list_decl'][1:]

    def get_list_env(self):
        return self.list_env
    
    def get_list_decl(self, nameEnv):
        list_decl_global = self.env['program']['list_decl']
        list_param_current_env = self.get_param_decl(nameEnv)
        list_decl_current_env = self.env[nameEnv]['list_decl']
        list_decl = []
        for item in list_decl_current_env:
            list_decl = list_decl + item
        list_decl = list_decl + list_param_current_env
        for item in list_decl_global:
            list_decl = list_decl + item
        
        return list_decl
    
    def get_list_decl_current_env(self):
        return self.env[self.current_env]['list_decl'][0] 
    
    # def set_type_decl(self, name, new_type):
    #     list_decl = self.env[self.current_env]['list_decl'][0]
    #     for decl in list_decl:
    #         if decl['name'] == name:
    #             decl['type'] = new_type

    def add_param_decl(self, name, param):
        self.env[name]['list_param'].append(param)

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
        list_decl = self.get_list_decl(self.current_env)
        for decl in list_decl:
            if decl['name'] == name_decl:
                return decl['type']
        return Unknown()

    def set_return_type(self, name,return_type):
        self.env[name]['type'] = return_type
    
    def get_env(self, name):
        return self.env[name]

    def add_function_decl(self, name):
        self.list_function_decl.append(name)
    
    def get_list_function_decl(self):
        return self.list_function_decl

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
        
        if len(env.env[env.current_env]['list_decl']) == 1:
            for decl in list_param:
                if decl['name'] == name:
                    return True
        
        return False

    def check_un_declare(self, env, nameEnv, name):
        list_decl = env.get_list_decl(nameEnv)
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

        for x in ast.decl:
            if type(x) is VarDecl:
                self.visit(x, env)

        for item in ast.decl:
            if type(item) is FuncDecl:
                nameFunc = item.name.name
                if self.check_re_declare(env, nameFunc):
                    raise Redeclared(Function(), nameFunc)
                env.add_decl({
                    'name': nameFunc,
                    'dimen': [],
                    'type': Unknown()
                })
                env.add_env(nameFunc)
                env.add_function_decl(nameFunc)
                for param in item.param:
                    nameParam = param.variable.name
                    if len(list(filter(lambda x: x['name'] == nameParam, env.get_param_decl(nameFunc)))) > 0:
                        raise Redeclared(Parameter(), nameParam)
                    new_param = {
                                "name": nameParam,
                                'dimen': param.varDimen,
                                "type": Unknown()
                            }
                    env.add_param_decl(nameFunc, new_param)
                env.current_env = 'program'

        for x in ast.decl:
            if type(x) is FuncDecl:
                self.visit(x, env)

        if 'main' not in env.get_list_env():
            if env.get_type_decl('main') is not 'FunctionType':
                raise NoEntryPoint()

    
    def visitVarDecl(self, ast, c):
        id = self.visit(ast.variable, c)
        type_decl = self.visit(ast.varInit, c) if ast.varInit else {
            'type': Unknown()
        }

        name_variable = id['name']

        if self.check_re_declare(c, name_variable):
            if (c.env[c.current_env]['param_check']):
                raise Redeclared(Parameter(), name_variable)
            raise Redeclared(Variable(), name_variable)
        
        c.add_decl({
            'name': name_variable,
            'dimen': ast.varDimen,
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

        #if self.check_re_declare(c, name_function):
        #    raise Redeclared(Function(), name_function)
        
        c.current_env = name_function

        # visit list decl
        list(map(lambda x: self.visit(x, c), ast.body[0]))

        # visit list statement
        list(map(lambda x: self.visit(x, c), ast.body[1]))

        c.set_current_env(current_env)

    def visitAssign(self, ast, c):
        lhs_id = self.visit(ast.lhs, c)
        rhs_exp = self.visit(ast.rhs, c)

        if type(ast.lhs) is Id:
            if self.check_un_declare(c, c.current_env, lhs_id['name']):
                raise Undeclared(Identifier(), lhs_id['name'])

        if type(ast.rhs) is Id:
            if self.check_un_declare(c, c.current_env, rhs_exp['name']):
                raise Undeclared(Identifier(), rhs_exp['name'])
            
        type_lhs = type(lhs_id['type'])
        type_rhs = type(rhs_exp['type'])

        if type_rhs is VoidType:
            raise TypeMismatchInStatement(ast)
        

        if (type_lhs is Unknown) and (type_rhs is Unknown):
            raise TypeCannotBeInferred(ast)
        elif (type_lhs is Unknown) and (type_rhs is not Unknown):
            lhs_id['type'] = rhs_exp['type']
        elif (type_lhs is not Unknown) and (type_rhs is Unknown):
            rhs_exp['type'] = lhs_id['type']
        elif (type_lhs is not Unknown) and (type_rhs is not Unknown):
            if type_lhs is not type_rhs:
                raise TypeMismatchInStatement(ast)

    def visitBinaryOp(self, ast, c):
        lhs = self.visit(ast.left, c)
        rhs = self.visit(ast.right, c)

        if type(ast.right) is Id:
            if self.check_un_declare(c, c.current_env, rhs["name"]):
                raise Undeclared(Identifier(), rhs['name'])
        
        if type(ast.left) is Id:
            if self.check_un_declare(c, c.current_env,lhs["name"]):
                raise Undeclared(Identifier(), lhs['name'])

        type_lhs = type(lhs['type'])
        type_rhs = type(rhs['type'])


        if StringType in [type_lhs, type_rhs] or VoidType in [type_lhs, type_rhs]:
            raise TypeMismatchInExpression(ast)
        elif ast.op in ['+.', '-.', '*.', '\.', '=/=', '<.', '>.', '<=.', '>=.']:
            if type_lhs is Unknown: 
                lhs['type'] = FloatType()
                type_lhs = FloatType
            if type_rhs is Unknown:
                rhs['type'] = FloatType()
                type_rhs = FloatType
            if type_lhs is not FloatType or type_rhs is not FloatType:
                raise TypeMismatchInExpression(ast)
            else:
                if ast.op in ['+.', '-.', '*.', '\.']:
                    return {
                        'type': FloatType()
                    }
                else:
                    return {
                        'type': BoolType()
                    }
        elif ast.op in ['+', '-', '*', '\\', '%', '==', '!=', '<', '>', '<=', '>=']:
            if type_lhs is Unknown: 
                lhs['type'] = IntType()
                type_lhs = IntType
            if type_rhs is Unknown:
                rhs['type'] = IntType()
                type_rhs = IntType
            
            if type_lhs is not IntType or type_rhs is not IntType:
                raise TypeMismatchInExpression(ast)
            else:
                if ast.op in ['+', '-', '*', '\\', '%']:
                    return {
                        'type': IntType()
                    }
                else: 
                    return {
                        'type': BoolType()
                    }
        elif ast.op in ['!', '&&', '||']:
            if type_lhs is Unknown: 
                lhs['type'] = BoolType()
                type_lhs = BoolType
            if type_rhs is Unknown:
                rhs['type'] = BoolType()
                type_rhs = BoolType

            if type_lhs is not BoolType or type_rhs is not BoolType:
                raise TypeMismatchInExpression(ast)
            else:
                return {
                    'type': BoolType()
                }
        else:
            raise TypeMismatchInExpression(ast)
    
    def visitUnaryOp(self, ast, c):
        exp = self.visit(ast.body, c)

        if type(ast.body) is Id:
            if self.check_un_declare(c, c.current_env, exp["name"]):
                raise Undeclared(Identifier(), exp['name'])

        try:
            type_exp = type(exp['type'])
        except: 
            type_exp = Unknown

        if ast.op == '-':
            if type_exp is not IntType:
                raise TypeMismatchInExpression(ast)
        elif ast.op == '-.':
            if type_exp is not FloatType:
                raise TypeMismatchInExpression(ast)
        elif ast.op == '!':
            if type_exp is not BoolType:
                raise TypeMismatchInExpression(ast)
        else:
            raise TypeMismatchInExpression(ast)

        return exp

    def visitCallExpr(self, ast, c):
        method = self.visit(ast.method, c)
        param_send = []

        for item in ast.param:
            param = self.visit(item, c)
            if type(item) is Id:
                if self.check_un_declare(c, c.current_env, param['name']):
                    raise Undeclared(Identifier(), param['name']) 
            param_send.append(param)


        method_name = method['name']

        for item in self.global_envi:
            if item.name == method_name:
                if len(param_send) != len(item.mtype.intype):
                    raise TypeMismatchInExpression(ast)
                
                for index in range(0, len(item.mtype.intype)):
                    param_send_index_type = type(param_send[index]['type'])
                    param_index_type = type(item.mtype.intype[index])
                    if param_send_index_type is Unknown:
                        param_send[index]['type'] = item.mtype.intype[index]
                        continue
                    if param_send_index_type is not param_index_type:
                        raise TypeMismatchInExpression(ast)
                return {
                    'name': method_name,
                    'type': item.mtype.restype
                }
        
        if method_name not in c.get_list_function_decl():
            raise Undeclared(Function(), method_name)

        param_list = c.get_param_decl(method_name)

        if len(param_send) != len(param_list):
            raise TypeMismatchInExpression(ast)

        for index in range(0, len(param_list)):
            param_type = type(param_list[index]['type'])
            param_send_type = type(param_send[index]['type'])
            if param_type is Unknown and param_send_type is Unknown:
                raise TypeCannotBeInferred(ast)
            elif param_type is Unknown and param_send_type is not Unknown:
                param_list[index]['type'] = param_send[index]['type']
            elif param_type is not Unknown and param_send_type is Unknown:
                param_send[index]['type'] = param_list[index]['type']
            elif param_send_type is not param_type:
                raise TypeMismatchInExpression(ast)

        return c.get_env(method_name)

    def visitIf(self, ast, c):
        for item in ast.ifthenStmt:
            expr = self.visit(item[0], c)

            if type(item[0]) is Id:
                if self.check_un_declare(c, c.current_env, expr['name']):
                    raise Undeclared(Identifier(), expr['name'])

            type_expr = type(expr['type'])

            if type_expr is Unknown:
                expr['type'] = BoolType()
                type_expr = BoolType

            if type_expr is not BoolType:
                raise TypeMismatchInStatement(ast)
            c.add_sub_env()
            for var_decl in item[1]:
                self.visit(var_decl, c)
            for stmt in item[2]:
                self.visit(stmt, c)
            c.delete_sub_env()
        c.add_sub_env()
        if ast.elseStmt:
            for var_decl in ast.elseStmt[0]:
                self.visit(var_decl, c)
            for stmt in ast.elseStmt[1]:
                self.visit(stmt, c)
        c.delete_sub_env()

    def visitFor(self, ast, c):
        index_for = self.visit(ast.idx1, c)
        expr1 = self.visit(ast.expr1, c)
        expr2 = self.visit(ast.expr2, c)
        expr3 = self.visit(ast.expr3, c)

        if type(ast.idx1) is Id:
            if self.check_un_declare(c,  c.current_env,index_for['name']):
                raise Undeclared(Identifier(), index_for['name'])
        
        if type(ast.expr1) is Id:
                if self.check_un_declare(c,  c.current_env,expr1['name']):
                    raise Undeclared(Identifier(), expr1['name'])

        if type(ast.expr2) is Id:
            if self.check_un_declare(c,  c.current_env,expr2['name']):
                raise Undeclared(Identifier(), expr2['name'])
        if type(ast.expr3) is Id:
                if self.check_un_declare(c,  c.current_env,expr3['name']):
                    raise Undeclared(Identifier(), expr3['name'])

        index_for_type = type(index_for['type'])
        expr1_type = type(expr1['type'])
        expr2_type = type(expr2['type'])
        expr3_type = type(expr3['type'])

        if index_for_type is Unknown:
            index_for['type'] = IntType()
        
        if expr1_type is Unknown:
            expr1['type'] = IntType()
        
        if expr2_type is Unknown:
            expr2['type'] = BoolType()
        
        if expr3_type is Unknown:
            expr3['type'] = IntType()

        if index_for_type is not IntType or expr1_type is not IntType or expr2_type is not BoolType or expr3_type is not IntType:
            raise TypeMismatchInStatement(ast)
        c.add_sub_env()
        for var_decl in ast.loop[0]:
            self.visit(var_decl, c)
        for stmt in ast.loop[1]:
            self.visit(stmt, c)
        c.delete_sub_env()

    def visitBreak(self, ast, c):
        pass

    def visitContinue(self, ast, c):
        pass

    def visitReturn(self, ast, c):
        current_env = c.get_env(c.current_env)
        return_expr = {
            'type': VoidType()
        }

        current_env_type = type(current_env['type'])
        
        if ast.expr:
            return_expr = self.visit(ast.expr, c)

        return_expr_type = type(return_expr['type'])

        if current_env_type is Unknown and return_expr_type is not Unknown:
            c.set_return_type(c.current_env, return_expr['type'])
        elif current_env_type is not Unknown and return_expr_type is Unknown:
            return_expr['type'] = current_env['type']
        elif current_env_type != return_expr_type:
            raise TypeMismatchInStatement(ast)
        

    def visitDowhile(self, ast, c):
        exp = self.visit(ast.exp, c)

        if type(ast.exp) is Id:
            if self.check_un_declare(c,  c.current_env,exp['name']):
                raise Undeclared(Identifier(), exp['name'])


        exp_type = type(exp['type'])

        if exp_type is Unknown:
            exp['type'] = BoolType()

        if exp_type is not BoolType:
            raise TypeMismatchInStatement(ast)
        c.add_sub_env()
        for var_decl in ast.sl[0]:
            self.visit(var_decl, c)
        for stmt in ast.sl[1]:
            self.visit(stmt, c)
        c.delete_sub_env()
        

    def visitWhile(self, ast, c):
        exp = self.visit(ast.exp, c)

        if type(ast.exp) is Id:
            if self.check_un_declare(c, c.current_env, exp['name']):
                raise Undeclared(Identifier(), exp['name'])


        exp_type = type(exp['type'])
        
        if exp_type is Unknown:
            exp['type'] = BoolType()
            exp_type = BoolType


        if exp_type is not BoolType:
            raise TypeMismatchInStatement(ast)
        c.add_sub_env()
        for var_decl in ast.sl[0]:
            self.visit(var_decl, c)
        for stmt in ast.sl[1]:
            self.visit(stmt, c)
        c.delete_sub_env()

    def visitCallStmt(self, ast, c):
        method = self.visit(ast.method, c)
        param_send = []

        for item in ast.param:
            param = self.visit(item, c)
            if type(item) is Id:
                if self.check_un_declare(c, c.current_env, param['name']):
                    raise Undeclared(Identifier(), param['name']) 
            param_send.append(param)

        method_name = method['name']

        for item in self.global_envi:
            if item.name == method_name:
                if len(param_send) != len(item.mtype.intype):
                    raise TypeMismatchInStatement(ast)
                
                for index in range(0, len(item.mtype.intype)):
                    param_send_index_type = type(param_send[index]['type'])
                    param_index_type = type(item.mtype.intype[index])
                    if param_send_index_type is Unknown:
                        param_send[index]['type'] = item.mtype.intype[index]
                        continue
                    if param_send_index_type is not param_index_type:
                        raise TypeMismatchInStatement(ast)
                return {
                    'name': method_name,
                    'type': item.mtype.restype
                }
        
        if method_name not in c.get_list_function_decl():
            raise Undeclared(Function(), method_name)

        param_list = c.get_param_decl(method_name)

        if len(param_send) != len(param_list):
            raise TypeMismatchInStatement(ast)

        for index in range(0, len(param_list)):
            param_type = type(param_list[index]['type'])
            param_send_type = type(param_send[index]['type'])
            if param_type is Unknown:
                if param_send_type is Unknown:
                    raise TypeCannotBeInferred(ast)
                else:
                    param_list[index]['type'] = param_send[index]['type']
                    continue
            if param_send_type is not param_type:
                raise TypeMismatchInStatement(ast)
        
        c.set_return_type(method_name, VoidType())
        return method

    def visitId(self, ast, c):
        for item in c.get_list_decl(c.current_env):
            if item['name'] == ast.name:
                return item
        return {
            'name': ast.name,
        }

    def visitArrayCell(self, ast, c):
        arr = self.visit(ast.arr, c)
        for item in ast.idx:
            index = self.visit(item, c)
            if type(index['type']) is not IntType:
                raise TypeMismatchInExpression(ast)
        return arr
    
    def visitIntLiteral(self, ast, c):
        return {
            'type': IntType()
        }

    def visitFloatLiteral(self, ast, c):
        return {
            'type': FloatType()
        }

    def visitStringLiteral(self, ast, c):
        return {
            'type': StringType()
        }

    def visitBooleanLiteral(self, ast, c):
        return {
            'type': BoolType()
        }

    def visitArrayLiteral(self, ast, c):
        array_type = Unknown()
        type_item  = Unknown
        for item in ast.value:
            value = self.visit(item, c)
            if type_item is Unknown:
                type_item = type(value['type'])
            elif type_item is not type(value['type']):
                raise InvalidArrayLiteral(ast)
        return {
            'type':type_item
        }