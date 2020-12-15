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
        input = """ 
                    Var: a, x = 1;
                    Function: main
                    Body:
                        While(a <= 3)Do
                            a = 1;
                            main();
                            x = main();
                        EndWhile.
                    EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("main"),[]))))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test_26(self):
        input = """ 
            Function: main
            Parameter: a
                    Body:
                        While(b <= 3)Do
                            b = 1;
                        EndWhile.
                    EndBody."""
        expect = str(Undeclared(Identifier(), "b"))
        self.assertTrue(TestChecker.test(input,expect,426))
    
    def test_27(self):
        input = """ 
            Function: main
            Parameter: a
                    Body:
                        While(a <= 3)Do
                            a = -b;
                        EndWhile.
                    EndBody."""
        expect = str(Undeclared(Identifier(), "b"))
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_28(self):
        input = """ 
            Function: main
            Parameter: a
                    Body:
                        If(b) Then a =1;
                        EndIf.
                    EndBody."""
        expect = str(Undeclared(Identifier(), "b"))
        self.assertTrue(TestChecker.test(input,expect,428))

    def test_29(self):
        input = """ 
            Function: main
            Parameter: a
                    Body:
                        If(b) Then a =1;
                        EndIf.
                    EndBody."""
        expect = str(Undeclared(Identifier(), "b"))
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_30(self):
        input = """ 
            Function: main
            Parameter: a
                    Body:
                        For(a = 1, a < 1, a = b +1)
                        Do a = a + 1; 
                        EndFor.
                    EndBody."""
        expect = str(Undeclared(Identifier(), "b"))
        self.assertTrue(TestChecker.test(input,expect,430))
    
    def test_31(self):
        input = """ 
            Function: main
            Parameter: a
            Body:
                For(a = 1, a < 1, a = a +1) Do
                    Var: a;
                    a = True;
                    main(1);
                    If(a) Then
                        Var: a;
                        a = 1.2;
                        main(a);
                    EndIf.
                EndFor.
            EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("main"), [Id('a')])))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test_32(self):
        input = """ 
            Function: main
            Parameter: a
            Body:
                Var: x;
                x = True;
                For(a = 1, a < 1, a = a +1) Do
                    Var: a;
                    a = True;
                    main(1);
                    If(a) Then
                        Var: a;
                        x = 1.2;
                        a = 1.2;
                        main(a);
                    EndIf.
                EndFor.
            EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_33(self):
        input = """ 
            Function: main
            Parameter: a
            Body:
                Var: x;
                x = True;
                For(a = 1, a < 1, a = a +1) Do
                    Var: a;
                    a = True;
                    main(1);
                    If(a) Then
                        Var: a;
                        x = 1.2;
                        a = 1.2;
                        main(a);
                    EndIf.
                EndFor.
            EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_34(self):
        input = """ 
            Function: main
            Parameter: a
            Body:
                Var: x;
                x = True;
                While(a) Do    
                    If(a) Then
                        Var: a;
                        x = 1.2;
                        a = 1.2;
                        main(a);
                    EndIf.
                EndWhile.
            EndBody."""
        expect = str(TypeMismatchInStatement(Assign(Id('x'), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_35(self):
        input = """ 
            Function: main
            Parameter: a
            Body:
                Var: x;
                x = True;
                While(x || a || False) Do    
                    If(a) Then
                        x = x + 1;
                    EndIf.
                EndWhile.
            EndBody."""
        expect = str(TypeMismatchInExpression(BinaryOp("+", Id("x"), IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,435))

    def test_36(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x;
                While(x || a || False) Do    
                    If(a) Then
                        x = False;
                    EndIf.
                EndWhile.
            EndBody.
            Function: foo
            Body:
                a = False;
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), BooleanLiteral(False))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_37(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x;
                While(x || a || False) Do    
                    If(a) Then
                        x = False;
                    EndIf.
                EndWhile.
            EndBody.
            Function: foo
            Body:
                main(False);
                a = 2;
                a = main(False);
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("main"), [BooleanLiteral(False)]))))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_38(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True;
                x  = main(True);
                While(x) Do
                    If(a) Then
                        x = False;
                    EndIf.
                EndWhile.
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var:a;
                a = False;
                a = main(1);
            EndBody.
            """
        expect = str(TypeMismatchInExpression(CallExpr(Id('main'), [IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_39(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True;
                x  = main(True);
                While(x) Do
                    If(a) Then
                        x = False;
                    EndIf.
                EndWhile.
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var:a;
                a = 1;
                a = main(False);
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("main"), [BooleanLiteral(False)]))))
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_40(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True;
                x  = foo(True);
                While(x) Do
                    If(a) Then
                        x = False;
                    EndIf.
                EndWhile.
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var:a;
                a = 1;
                x = a;
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id("x"), Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_41(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                z  = foo(True) + goo(x);
                While(x) Do
                    If(a) Then
                        x = False;
                    EndIf.
                EndWhile.
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var:a;
                a = "string";
                a = goo(True);
            EndBody.
            Function: goo
            Parameter: x
            Body:
                Var:a;
            EndBody.
            """
        expect = str(TypeMismatchInStatement(Assign(Id('a'), CallExpr(Id("goo"), [BooleanLiteral(True)]))))
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_42(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                z  = foo(True) + goo(x);
                While(x) Do
                    If(a) Then
                            x = False;
                        EndIf.
                    EndWhile.
                EndBody.
                Function: foo
                Parameter: x
                Body:
                    Var:a;
                    a = 1;
                    a = goo(True);
                EndBody.
                Function: goo
                Parameter: x
                Body:
                    Var:a = 1;
                    a = main(x);
                    nomatch(x);
                EndBody.
                """
        expect = str(Undeclared(Function(), "nomatch"))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test_43(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                z  = foo(True) + goo(x);
                While(x) Do
                    If(a) Then
                            x = False;
                        EndIf.
                    EndWhile.
                EndBody.
                Function: foo
                Parameter: x
                Body:
                    Var:a;
                    a = 1;
                    a = goo(True);
                EndBody.
                Function: goo
                Parameter: x
                Body:
                    Var:a = 1;
                    a = main(x);
                    a = a + 110 * 1.2;
                EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("*", IntLiteral(110), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,443))
    
    def test_44(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                z  = foo(True) + goo(x);
                While(x) Do
                    If(a) Then
                            x = False;
                        EndIf.
                EndWhile.
                EndBody.
                Function: foo
                Parameter: x
                Body:
                    Var:a;
                    a = 1;
                    a = goo(True);
                EndBody.
                Function: goo
                Parameter: x
                Body:
                    Var:a = 1;
                    a = main(x);
                    Return x;
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_45(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a, b, c, d
            Body:
                Var: x = True, z;
                z  = foo(True) + goo(x);
                While(x) Do
                    If(a) Then
                            x = False;
                        EndIf.
                EndWhile.
                EndBody.
                Function: foo
                Parameter: x
                Body:
                    Var:a;
                    a = 1;
                    main(True, 1, 1.2, "string");
                    a = goo(True);
                EndBody.
                Function: goo
                Parameter: x
                Body:
                    Var:a = 1;
                    Var: notstring = 1.2;
                    a = main(x, 2, 3.1, notstring);
                EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id("main"), [Id("x"), IntLiteral(2), FloatLiteral(3.1), Id("notstring")])))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_46(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a, b, c, d
            Body:
                Var: x = True, z;
                z  = foo(True) + goo("string");
                While(x) Do
                    If(a) Then
                            x = False;
                        EndIf.
                EndWhile.
                EndBody.
                Function: foo
                Parameter: x
                Body:
                    Var:a;
                    a = 1;
                    a = main(True, 1, 1.2, "string");
                    a = goo("this is string");
                EndBody.
                Function: goo
                Parameter: x
                Body:
                    Var:a = 1;
                    Var: notstring = 1.2;
                    goo(notstring);
                    x = "string";
                EndBody.
                """
        expect = str(TypeMismatchInStatement(CallStmt(Id('goo'), [Id("notstring")])))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_47(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    If(a) Then
                        x = False;
                        main(1);    
                    EndIf.
                EndWhile.
            EndBody.
                """
        expect = str(TypeMismatchInStatement(CallStmt(Id('main'), [IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_48(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    If(a) Then
                        x = False;
                        x = main(x);
                    EndIf.
                EndWhile.
                z = 1;
                Return z;
            EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_49(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    x = main(a);
                EndWhile.
                Return z;
            EndBody.
                """
        expect = str(TypeCannotBeInferred(CallExpr(Id("main"), [Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_50(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    a = z;
                EndWhile.
                Return z;
            EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id("a"), Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_51(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    a = 1;
                    a = main(a);
                EndWhile.
                z = "string";
                Return z;
            EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_52(self):
        input = """
        Function: main
        Body:
            Var: x;
            test(x);
        EndBody.
        Function: test
        Parameter: x
        Body:
        EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id('test'),[Id('x')])))
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_53(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: x[1];
            x[0] = 1;
            x[1] = 1.2;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x"), [IntLiteral(1)]), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_54(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: x[1];
            x = { 1 , 2};
            x[0] = "string";
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x"), [IntLiteral(0)]), StringLiteral("string"))))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test_55(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: x[1];
            x[0] = a;
        EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(ArrayCell(Id('x'), [IntLiteral(0)]), Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_56(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: x[1];
            x[0] = "string";
            x = {1};
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"), ArrayLiteral([IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_self_call_array(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: x = 1;
            x = main(1)[0];
            x = {1};
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"), ArrayLiteral([IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,457))
    
    def test_func_call_array(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Return { 1, 2 ,3 };
        EndBody.
        Function: foo
        Parameter: a
        Body:
            Var: x[3] = { 2.1 };
            x[3] = "string";
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(ArrayCell(Id("x"), [IntLiteral(3)]), StringLiteral("string"))))
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_return_two_time(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Return { 1, 2 ,3 };
        EndBody.
        Function: foo
        Parameter: a
        Body:
            If (a) Then
                Return 1;
            EndIf.
            Return a;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_self_return(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Return;
        EndBody.
        Function: foo
        Parameter: a
        Body:
            a = main(123);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("main"), [IntLiteral(123)]))))
        self.assertTrue(TestChecker.test(input,expect,460))
    
    def test_call_function_with_wrong_param(self):
        input = """
        Function: main
        Parameter: a
        Body:
            foo(a);
        EndBody.
        Function: foo
        Parameter: a
        Body:
            a = main(123);
        EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id('foo'), [Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,461))
    
    def test_wrong_return(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: b = 1;
            b = main(b);
            Return 2.1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(2.1))))
        self.assertTrue(TestChecker.test(input,expect,462))
    
    def test_wrong_call(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: b = 1;
            Do
                While bool_of_string("True") Do
                    b = float_of_int(b);
                EndWhile.
            While True
            EndDo.
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("b"), CallExpr(Id("float_of_int"), [Id("b")]))))
        self.assertTrue(TestChecker.test(input,expect,463))
    
    def test_wrong_param(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Var: b = 1;
            Do
                While bool_of_string("True") Do
                    b = float_of_int("string");
                EndWhile.
            While True
            EndDo.
        EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("float_of_int"), [StringLiteral("string")])))
        self.assertTrue(TestChecker.test(input,expect,464))
    
    def test_return_fun(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Do
                While bool_of_string("True") Do
                    Return bool_of_string("False");
                EndWhile.
            While True
            EndDo.
        EndBody.
        Function: foo
        Parameter: a
        Body:
            a = main(1);
            a = 1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,465))
    
    def test_call_func_with_param(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Do
                While bool_of_string("True") Do
                    Return bool_of_string("False");
                EndWhile.
            While True
            EndDo.
        EndBody.
        Function: foo
        Parameter: a
        Body:
            a = main(1);
            printLn(a);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("printLn"), [Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,466))
    
    def test_wrong_assign(self):
        input = """
        Function: main
        Parameter: a
        Body:
            Do
                While bool_of_string("True") Do
                    a = float_of_string("12.3") +. float_of_int(123);
                    Return a;
                EndWhile.
            While True
            EndDo.
            a = 1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,467))
    
    def test_wrong_parse_type(self):
        input = """
        Function: main
        Parameter: a
        Body:
            a = int_of_float(1.2);
            a = float_of_int(1);
            a = 1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("float_of_int"), [IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test_fun_call(self):
        input = """
        Function: fun
        Parameter: a, b
        Body:
            Return int_of_float(a) + int_of_string(b);
        EndBody.
        Function: main
        Parameter: a
        Body:
            a = "string";
            a = fun(1.0, "1");
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("fun"), [FloatLiteral(1.0), StringLiteral("1")]))))
        self.assertTrue(TestChecker.test(input,expect,469))
    
    def test_complex_binaryOp(self):
        input = """
        Function: fun
        Parameter: a, b
        Body:
            Return int_of_float(1.0 +. 23.4  \. a -. 14.5 *. 124.3) + int_of_string("still string");
        EndBody.
        Function: main
        Parameter: a
        Body:
            a = "string";
            a = fun(1.0, "1");
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("fun"), [FloatLiteral(1.0), StringLiteral("1")]))))
        self.assertTrue(TestChecker.test(input,expect,470))
    
    def test_div(self):
        input = """
        Function: fun
        Parameter: a, b
        Body:
            Return int_of_float(1.0 +. 23.4  \. a -. 14.5 *. 124.3) + int_of_string("still string");
        EndBody.
        Function: main
        Parameter: a
        Body:
            a = "string";
            a = fun(float_of_int(4 % 1), "1");
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), CallExpr(Id("fun"), [CallExpr(Id("float_of_int"), [BinaryOp("%", IntLiteral(4), IntLiteral(1))]), StringLiteral("1")]))))
        self.assertTrue(TestChecker.test(input,expect,471))
    
    def test_complex_if(self):
        input = """
        Function: fun
        Parameter: a, b
        Body:
            Return int_of_float(1.0 +. 23.4  \. a -. 14.5 *. 124.3) + int_of_string("still string");
        EndBody.
        Function: main
        Parameter: a
        Body:
            If ((a == 1) || (int_of_float(123.3) == 123) && (float_of_int(1) >=. 0.9)) Then
                a = "string";
            EndIf.
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), StringLiteral("string"))))
        self.assertTrue(TestChecker.test(input,expect,472))
    
    def test_call_func_two_time(self):
        input = """
        Function: main
                    Parameter: a
                    Body:
                        Var:x;
                        main(123);
                        main(123.314);
                    EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("main"), [FloatLiteral(123.314)])))
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_wrong_string(self):
        input = """
        Function: fun
        Parameter: a, b
        Body:
            Return int_of_float(1.0 +. 23.4  \. a -. 14.5 *. 124.3) + int_of_string(b);
        EndBody.
        Function: main
        Parameter: a
        Body:
            a = "string";
            a = fun(1, 1);
        EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("fun"), [IntLiteral(1), IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,474))
    
    def test_self_call_(self):
        input = """
        Function: fun
        Parameter: a, b
        Body:
            Return int_of_float(1.0 +. 23.4  \. a -. 14.5 *. 124.3) + int_of_string(b);
            fun(1.2, "1");
        EndBody.
        Function: main
        Parameter: a
        Body:
            a = "string";
            a = fun(1, 1);
        EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("fun"), [IntLiteral(1), IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,475))
    
    def test_call(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    a = 1;
                    z = main(x);
                EndWhile.
                Return z;
            EndBody.
                """
        expect = str(TypeMismatchInExpression(CallExpr(Id("main"), [Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,476))
    
    def test_suy_dien(self):
        input = """
            Var: a = 1;
            Function: main
            Parameter: a
            Body:
                Var: x = True, z;
                While(x) Do
                    a = 1;
                    z = main(1);
                EndWhile.
                Return z;
            EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('z'), CallExpr(Id("main"), [IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,477))
    
    def test_suy_dien_2(self):
        input = """
            Var: a, z;
            Function: main
            Body:
                Var: x = True, z;
                While(x) Do
                    z = 1;
                    a = main();
                EndWhile.
                Return z;
            EndBody.
                """
        expect = str(TypeCannotBeInferred(Assign(Id('a'), CallExpr(Id("main"), []))))
        self.assertTrue(TestChecker.test(input,expect,478))
    
    def test_call_undecl(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                foo();
            EndBody.
                """
        expect = str(Undeclared(Function(), 'foo'))
        self.assertTrue(TestChecker.test(input,expect,479))
    
    def test_undecl(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = 1;
                a = a + z - c;
            EndBody.
                """
        expect = str(Undeclared(Identifier(), 'c'))
        self.assertTrue(TestChecker.test(input,expect,480))
    
    def test_call_with_undecl(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = 1;
                main(c);
            EndBody.
                """
        expect = str(Undeclared(Identifier(), 'c'))
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_redcecl_func(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = 1;
            EndBody.
            Function: main
            Parameter: a
            Body:
                z = 1;
                main(c);
            EndBody.
                """
        expect = str(Redeclared(Function(), 'main'))
        self.assertTrue(TestChecker.test(input,expect,482))
    
    def test_wrong_binaryop(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = a + 1 -. 1.2;
            EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("-.", BinaryOp("+", Id("a"), IntLiteral(1)), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,483))
    
    def test_wrong_binaryop2(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = a + 1 -. True;
            EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("-.", BinaryOp("+", Id("a"), IntLiteral(1)), BooleanLiteral(True))))
        self.assertTrue(TestChecker.test(input,expect,484))
    
    def test_wrong_string_2(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = a + "String";
            EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("+", Id("a"), StringLiteral("String"))))
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_sign_number(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                a = z +. 1.2;
            EndBody.
                """
        expect = str(TypeMismatchInExpression(BinaryOp("+.", Id("z"), FloatLiteral(1.2))))
        self.assertTrue(TestChecker.test(input,expect,486))
    
    def test_unop(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                If !z Then
                z = -2;
                EndIf.
            EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("!", Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,487))
    
    def test_unop2(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                If !True Then
                z = -.z;
                EndIf.
            EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-.", Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,488))
    
    def test_complex_op(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                If !True Then
                    z = z + -z \ z + -1;
                    printLn();
                    z = -2.3;
                EndIf.
            EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-", FloatLiteral(2.3))))
        self.assertTrue(TestChecker.test(input,expect,489))
    
    def test_complex_while(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                While !(z == -1) Do
                    z = z + -z \ z + -1;
                    printLn();
                    z = -2.9;
                EndWhile.
            EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-", FloatLiteral(2.9))))
        self.assertTrue(TestChecker.test(input,expect,490))
    
    def test_complex_if_2(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                If ((!(z == -1)) && (1.2 =/= 1.3)) Then
                    z = z + -z \ z + -1;
                    printLn();
                    z = -0.4;
                EndIf.
            EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-", FloatLiteral(0.4))))
        self.assertTrue(TestChecker.test(input,expect,491))

    def test_complex_for(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                For(z = 1, z < z + 1, z = z - 1) Do
                    z = -0.415;
                EndFor.
            EndBody.
                """
        expect = str(TypeMismatchInExpression(UnaryOp("-", FloatLiteral(0.415))))
        self.assertTrue(TestChecker.test(input,expect,492))
    
    def test_complex_for_2(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                For(z = 1, ((!(z == -1)) && (1.2 =/= 1.3)), z = z - 1) Do
                    z = 124.5;
                EndFor.
            EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id("z"), FloatLiteral(124.5))))
        self.assertTrue(TestChecker.test(input,expect,493))
    
    def test_string(self):
        input = """
            Var: a, z;
            Function: main
            Parameter: a
            Body:
                z = -1;
                For(z = 1, ((!(z == -1)) && (1.2 =/= 1.3)), z = a - 1) Do
                    a = "PPL that dang so";
                EndFor.
            EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), StringLiteral("PPL that dang so"))))
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_return_none(self):
        input = """
        Var: a, b, arr;
        Function: main
        Parameter: x, y
        Body:
            f()[2][3] = a * 2;
        EndBody.
        Function: f
        Body:
            Return;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input, expect, 495))
    
    def test_add_string(self):
        input = """
        Var: a, b, arr;
        Function: main
        Body:
            a = "p" + "p" + "l";
        EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+", StringLiteral("p"), StringLiteral("p"))))
        self.assertTrue(TestChecker.test(input, expect, 496))
    
    def test_read_write(self):
        input = """
        Var: a, b, arr;
        Function: main
        Body:
            a = read();
            printLn(a);
        EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("printLn"), [Id("a")])))
        self.assertTrue(TestChecker.test(input, expect, 497))
    
    def test_print_ln(self):
        input = """
        Var: a, b, arr;
        Function: main
        Body:
            a = read();
            printStr(a);
            a = 1;
        EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"), IntLiteral(1))))
        self.assertTrue(TestChecker.test(input, expect, 498))
    
    def test_hard(self):
        input = """
        Var: a, b, arr;
        Function: main
        Body:
            printStr("Done");
            a = b;
        EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("a"), Id("b"))))
        self.assertTrue(TestChecker.test(input, expect, 499))