from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            completed_at=data_dict["completed_at"]
        )

    def to_dict(self):
        #if not self.completed_at:
        #    is_complete_temp=False
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at != None
        )        
    
