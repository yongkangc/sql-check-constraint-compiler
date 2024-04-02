import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from pgcheck.translator.translator import Translator

def ut_constraint_15_and():
    test_name = 'ut_constraint_15_and'
    result = False
    test_1 = False
    test_2 = False
    test_3 = False

    query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age >= 20 AND name LIKE 'test%')
    );"""

    translator_obj = Translator()
    translator_obj.translate(query)

    no_violation = "INSERT INTO users(name, age) VALUES('test without violation', 20)"
    translator_obj.execute_pg(no_violation)

    try:
        violation = "INSERT INTO users(name, age) VALUES('name violation', 20)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_20_AND_name_LIKE_test_ constraint violated'):
            test_1 = True
        else:
            raise e

    try:
        violation = "INSERT INTO users(name, age) VALUES('test age violation', 1)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_20_AND_name_LIKE_test_ constraint violated'):
            test_2 = True
        else:
            raise e

    try:
        violation = "INSERT INTO users(name, age) VALUES('name and age violation', 1)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_20_AND_name_LIKE_test_ constraint violated'):
            test_3 = True
        else:
            raise e

    result = test_1 and test_2 and test_3
    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_15_and()