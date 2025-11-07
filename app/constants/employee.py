import enum


class GradeEnum(str, enum.Enum):
    Junior = "Junior"
    Middle = "Middle"
    Senior = "Senior"
    Lead = "Lead"


class PositionEnum(str, enum.Enum):
    Frontend = "Frontend Developer"
    Backend = "Backend Developer"
    Fullstack = "Fullstack Developer"
    Designer = "Designer"
    QA = "QA Engineer"
    PM = "Project Manager"
