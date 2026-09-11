class DictionaryCRUD:
    
    def __init__(self):
        # Initialize an empty dictionary to store records
        self.data_store = {}

    def insert(self, key: str, value: dict) -> str:
        """Inserts a new record. Fails if the key already exists."""
        if key in self.data_store:
            return f"Error: Key '{key}' already exists."
        
        self.data_store[key] = value
        return f"Success: Inserted '{key}'."

    def read(self, key: str):
        """Retrieves a record by its key."""
        # Returns None if the key doesn't exist
        return self.data_store.get(key, f"Error: Key '{key}' not found.")

    def update(self, key: str, new_value: dict) -> str:
        """Updates an existing record. Fails if the key doesn't exist."""
        if key not in self.data_store:
            return f"Error: Key '{key}' not found. Cannot update."
        
        # Using dict.update() to merge or overwrite the values
        self.data_store[key].update(new_value)
        return f"Success: Updated '{key}'."

    def delete(self, key: str) -> str:
        """Removes a record from the dictionary."""
        if key in self.data_store:
            del self.data_store[key]
            return f"Success: Deleted '{key}'."
        return f"Error: Key '{key}' not found."

    def display_all(self):
        """Helper method to see the entire dictionary."""
        return self.data_store

def insertData():

        # 1. INSERT (Create)
    print(db.insert("emp_101", {"name": "Alice", "role": "Engineer"}))
    print(db.insert("emp_102", {"name": "Bob", "role": "Designer"}))
    
    # 2. READ
    print("\nRead emp_101:", db.read("emp_101"))
    
    # 3. UPDATE
    print("\nUpdate emp_101:", db.update("emp_101", {"role": "Senior Engineer", "location": "NY"}))
    print("Read emp_101 after update:", db.read("emp_101"))
    
    # 4. DELETE
    print("\nDelete emp_102:", db.delete("emp_102"))
    
    # Display final state
    print("\nFinal Data Store:", db.display_all())

def instart Data(keysList, valuesList)

    list1 = ["a", "b", "c"]
    list2 = [1, 2, 3, 4]  # Intentional size mismatch for testing

    try:
        # Check if the lengths are equal before creating the dictionary
        if len(list1) != len(list2):
            raise ValueError("Size not equal")

        # Create the dictionary using inline zip notation
        my_dict = dict(zip(list1, list2))
        print("Dictionary created:", my_dict)

    except ValueError as e:
        print(e)


def create_word_dict(keys: list, words: list) -> dict:
    try:
        # Check if the sizes are not equal
        if len(keys) != len(words):
            raise ValueError("sizeNotEqual: The number of keys and words must be the same.")
            
    except ValueError as sizeNotEqual:
        # Catch the specific size mismatch exception
        print(f"Caught an error: {sizeNotEqual}")
        
    finally:
        # The finally block always runs and returns the dictionary mapping
        return dict(zip(keys, words))

    
# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the CRUD manager
    db = DictionaryCRUD()

    # 1. INSERT (Create)
    print(db.insert("emp_101", {"name": "Alice", "role": "Engineer"}))
    print(db.insert("emp_102", {"name": "Bob", "role": "Designer"}))
    
    # 2. READ
    print("\nRead emp_101:", db.read("emp_101"))
    
    # 3. UPDATE
    print("\nUpdate emp_101:", db.update("emp_101", {"role": "Senior Engineer", "location": "NY"}))
    print("Read emp_101 after update:", db.read("emp_101"))
    
    # 4. DELETE
    print("\nDelete emp_102:", db.delete("emp_102"))
    
    # Display final state
    print("\nFinal Data Store:", db.display_all())


   # Initialize the CRUD manager
    db = DictionaryCRUD()


