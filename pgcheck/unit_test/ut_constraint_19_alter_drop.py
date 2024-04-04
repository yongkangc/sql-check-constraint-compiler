import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from pgcheck.translator.translator import Translator

def ut_constraint_19_alter_drop():
    test_name = 'ut_constraint_19_alter_drop'
    result = False

    create_query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CONSTRAINT age_check CHECK (age > 18)
    );"""
    
    alter_query = '''
    ALTER TABLE users
    DROP CONSTRAINT age_check;
    '''

    translator_obj = Translator()
    translator_obj.translate(create_query)

    no_violation = "INSERT INTO users(name, age) VALUES('without violation', 1)"
    try:
        translator_obj.execute_pg(no_violation)
    except Exception as e:
        if str(e).startswith('age_check constraint violated'):
            pass
        else:
            raise e
    else:
        raise Exception()
        
    translator_obj.translate(alter_query)

    try:
        violation = "INSERT INTO users(name, age) VALUES('with violation', 1)"
        translator_obj.execute_pg(violation)
    except Exception as e:
        raise e
    else:
        result = True

    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_19_alter_drop()