if __name__ == "__main__":
    from db import db_adapter
    db_adapter.drop_tables()
    db_adapter.create_tables()