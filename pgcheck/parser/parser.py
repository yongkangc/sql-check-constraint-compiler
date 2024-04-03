from pglast import enums
from pglast.ast import Node, Constraint
from pglast.visitors import Visitor, Delete

from enum import Enum

class StatementType(Enum):
    CREATE = 'CREATE'
    ALTER = 'ALTER'
    
class AlterTableAction(Enum):
    ADD = 'ADD'
    DROP = 'DROP'
    
class Constraint:
    def __init__(
        self,
        statement_type: StatementType,
        statement_node: Node,
        alter_action: AlterTableAction,
        constraint_node: Constraint,
        constraint_name: str
        ):
        
        self.statement_type = statement_type
        self.statement_node = statement_node
        self.alter_action = alter_action
        self.constraint_node = constraint_node
        self.constraint_name = constraint_name
        
    def __str__(self):
        return f'''
            Statement Type: {self.statement_type}
            Action: {self.alter_action.name}
            Constraint: {self.constraint_name}
            {self.constraint_node}
        '''
        
class EmptyStatementException(Exception):
    def __init__(self):
        self.message = 'Statement has no more clauses'
        
class PrintCheckConstraints(Visitor):
    def __call__(self, node):
        self.statement_type = None
        self.statement_node = None
        self.alter_action = None
        self.constraint_nodes = []
        self.constraint_columns = []
        super().__call__(node)

    def visit(self, ancestors, node):
        # check statement type
        if node.__class__.__name__ == "CreateStmt":
            self.statement_type = StatementType.CREATE
            self.statement_node = node
        elif node.__class__.__name__ == "AlterTableStmt":
            self.statement_type = StatementType.ALTER
            self.statement_node = node
            
        # then check for action on constraint
        if self.statement_type == StatementType.ALTER and node.__class__.__name__ == "AlterTableCmd":
            
            if node.subtype == enums.parsenodes.AlterTableType.AT_AddConstraint:
                self.alter_action = AlterTableAction.ADD
                
            elif node.subtype == enums.parsenodes.AlterTableType.AT_DropConstraint:
                self.alter_action = AlterTableAction.DROP
                self.constraint_nodes.append(
                    Constraint(self.statement_type,
                               self.statement_node,
                               self.alter_action,
                               None,
                               node.name)
                )
            
        # lastly check for constraints
        if node.__class__.__name__ == "Constraint":
            if node.contype == enums.ConstrType.CONSTR_CHECK:
                self.constraint_nodes.append(
                    Constraint(self.statement_type,
                               self.statement_node,
                               self.alter_action,
                               node,
                               node.conname)
                )
        if node.__class__.__name__ == "ColumnRef":
            self.constraint_columns.append(node.fields[0].sval)

class DeleteCheckConstraints(Visitor):
    def visit_Constraint(self, ancestors, node):
        if node.contype == enums.ConstrType.CONSTR_CHECK:
            return Delete
        
    def visit_AlterTableStmt(self, ancestors, node):
        # Check if the AlterTableStmt node contains only check constraints
        has_only_check_constraints = True
        for cmd in node.cmds:
            if cmd.subtype in [enums.parsenodes.AlterTableType.AT_AddConstraint,
                               enums.parsenodes.AlterTableType.AT_DropConstraint]:
                has_only_check_constraints = False
                break

        # If AlterTableStmt contains only check constraints, delete the ancestor AlterTableStmt node
        if has_only_check_constraints:
            raise EmptyStatementException()
        
    def visit_AlterTableCmd(self, ancestors, node):
        if node.subtype in [enums.parsenodes.AlterTableType.AT_AddConstraint,
                            enums.parsenodes.AlterTableType.AT_DropConstraint]:
            return Delete
        
