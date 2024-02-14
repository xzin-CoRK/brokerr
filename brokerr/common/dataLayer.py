import os
import sqlite3
from contextlib import closing
from redis import Redis
from config.settings import REDIS_URL

redis = Redis.from_url(REDIS_URL)

def setup_database():
    # Create the base directory for screenshots
    screenshots_directory = '/config/screenshots'

    if not os.path.exists(screenshots_directory):
        try:
            os.makedirs(screenshots_directory)
            print(f"Directory '{screenshots_directory}' created.")
        except OSError as e:
            print(f"Error creating directory '{screenshots_directory}': {e}")

    # Create the sqlite database
    with closing(sqlite3.connect('/config/brokerr.db')) as connection:
        with closing(connection.cursor()) as cursor:
            # Create trackers table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS trackers(tracker TEXT PRIMARY KEY, last_insured INTEGER, num_insured INTEGER, favicon_path TEXT)")
            # Create insurance table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS insurance(
                    tracker TEXT,
                    insurance_date INTEGER,
                    image_path TEXT,
                    FOREIGN KEY (tracker) REFERENCES trackers(tracker)
                )
            ''')

            cursor.execute('''
                CREATE TRIGGER IF NOT EXISTS update_trackers
                AFTER INSERT ON insurance
                FOR EACH ROW
                BEGIN
                    -- Check if there is an existing record in trackers
                    INSERT OR IGNORE INTO trackers (tracker) VALUES (NEW.tracker);
                           
                    -- Increment the num_insured field in trackers
                    UPDATE trackers
                    SET num_insured = COALESCE(num_insured, 0) + 1
                    WHERE tracker = NEW.tracker;

                    -- Update last_insured in trackers with the maximum insurance_date from insurance
                    UPDATE trackers
                    SET last_insured = NEW.insurance_date
                    WHERE tracker = NEW.tracker;
                END;
            ''')

            connection.commit()


def get_recent_insurance(tracker: str) -> list:
    results = []

    with closing(sqlite3.connect('/config/brokerr.db', isolation_level=None)) as connection:
        with closing(connection.cursor()) as cursor:
            # Create insurance table if it doesn't exist
            res = cursor.execute("SELECT insurance_date, image_path FROM insurance WHERE tracker = ? ORDER BY insurance_date DESC LIMIT 10", (tracker,))
            results = res.fetchall()

    return results


def get_tracker_stats(tracker: str) -> any:

    with closing(sqlite3.connect('/config/brokerr.db', isolation_level=None)) as connection:
        with closing(connection.cursor()) as cursor:
            # Create insurance table if it doesn't exist
            res = cursor.execute("SELECT last_insured, num_insured FROM trackers WHERE tracker = ?", (tracker,))
            return res.fetchone()


def store_success(tracker, timestamp, image_path):
    with closing(sqlite3.connect('/config/brokerr.db', isolation_level=None)) as connection:
        with closing(connection.cursor()) as cursor:
            # Create insurance table if it doesn't exist
            query = "INSERT INTO insurance(tracker, insurance_date, image_path) VALUES(?, ?, ?)"
            cursor.execute(query, (tracker, timestamp, image_path))


def get_trackers_without_favicon():
    with closing(sqlite3.connect('/config/brokerr.db', isolation_level=None)) as connection:
        with closing(connection.cursor()) as cursor:
            res = cursor.execute("SELECT tracker FROM trackers WHERE favicon_path IS NULL")
            return res.fetchall()