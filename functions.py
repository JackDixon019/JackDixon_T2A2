from decorators import authorise_as_admin
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
    
def find_all_entities(model, rule):
    stmt = db.select(model).order_by(rule)
    return db.session.scalars(stmt)
    
# for deleting entity only admin is allowed to delete
@authorise_as_admin
def delete_admin_entity(entity):
    table_name = entity.__tablename__
    entity_id = entity.id
    db.session.delete(entity)
    db.session.commit()
    return {"message":f"{table_name} with id: {entity_id} successfully deleted"}