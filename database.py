from replit import db

def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = list(db["encouragements"])
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
    if "encouragements" in db.keys():
        encouragements = list(db["encouragements"])
        if len(encouragements) > index:
            del encouragements[index]
            db["encouragements"] = encouragements
