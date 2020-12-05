import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):

    def test_0(self):
        """Simple program: main"""
        input = """Var: a,a;"""
        expect = str(Redeclared(VarDecl(Id('a'), [], None), 'a'))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_1(self):
        """Simple program: main"""
        input = """Var: a,b,c,a;"""
        expect = str(Redeclared(VarDecl(Id('a'), [], None), 'a'))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_2(self):
        """Simple program: main"""
        input = """
            Function: main
            Body:
                a = 1;
            EndBody.
        """
        expect = str(Undeclared(Assign(Id('a'), IntLiteral(1)), 'a'))
        self.assertTrue(TestChecker.test(input,expect,402))
    
    def test_3(self):
        """Simple program: main"""
        input = """
            Var: a = 1.1;
            Function: main
            Body:
                Var: a = 1;
                a = 1.1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'), FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,403))
    
    def test_4(self):
        """Simple program: main"""
        input = """
            Var: a = 1.1;
            Function: main
            Parameter: a, a
            Body:
                Var: a = 1;
                a = 1.1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'), FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input,expect,403))

    # def test_2(self):



    # def test_diff_numofparam_stmt(self):
    #     """Complex program"""
    #     input = """Function: main  
    #                Body:
    #                     printStrLn();
    #                 EndBody."""
    #     expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
    #     self.assertTrue(TestChecker.test(input,expect,401))
    
    # def test_diff_numofparam_expr(self):
    #     """More complex program"""
    #     input = """Function: main 
    #                 Body:
    #                     printStrLn(read(4));
    #                 EndBody."""
    #     expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
    #     self.assertTrue(TestChecker.test(input,expect,402))

    # def test_undeclared_function_use_ast(self):
    #     """Simple program: main """
    #     input = Program([FuncDecl(Id("main"),[],([],[
    #         CallExpr(Id("foo"),[])]))])
    #     expect = str(Undeclared(Function(),"foo"))
    #     self.assertTrue(TestChecker.test(input,expect,403))

    # def test_diff_numofparam_expr_use_ast(self):
    #     """More complex program"""
    #     input = Program([
    #             FuncDecl(Id("main"),[],([],[
    #                 CallStmt(Id("printStrLn"),[
    #                     CallExpr(Id("read"),[IntLiteral(4)])
    #                     ])]))])
    #     expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
    #     self.assertTrue(TestChecker.test(input,expect,404))

    # def test_diff_numofparam_stmt_use_ast(self):
    #     """Complex program"""
    #     input = Program([
    #             FuncDecl(Id("main"),[],([],[
    #                 CallStmt(Id("printStrLn"),[])]))])
    #     expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
    #     self.assertTrue(TestChecker.test(input,expect,405))