import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from pgcheck.translator.translator import Translator

def ut_constraint_18_alter_add():
    test_name = 'ut_constraint_18_alter_add'
    result = False

    create_query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER
    );"""
    
    alter_query = '''
    ALTER TABLE users
    ADD CHECK (age > 18);
    '''

    translator_obj = Translator()
    translator_obj.translate(create_query)

    no_violation = "INSERT INTO users(name, age) VALUES('without violation', 1)"
    translator_obj.execute_pg(no_violation)
    
    translator_obj.translate(alter_query)

    try:
        violation = "INSERT INTO users(name, age) VALUES('with violation', 1)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        if str(e).startswith('age_18 constraint violated'):
            result = True
        else:
            raise e

    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_18_alter_add()