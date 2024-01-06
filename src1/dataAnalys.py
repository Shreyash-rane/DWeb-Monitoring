import psycopg2
from bs4 import BeautifulSoup
import re
from configparser import ConfigParser

class DataAnalyzer:
    def __init__(self, dbname, user, password, host, port):
        # Connect to the PostgreSQL database
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

        # Create the analytic_table if not exists
        self.create_analytic_table()

    def create_analytic_table(self):
        try:
            create_analytic_table_query = """
                CREATE TABLE IF NOT EXISTS analytic_table (
                    url TEXT,
                    email TEXT,
                    username TEXT,
                    links TEXT[]
                );
            """
            self.cursor.execute(create_analytic_table_query)
            self.connection.commit()
        except Exception as e:
            print(f"Error creating analytic_table: {e}")

    def analyze_data(self, batch_size=100):
        try:
            # Fetch a batch of rows where result is not null
            select_query = f"SELECT id, url, result FROM master_table WHERE result IS NOT NULL LIMIT {batch_size}"
            self.cursor.execute(select_query)
            rows = self.cursor.fetchall()

            if not rows:
                print("No rows found where result is not null.")
                return

            for row in rows:
                id, url, result = row
                print(f"Analyzing data for URL {url} with ID {id}")

                # Perform data analysis on the HTML content
                emails, usernames, links = self.extract_information(result)

                if not emails and not usernames:
                    print(f"No emails or usernames found for URL {url}")
                    continue

                # Insert the extracted data into analytic_table
                insert_analytic_query = "INSERT INTO analytic_table (url, email, username, links) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(insert_analytic_query, (url, emails, usernames, links))
                self.connection.commit()

                print(f"Data inserted into analytic_table for URL {url}")

        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    def extract_information(self, html_content):
        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract emails using a regular expression
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = list(set(re.findall(email_pattern, html_content)))

        # Extract usernames (modify this based on your HTML structure)
        usernames = [element.text.strip() for element in soup.find_all('span', class_='username')]

        # Extract links
        links = self.extract_links(soup)

        return emails, usernames, links

    def extract_links(self, soup):
        # Extract links (modify this based on your HTML structure)
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

    def __del__(self):
        # Close the database connection when the object is destroyed
        self.cursor.close()
        self.connection.close()

    @staticmethod
    def load_config(filename='ahima/database/database.ini', section='postgresql'):
        # Load database configuration from the configuration file
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

# Example usage:
if __name__ == '__main__':
    # Replace these values with your actual database credentials
    dbname, user, password, host, port = DataAnalyzer.load_config()

    # Create an instance of DataAnalyzer
    data_analyzer = DataAnalyzer(dbname, user, password, host, port)

    # Analyze the data and update the database
    data_analyzer.analyze_data()
