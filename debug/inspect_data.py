import os
import click
import sqlite3
import pandas as pd

conn = sqlite3.connect("db/messages.db", check_same_thread=False)
cursor = conn.cursor()

@click.group()
def cli():
    pass

@cli.command("size")
def show_db_size():
    cursor.execute("SELECT COUNT(*) FROM messages")
    print("There are {} messages in the database".format(cursor.fetchone()[0]))

@cli.command("show_pd")
@click.option("--n", default=10, help="Number of messages to show")
def show_last_n(n=10):
    df = pd.read_sql_query("SELECT * FROM messages ORDER BY timestamp DESC LIMIT {}".format(n), conn)
    print(df)

@cli.command("show")
@click.option("--n", default=10, help="Number of messages to show")
def show_last_n_human(n=10):
    df = pd.read_sql_query("SELECT * FROM messages ORDER BY timestamp DESC LIMIT {}".format(n), conn)
    print("hello")
    for i, row in df.iterrows():
        print("Timestamp: {}".format(row["timestamp"]))
        print("User: {}".format(row["username"]))
        print("Prompt: {}".format(row["prompt"]))
        print("Response: {}".format(row["response"]))
        # make a line
        print("-" * 80)
        print("")

@click.command("reset")
def reset_db():
    os.system("scripts/reset_database.sh")
