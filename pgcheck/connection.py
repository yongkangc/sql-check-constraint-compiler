import psycopg2

def perform_connection(database="postgres", username="postgres", password="Chelicia123!@#", host="localhost", port="5432"):
    # Implementation for database connection
    return psycopg2.connect(database=database, user=username, password=password, host=host, port=port)
