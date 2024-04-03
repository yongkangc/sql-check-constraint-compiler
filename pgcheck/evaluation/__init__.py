from pgcheck.evaluation.performance import *


def perform_performance_test(report: str):
    evaluator = PerformanceEvaluator()
    sql_statements = [
        '''
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            salary DECIMAL(10, 2),
            hire_date DATE,
            department VARCHAR(50),
            CHECK (salary > 0),
            CHECK (hire_date <= CURRENT_DATE),
            CHECK (email LIKE '%@company.com')
        )
        ''',
        # ... (include the rest of the SQL statements)
    ]

    results = evaluator.evaluate_performance(sql_statements)
    report_content = evaluator.generate_report(results)

    with open(report, 'w') as file:
        file.write(report_content)
