from pgcheck.evaluation.performance import *


def perform_performance_test():
    evaluator = PerformanceEvaluator()
    sql_statements = {}
    n = 500

    ''' Comparison Operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age > 19)
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' ANY operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age = ANY (ARRAY[19, 20, 21, 22]) )
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' ALL operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age > ALL (ARRAY[2, 3, 18, 19]) )
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' NULLIF operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (NULLIF(age, 4) IS NOT NULL)
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' IN operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age IN (19,20,21))
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' LIKE operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (name LIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' ILIKE operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (name ILIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('TEST without violation', 20)"] * n

    ''' SIMILAR TO operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (name SIMILAR TO 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' BETWEEN operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age BETWEEN 10 AND 30)
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' NOT BETWEEN operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age NOT BETWEEN 0 AND 5)
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' AND operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age >= 20 AND name LIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    ''' OR operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age >= 20 OR name LIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test with age violation only', 1)"] * n 

    ''' NOT operator '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (NOT age < 10)
    );"""] = ["INSERT INTO users(name, age) VALUES('without violation', 20)"] * n

    ''' Alter Add '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER
    );
    ALTER TABLE users
    ADD CHECK (age > 18);"""] = ["INSERT INTO users(name, age) VALUES('without violation', 20)"] * n

    ''' Alter Drop '''
    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CONSTRAINT age_check CHECK (age > 18)
    );
    ALTER TABLE users
    DROP CONSTRAINT age_check;"""] = ["INSERT INTO users(name, age) VALUES('without violation', 20)"] * n
    
    fp1 = evaluator.evaluate_performance(sql_statements, translated=False)
    fp2 = evaluator.evaluate_performance(sql_statements)

    evaluator.generate_dashboard(n)

    return fp1, fp2
