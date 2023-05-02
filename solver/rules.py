from typing import Union

from statements.influence_statement import IStatement
from statements.rectangle_statement import RStatement
from statements.trapezoid_statement import TStatement


def transitivity_rule(statement_a: RStatement, statement_b: IStatement) -> Union[RStatement, None]:
    if statement_a.start != statement_b.start or statement_a.end != statement_b.end:
        return None

    return RStatement(
        statement_a.start + statement_b.start_time, statement_a.end + statement_b.end_time,
        statement_b.lower, statement_b.upper)


def smallest_rectangle_rule(statement: TStatement) -> RStatement:
    return RStatement(
        statement.start, statement.end,
        min(statement.lower, statement.lower + (statement.start - statement.end) * statement.slope_lower),
        max(statement.upper, statement.upper + (statement.end - statement.start) * statement.upper))


def to_trapezoid_rule(statement: RStatement) -> TStatement:
    return TStatement(statement.start, statement.end, statement.lower, statement.upper, 0, 0)


def to_rectangle_rule(statement: TStatement) -> Union[RStatement, None]:
    if statement.slope_lower != 0 or statement.slope_upper != 0:
        return None

    return RStatement(statement.start, statement.end, statement.lower, statement.upper)
