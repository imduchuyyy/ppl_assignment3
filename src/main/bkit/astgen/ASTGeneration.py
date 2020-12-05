from BKITVisitor import BKITVisitor
from BKITParser import BKITParser
from AST import *

class ASTGeneration(BKITVisitor):
    def visitProgram(self,ctx:BKITParser.ProgramContext):
        return Program(ctx.many_declare().accept(self))
    
    #-------------------- VARIABLE DECLARE ---------------------
    def visitMany_declare(self,ctx:BKITParser.Many_declareContext):
        varDecl = []
        funcDecl = []
        if ctx.var_declare_list():
            varDecl = self.visit(ctx.var_declare_list())
        if ctx.func_declare_list():
            funcDecl = self.visit(ctx.func_declare_list())
        return varDecl + funcDecl

        
    def visitVar_declare_list(self, ctx:BKITParser.Var_declare_listContext):
        if ctx.var_declare_list():
            return self.visit(ctx.var_declare()) + self.visit(ctx.var_declare_list())
        else:
            return self.visit(ctx.var_declare())

    def visitFunc_declare_list(self, ctx:BKITParser.Func_declare_listContext):
        if ctx.func_declare_list():
            return self.visit(ctx.func_declare()) + self.visit(ctx.func_declare_list())
        else:
            return self.visit(ctx.func_declare())
    
    
    def visitVar_declare(self, ctx:BKITParser.Var_declareContext):
        return ctx.ids_list().accept(self)
    
    def visitIds_list(self, ctx:BKITParser.Ids_listContext):
        if ctx.ids_list():
            return ctx.id_declare().accept(self) + ctx.ids_list().accept(self)
        elif ctx.id_declare():
            return ctx.id_declare().accept(self)
    
    def visitId_declare(self, ctx:BKITParser.Id_declareContext):
        id = Id(ctx.ID().getText())
        array_declares = self.visit(ctx.array_declares()) if ctx.array_declares() else None
        type_list = self.visit(ctx.type_list()) if ctx.type_list() else None
        return [VarDecl(Id(ctx.ID().getText()), array_declares, type_list)]

    # --------------------------- ARRAY DECLARE -----------------------------
    def visitArray_declares(self, ctx:BKITParser.Array_declaresContext):
        if ctx.array_declares():
            return [self.visit(ctx.array())] + self.visit(ctx.array_declares())
        else:
            return [self.visit(ctx.array())]
    
    def visitArray(self, ctx:BKITParser.ArrayContext):
        return ctx.INTLIT().getText()

    def visitArray_id(self, ctx:BKITParser.Array_idContext):
        lhs = None
        if ctx.ID():
            lhs = Id(ctx.ID().getText())
        elif ctx.function_call():
            lhs = self.visit(ctx.function_call())
        return ArrayCell(lhs ,self.visit(ctx.list_index()))

    # ------------------------- FUNCTION DECLARE --------------------
    def visitFunc_declare(self, ctx:BKITParser.Func_declareContext):
        idFunc = self.visit(ctx.header_stm())
        param = self.visit(ctx.paramater_stm()) if ctx.paramater_stm() else []
        body = self.visit(ctx.body_stm())
        return [FuncDecl(idFunc, param, body)]
    
    def visitHeader_stm(self, ctx:BKITParser.Header_stmContext):
        return Id(ctx.ID().getText())

    # -------------------------- PARAMATER STATEMENT -------------------
    def visitParamater_stm(self, ctx:BKITParser.Paramater_stmContext):
        return self.visit(ctx.paramater_list())
    
    def visitParamater_list(self, ctx:BKITParser.Paramater_listContext):
        if ctx.paramater_list():
            return self.visit(ctx.ids_list()) + self.visit(ctx.paramater_list())
        else: 
            return self.visit(ctx.ids_list())

    #------------------- BODY STATEMENT -----------------------
    def visitBody_stm(self, ctx:BKITParser.Body_stmContext):
        list_varDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        list_statement = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return (list_varDecl, list_statement) # tuple
    
    def visitStatement_list(self, ctx:BKITParser.Statement_listContext):
        if ctx.statement_list():
            return self.visit(ctx.statement()) + self.visit(ctx.statement_list())
        else:
            return self.visit(ctx.statement())
    
    def visitStatement(self, ctx:BKITParser.StatementContext):
        return [self.visit(ctx.getChild(0))]
    
    #---------------------- ASSIGN STATEMENT ----------------
    def visitAssign_statement(self, ctx:BKITParser.Assign_statementContext):
        lhs = Id(ctx.ID().getText()) if ctx.ID() else self.visit(ctx.array_id())
        rhs = self.visit(ctx.expressions())
        return Assign(lhs, rhs)
    
    # ---------------------- IF STATEMENT --------------------
    def visitIf_statement(self, ctx:BKITParser.If_statementContext):
        ifThenStm = self.visit(ctx.if_then_statement())
        elseIfStm = self.visit(ctx.else_if_statements()) if ctx.else_if_statements() else []
        elseStm  = self.visit(ctx.else_statement()) if ctx.else_statement() else []
        return If(ifThenStm + elseIfStm, elseStm)

    def visitIf_then_statement(self, ctx:BKITParser.If_then_statementContext):
        expressions = self.visit(ctx.expressions())
        varsDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        statements = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return [(expressions, varsDecl, statements)] #tuple
    
    def visitElse_if_statements(self, ctx:BKITParser.Else_if_statementsContext):
        if ctx.else_if_statements():
            return self.visit(ctx.else_if_statement()) + self.visit(ctx.else_if_statements())
        else:
            return self.visit(ctx.else_if_statement())
    
    def visitElse_if_statement(self, ctx:BKITParser.Else_if_statementsContext):
        expressions = self.visit(ctx.expressions())
        varsDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        statements = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return [(expressions, varsDecl, statements)] #tuple
    
    def visitElse_statement(self, ctx:BKITParser.Else_statementContext):
        varsDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        statements = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return (varsDecl, statements) #tuple

    #---------------------- FOR STATEMENT ------------------------
    def visitFor_statement(self, ctx:BKITParser.For_statementContext):
        (id, expr1, expr2, expr3) = self.visit(ctx.for_condition())
        varsDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        statements = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return For(id, expr1, expr2, expr3, (varsDecl, statements))
    
    def visitFor_condition(self, ctx:BKITParser.For_conditionContext):
        id = Id(ctx.ID(0).getText())
        expr1 = self.visit(ctx.expressions(0))
        expr2 = self.visit(ctx.expressions(1))
        expr3 = self.visit(ctx.expressions(2))
        return (id, expr1, expr2, expr3)

    #---------------------- WHILE STATEMENT ----------------------
    def visitWhile_statement(self, ctx:BKITParser.While_statementContext):
        expressions = self.visit(ctx.expressions())
        varsDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        statements = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return While(expressions, (varsDecl, statements))
    
    #---------------------- DO WHILE STATEMENT -------------------
    def visitDo_while_statement(self, ctx:BKITParser.Do_while_statementContext):
        expressons = self.visit(ctx.expressions())
        varsDecl = self.visit(ctx.var_declare_list()) if ctx.var_declare_list() else []
        statements = self.visit(ctx.statement_list()) if ctx.statement_list() else []
        return Dowhile((varsDecl, statements), expressons)

    #---------------------- BREAK STATEMENT ----------------------
    def visitBreak_statement(self, ctx:BKITParser.Break_statementContext):
        return Break()

    #---------------------- CONTINUE STATEMENT -------------------
    def visitContinue_statement(self, ctx: BKITParser.Continue_statementContext):
        return Continue()

    #---------------------- FUNCTION CALL STATEMENT --------------
    def visitFunction_call_statement(self, ctx: BKITParser.Function_call_statementContext):
        id = Id(ctx.ID().getText())
        list_expr = [self.visit(expressions) for expressions in ctx.expressions()] if ctx.expressions() else []
        return CallStmt(id, list_expr)
    
    #---------------------- RETURN STATEMENT ---------------------
    def visitReturn_statement(self, ctx: BKITParser.Return_statementContext):
        expr = self.visit(ctx.expressions()) if ctx.expressions() else None
        return Return(expr)
    
    #---------------------- EXPRESSION ---------------------------
    def visitExpressions(self, ctx: BKITParser.ExpressionsContext):
        if ctx.EQUALOP():
            return BinaryOp(ctx.EQUALOP().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.NOTEQUALOP():
            return BinaryOp(ctx.NOTEQUALOP().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.LESSOP():
            return BinaryOp(ctx.LESSOP().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.LESSOREQUALOP():
            return BinaryOp(ctx.LESSOREQUALOP().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.GREATEROP():
            return BinaryOp(ctx.GREATEROP().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.GREATEOREQUALOP():
            return BinaryOp(ctx.GREATEOREQUALOP().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.NOTEQUALOPFLOAT():
            return BinaryOp(ctx.NOTEQUALOPFLOAT().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.LESSOPDOT():
            return BinaryOp(ctx.LESSOPDOT().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.LESSOREQUALOPDOT():
            return BinaryOp(ctx.LESSOREQUALOPDOT().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.GREATEROPDOT():
            return BinaryOp(ctx.GREATEROPDOT().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        elif ctx.GREATEOREQUALOPDOT():
            return BinaryOp(ctx.GREATEOREQUALOPDOT().getText(), self.visit(ctx.exp1()[0]), self.visit(ctx.exp1()[1]))
        else:
            return self.visit(ctx.exp1()[0])
    
    def visitExp1(self, ctx: BKITParser.Exp1Context):
        if ctx.ANDOP():
            return BinaryOp(ctx.ANDOP().getText(), self.visit(ctx.exp1()), self.visit(ctx.exp2()))
        elif ctx.OROP():
            return BinaryOp(ctx.OROP().getText(), self.visit(ctx.exp1()), self.visit(ctx.exp2()))
        else:
            return self.visit(ctx.exp2())
    
    def visitExp2(self, ctx: BKITParser.Exp2Context):
        if ctx.ADDOP():
            return BinaryOp(ctx.ADDOP().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        elif ctx.ADDOPDOT():
            return BinaryOp(ctx.ADDOPDOT().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        elif ctx.SUBOP():
            return BinaryOp(ctx.SUBOP().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        elif ctx.SUBOPDOT():
            return BinaryOp(ctx.SUBOPDOT().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        else:
            return self.visit(ctx.exp3())
        
    def visitExp3(self, ctx: BKITParser.Exp3Context):
        if ctx.MULOP():
            return BinaryOp(ctx.MULOP().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        elif ctx.MULOPDOT():
            return BinaryOp(ctx.MULOPDOT().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        elif ctx.DIVOP():
            return BinaryOp(ctx.DIVOP().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        elif ctx.DIVOPDOT():
            return BinaryOp(ctx.DIVOPDOT().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        elif ctx.MODOP():
            return BinaryOp(ctx.MODOP().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        else:
            return self.visit(ctx.exp4())
    
    def visitExp4(self, ctx: BKITParser.Exp4Context):
        if(ctx.NOTOP()):
            return UnaryOp(ctx.NOTOP().getText(), self.visit(ctx.exp5()))
        else:
            return self.visit(ctx.exp5())
        
    def visitExp5(self, ctx: BKITParser.Exp5Context):
        if(ctx.SUBOP()):
            return UnaryOp(ctx.SUBOP().getText(), self.visit(ctx.exp6()))
        elif (ctx.SUBOPDOT()):
            return UnaryOp(ctx.SUBOPDOT().getText(), self.visit(ctx.exp6()))
        else:
            return self.visit(ctx.exp6())

    def visitExp6(self, ctx: BKITParser.Exp6Context):
        if ctx.list_index():
            return ArrayCell(self.visit(ctx.operand()), self.visit(ctx.list_index()))
        else:
            return self.visit(ctx.operand())

    def visitOperand(self, ctx: BKITParser.OperandContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.type_list():
            return self.visit(ctx.type_list())
        elif ctx.sub_expression():
            return self.visit(ctx.sub_expression())
        elif ctx.array_id():
            return self.visit(ctx.array_id())
        elif ctx.function_call():
            return self.visit(ctx.function_call())
        elif ctx.index_operator():
            return self.visit(ctx.index_operator())

    def visitSub_expression(self, ctx: BKITParser.Sub_expressionContext):
        return self.visit(ctx.expressions())
    
    def visitFunction_call(self, ctx: BKITParser.Function_callContext):
        exp = self.visit(ctx.list_expression()) if ctx.list_expression() else []
        return CallExpr(Id(ctx.ID().getText()), exp)
    
    def visitList_expression(self, ctx: BKITParser.List_expressionContext):
        if ctx.list_expression():
            return [self.visit(ctx.expressions())] + self.visit(ctx.list_expression())
        else:
            return [self.visit(ctx.expressions())]
        
    def visitIndex_operator(self, ctx: BKITParser.Index_operatorContext):
        return ArrayCell(Id(ctx.ID().getText()), self.visit(ctx.list_index()))
    
    def visitList_index(self, ctx: BKITParser.Index_operatorContext):
        if ctx.list_index():
            return self.visit(ctx.index()) + self.visit(ctx.list_index())
        else:
            return self.visit(ctx.index())
    
    def visitIndex(self, ctx: BKITParser.IndexContext):
        return self.visit(ctx.list_expression())

    # --------------------- TYPE LIST ----------------------------
    def visitType_list(self, ctx:BKITParser.Type_listContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.array_lit():
            return self.visit(ctx.array_lit())

    def visitArray_lit(self, ctx:BKITParser.Array_litContext):
        array_lits = self.visit(ctx.array_lits()) if ctx.array_lits() else []
        return ArrayLiteral(array_lits)
    
    def visitArray_lits(self, ctx:BKITParser.Array_litsContext):
        if ctx.array_lits():
            return [self.visit(ctx.type_list())]  + self.visit(ctx.array_lits())
        else :
            return [self.visit(ctx.type_list())]
