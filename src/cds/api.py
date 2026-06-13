from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from cds import schema


def _require_id(id: str | None = None) -> str:
    if id is None:
        raise ValueError("id is required but got None")
    return id


def _require_year(year: str | None = None) -> str:
    if year is None:
        raise ValueError("id is required but got None")
    return year


class APIModel(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> APIModel:
        pass


class Enrollment(APIModel):
    undergraduate: Optional[int] = None
    graduate: Optional[int] = None
    total: Optional[int] = None

    @staticmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> Enrollment:
        enrollment = inst_cds.enrollment_and_persistence.enrollment
        if enrollment is None:
            return Enrollment()
        return Enrollment(
            undergraduate=enrollment.grand_total_undergraduates,
            graduate=enrollment.grand_total_graduates,
            total=enrollment.grand_total_all_students,
        )


class InstitutionCard(BaseModel):
    id: str
    name: str
    location: Optional[str]
    available_years: list[str]
    enrollment: Enrollment


class Identity(APIModel):
    name: str
    city: Optional[str] = None
    state: Optional[str] = None
    control: Optional[schema.InstitutionalControl] = None
    calendar: Optional[schema.AcademicCalendar] = None
    website: Optional[str] = None

    @staticmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> Identity:
        info = inst_cds.general_information
        return Identity(
            name=info.institution_name,
            city=info.city,
            state=info.state,
            control=info.institutional_control,
            calendar=info.calendar,
            website=info.website,
        )


class Admissions(APIModel):
    applied: Optional[int] = None
    admitted: Optional[int] = None
    enrolled: Optional[int] = None
    acceptance_rate: Optional[float] = None
    yield_rate: Optional[float] = None
    test_optional: Optional[bool] = None
    sat_range: Optional[tuple[int, int]] = None
    act_range: Optional[tuple[int, int]] = None

    @staticmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> Admissions:
        applications = inst_cds.first_time_first_year_admission.applications
        test_policies = inst_cds.first_time_first_year_admission.test_policies
        test_scores = inst_cds.first_time_first_year_admission.test_scores

        if applications is not None:
            applied = (
                applications.applied.total if applications.applied is not None else None
            )
            admitted = (
                applications.admitted.total
                if applications.admitted is not None
                else None
            )
            enrolled = (
                applications.enrolled.total
                if applications.enrolled is not None
                else None
            )

            if applied is not None and admitted is not None:
                acceptance_rate = round(admitted / applied, 4)
            else:
                acceptance_rate = None

            if admitted is not None and enrolled is not None:
                yield_rate = round(enrolled / admitted, 4)
            else:
                yield_rate = None
        else:
            applied = None
            admitted = None
            enrolled = None
            acceptance_rate = None
            yield_rate = None

        if test_policies is not None and test_policies.sat_or_act_policy is not None:
            test_optional = test_policies.sat_or_act_policy not in (
                "required",
                "required_for_some",
            )
        else:
            test_optional = None

        if test_scores is not None:
            if (
                test_scores.sat_composite is not None
                and test_scores.sat_composite.p25 is not None
                and test_scores.sat_composite.p75 is not None
            ):
                sat_range = (
                    round(test_scores.sat_composite.p25),
                    round(test_scores.sat_composite.p75),
                )
            else:
                sat_range = None

            if (
                test_scores.act_composite is not None
                and test_scores.act_composite.p25 is not None
                and test_scores.act_composite.p75 is not None
            ):
                act_range = (
                    round(test_scores.act_composite.p25),
                    round(test_scores.act_composite.p75),
                )
            else:
                act_range = None
        else:
            sat_range = None
            act_range = None

        return Admissions(
            applied=applied,
            admitted=admitted,
            enrolled=enrolled,
            acceptance_rate=acceptance_rate,
            yield_rate=yield_rate,
            test_optional=test_optional,
            sat_range=sat_range,
            act_range=act_range,
        )


class Cost(APIModel):
    tuition: Optional[float] = None
    required_fees: Optional[float] = None
    food_and_housing: Optional[float] = None
    total: Optional[float] = None

    @staticmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> Cost:
        charges = inst_cds.annual_expenses.all_undergraduate_charges
        if charges is None:
            return Cost()

        tuition = charges.public_out_of_state_tuition or charges.private_tuition
        food_and_housing = charges.food_and_housing
        fees = charges.required_fees

        if tuition is not None and food_and_housing is not None:
            main_expenses = tuition + food_and_housing
        else:
            main_expenses = charges.comprehensive_tuition_food_housing

        if main_expenses is not None and fees is not None:
            total = main_expenses + fees
        else:
            total = None

        return Cost(
            tuition=tuition,
            required_fees=fees,
            food_and_housing=food_and_housing,
            total=total,
        )


class FinancialAid(APIModel):
    pct_receiving_aid: Optional[float] = None
    pct_need_met: Optional[float] = None
    average_aid: Optional[float] = None

    @staticmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> FinancialAid:
        awarded_aid = inst_cds.financial_aid.students_awarded_aid

        pct_receiving_aid = None

        if awarded_aid is not None and awarded_aid.full_time_undergrad is not None:
            num_awarded = awarded_aid.full_time_undergrad.awarded_any_aid
            num_degree_seeking = awarded_aid.full_time_undergrad.degree_seeking_count
            if num_awarded is not None and num_degree_seeking is not None:
                pct_receiving_aid = num_awarded / num_degree_seeking

            pct_need_met = awarded_aid.full_time_undergrad.avg_percent_need_met
            average_aid = awarded_aid.full_time_undergrad.avg_aid_package

        return FinancialAid(
            pct_receiving_aid=pct_receiving_aid,
            pct_need_met=pct_need_met,
            average_aid=average_aid,
        )


class InstitutionProfile(APIModel):
    id: str
    year: str
    identity: Identity
    enrollment: Enrollment
    admissions: Admissions
    cost: Cost
    financial_aid: FinancialAid

    @staticmethod
    def from_cds(
        inst_cds: schema.CommonDataSet, id: str | None = None, year: str | None = None
    ) -> InstitutionProfile:
        return InstitutionProfile(
            id=_require_id(id),
            year=_require_year(year),
            identity=Identity.from_cds(inst_cds),
            enrollment=Enrollment.from_cds(inst_cds),
            admissions=Admissions.from_cds(inst_cds),
            cost=Cost.from_cds(inst_cds),
            financial_aid=FinancialAid.from_cds(inst_cds),
        )
