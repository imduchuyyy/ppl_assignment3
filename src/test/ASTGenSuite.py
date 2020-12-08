import unittest
from TestUtils import TestAST
from AST import *

#Program([ FuncDecl(Id("main"),[],([],[]))])

class ASTGenSuite(unittest.TestCase):
    def test_var_declare(self):
        """Simple program: int main() {} """
        input = """Var:x;"""
        expect = Program([VarDecl(Id("x"),[],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """Var:x,y= True;"""
        expect = Program([VarDecl(Id("x"),[],None),VarDecl(Id("y"),[],BooleanLiteral("true"))])
        self.assertTrue(TestAST.checkASTGen(input,expect,301))
    
    def test_more_complex_program(self):
        input = """
        Function: main
        Body:
            x = 10;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[
                Assign(Id("x"),IntLiteral(10))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,302))

    def test_declare_var(self):
        input = """
        Var:x = 10;
        """
        expect = Program([VarDecl(Id("x"),[],IntLiteral(10))])
        self.assertTrue(TestAST.checkASTGen(input,expect,303))

    def test_declare_var1(self):
        input = """
        Var:x[3] = 10;
        """
        expect = Program([VarDecl(Id("x"),[3],IntLiteral(10))])
        self.assertTrue(TestAST.checkASTGen(input,expect,304))

    def test_declare_var2(self):
        input = """
        Var:x[3] = 9.3;
        """
        expect = Program([VarDecl(Id("x"),[3],FloatLiteral(9.3))])
        self.assertTrue(TestAST.checkASTGen(input,expect,305))


    def test_declare_var5(self):
        input = """
        Var:x[3] = "hello";
        """
        expect = Program([VarDecl(Id("x"),[3],StringLiteral("hello"))])
        self.assertTrue(TestAST.checkASTGen(input,expect,306))
    
    def test_declare_var6(self):
        input = """
        Var:x[3] = "hello", y = 1, z = 2.3;
        
        """
        expect = Program([VarDecl(Id("x"),[3],StringLiteral("hello")),VarDecl(Id("y"),[],IntLiteral(1)), VarDecl(Id("z"),[],FloatLiteral(2.3))])
        self.assertTrue(TestAST.checkASTGen(input,expect,307))

    def test_declare_func(self):
        input = """
        Function: main
        Body:
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,308))
    
    def test_declare_func2(self):
        input = """
        Function: main
        Parameter: s, z
        Body:
            Var: x;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[VarDecl(Id("s"),[], None), VarDecl(Id("z"),[], None)],([VarDecl(Id("x"),[], None)],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,309))

    def test_declare_func5(self):
        input = """
        Function: main
        Parameter: s = 3, z = 4
        Body:
            Var: x;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[VarDecl(Id("s"),[], IntLiteral(3)), VarDecl(Id("z"),[], IntLiteral(4))],([VarDecl(Id("x"),[], None)],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,310))

    def test_declare_func4(self):
        input = """
        Function: main
        Parameter: s = 3, z = 4
        Body:
            print(x);
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[VarDecl(Id("s"),[], IntLiteral(3)), VarDecl(Id("z"),[], IntLiteral(4))],([],[CallStmt(Id("print"),[Id("x")])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,311))
    
    def test_declare_var7(self):
        input = """
        Var:x = "hello", z = 10, y = 1.1 ;
        """
        expect = Program([VarDecl(Id("x"),[],StringLiteral("hello")), VarDecl(Id("z"),[],IntLiteral(10)), VarDecl(Id("y"),[],FloatLiteral(1.1))])
        self.assertTrue(TestAST.checkASTGen(input,expect,312))

    def test_declare_var8(self):
        input = """
        Var:x, z[3] = 10, y = 1.1 ;
        """
        expect = Program([VarDecl(Id("x"),[],None), VarDecl(Id("z"),[3],IntLiteral(10)), VarDecl(Id("y"),[],FloatLiteral(1.1))])
        self.assertTrue(TestAST.checkASTGen(input,expect,313))
    
    def test_declare_var9(self):
        input = """
        Function: main
        Body:
            Var:x, z[3] = 10, y = 1.1 ;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([VarDecl(Id("x"),[],None), VarDecl(Id("z"),[3],IntLiteral(10)), VarDecl(Id("y"),[],FloatLiteral(1.1))],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,314))

    def test_simple_func5(self):
        input = """Function: main
                    Parameter: a,b[1][2]
                    Body:
                    EndBody.
                    Function: foo
                    Body:
                    EndBody."""
        expect = Program([FuncDecl(Id("main"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[1,2],None)],([],[])),
                            FuncDecl(Id("foo"),[],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,315))
    
    def test_var_declare10(self):
        input = """ Var:x={3,{3.5},7};"""
        expect = Program([VarDecl(Id('x'),[],ArrayLiteral([IntLiteral(3),ArrayLiteral([FloatLiteral(3.5)]),IntLiteral(7)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,316))

    def test_declare_func1(self):
        input = """
        Function: main
        Body:
            Var: x;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([VarDecl(Id("x"),[], None)],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,317))

    def test_declare_func3(self):
        input = """
        Function: main
        Body:
            Var: x;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([VarDecl(Id("x"),[], None)],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,318))
    
    def test_assign_statement(self):
        input = """
        Function: main
        Body:
            x = 10;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[Assign(Id("x"),IntLiteral(10))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,319))

    def test_assign_statement1(self):
        input = """
        Function: main
        Body:
            x = "hello";
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[Assign(Id("x"),StringLiteral("hello"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,320))

    def test_assign_statement2(self):
        input = """
        Function: main
        Body:
            x = 1.3;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[Assign(Id("x"),FloatLiteral(1.3))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,321))

    def test_assign_statement3(self):
        input = """
        Function: main
        Body:
            x = {1,3,4 };
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[Assign(Id("x"),ArrayLiteral([IntLiteral(1), IntLiteral(3), IntLiteral(4)]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,322))
    
    def test_if_statement(self):
        input = """
        Function: main
        Body:
            If (a > b)
               Then a = 1.3;
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[If([(BinaryOp('>', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.3))])], [])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,323))
    
    def test_if_statement1(self):
        input = """
        Function: main
        Body:
            If (a > b)
               Then a = 1.3;
            Else a = 1.1;
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[If([(BinaryOp('>', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.3))])], ([], [Assign(Id('a'), FloatLiteral(1.1))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,324))
    
    def test_if_statement2(self):
        input = """
        Function: main
        Body:
            If (a > b)
                Then a = 1.3;
            ElseIf (a == b)
                Then a = 1.1;
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[If([(BinaryOp('>', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.3))]), (BinaryOp('==', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.1))]) ], None)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,325))
    
    def test_if_statement3(self):
        input = """
        Function: main
        Body:
            If (a > b)
                Then a = 1.3;
            ElseIf (a == b)
                Then a = 1.1;
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[If([(BinaryOp('>', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.3))]), (BinaryOp('==', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.1))]) ], None)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,326))

    
    def test_for_in_for(self):
         input = """
         Function: main
         Body:
             For(b = 3, b >= 0, b = b + 1)Do
                For(b = 3, b >= 0, b = b + 1)Do
                    a = 3;
                EndFor.
             EndFor.
         EndBody.
         """
         expect = "Program([FuncDecl(Id(main)[],([][For(Id(b),IntLiteral(3),BinaryOp(>=,Id(b),IntLiteral(0)),BinaryOp(+,Id(b),IntLiteral(1)),[],[For(Id(b),IntLiteral(3),BinaryOp(>=,Id(b),IntLiteral(0)),BinaryOp(+,Id(b),IntLiteral(1)),[],[Assign(Id(a),IntLiteral(3))])])]))])"
         self.assertTrue(TestAST.checkASTGen(input,expect,327))

    def test_break(self):
        input = """Var: x = 5;
        Function: main
        Body:
            x = 10;
            Break;
            printLn(x);
        EndBody.
        """
        expect = Program([
            VarDecl(Id("x"),[],IntLiteral(5)),
            FuncDecl(Id("main"),[],([],[
                Assign(Id("x"),IntLiteral(10)),
                Break(),
                CallStmt(Id("printLn"),[Id("x")])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,328))
    
    def test_return(self):
        input = """Var: x = 5;
        Function: main
        Body:
            x = 10;
            Return x + 10;
        EndBody.
        """
        expect = Program([
            VarDecl(Id("x"),[],IntLiteral(5)),
            FuncDecl(Id("main"),[],([],[
                Assign(Id("x"),IntLiteral(10)),
                Return(BinaryOp('+', Id('x'), IntLiteral(10)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,329))
    
    def test_return1(self):
        input = """Var: x = 5;
        Function: main
        Body:
            x = 10;
            Return x;
        EndBody.
        """
        expect = Program([
            VarDecl(Id("x"),[],IntLiteral(5)),
            FuncDecl(Id("main"),[],([],[
                Assign(Id("x"),IntLiteral(10)),
                Return(Id("x"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,330))

    def test_if_statement4(self):
        input = """
        Function: main
        Body:
            If (a > b)
                Then a = 1.3;
            ElseIf (a == b)
                Then a = 1.1;
            Else a = 2.1;
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[If([(BinaryOp('>', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.3))]), (BinaryOp('==', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.1))]) ], ([], [Assign(Id('a'), FloatLiteral(2.1))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,331))

    def test_for_statement(self):
        input = """
        Function: main
        Body:
            For(b = 3, b >= 0, b = b + 1)Do
                a = 1;
            EndFor.
        EndBody.
        """
        expect = Program([
        FuncDecl(Id("main"),[],([],[For(Id('b'), IntLiteral(3),BinaryOp('>=', Id('b'), IntLiteral(0)), BinaryOp('+', Id('b'), IntLiteral(1)), ([], [Assign(Id('a'), IntLiteral(1))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,332))
    
    def test_for_statement2(self):
        input = """
        Function: main
        Body:
            For(b = 3, b >= 0, b = b + 1)Do
                If (b >= 0) Then b = 0;
                EndIf.
            EndFor.
        EndBody.
        """
        expect = Program([
        FuncDecl(Id("main"),[],([],[For(Id('b'), IntLiteral(3),BinaryOp('>=', Id('b'), IntLiteral(0)), BinaryOp('+', Id('b'), IntLiteral(1)), ([], [If([(BinaryOp('>=', Id('b'), IntLiteral(0)),[], [Assign(Id('b'), IntLiteral(0))])], ())]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,333))
    
    def test_for_statement3(self):
        input = """
        Function: main
        Body:
            For(b = 3, b >= 0, b = b + 1)Do
                b = b + 1;
            EndFor.
        EndBody.
        """
        expect = Program([
        FuncDecl(Id("main"),[],([],[For(Id('b'), IntLiteral(3),BinaryOp('>=', Id('b'), IntLiteral(0)), BinaryOp('+', Id('b'), IntLiteral(1)), ([], [Assign(Id('b'), BinaryOp('+', Id('b'), IntLiteral(1)))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,334))
    
    def test_while_statement(self):
        input = """
        Function: main
        Body:
            While(b <= 3)Do
                b = 1;
            EndWhile.
        EndBody.
        """
        expect = Program([
        FuncDecl(Id("main"),[],([],[While(BinaryOp('<=', Id('b'), IntLiteral(3)), ([], [Assign(Id('b'), IntLiteral(1))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,335))
    
    def test_while_statement_1(self):
        input = """
        Function: main
        Body:
            While(b <= 3)Do
                For(b = 3, b >= 0, b = b + 1)Do
                    b = b + 1;
                EndFor.
            EndWhile.
        EndBody.
        """
        expect = Program([
        FuncDecl(Id("main"),[],([],[While(BinaryOp('<=', Id('b'), IntLiteral(3)), ([], [For(Id('b'), IntLiteral(3),BinaryOp('>=', Id('b'), IntLiteral(0)), BinaryOp('+', Id('b'), IntLiteral(1)), ([], [Assign(Id('b'), BinaryOp('+', Id('b'), IntLiteral(1)))]))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,336))
    
    def test_do_while_statement(self):
        input = """
        Function: main
        Body:
            Do
                b = 1;
            While (b <= 3) EndDo.
        EndBody.
        """
        expect = Program([ FuncDecl(Id("main"),[],([],[Dowhile(([] ,[Assign(Id('b'), IntLiteral(1))]), BinaryOp('<=', Id('b'), IntLiteral(3)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,337))

    def test_do_while_statement2(self):
        input = """
        Function: main
        Body:
            Do
                If a == b Then a = 1;
                EndIf.
            While (b <= 3) EndDo.
        EndBody.
        """
        expect = Program([ FuncDecl(Id("main"),[],([],[Dowhile(([] ,[If([(BinaryOp('==', Id('a'), Id('b')), [], [Assign(Id('a'), IntLiteral(1))])], None)]), BinaryOp('<=', Id('b'), IntLiteral(3)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,338))

    def test_continue_statement(self):
        input = """
        Function: main
        Body:
            Continue;
        EndBody.
        """
        expect = Program([ FuncDecl(Id("main"),[],([],[Continue()]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,339))

    def test_function_call_statement(self):
        input = """
        Function: main
        Body:
            check(a);
        EndBody.
        """
        expect = Program([ FuncDecl(Id("main"),[],([],[CallStmt(Id('check'), [Id('a')])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,340))
    
    def test_expression_statement(self):
        input = """
        Function: main
        Body:
            b = b + 1;
        EndBody.
        """
        expect = Program([ FuncDecl(Id("main"),[],([],[Assign(Id('b'), BinaryOp('+', Id('b'), IntLiteral(1)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,341))
    
    def test_expression_statement1(self):
        input = """
        Function: main
        Body:
            b = b > 1;
        EndBody.
        """
        expect = Program([ FuncDecl(Id("main"),[],([],[Assign(Id('b'), BinaryOp('>', Id('b'), IntLiteral(1)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,342))
    
    def test_function_call1(self):
        input = """Var: x = 5;
             Function: main
             Body:
                 printLn(x);
                 printLn(x, y);
             EndBody.
             """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([], [
                CallStmt(Id("printLn"), [Id("x")]),
                CallStmt(Id("printLn"), [Id("x"),Id("y")])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))
    
    def test_return_statement1(self):
        input = """Var: x = 5;
             Function: main
             Body:
                Return;
             EndBody.
             """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([
                
            ], [
                Return(None)
            ]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))
    
    def test_call_exp(self):
        input = """Var: x = 5;
             Function: main
             Body:
                a = valueOf(x);
             EndBody.
             """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([
                
            ], [
                Assign(Id('a'), CallExpr(Id('valueOf'), [Id('x')]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))

    def test_index_operator(self):
        input = """Var: x = 5;
             Function: main
             Body:
                a = array[x];
             EndBody.
             """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([
                
            ], [
                Assign(Id('a'), ArrayCell(Id('array'), [Id("x")]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))
    
    def test_decale_array(self):
        input = """Var: x = 5;
             Function: main
             Body:
                array = {1,2,3};
             EndBody.
             """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([
                
            ], [
                Assign(Id('array'), ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))

    def test_for_statement4(self):
         input = """
         Function: main
         Body:
            For(b = 3, b >= 0, b = b + 1)Do
                var = a * (b - 10);
            EndFor.
         EndBody.
         """
         expect = Program([
             FuncDecl(Id("main"),[],([],
                 [For(Id("b"), IntLiteral(3),
                      BinaryOp( ">=", Id("b"), IntLiteral(0)), BinaryOp("+", Id("b"), IntLiteral(1)),
                      [[], [Assign(Id("var"), BinaryOp("*", Id("a") ,BinaryOp("-",Id("b"), IntLiteral(10))))]])]))])
         self.assertTrue(TestAST.checkASTGen(input,expect,348))
        

    def test_for_statement5(self):
         input = """
         Function: main
         Body:
             For(b = 3, b >= 0, b = b + 1)Do
             temp = a *. (b -. 10);
             EndFor.
         EndBody.
         """
         expect = Program([
             FuncDecl(Id("main"),[],([],
                 [For(Id("b"), IntLiteral(3),
                      BinaryOp( ">=", Id("b"), IntLiteral(0)), BinaryOp("+", Id("b"), IntLiteral(1)),
                      [[], [Assign(Id("temp"), BinaryOp("*.", Id("a") ,BinaryOp("-.",Id("b"), IntLiteral(10))))]])]))])
         self.assertTrue(TestAST.checkASTGen(input,expect,349))
        
    def test_while_statement2(self):
        input = """
        Function: main
        Body:
            While(b <= 3)Do
                If(b == 1) Then Break;
                EndIf.
            EndWhile.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
                
            ], [
                While(BinaryOp('<=', Id('b'), IntLiteral(3)), ([], [
                    If([(BinaryOp('==', Id('b'), IntLiteral(1)), [], [Break()])], None)
                ]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,350))
    
    def test_complex_func(self):
        input = """
        Function: main
        Body:
            Var: x = 10, y;
            y = read();
            If (x == y) Then
                print("X == Y");
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
                VarDecl(Id('x'), [], IntLiteral(10)),
                VarDecl(Id('y'), [], None)
            ], [
                Assign(Id('y'), CallExpr(Id('read'), [])),
                If([(BinaryOp('==', Id('x'), Id('y')),[], [CallStmt(Id('print'), [StringLiteral("X == Y")])])], [])
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,351))
    
    def test_complex_func1(self):
        input = """
        Function: main
        Body:
            Var: x = 10, y;
            y = read();
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
                VarDecl(Id('x'), [], IntLiteral(10)),
                VarDecl(Id('y'), [], None)
            ], [
                Assign(Id('y'), CallExpr(Id('read'), [])),
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,352))
    
    def test_complex_func2(self):
        input = """
        Function: main
        Body:
            Var: x = 10, y;
            y = read();
            While(x != y)Do
                x = x + 1;
            EndWhile.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
                VarDecl(Id('x'), [], IntLiteral(10)),
                VarDecl(Id('y'), [], None)
            ], [
                Assign(Id('y'), CallExpr(Id('read'), [])),
                While(BinaryOp('!=', Id('x'), Id('y')), ([

                ],[
                    Assign(Id('x'), BinaryOp('+', Id('x'), IntLiteral(1)))
                ]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,353))

    def test_complex_func3(self):
        input = """
        Function: main
        Body:
            Var: x = 10.1, y;
            y = read();
            print(y);
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
                VarDecl(Id('x'), [], FloatLiteral(10.1)),
                VarDecl(Id('y'), [], None)
            ], [
                Assign(Id('y'), CallExpr(Id('read'), [])),
                CallStmt(Id('print'), [Id('y')])
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,354))
    
    def test_complex_func4(self):
        input = """
        Function: main
        Body:
            Var: x = 10.1, y;
            y = read();
            Return x + y;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
                VarDecl(Id('x'), [], FloatLiteral(10.1)),
                VarDecl(Id('y'), [], None)
            ], [
                Assign(Id('y'), CallExpr(Id('read'), [])),
                Return(BinaryOp('+', Id('x'), Id('y')))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,355))
    
    def test_complex_func5(self):
        input = """Var: a, b;
             Function: sum
             Parameter: a, b
             Body:
                 Var: temp = 0;
                 temp = a * b;
                 Return temp;
             EndBody.
             """
        expect = Program([
            VarDecl(Id("a"), [], None),
            VarDecl(Id("b"), [], None),
            FuncDecl(Id("sum"), [VarDecl(Id("a"), [], None),
            VarDecl(Id("b"), [], None),], ([
                VarDecl(Id("temp"), [], IntLiteral(0))], [
                Assign(Id("temp"), BinaryOp("*", Id("a"), Id("b"))),
                Return(Id("temp"))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))
    
    def test_function_return_array(self):
        input = """
             Function: main
             Parameter: a, b
             Body:
                Return a[b];
             EndBody.
             """
        expect = Program([
            FuncDecl(Id("main"), [VarDecl(Id("a"), [], None),
            VarDecl(Id("b"), [], None)], ([
            ], [
                Return(ArrayCell(Id('a'), [Id('b')]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,357))
    
    def test_exp_Sub_exp_more(self):
         input = """
         Function: main
         Body:
             While(!(b < 3))Do
             b = (b + 1) * (b - 1);
             EndWhile.
         EndBody.
         """
         expect = Program([
             FuncDecl(Id("main"),[],([],[While(
             UnaryOp( "!", BinaryOp("<", Id("b"), IntLiteral(3))),[[], [
             Assign(Id("b"), BinaryOp("*", BinaryOp("+",Id("b"),IntLiteral(1)),BinaryOp("-",Id("b"),IntLiteral(1))))]])]))])
         self.assertTrue(TestAST.checkASTGen(input,expect,358))

    def test_func_call(self):
        input = """
        Function: main
        Body:
            x = sum(a, b);
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                Assign(Id('x'), CallExpr(Id('sum'), [Id('a'), Id('b')]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,359))
    
    def test_func_call1(self):
        input = """
        Function: main
        Body:
            x = sum(parseInt(a), b);
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                Assign(Id('x'), CallExpr(Id('sum'), [CallExpr(Id('parseInt'), [Id('a')]), Id('b')]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,360))
    
    def test_print_func(self):
        input = """
        Function: main
        Body:
            print("I love PPL");
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                CallStmt(Id('print'), [StringLiteral('I love PPL')])
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,361))

    def test_dowhile_in_dowhile(self):
        input = """
            Function: main
            Body:
                Var: b = 0;
                Do
                    Do
                        b = b + 1;
                    While(b >= 0)
                    EndDo.
                While(b <= 3)
                EndDo.
            EndBody.
            """
        expect = Program([FuncDecl(Id("main"), [], ([
                    VarDecl(Id("b"), [], IntLiteral(0))], [
                    Dowhile([[], [
                        Dowhile([[], [
                            Assign(Id("b"), BinaryOp("+", Id("b"), IntLiteral(1)))]],
                        BinaryOp(">=", Id("b"), IntLiteral(0)))]],
                    BinaryOp("<=", Id("b"), IntLiteral(3)))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))
    
    def test_if_else_if(self):
        input = """
        Function: main
        Body:
            If (a > b)
                Then a = 1.3;
            ElseIf (a < b)
                Then a = 1.1;
            Else a = 1;
            EndIf.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[If([(BinaryOp('>', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.3))]), (BinaryOp('<', Id('a'), Id('b')), [], [Assign(Id('a'), FloatLiteral(1.1))]) ], ([], [Assign(Id('a'), IntLiteral(1))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,363))
    
    def test_while_statement_2(self):
        input = """
        Function: main
        Body:
            Var: b = 0;
            While(b <= 3)Do
            temp = a % (b \ 10);
            EndWhile.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([
                VarDecl(Id("b"),[],IntLiteral(0))],[
                While(BinaryOp( "<=", Id("b"), IntLiteral(3)),[[], [
                    Assign(Id("temp"), BinaryOp("%", Id("a") ,BinaryOp("\\",Id("b"), IntLiteral(10))))]])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,364))  
    
    def test_many_exp(self):
        input = """
        Function: main
        Body:
            While(!(b < 3))Do
            b = (b + 1) * (b - 1);
            EndWhile.
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[While(
            UnaryOp( "!", BinaryOp("<", Id("b"), IntLiteral(3))),[[], [
            Assign(Id("b"), BinaryOp("*", BinaryOp("+",Id("b"),IntLiteral(1)),BinaryOp("-",Id("b"),IntLiteral(1))))]])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,365))
    
    def test_callStatement_more_value(self):
        input = """Var: x = 5;
            Function: main
            Body:
                x = 10;
                printLn(x);
                y = 20;
                printLn(x, y);
            EndBody.
            """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([], [
                Assign(Id("x"), IntLiteral(10)),
                CallStmt(Id("printLn"), [Id("x")]),
                Assign(Id("y"), IntLiteral(20)),
                CallStmt(Id("printLn"), [Id("x"),Id("y")])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))
    
    def test_float(self):
        input = """Var: x = 5;
            Function: main
            Body:
                x = 10.23;
                printLn(x);
                y = 20e-10;
                printLn(x, y);
            EndBody.
            """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([], [
                Assign(Id("x"), FloatLiteral(10.23)),
                CallStmt(Id("printLn"), [Id("x")]),
                Assign(Id("y"), FloatLiteral(20e-10)),
                CallStmt(Id("printLn"), [Id("x"),Id("y")])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))
    
    def test_float1(self):
        input = """Var: x = 5;
            Function: main
            Body:
                x = 10.23;
                printLn(x);
                y = 20.23e-10;
                printLn(x, y);
            EndBody.
            """
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(5)),
            FuncDecl(Id("main"), [], ([], [
                Assign(Id("x"), FloatLiteral(10.23)),
                CallStmt(Id("printLn"), [Id("x")]),
                Assign(Id("y"), FloatLiteral(20.23e-10)),
                CallStmt(Id("printLn"), [Id("x"),Id("y")])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))
    
    def test_index_operator1(self):
        input = """
            Function: main
            Body:
                a = array[10 - 1][12 \ 10];
            EndBody.
            """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                Assign(Id('a'), ArrayCell(Id('array'), [BinaryOp('-', IntLiteral(10), IntLiteral(1)), BinaryOp('\\', IntLiteral(12), IntLiteral(10))]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,369))
    
    def test_complex_index_operator(self):
        input = """
            Function: main
            Body:
                a = array[foo(x) - 1][12 \ 10];
            EndBody.
            """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                Assign(Id('a'), ArrayCell(Id('array'), [BinaryOp('-', CallExpr(Id('foo'), [Id('x')]), IntLiteral(1)), BinaryOp('\\', IntLiteral(12), IntLiteral(10))]))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,370))
    
    def test_many_exp2(self):
        input = """
        Function: main
        Body:
            Return 7 % (3 + 10 * foo(a[2+7][2*3])) \. 2 ;
        EndBody.
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[Return(BinaryOp("\.",BinaryOp("%",IntLiteral(7),BinaryOp("+",IntLiteral(3),BinaryOp("*",IntLiteral(10),CallExpr(Id("foo"),[ArrayCell(Id("a"),[BinaryOp("+",IntLiteral(2),IntLiteral(7)),BinaryOp("*",IntLiteral(2),IntLiteral(3))])])))),IntLiteral(2)))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,371))
    
    def test_many_exp3(self):
        input = """
        Function: main
        Body:
        a = 1 + 1 - 2 * 3 + foo(2) - a[7]; 
        EndBody.
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),BinaryOp("-",BinaryOp("+",BinaryOp("-",BinaryOp("+",IntLiteral(1),IntLiteral(1)),BinaryOp("*",IntLiteral(2),IntLiteral(3))),CallExpr(Id("foo"),[IntLiteral(2)])),ArrayCell(Id("a"),[IntLiteral(7)])))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,372))
    
    def test_false(self):
        input = """Var:z=False;
        """ 
        expect = Program([VarDecl(Id("z"),[],BooleanLiteral(False))])
        self.assertTrue(TestAST.checkASTGen(input,expect,373))

    def test_many_exp4(self):
        input = """
        Function: main
        Body:
            a = 1 + 1 - 2 * 3 + foo(2) - a[{1,2,3}+23.]; 
        EndBody.
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),BinaryOp("-",BinaryOp("+",BinaryOp("-",BinaryOp("+",IntLiteral(1),IntLiteral(1)),BinaryOp("*",IntLiteral(2),IntLiteral(3))),CallExpr(Id("foo"),[IntLiteral(2)])),ArrayCell(Id("a"),[BinaryOp("+",ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]),FloatLiteral(23.0))])))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,374))
    
    def test_sign_int(self):
        input = """
        Function: main
        Body:
        a = -2 + 7 * 2 * -.2;
        EndBody.
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),BinaryOp("+",UnaryOp("-",IntLiteral(2)),BinaryOp("*",BinaryOp("*",IntLiteral(7),IntLiteral(2)),UnaryOp("-.",IntLiteral(2)))))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,375))
    
    def test_comment(self):
        input = """
        **This is comment**
        **This is comment**
        Function: main
        Body:
        a = -2 + 7 * 2 * -.2;
        EndBody.
""" 
        expect = Program([FuncDecl(Id("main"),[],([],[Assign(Id("a"),BinaryOp("+",UnaryOp("-",IntLiteral(2)),BinaryOp("*",BinaryOp("*",IntLiteral(7),IntLiteral(2)),UnaryOp("-.",IntLiteral(2)))))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,376))
    
    def test_none_int(self):
        input = """Var: i={{},{3,4},{}};
        """ 
        expect = Program([VarDecl(Id("i"),[],ArrayLiteral([ArrayLiteral([]),ArrayLiteral([IntLiteral(3),IntLiteral(4)]),ArrayLiteral([])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,377))
    
    def test_many_func(self):
        input = """
        **This is comment**
        Function: main
        Body:
           
        EndBody.
        Function: get
        Body:
           
        EndBody.
        """ 
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
            ])),
            FuncDecl(Id("get"), [], ([
            ], [
            ]))
            ])
        self.assertTrue(TestAST.checkASTGen(input,expect,378))

    def test_expression_statement2(self):
        input = """
            Function: main
            Body:
                a = i <=. 10 || (i > 7);
            EndBody.
            """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                Assign(Id('a'), BinaryOp('<=.', Id('i'), BinaryOp('||', IntLiteral(10), BinaryOp('>', Id('i'), IntLiteral(7)))))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,379))
    
    def test_function_with_index(self):
        input = """
        Function: main
        Body:
            foo(2)[3][4] = 1;
            a = {3,4};
        EndBody.              
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[Assign(ArrayCell(CallExpr(Id("foo"),[IntLiteral(2)]),[IntLiteral(3),IntLiteral(4)]),IntLiteral(1)),Assign(Id("a"),ArrayLiteral([IntLiteral(3),IntLiteral(4)]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,380))
    
    def test_none_body(self):
        input = """Var: x;
        Function: main
        Parameter: n
        Body:
        EndBody. 
        """ 
        expect = Program([VarDecl(Id("x"),[],None),FuncDecl(Id("main"),[VarDecl(Id("n"),[],None)],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,381))
    
    def test_assign_array(self):
        input = """
        Function: main
        Body:
        a[3][4] = 1;
        EndBody.              
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[Assign(ArrayCell(Id("a"),[IntLiteral(3),IntLiteral(4)]),IntLiteral(1))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,382))
    
    def test_complex_expression(self):
        input = """
        Function: main
        Body:
        a[3][4] = i - 7 \ 3 +. 1;
        EndBody.              
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[
            Assign(ArrayCell(Id('a'), [IntLiteral(3), IntLiteral(4)]), BinaryOp('+.', BinaryOp('-', Id('i'), BinaryOp('\\', IntLiteral(7), IntLiteral(3))), IntLiteral(1)))
        ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,383))
    
    def test_complex_expression2(self):
        input = """
        Function: qua_met_moi
        Body:
        a = "day la test case kho nhat tung viet";
        EndBody.              
        """ 
        expect = Program([FuncDecl(Id("qua_met_moi"),[],([],[
            Assign(Id('a'), StringLiteral("day la test case kho nhat tung viet"))
        ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,384))
    
    def test_for_statement6(self):
        input = """
        Function: main
        Body:
        For (i = 0, i < 10, 2) Do
            writeln(i);
            i = i-1;
        EndFor.
        EndBody.
        """ 
        expect = Program([FuncDecl(Id("main"),[],([],[For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(10)),IntLiteral(2),([],[CallStmt(Id("writeln"),[Id("i")]),Assign(Id("i"),BinaryOp("-",Id("i"),IntLiteral(1)))]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,385))
    
    def test_return_statement2(self):
        input = """
        Function: main
        Body:
            Return 7 % (3 \ 000.2e7 + 10 * main(a[1]));
        EndBody.
        """ 
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                Return(BinaryOp('%', IntLiteral(7) ,BinaryOp('+', BinaryOp('\\', IntLiteral(3), FloatLiteral(000.2e7)), BinaryOp('*', IntLiteral(10), CallExpr(Id('main'), [ArrayCell(Id('a'), [IntLiteral(1)])])))))
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,386))

    def test_var_declare11(self):
        input = """Var:x = 8, y = 1.3, z = "hello";"""
        expect = Program([
            VarDecl(Id("x"), [], IntLiteral(8)),
            VarDecl(Id("y"), [], FloatLiteral(1.3)),
            VarDecl(Id("z"), [], StringLiteral("hello"))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))
    
    def test_function1(self):
        input = """Var: x;
        Function: main
        Body:
            x = 1248123512;
        EndBody.
        """
        expect = Program([
            VarDecl(Id("x"), [], None),
            FuncDecl(Id("main"),[],([],[
                Assign(Id("x"),IntLiteral(1248123512))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,388))
    
    def test_assign(self):
        input = """
        Function: main
        Body:
            n = True;
            p = 8;
            c = 3.4;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[
                Assign(Id("n"),BooleanLiteral("true")),
                Assign(Id("p"),IntLiteral(8)),
                Assign(Id("c"),FloatLiteral(3.4))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,389))
    
    def test_many_func_and_many_var(self):
        input = """
        Var: x, y,z;
        Function: main
        Body:
           
        EndBody.
        Function: helper
        Body:
           
        EndBody.
        """ 
        expect = Program([
            VarDecl(Id('x'), [], None),
            VarDecl(Id('y'), [], None),
            VarDecl(Id('z'), [], None),
            FuncDecl(Id("main"), [], ([
            ], [
            ])),
            FuncDecl(Id("helper"), [], ([
            ], [
            ]))
            ])
        self.assertTrue(TestAST.checkASTGen(input,expect,390))
    
    def test_something(self):
        input = """
        Var: hello = "hello";
        """ 
        expect = Program([
            VarDecl(Id('hello'), [], StringLiteral("hello")),
            ])
        self.assertTrue(TestAST.checkASTGen(input,expect,391))
    
    def test_too_much(self):
        input = """
        Function: main
        Body:
            print("I am working very hard");
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"), [], ([
            ], [
                CallStmt(Id('print'), [StringLiteral("I am working very hard")])
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,392))
    
    def test_bool(self):
        input = """ 
            Function: foo 
            Body:
                true = True;
                false = False;
            EndBody."""
        expect = Program([FuncDecl(Id("foo"), [], ([], [
                Assign(Id('true'), BooleanLiteral(True)),
                Assign(Id('false'), BooleanLiteral(False)),
            ]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 393))
    
    def test_assign_array1(self):
        input = """
        Var:x[3] = {1,2,3};
        """
        expect = Program([VarDecl(Id("x"),[3],ArrayLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,394))

    def test_assign1(self):
        input = """
        Function: main
        Body:
            x = 10000000;
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[
                Assign(Id("x"),IntLiteral(10000000))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,395))
    
    def test_test_test(self):
        input = """
        Function: main
        Body:
            hic = "em met qua roi hic hic";
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[
                Assign(Id("hic"),StringLiteral("em met qua roi hic hic"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,396))
    
    def test_again(self):
        input = """
        Function: main
        Body:
            Var: hic = "Em khong hieu sao thoi gian chay test case lai lau nhu vay, chac do em viet bkit theo dang de quy";
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([
                VarDecl(Id('hic'), [], StringLiteral("Em khong hieu sao thoi gian chay test case lai lau nhu vay, chac do em viet bkit theo dang de quy"))
            ],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,397))
    
    def test_again1(self):
        input = """
        Function: main
        Body:
            Var: hic = "Mong la thay se khong xet thoi gian chay test";
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([
                VarDecl(Id('hic'), [], StringLiteral("Mong la thay se khong xet thoi gian chay test"))
            ],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,398))
    
    def test_cuoi_cung(self):
        input = """
        Function: main
        Body:
            print("Em met qua thay a, da 2 ngay roi em chua the ngu vi bai assignment nay");
        EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([
            ],[
                CallStmt(Id('print'), [StringLiteral("Em met qua thay a, da 2 ngay roi em chua the ngu vi bai assignment nay")])
            ]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,399))