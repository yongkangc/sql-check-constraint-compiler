import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from pgcheck.translator.translator import Translator

def ut_constraint_02_op_any():
    test_name = 'ut_constraint_02_op_any'
    result = False

    query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age = ANY (ARRAY[19, 20, 21, 22]) )
    );"""

    translator_obj = Translator()
    translator_obj.translate(query)

    no_violation = "INSERT INTO users(name, age) VALUES('test without violation', 20)"
    translator_obj.execute_pg(no_violation)

    try:
        violation = "INSERT INTO users(name, age) VALUES('test with violation', 1)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_ANY_ARRAY_19_20_21_22_ constraint violated'):
            result = True
        else:
            raise e

    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_02_op_any()