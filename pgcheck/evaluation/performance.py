import time
import psutil
import os
import pandas as pd
import matplotlib.pyplot as plt
from pgcheck.translator import perform_translation
from pgcheck.translator.translator import Translator


class PerformanceEvaluator:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.data = pd.DataFrame()
        self.translated_data = pd.DataFrame()

    def evaluate_performance(self, sql_statements, translated = True):
        results = []
        translator = Translator()
        name = ['t', '0'] if translated else ['n' , '0']
        i = 1

        for create_stmt, insert_stmt in sql_statements.items():
            name[1] = str(i)

            create_start_time = time.time()
            create_start_memory = self.process.memory_info().rss

            if translated:
                perform_translation(create_stmt)
            else:
                translator.execute_pg(create_stmt)
            
            create_end_time = time.time()
            create_end_memory = self.process.memory_info().rss

            create_time = create_end_time - create_start_time
            create_memory_usage = create_end_memory - create_start_memory

            for stmt in insert_stmt:
                time.sleep(.1)
                insert_start_time = time.time()
                insert_start_memory = self.process.memory_info().rss

                translator.execute_pg(stmt)

                insert_end_time = time.time()
                insert_end_memory = self.process.memory_info().rss

                insert_time = insert_end_time - insert_start_time
                insert_memory_usage = insert_end_memory - insert_start_memory
                result = {
                    'test': ''.join(name),
                    'create_table_time' : create_time,
                    'create_table_memory' : create_memory_usage,
                    'insertion_time': insert_time,
                    'insert_memory_usage': insert_memory_usage
                }
                results.append(result)

                if translated:
                    self.translated_data = pd.concat((self.translated_data, pd.DataFrame(data=result, index=[0])), ignore_index = True)
                else:
                    self.data = pd.concat((self.data, pd.DataFrame(data=result, index=[0])), ignore_index = True)

            i += 1

        filepath = 'performance_report.txt' if not translated else 'performance_report_translated.txt'
        
        self.generate_report(results, filepath)
        return filepath

    def generate_report(self, results, filepath):
        total_create_time = sum(
            result['create_table_time'] for result in results) / (len(results) / 8)
        total_create_memory = sum(
            result['create_table_memory'] for result in results) / (len(results) / 8)
        total_execution_time = sum(
            result['insertion_time'] for result in results)
        total_memory_usage = sum(result['insert_memory_usage'] for result in results)

        average_execution_time = total_execution_time / len(results)
        average_memory_usage = total_memory_usage / len(results)

        report = f"""
        Performance Evaluation Report:
        
        Total Time Used In Creating Table: {total_create_time:.2f} seconds
        Total Execution Time For Insert Queries: {total_execution_time:.2f} seconds
        Average Execution Time For Insert Queries: {average_execution_time:.2f} seconds

        Total Memory Used In Creating Table: {total_create_memory} bytes
        Total Memory Usage For Insert Queries: {total_memory_usage} bytes
        Average Memory Usage For Insert Queries: {average_memory_usage} bytes
        """

        with open(filepath, 'w') as file:
            file.write(report)

        return filepath
    
    def generate_dashboard(self):
        n = 100

        def plot_create_table_time():
            plt.plot(list(range(int(len(self.data) / n))), self.data.loc[::n, 'create_table_time'], color='grey')
            plt.plot(list(range(int(len(self.translated_data) / n))), self.translated_data.loc[::n, 'create_table_time'], color='red')

            plt.title("Plot of time taken to create table across different unit tests", fontsize = 8)
            plt.ylabel("Time taken (seconds)")
            plt.legend(['Original', 'Translated'])
            plt.savefig('./create_table_time.png')
            plt.close()

        def plot_insert_time():
            plt.plot(list(range(int(len(self.data) / n))), self.data.groupby('test')['insertion_time'].mean(), color='grey')
            plt.plot(list(range(int(len(self.translated_data) / n))), self.translated_data.groupby('test')['insertion_time'].mean(), color='red')

            plt.title("Plot of average time taken to insert individual records across different unit tests", fontsize = 8)
            plt.ylabel("Time taken (seconds)")
            plt.legend(['Original', 'Translated'])
            plt.savefig('./insert_time.png')
            plt.close()

        def plot_create_table_memory():
            plt.plot(list(range(int(len(self.data) / n))), self.data.loc[::n, 'create_table_memory'], color='grey')
            plt.plot(list(range(int(len(self.translated_data) / n))), self.translated_data.loc[::n, 'create_table_memory'], color='red')

            plt.title("Plot of memory used to create table across different unit tests", fontsize = 8)
            plt.ylabel("Memory Usage (bytes)")
            plt.yticks(fontsize=8)
            plt.legend(['Original', 'Translated'])
            plt.savefig('./create_table_memory.png')
            plt.close()

        def plot_insert_memory():
            plt.plot(list(range(int(len(self.data) / n))), self.data.groupby('test')['insert_memory_usage'].mean(), color='grey')
            plt.plot(list(range(int(len(self.translated_data) / n))), self.translated_data.groupby('test')['insert_memory_usage'].mean(), color='red')

            plt.title("Plot of average memory used to insert individual records across different unit tests", fontsize = 8)
            plt.ylabel("Memory Usage (bytes)")
            plt.legend(['Original', 'Translated'])
            plt.savefig('./insert_memory.png')
            plt.close()

        plot_create_table_time()
        plot_insert_time()
        plot_create_table_memory()
        plot_insert_memory()

