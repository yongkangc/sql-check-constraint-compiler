from pglast import enums
from pglast.visitors import Visitor, Delete

class PrintCheckConstraints(Visitor):
    def __call__(self, node):
        self.createstatement_node = None
        self.constraint_node = None
        self.constraint_columns = []
        super().__call__(node)

    def visit(self, ancestors, node):
        if node.__class__.__name__ == "CreateStmt":
            self.createstatement_node = node
        if node.__class__.__name__ == "Constraint":
            if node.contype == enums.ConstrType.CONSTR_CHECK:
                self.constraint_node = node
        if node.__class__.__name__ == "ColumnRef":
            self.constraint_columns.append(node.fields[0].sval)

class DeleteCheckConstraints(Visitor):
    def visit_Constraint(self, ancestors, node):
        if node.contype == enums.ConstrType.CONSTR_CHECK:
            return Delete