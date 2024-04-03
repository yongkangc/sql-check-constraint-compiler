import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from pgcheck.translator.translator import Translator

def ut_simple_query():
    test_name = 'ut_simple_query'
    result = True

    simple_query = """CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INTEGER,
    size INTEGER,
    CHECK (age > ANY(ARRAY[1, 2, 3]) AND size < 2.5));"""
    
    translator_obj = Translator()
    translator_obj.translate(simple_query)

    no_violation = "INSERT INTO users(name, age) VALUES('without violation', 20)"
    translator_obj.execute_pg(no_violation)

    try:
        violation = "INSERT INTO users(name, age) VALUES('with violation', 1)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_ANY_ARRAY_1_2_3_AND_size_2_5 constraint violated'):
            result = True
        else:
            raise e

    if result:
        print(test_name, ' ok.')
    return test_name, result

if __name__ == "__main__":
    ut_simple_query()