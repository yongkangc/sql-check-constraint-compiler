import re
import psycopg2
from pglast import enums, parse_sql
from pglast.parser import ParseError
from pglast.stream import RawStream

from pgcheck.parser.parser import (
    PrintCheckConstraints,
    DeleteCheckConstraints,
    StatementType,
    AlterTableAction,
    EmptyStatementException
)
from pgcheck.connection import perform_connection


class Translator():
    def __init__(self):
        self.conn = None
        self.connect_pg()

        self.operator_mapping = {'>=': 'MTET', '>': 'MT',
                                 '<=': 'LTET', '<': 'LT',
                                 '=': 'ET'}

    def connect_pg(self):
        self.conn = perform_connection()

    def execute_pg(self, query):
        self.connect_pg()
        with self.conn.cursor() as cur:
            cur.execute(query)
            print(query)

        self.conn.commit()
        self.conn.close()

    def execute_create_table(self, table_name, query):
        query = f"""
            DROP TABLE IF EXISTS {table_name};
            {query}
        """
        self.execute_pg(query)
        
    def execute_alter_table(self, query):
        self.execute_pg(query)

    def translate(self, query):
        try:
            root = parse_sql(query)
        except ParseError:
            print("This SQL statement is invalid.")
            raise

        print_constraints = PrintCheckConstraints()
        print_constraints(root)
        
        # assuming only 1 transaction per query
        # parser statement type should be consistent for all constraints
        
        table_name = print_constraints.statement_node.relation.relname
        
        # constraint_lhs = print_constraints.constraint_node.raw_expr.lexpr.fields[0].sval
        # constraint_operator = print_constraints.constraint_node.raw_expr.name[0].sval
        # constraint_rhs = str(print_constraints.constraint_node.raw_expr.rexpr.val.ival)

        original_statement = RawStream()(root)
        try:
            DeleteCheckConstraints()(root)
        except EmptyStatementException:
            root = None
        
        modified_statement = RawStream()(root) if root else None

        if print_constraints.statement_type == StatementType.CREATE:
            original_statement
            self.execute_create_table(
                table_name+'_orig', original_statement.replace(table_name, table_name+'_orig'))
            self.execute_create_table(table_name, modified_statement)
            
        elif print_constraints.statement_type == StatementType.ALTER:
            self.execute_alter_table(
                original_statement.replace(table_name, table_name+'_orig'))
            
            if root:
                self.execute_create_table(table_name, modified_statement)

        constraint_columns = list(set(print_constraints.constraint_columns))
        
        for node in print_constraints.constraint_nodes:
            
            if node.statement_type == StatementType.CREATE or \
                (node.statement_type == StatementType.ALTER and \
                    node.alter_action == AlterTableAction.ADD):
                    
                constraint_name, constraint_node = node.constraint_name, node.constraint_node
                constraint_statement = RawStream()(constraint_node.raw_expr)
                self.translate_sql_template(
                    table_name, constraint_statement, constraint_columns, constraint_name)
                
            elif node.statement_type == StatementType.ALTER and \
                node.alter_action == AlterTableAction.DROP:
                    self.remove_trigger(node.constraint_name, table_name)

    def translate_sql_template(self, table_name, constraint_statement, constraint_columns, constraint_name):

        print(constraint_columns)
        constraint_clause = constraint_statement
        for col in constraint_columns:
            constraint_clause = constraint_clause.replace(col, 'NEW.'+col)

        if constraint_name is None:
            constraint_name = constraint_statement
            for key, value in self.operator_mapping.items():
                constraint_name = constraint_name.replace(key, value)
            constraint_name = re.sub('[^0-9a-zA-Z]+', '_', constraint_statement)

        function_name = 'func_' + constraint_name
        function_sql = f"""
            CREATE OR REPLACE FUNCTION {function_name}()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NOT ({constraint_clause}) THEN
                    RAISE EXCEPTION '{constraint_name} constraint violated';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """
        self.execute_pg(function_sql)

        trigger_name = 'trig_' + constraint_name
        trigger_sql = f"""
            CREATE CONSTRAINT TRIGGER {trigger_name}
            AFTER INSERT OR UPDATE ON {table_name}
            DEFERRABLE INITIALLY DEFERRED
            FOR EACH ROW
            EXECUTE FUNCTION {function_name}();
        """
        self.execute_pg(trigger_sql)
        
    def remove_trigger(self, constraint_name, table_name):
        function_name = 'func_' + constraint_name
        trigger_name = 'trig_' + constraint_name
        
        remove_trigger_sql = f'DROP TRIGGER IF EXISTS {trigger_name} ON {table_name};'
        self.execute_pg(remove_trigger_sql)
        
        remove_function_sql = f'DROP FUNCTION IF EXISTS {function_name}();'
        self.execute_pg(remove_function_sql)