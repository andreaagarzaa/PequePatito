# Generated from C:/Users/andre/PycharmProjects/littleDuck/PequePatito.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PequePatitoParser import PequePatitoParser
else:
    from PequePatitoParser import PequePatitoParser

# This class defines a complete generic visitor for a parse tree produced by PequePatitoParser.

class PequePatitoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PequePatitoParser#programa.
    def visitPrograma(self, ctx:PequePatitoParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#p.
    def visitP(self, ctx:PequePatitoParser.PContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#v.
    def visitV(self, ctx:PequePatitoParser.VContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#f.
    def visitF(self, ctx:PequePatitoParser.FContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#vars.
    def visitVars(self, ctx:PequePatitoParser.VarsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#var_declaracion.
    def visitVar_declaracion(self, ctx:PequePatitoParser.Var_declaracionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#id_list.
    def visitId_list(self, ctx:PequePatitoParser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#vars_list.
    def visitVars_list(self, ctx:PequePatitoParser.Vars_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#funcs.
    def visitFuncs(self, ctx:PequePatitoParser.FuncsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#params.
    def visitParams(self, ctx:PequePatitoParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#cuerpo.
    def visitCuerpo(self, ctx:PequePatitoParser.CuerpoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#estatutos.
    def visitEstatutos(self, ctx:PequePatitoParser.EstatutosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#estatuto.
    def visitEstatuto(self, ctx:PequePatitoParser.EstatutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#asigna.
    def visitAsigna(self, ctx:PequePatitoParser.AsignaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#imprime.
    def visitImprime(self, ctx:PequePatitoParser.ImprimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#p_imp.
    def visitP_imp(self, ctx:PequePatitoParser.P_impContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#condicion.
    def visitCondicion(self, ctx:PequePatitoParser.CondicionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#else_part.
    def visitElse_part(self, ctx:PequePatitoParser.Else_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#ciclo.
    def visitCiclo(self, ctx:PequePatitoParser.CicloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#llamada.
    def visitLlamada(self, ctx:PequePatitoParser.LlamadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#expresion.
    def visitExpresion(self, ctx:PequePatitoParser.ExpresionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#exp.
    def visitExp(self, ctx:PequePatitoParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#termino.
    def visitTermino(self, ctx:PequePatitoParser.TerminoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#bo.
    def visitBo(self, ctx:PequePatitoParser.BoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#factor.
    def visitFactor(self, ctx:PequePatitoParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#f_otro.
    def visitF_otro(self, ctx:PequePatitoParser.F_otroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#tipo.
    def visitTipo(self, ctx:PequePatitoParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PequePatitoParser#cte.
    def visitCte(self, ctx:PequePatitoParser.CteContext):
        return self.visitChildren(ctx)



del PequePatitoParser