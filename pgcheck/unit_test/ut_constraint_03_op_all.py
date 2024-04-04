import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from pgcheck.translator.translator import Translator

def ut_constraint_03_op_all():
    test_name = 'ut_constraint_03_op_all'
    result = False

    query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age > ALL (ARRAY[2, 3, 18, 19]) )
    );"""

    translator_obj = Translator()
    translator_obj.translate(query)

    no_violation = "INSERT INTO users(name, age) VALUES('test without violation', 20)"
    translator_obj.execute_pg(no_violation)

    try:
        violation = "INSERT INTO users(name, age) VALUES('test with violation', 4)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_ALL_ARRAY_2_3_18_19_ constraint violated'):
            result = True
        else:
            raise e

    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_03_op_all()