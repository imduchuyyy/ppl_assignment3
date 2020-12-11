import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):
    def test_0(self):
        """Simple program: main"""
        input = """Var: a,a;"""
        expect = str(Redeclared(Variable(), 'a'))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_1(self):
        """Simple program: main"""
        input = """Var: a,b,c,a;"""
        expect = str(Redeclared(Variable(), 'a'))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_2(self):
        """Simple program: main"""
        input = """
            Function: main
            Body:
                a = 1;
            EndBody.
        """
        expect = str(Undeclared(Identifier(), 'a'))
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
                a = 1.1;
            EndBody.
        """
        expect = str(Redeclared(Parameter(), 'a'))
        self.assertTrue(TestChecker.test(input,expect,404))
    
    def test_5(self):
        """Simple program: main"""
        input = """
            Var: a = 1.1;
            Function: main
            Parameter: a
            Body:
                a = 1;
            EndBody.
            Function: main
            Parameter: a
            Body:
                a = 1;
            EndBody.
        """
        expect = str(Redeclared(Function(), 'main'))
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_6(self):
        """Simple program: main"""
        input = """
            Var: a = 1.1;
            Function: notmain
            Parameter: a
            Body:
                a = 1;
            EndBody.
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_7(self):
        """Simple program: main"""
        input = """
            Var: a = 1.1;
            Function: main
            Parameter: c
            Body:
                Var: b = 1;
                c = a + b;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+', Id('a'), Id('b'))))
        self.assertTrue(TestChecker.test(input,expect,407))
    
    def test_8(self):
        """Simple program: main"""
        input = """
            Var: a = True, c = 1;
            Function: main
            Parameter: c
            Body:
                Var: b = False;
                c = a || b;
                If (c) Then 
                    Var: x;
                    x = 1;
                EndIf.
                x = 1;
            EndBody.
        """
        expect = str(Undeclared(Identifier(), 'x'))
        self.assertTrue(TestChecker.test(input,expect,408))
    
    def test_9(self):
        """Simple program: main"""
        input = """
            Var: a = 1, c = 1;
            Function: main
            Parameter: c
            Body:
                Var: b = 2;
                c = a + b;
                If (c) Then 
                    x = 1;
                EndIf.
                x = 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(Id('c'),[], [Assign(Id('x'), IntLiteral(1))])], ())))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_10(self):
        """Simple program: main"""
        input = """
            Var: a = 1, c = 1;
            Function: main
            Parameter: c = 1
            Body:
                c = 1;
                Return c;
            EndBody.
            Function: main2
            Parameter: c
            Body:
                c = 1.2;
                c = main(1);
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('c'), CallExpr(Id('main'), [IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,410))
    
    def test_11(self):
        """Simple program: main"""
        input = """
            Var: a = 1, c = 1;
            Function: main
            Parameter: c
            Body:
                c = 1;
                Return c;
            EndBody.
            Function: main2
            Parameter: c
            Body:
                c = 1.2;
                c = main(c);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id('main'), [Id('c')])))
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_12(self):
        """Simple program: main"""
        input = """
            Var: a = 1, c = 1;
            Function: main
            Parameter: c = True
            Body:
                Var:x = 0;
                If (c) Then 
                    x = 1;
                Else
                    x = 1.2;
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('x'), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,412))
    
    def test_13(self):
        """Simple program: main"""
        input = """
            Var: a = 1, x = 1;
            Function: main
            Body:
                x = 1.2;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('x'), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,413))
    
    def test_14(self):
        """Simple program: main"""
        input = """
            Var: a = 1, x = 1;
            Function: main
            Parameter: x
            Body:
                If (x) Then 
                    Var: a = 1;
                EndIf.
                x = 1.2;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id('x'), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,414))
    
    def test_15(self):
        """Simple program: main"""
        input = """
            Function: main
            Parameter: a,b
            Body:
                Var:y;
                Do
                    While main(0,1.5)==y Do
                    EndWhile.
                While True
                EndDo.
                y=main(0,1);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id('main'), [IntLiteral(0), IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_16(self):
        """Simple program: main"""
        input = """
            Var:a;
            Function: main
            Parameter: a
            Body:
                Var: a;
                If True Then
                    Var: a;
                    a = 1;
                EndIf.
            EndBody.
        """
        expect = str(Redeclared(Variable(), 'a'))
        self.assertTrue(TestChecker.test(input,expect,416))
    
    def test_17(self):
        """Simple program: main"""
        input = """
            Function: main
            Parameter: a
            Body:
                a = 1;
            EndBody.
            Function: foo
            Body:
                a = 2;
            EndBody.
        """
        expect = str(Undeclared(Identifier(), 'a'))
        self.assertTrue(TestChecker.test(input,expect,417))
    
    def test_18(self):
        input = """ Function: main
                    Parameter: a
                    Body:
                        Var:x;
                        main(123);
                        x = main(1);
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("main"),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_19(self):
        input = """ Function: main
                    Parameter: a
                    Body:
                        Var:x;
                        x = 1;
                        main(2);
                        x = main(1);
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("main"),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test_diff_numofparam_stmt(self):
        """Complex program"""
        input = """Function: main  
                   Body:
                        printStrLn();
                    EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,420))
    
    def test_diff_numofparam_expr(self):
        """More complex program"""
        input = """Function: main 
                    Body:
                        printStrLn(read(4));
                    EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_undeclared_function_use_ast(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"),[],([],[
            CallExpr(Id("foo"),[])]))])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[
                        CallExpr(Id("read"),[IntLiteral(4)])
                        ])]))])
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_diff_numofparam_stmt_use_ast(self):
        """Complex program"""
        input = Program([
                FuncDecl(Id("main"),[],([],[
                    CallStmt(Id("printStrLn"),[])]))])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_25(self):
        input = """ Function: main
                    Parameter: a
                    Body:
                        While(b <= 3)Do
                            b = 1;
                        EndWhile.
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("main"),[IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,425))