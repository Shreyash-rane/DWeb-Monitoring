import requests
import csv
import os
import psycopg2
from configparser import ConfigParser

class tor_searcher:
    @staticmethod
    def torSearcher():
        try:
            # Load database connection parameters from the configuration file
            dbname, user, password, host, port = tor_searcher.load_config()

            # Connect to the PostgreSQL database
            connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            cursor = connection.cursor()

            def get_tor_session():
                session = requests.session()
                # Tor uses the 9050 port as the default socks port
                session.proxies = {'http': 'socks5h://127.0.0.1:9050',
                                'https': 'socks5h://127.0.0.1:9050'}
                return session

            # Fetch URLs from the master_table
            select_query = "SELECT id, url FROM master_table"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            for row in rows:
                id, url = row

                # Prepend "http://" to the URL if it doesn't have a scheme
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url

                # Make a request through the Tor connection
                # IP visible through Tor
                session = get_tor_session()

                try:
                    print("Getting ...", url)
                    result = session.get(url).text
                except requests.RequestException as e:
                    print(f"Error during request for {url}: {e}")

                    # Remove the row from the database if an exception occurs
                    delete_query = "DELETE FROM master_table WHERE id = %s"
                    cursor.execute(delete_query, (id,))

                    # Print debug information
                    print(f"Data removed from the database for ID {id} and URL {url}")

                    # Commit the transaction
                    connection.commit()

                    continue  # Skip to the next URL in case of an error

                # Update the row in the database with the result
                update_query = "UPDATE master_table SET result = %s WHERE id = %s"
                cursor.execute(update_query, (result, id))
                connection.commit()

                print(f"Data updated in the database for ID {id} and URL {url}")

        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")
        finally:
            # Close the database connection
            if connection:
                connection.close()


    @staticmethod
    def load_config(filename='ahima/database/database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            return (
                parser.get(section, 'dbname'),
                parser.get(section, 'user'),
                parser.get(section, 'password'),
                parser.get(section, 'host'),
                parser.get(section, 'port')
            )
        else:
            raise Exception(f'Section {section} is not found in the {filename} file.')

# Example usage
tor_searcher.torSearcher()
print("Code executed successfully.")
