from pglast import enums, parse_sql
from pglast.visitors import Visitor
from pglast.ast import Node
from pgcheck.models import AstParser

class Translator:
    def __init__(self):
        self._parser = AstParser()