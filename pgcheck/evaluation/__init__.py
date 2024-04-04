from pgcheck.evaluation.performance import *


def perform_performance_test():
    evaluator = PerformanceEvaluator()
    sql_statements = {}
    n = 100

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (name LIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (name ILIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('TEST without violation', 20)"] * n

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (name SIMILAR TO 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age BETWEEN 10 AND 30)
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age NOT BETWEEN 0 AND 5)
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age >= 20 AND name LIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test without violation', 20)"] * n

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (age >= 20 OR name LIKE 'test%')
    );"""] = ["INSERT INTO users(name, age) VALUES('test with age violation only', 1),('with name violation only', 20)"] * n 

    sql_statements["""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER,
        size INTEGER,
        CHECK (NOT age < 10)
    );"""] = ["INSERT INTO users(name, age) VALUES('without violation', 20)"] * n
    
    fp1 = evaluator.evaluate_performance(sql_statements, translated=False)
    fp2 = evaluator.evaluate_performance(sql_statements)

    evaluator.generate_dashboard()

    return fp1, fp2
