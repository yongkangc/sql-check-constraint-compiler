import time
import psutil
import os
from pgcheck.translator import perform_translation


class PerformanceEvaluator:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def evaluate_performance(self, sql_statements):
        results = []

        for sql in sql_statements:
            start_time = time.time()
            start_memory = self.process.memory_info().rss

            perform_translation(sql)

            end_time = time.time()
            end_memory = self.process.memory_info().rss

            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory

            result = {
                'sql': sql,
                'execution_time': execution_time,
                'memory_usage': memory_usage
            }
            results.append(result)

        return results

    def generate_report(self, results):
        total_execution_time = sum(
            result['execution_time'] for result in results)
        total_memory_usage = sum(result['memory_usage'] for result in results)

        average_execution_time = total_execution_time / len(results)
        average_memory_usage = total_memory_usage / len(results)

        report = f"""
        Performance Evaluation Report:
        Total SQL Statements: {len(results)}
        Total Execution Time: {total_execution_time:.2f} seconds
        Average Execution Time: {average_execution_time:.2f} seconds
        Total Memory Usage: {total_memory_usage} bytes
        Average Memory Usage: {average_memory_usage} bytes
        """

        return report
