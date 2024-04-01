from pglast import enums, parse_sql
from pglast.visitors import Visitor
from pglast.ast import Node, Constraint, A_Expr, BoolExpr
from pglast.enums.primnodes import BoolExprType
from pglast.enums.parsenodes import A_Expr_Kind

from typing import List

from pgcheck.exceptions.TranslatorException import EmptyNameException

# Visitor classes
class GetCheckConstraints(Visitor):
    def __init__(self):
        super().__init__()
        self.check_constraints = []
    
    def __call__(self, node):
        super().__call__(node)

    def visit(self, ancestors, node):
        if node.__class__.__name__ == "Constraint":
            if node.contype == enums.ConstrType.CONSTR_CHECK:
                self.check_constraints.append(node)
                
    def get_check_constraints(self) -> List[Constraint]:
        return self.check_constraints
                
                
# AST Parser Wrapper class
class AstParser:
    
    def get_all_check_constraints(self, root: Node) -> List[Constraint]:
        '''
        To get all the check constraints that exist in a query
        '''
        constraints_getter = GetCheckConstraints()
        constraints_getter(root)
        return constraints_getter.get_check_constraints()
    
    def handle_node(self, node: Node) -> str:
        node_class = node.__class__.__name__
        
        match node_class:
            case "Integer":
                return str(node.ival)
            case "Float":
                return str(node.fval)
            case "String":
                return node.sval
            case "A_Const":
                return self.handle_node(node.val)
            case "ColumnRef":
                column_name = self.extract_value(node.fields)
                return f'NEW.{column_name}'
            case "BoolExpr":
                return self.translate_boolexpr(node)
            case "A_Expr":
                return self.translate_a_expr(node)
    
    def translate_boolexpr(self, node: BoolExpr) -> str:
        kind = node.boolop
        expressions = [self.handle_node(n) for n in node.args]

        match kind:
            case BoolExprType.AND_EXPR:
                return ' AND '.join(expressions)
            case BoolExprType.OR_EXPR:
                return ' OR '.join(expressions)
            case BoolExprType.NOT_EXPR:
                return f"NOT ({expressions[0]})"
            
    def extract_value(self, iterable: tuple) -> str:
        try:
            comp_node = iterable[0]
        except (TypeError, IndexError) as e:
            raise EmptyNameException()
        
        return self.handle_node(comp_node)
    
    def translate_a_expr(self, node: A_Expr) -> str:
        kind = node.kind
        lexpr = self.handle_node(node.lexpr)
        rexpr = self.handle_node(node.rexpr)

        if kind == A_Expr_Kind.AEXPR_OP:
            comp = self.extract_value(node.name)
            return f"{lexpr} {comp} {rexpr}"
        elif kind == A_Expr_Kind.AEXPR_OP_ANY:
            comp = self.extract_value(node.name)
            return f"{lexpr} {comp} ANY ({rexpr})"
        elif kind == A_Expr_Kind.AEXPR_OP_ALL:
            comp = self.extract_value(node.name)
            return f"{lexpr} {comp} ALL ({rexpr})"
        elif kind == A_Expr_Kind.AEXPR_DISTINCT:
            return f"{lexpr} IS DISTINCT FROM {rexpr}"
        elif kind == A_Expr_Kind.AEXPR_NOT_DISTINCT:
            return f"{lexpr} IS NOT DISTINCT FROM {rexpr}"
        elif kind == A_Expr_Kind.AEXPR_NULLIF:
            return f"NULLIF({lexpr}, {rexpr})"
        elif kind == A_Expr_Kind.AEXPR_IN:
            return f"{lexpr} IN ({rexpr})"
        elif kind == A_Expr_Kind.AEXPR_LIKE:
            return f"{lexpr} LIKE {rexpr}"
        elif kind == A_Expr_Kind.AEXPR_ILIKE:
            return f"{lexpr} ILIKE {rexpr}"
        elif kind == A_Expr_Kind.AEXPR_SIMILAR:
            return f"{lexpr} SIMILAR TO {rexpr}"
        elif kind in [A_Expr_Kind.AEXPR_BETWEEN, A_Expr_Kind.AEXPR_NOT_BETWEEN]:
            return f"{lexpr} {'NOT ' if kind == 'AEXPR_NOT_BETWEEN' else ''}BETWEEN {rexpr[0]} AND {rexpr[1]}"
        elif kind in [A_Expr_Kind.AEXPR_BETWEEN_SYM,\
                      A_Expr_Kind.AEXPR_NOT_BETWEEN_SYM]:
            return f"{lexpr} {'NOT ' if kind == 'AEXPR_NOT_BETWEEN_SYM' else ''}SYMMETRIC BETWEEN {rexpr[0]} AND {rexpr[1]}"
    
    def translate_constraint_into_expression(
        self,
        constraint: Constraint) -> str:
        return self.handle_node(constraint.raw_expr)