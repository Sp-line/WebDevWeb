import enum


class GradeEnum(enum.StrEnum):
    Junior = "Junior"
    Middle = "Middle"
    Senior = "Senior"
    Lead = "Lead"


class PositionEnum(enum.StrEnum):
    Frontend = "Frontend Developer"
    Backend = "Backend Developer"
    Fullstack = "Fullstack Developer"
    Designer = "Designer"
    QA = "QA Engineer"
    PM = "Project Manager"
