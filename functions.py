from init import db

from marshmallow import ValidationError

# flexible function to find entity by id
def find_entity_by_id(model, id):
    stmt = db.select(model).filter_by(id=id)
    if db.session.scalar(stmt):
        return db.session.scalar(stmt)
    else:
        # Finds the name of the table being searched, for flexible error-handling
        table_name = db.session.scalar(db.select(model)).__tablename__
        raise ValidationError(f'No {table_name} with id: {id} found')