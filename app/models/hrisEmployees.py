from database import db

class HRISEmployees(db.Model):
    __tablename__ = 'vwAtKWE'
    __bind_key__ = 'hris_db'

    SystemId = db.Column(db.Integer, primary_key=True)
    EmployeeId = db.Column(db.String)
    FullName = db.Column(db.String)
    EmailAddress = db.Column(db.String)
    DateHired = db.Column(db.String)
    Company = db.Column(db.String)
    OASId = db.Column(db.String)
    Tag = db.Column(db.String)


    def to_dict(self):
        return {
            "SystemId" : self.SystemId,
            "EmployeeId" : self.EmployeeId,
            "FullName" : self.FullName or 'No FullName Provided', 
            "EmailAddress" : self.EmailAddress,
            "DateHired" : self.DateHired,
            "Company" : self.Company,
            "OASId" : self.OASId,
            "Tag" : self.Tag
        }