from init import db

def find_entity_by_id(model, id):
    stmt = db.select(model).filter_by(id=id)
    return db.session.scalar(stmt)