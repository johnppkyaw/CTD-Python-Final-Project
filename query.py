import readline  # Provides command line editing and history
import sqlite3   # For SQL command execution
import sys

# Connect to the existing database
conn = sqlite3.connect("./db/baseball.db",isolation_level='IMMEDIATE')
conn.execute("PRAGMA foreign_keys = 1")

cursor = conn.cursor()

tables = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY 'name'").fetchall()
print("The tables in this database are:")
for row in tables:
    print(row[0])

def main():
    hitting_stats = [
        "Base on Balls",
        "Batting Average",
        "Doubles",
        "Hits",
        "Home Runs",
        "On Base Percentage",
        "RBI",
        "Runs",
        "Slugging Average",
        "Stolen Bases",
        "Total Bases",
        "Triples"
    ]

    pitching_stats = [
        "Complete Games",
        "ERA",
        "Games",
        "Saves",
        "Shutouts",
        "Strikeouts",
        "Winning Percentage",
        "Wins"
    ]
    
    print("Welcome to the American League player stat database! Type 'exit;' to quit.")

    while True:
        try:
            #Year selection prompt
            prompt = "Which year would you like to check from 1901-2025 (Type 'exit;' to quit.)?: "
            year_selection = input(prompt).strip().lower()

            # Check for exit command immediately
            if year_selection == "exit;" or year_selection == "exit":
                print("Exiting.")
                conn.close()
                break
            
            # Validate Year
            if not year_selection.isdigit() or not (1901 <= int(year_selection) <= 2025):
                print("Invalid input. Please enter a valid year.")
                continue

            print(f'You selected: {year_selection}.')

            #Hitter or Pitcher
            while True:
                prompt = "Would you like to search the top hitter or pitcher? (Enter 'Hitter' or 'Pitcher.'  Type 'Both' to see if a single team had both leaders.  Type 'exit' to quit): "
                player_selection = input(prompt).strip().lower().capitalize()

                if player_selection.lower() == 'exit' or player_selection.lower() == 'exit;':
                    print("Exiting.")
                    conn.close()
                    break

                if player_selection not in ['Hitter', 'Pitcher', 'Both']:
                    print("Invalid selection. Please try again.\n")
                else:
                    print(f'You selected: {player_selection}.\n')
                    break

            #Stats
            if player_selection != "Both":
                while True:
                    prompt = "Enter a specific statistic to filter (Type 'exit' to quit): "
                    stat_selection = input(prompt).strip()
                    
                    if stat_selection.lower() == 'exit' or stat_selection.lower() == 'exit;':
                        print("Exiting.")
                        conn.close()
                        break

                    if stat_selection not in hitting_stats and stat_selection not in pitching_stats:
                        print("Invalid stat. Please try again.\n")
                    else:
                        print(f'You selected: {stat_selection}.\n')
                        break

            if player_selection != "Both":
                full_command = f"""SELECT Year, Statistic, Value, Name,  Team  from {player_selection}s as p WHERE p.Year = ? AND p.Statistic = ?"""
            else:
                full_command = """
                    SELECT h.Year, h.Team, 
                           h.Name, h.Statistic, 
                           p.Name, p.Statistic
                    FROM Hitters h
                    INNER JOIN Pitchers p 
                            ON h.Team = p.Team AND h.Year = p.Year
                    WHERE h.Year = ?
                """

            # Execute the command and handle any SQL exceptions
            try:
                if player_selection == "Both":
                    cursor.execute(full_command, (year_selection,))
                else:
                    cursor.execute(full_command, (year_selection,stat_selection))
                results = cursor.fetchall()

                if not results:
                    print("No query found")
                else:
                    for row in results:
                        print(row)
                
            except sqlite3.Error as e:
                print(f"SQL Error: {e}")
            
            # Commit changes if it’s an INSERT, UPDATE, or DELETE
            conn.commit()
                
        except EOFError:  # Handle Ctrl-D (EOF) gracefully
            print("\nExiting.")
            break
        except KeyboardInterrupt:  # Handle Ctrl-C (interrupt)
            print("\nCommand canceled.")
            command_buffer = []  # Reset the command buffer

    # Clean up the database connection
    conn.close()

if __name__ == "__main__":
    main()
