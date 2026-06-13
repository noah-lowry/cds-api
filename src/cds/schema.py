"""Common Data Set (CDS) 2025-2026 — Pydantic schema for structured LLM extraction.

Note: This schema was generated automatically by Claude Fable 5, with modifications afterwards.
The rest of this project, including the API models, were constructed by hand, so don't start
with the vibe code slop accusations! :)

Conventions
-----------
* Every section (A–J) is a standalone model; ``CommonDataSet`` composes them,
  so you can extract one section at a time or the whole document.
* Every field is Optional — institutions routinely leave items blank or N/A.
  Extractors should emit ``null`` for missing/blank/NA values, never 0.
* Counts are ``int``; dollars and rates are ``float``; percentages are 0–100
  floats (e.g. 82.14), not fractions. Dates are "MM/DD" strings.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CDSModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ---------------------------------------------------------------- shared ----


class SexBreakdown(CDSModel):
    """Headcount by sex. ``another_unknown`` = nonbinary or sex not reported."""

    men: Optional[int] = None
    women: Optional[int] = None
    another_unknown: Optional[int] = None

    @property
    def total(self) -> int | None:
        if self.men is None and self.women is None and self.another_unknown is None:
            return None
        return (self.men or 0) + (self.women or 0) + (self.another_unknown or 0)


class Importance(str, Enum):
    very_important = "very_important"
    important = "important"
    considered = "considered"
    not_considered = "not_considered"


class RequirementLevel(str, Enum):
    required_of_all = "required_of_all"
    required_of_some = "required_of_some"
    recommended_of_all = "recommended_of_all"
    recommended_of_some = "recommended_of_some"
    not_required = "not_required"


# ------------------------------------------------------------- Section A ----


class InstitutionalControl(str, Enum):
    public = "public"
    private_nonprofit = "private_nonprofit"
    proprietary = "proprietary"


class Coeducational(str, Enum):
    coeducational = "coeducational"
    mens_college = "mens_college"
    womens_college = "womens_college"


class AcademicCalendar(str, Enum):
    semester = "semester"
    quarter = "quarter"
    trimester = "trimester"
    four_one_four = "four_one_four"
    continuous = "continuous"
    differs_by_program = "differs_by_program"
    other = "other"


class DegreeLevel(str, Enum):
    certificate = "certificate"
    diploma = "diploma"
    associate = "associate"
    transfer_associate = "transfer_associate"
    terminal_associate = "terminal_associate"
    bachelors = "bachelors"
    post_bachelors_certificate = "post_bachelors_certificate"
    masters = "masters"
    post_masters_certificate = "post_masters_certificate"
    doctoral_research = "doctoral_research"
    doctoral_professional_practice = "doctoral_professional_practice"
    doctoral_other = "doctoral_other"


class RespondentInfo(CDSModel):
    """A0. Respondent contact info (not for publication)."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    title: Optional[str] = None
    office: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    cds_posted_on_website: Optional[bool] = None
    cds_url: Optional[str] = None


class SectionA(CDSModel):
    """Section A: General institution information (A0–A6)."""

    respondent: Optional[RespondentInfo] = None
    institution_name: str = Field(
        ..., description="A1. Official name of college/university"
    )
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    main_phone: Optional[str] = None
    website: Optional[str] = None
    admissions_phone: Optional[str] = None
    admissions_toll_free_phone: Optional[str] = None
    admissions_email: Optional[str] = None
    admissions_mailing_address: Optional[str] = Field(
        None, description="A1. Separate mailing address for applications, if any"
    )
    online_application_url: Optional[str] = None
    institutional_control: Optional[InstitutionalControl] = Field(
        None, description="A2. Source of institutional control"
    )
    coeducational: Optional[Coeducational] = Field(
        None, description="A3. Undergraduate institution classification"
    )
    calendar: Optional[AcademicCalendar] = Field(
        None, description="A4. Academic year calendar"
    )
    calendar_description: Optional[str] = Field(
        None,
        description="A4. Description if calendar is 'differs_by_program' or 'other'",
    )
    degrees_offered: Optional[list[DegreeLevel]] = Field(
        None, description="A5. All degree levels offered"
    )
    campus_belonging_url: Optional[str] = Field(
        None, description="A6. URL of office fostering a welcoming campus climate"
    )


# ------------------------------------------------------------- Section B ----


class EnrollmentRow(CDSModel):
    """One B1 row: headcounts by attendance status and sex as of fall census."""

    full_time: Optional[SexBreakdown] = None
    part_time: Optional[SexBreakdown] = None


class B1Enrollment(CDSModel):
    """B1. Institutional enrollment as of official fall reporting date (or Oct 15)."""

    degree_seeking_first_time_first_year: Optional[EnrollmentRow] = None
    other_first_year_degree_seeking: Optional[EnrollmentRow] = None
    all_other_degree_seeking_undergraduates: Optional[EnrollmentRow] = None
    total_degree_seeking_undergraduates: Optional[EnrollmentRow] = None
    all_other_undergraduates_in_credit_courses: Optional[EnrollmentRow] = Field(
        None,
        description="Non-degree-seeking undergrads, incl. dual-enrolled HS students",
    )
    total_undergraduates: Optional[EnrollmentRow] = None
    graduate_degree_seeking_first_time: Optional[EnrollmentRow] = None
    graduate_all_other_degree_seeking: Optional[EnrollmentRow] = None
    graduate_all_other_in_credit_courses: Optional[EnrollmentRow] = None
    total_graduate_students: Optional[EnrollmentRow] = None
    grand_total_undergraduates: Optional[int] = Field(
        None, description="Total all undergraduates, FT+PT, all sexes"
    )
    grand_total_graduates: Optional[int] = None
    grand_total_all_students: Optional[int] = None


class B2Row(CDSModel):
    """One racial/ethnic category across the three B2 cohort columns."""

    first_time_first_year: Optional[int] = Field(
        None, description="Degree-seeking, first-time, first-year"
    )
    total_degree_seeking_undergraduates: Optional[int] = Field(
        None, description="All degree-seeking undergrads, incl. first-time first-year"
    )
    total_undergraduates: Optional[int] = Field(
        None, description="Degree- and non-degree-seeking undergrads"
    )


class B2RaceEthnicity(CDSModel):
    """B2. Undergraduate enrollment by IPEDS racial/ethnic category. Nonresidents
    (international students on visas) are reported only in `nonresidents`."""

    nonresidents: Optional[B2Row] = None
    hispanic_latino: Optional[B2Row] = None
    black_african_american: Optional[B2Row] = None
    white: Optional[B2Row] = None
    american_indian_alaska_native: Optional[B2Row] = None
    asian: Optional[B2Row] = None
    native_hawaiian_pacific_islander: Optional[B2Row] = None
    two_or_more_races: Optional[B2Row] = None
    race_ethnicity_unknown: Optional[B2Row] = None
    total: Optional[B2Row] = None


class B3DegreesAwarded(CDSModel):
    """B3. Number of degrees awarded July 1 – June 30 of the prior year."""

    certificates_diplomas: Optional[int] = None
    associate: Optional[int] = None
    bachelors: Optional[int] = None
    post_bachelors_certificates: Optional[int] = None
    masters: Optional[int] = None
    post_masters_certificates: Optional[int] = None
    doctoral_research: Optional[int] = None
    doctoral_professional_practice: Optional[int] = None
    doctoral_other: Optional[int] = None


class AidStatusCounts(CDSModel):
    """Counts disaggregated by federal aid status; the three columns sum to total.
    Students with both Pell and subsidized Stafford go in `pell_recipients`."""

    pell_recipients: Optional[int] = None
    stafford_no_pell: Optional[int] = Field(
        None, description="Subsidized Stafford Loan recipients without a Pell Grant"
    )
    no_pell_no_stafford: Optional[int] = None
    total: Optional[int] = None


class AidStatusPercents(CDSModel):
    """Percentages (0-100) by federal aid status."""

    pell_recipients: Optional[float] = None
    stafford_no_pell: Optional[float] = None
    no_pell_no_stafford: Optional[float] = None
    total: Optional[float] = None


class GraduationRateCohort(CDSModel):
    """B4–B11 grid for one entering cohort of first-time, full-time bachelor's-seeking students."""

    cohort_fall_year: Optional[int] = Field(
        None, description="Fall entry year of the cohort, e.g. 2019"
    )
    initial_cohort: Optional[AidStatusCounts] = Field(
        None, description="Line A: initial cohort"
    )
    allowable_exclusions: Optional[AidStatusCounts] = Field(
        None,
        description="Line B: deceased, disabled, armed forces, foreign aid service, church missions",
    )
    adjusted_cohort: Optional[AidStatusCounts] = Field(
        None, description="Line C: initial cohort minus exclusions"
    )
    completed_within_4_years: Optional[AidStatusCounts] = Field(
        None, description="Line D"
    )
    completed_in_year_5: Optional[AidStatusCounts] = Field(
        None, description="Line E: >4 but ≤5 years"
    )
    completed_in_year_6: Optional[AidStatusCounts] = Field(
        None, description="Line F: >5 but ≤6 years"
    )
    total_completed_within_6_years: Optional[AidStatusCounts] = Field(
        None, description="Line G: D+E+F"
    )
    six_year_graduation_rate: Optional[AidStatusPercents] = Field(
        None, description="Line H: G/C as percent"
    )


class B12TwoYearCompletions(CDSModel):
    """B12–B21. Completion/transfer-out data for two-year institutions."""

    cohort_year: Optional[int] = None
    initial_cohort: Optional[int] = None
    allowable_exclusions: Optional[int] = None
    adjusted_cohort: Optional[int] = None
    completers_under_2yr_programs: Optional[int] = None
    completers_under_2yr_within_150pct_time: Optional[int] = None
    completers_2_to_4yr_programs: Optional[int] = None
    completers_2_to_4yr_within_150pct_time: Optional[int] = None
    total_transfers_out_within_3_years: Optional[int] = None
    transfers_to_two_year: Optional[int] = None
    transfers_to_four_year: Optional[int] = None


class B22Retention(CDSModel):
    """B22. First-to-second-fall retention of the full-time, first-time bachelor's-seeking cohort."""

    fall_cohort: Optional[int] = Field(
        None, description="Adjusted entering cohort (incl. preceding summer starts)"
    )
    retained: Optional[int] = Field(
        None, description="Still enrolled (or completed) as of the next fall census"
    )
    retention_rate: Optional[float] = Field(None, description="Percent retained, 0-100")


class SectionB(CDSModel):
    """Section B: Enrollment and persistence."""

    enrollment: Optional[B1Enrollment] = None
    race_ethnicity: Optional[B2RaceEthnicity] = None
    degrees_awarded: Optional[B3DegreesAwarded] = None
    graduation_rates: Optional[list[GraduationRateCohort]] = Field(
        None,
        description="B4–B11 for each reported cohort (typically two consecutive fall cohorts)",
    )
    two_year_completions: Optional[B12TwoYearCompletions] = None
    retention: Optional[B22Retention] = None


# ------------------------------------------------------------- Section C ----


class ResidencyRow(CDSModel):
    """Residency breakdown of first-time, first-year students (within C2 page)."""

    in_state: Optional[int] = None
    out_of_state: Optional[int] = None
    international: Optional[int] = None
    unknown: Optional[int] = None
    total: Optional[int] = None


class C1Applications(CDSModel):
    """C1. First-time, first-year applied / admitted / enrolled, Fall cohort.
    Includes early decision/action and summer starts."""

    applied: Optional[SexBreakdown] = None
    admitted: Optional[SexBreakdown] = None
    enrolled: Optional[SexBreakdown] = None
    enrolled_full_time: Optional[SexBreakdown] = None
    enrolled_part_time: Optional[SexBreakdown] = None
    applied_by_residency: Optional[ResidencyRow] = None
    admitted_by_residency: Optional[ResidencyRow] = None
    enrolled_by_residency: Optional[ResidencyRow] = None


class C2Waitlist(CDSModel):
    """C2. Waiting list policy and counts."""

    has_waitlist_policy: Optional[bool] = None
    offered_place_on_waitlist: Optional[int] = None
    accepted_place_on_waitlist: Optional[int] = None
    admitted_from_waitlist: Optional[int] = None
    waitlist_is_ranked: Optional[bool] = None
    rank_released_to_students: Optional[bool] = None
    rank_released_to_counselors: Optional[bool] = None


class HSCompletionRequirement(str, Enum):
    diploma_required_ged_accepted = "diploma_required_ged_accepted"
    diploma_required_ged_not_accepted = "diploma_required_ged_not_accepted"
    not_required = "not_required"


class CollegePrepPolicy(str, Enum):
    require = "require"
    recommend = "recommend"
    neither = "neither"


class HSUnits(CDSModel):
    """Carnegie units (1 unit = 1 year of study) of high school coursework."""

    required: Optional[float] = None
    recommended: Optional[float] = None


class C5HSUnitDistribution(CDSModel):
    """C5. Distribution of required/recommended high school units by subject."""

    total_academic: Optional[HSUnits] = None
    english: Optional[HSUnits] = None
    mathematics: Optional[HSUnits] = None
    science: Optional[HSUnits] = None
    science_lab: Optional[HSUnits] = Field(
        None, description="Of the science units, units that must be lab"
    )
    foreign_language: Optional[HSUnits] = None
    social_studies: Optional[HSUnits] = None
    history: Optional[HSUnits] = None
    academic_electives: Optional[HSUnits] = None
    computer_science: Optional[HSUnits] = None
    visual_performing_arts: Optional[HSUnits] = None
    other: Optional[HSUnits] = None
    other_description: Optional[str] = None


class C6OpenAdmission(CDSModel):
    """C6. Open admission policy."""

    open_admission_all: Optional[bool] = None
    open_admission_most: Optional[bool] = None
    selective_out_of_state: Optional[bool] = None
    selective_some_programs: Optional[bool] = None
    other: Optional[str] = None


class C7AdmissionFactors(CDSModel):
    """C7. Relative importance of each factor in first-time, first-year admission decisions."""

    rigor_of_secondary_record: Optional[Importance] = None
    class_rank: Optional[Importance] = None
    academic_gpa: Optional[Importance] = None
    standardized_test_scores: Optional[Importance] = None
    application_essay: Optional[Importance] = None
    recommendations: Optional[Importance] = None
    interview: Optional[Importance] = None
    extracurricular_activities: Optional[Importance] = None
    talent_ability: Optional[Importance] = None
    character_personal_qualities: Optional[Importance] = None
    first_generation: Optional[Importance] = None
    alumni_relation: Optional[Importance] = None
    geographical_residence: Optional[Importance] = None
    state_residency: Optional[Importance] = None
    religious_affiliation: Optional[Importance] = None
    volunteer_work: Optional[Importance] = None
    work_experience: Optional[Importance] = None
    level_of_applicant_interest: Optional[Importance] = None
    program_specific_notes: Optional[str] = Field(
        None, description="How factor importance differs by academic program, if noted"
    )


class TestUsePolicy(str, Enum):
    required = "required"
    required_for_some = "required_for_some"
    recommended = "recommended"
    considered_if_submitted = "considered_if_submitted"
    not_considered = "not_considered"


class C8TestPolicies(CDSModel):
    """C8. SAT/ACT policies for admission."""

    uses_test_scores_in_admission: Optional[bool] = Field(
        None, description="C8A. Whether SAT/ACT scores are used in admission decisions"
    )
    sat_or_act_policy: Optional[TestUsePolicy] = None
    act_only_policy: Optional[TestUsePolicy] = None
    sat_only_policy: Optional[TestUsePolicy] = None
    scores_used_for_advising: Optional[bool] = Field(None, description="C8D")
    latest_score_date: Optional[str] = Field(
        None, description="C8E. Latest MM/DD scores accepted for fall admission"
    )
    policy_clarification: Optional[str] = Field(None, description="C8F")
    placement_tests: Optional[list[str]] = Field(
        None,
        description="C8G. Tests used for placement, e.g. ['SAT','ACT','AP','CLEP','Institutional Exam','State Exam']",
    )


class ScorePercentiles(CDSModel):
    """25th/50th/75th percentile scores among enrolled students who submitted."""

    p25: Optional[float] = None
    p50: Optional[float] = None
    p75: Optional[float] = None


class SATCompositeDistribution(CDSModel):
    """Percent of enrolled first-time students in each SAT composite range (sums to 100)."""

    range_1400_1600: Optional[float] = None
    range_1200_1399: Optional[float] = None
    range_1000_1199: Optional[float] = None
    range_800_999: Optional[float] = None
    range_600_799: Optional[float] = None
    range_400_599: Optional[float] = None


class SATSectionDistribution(CDSModel):
    """Percent in each SAT section-score range (sums to 100)."""

    range_700_800: Optional[float] = None
    range_600_699: Optional[float] = None
    range_500_599: Optional[float] = None
    range_400_499: Optional[float] = None
    range_300_399: Optional[float] = None
    range_200_299: Optional[float] = None


class ACTDistribution(CDSModel):
    """Percent in each ACT score range (sums to 100)."""

    range_30_36: Optional[float] = None
    range_24_29: Optional[float] = None
    range_18_23: Optional[float] = None
    range_12_17: Optional[float] = None
    range_6_11: Optional[float] = None
    below_6: Optional[float] = None


class C9TestScores(CDSModel):
    """C9. Test score profile of ALL enrolled, degree-seeking first-time, first-year students."""

    percent_submitting_sat: Optional[float] = None
    number_submitting_sat: Optional[int] = None
    percent_submitting_act: Optional[float] = None
    number_submitting_act: Optional[int] = None
    sat_composite: Optional[ScorePercentiles] = None
    sat_evidence_based_reading_writing: Optional[ScorePercentiles] = None
    sat_math: Optional[ScorePercentiles] = None
    act_composite: Optional[ScorePercentiles] = None
    act_math: Optional[ScorePercentiles] = None
    act_english: Optional[ScorePercentiles] = None
    act_writing: Optional[ScorePercentiles] = None
    act_science: Optional[ScorePercentiles] = None
    act_reading: Optional[ScorePercentiles] = None
    sat_composite_distribution: Optional[SATCompositeDistribution] = None
    sat_erw_distribution: Optional[SATSectionDistribution] = None
    sat_math_distribution: Optional[SATSectionDistribution] = None
    act_composite_distribution: Optional[ACTDistribution] = None
    act_english_distribution: Optional[ACTDistribution] = None
    act_math_distribution: Optional[ACTDistribution] = None
    act_reading_distribution: Optional[ACTDistribution] = None
    act_science_distribution: Optional[ACTDistribution] = None


class C10ClassRank(CDSModel):
    """C10. High school class rank of enrolled first-time students who reported rank (percents 0-100)."""

    top_tenth: Optional[float] = None
    top_quarter: Optional[float] = None
    top_half: Optional[float] = None
    bottom_half: Optional[float] = None
    bottom_quarter: Optional[float] = None
    percent_submitting_rank: Optional[float] = None


class GPADistribution(CDSModel):
    """Percent of students in each high school GPA band on a 4.0 scale (sums to 100)."""

    gpa_4_0: Optional[float] = Field(None, description="GPA of exactly 4.0")
    gpa_3_75_to_3_99: Optional[float] = None
    gpa_3_50_to_3_74: Optional[float] = None
    gpa_3_25_to_3_49: Optional[float] = None
    gpa_3_00_to_3_24: Optional[float] = None
    gpa_2_50_to_2_99: Optional[float] = None
    gpa_2_00_to_2_49: Optional[float] = None
    gpa_1_00_to_1_99: Optional[float] = None
    below_1_0: Optional[float] = None


class C11GPA(CDSModel):
    """C11–C12. High school GPA profile of enrolled first-time students who reported GPA."""

    distribution_test_submitters: Optional[GPADistribution] = Field(
        None, description="Students who also submitted a test score"
    )
    distribution_non_submitters: Optional[GPADistribution] = Field(
        None, description="Students who did not submit a test score"
    )
    distribution_all: Optional[GPADistribution] = None
    average_gpa: Optional[float] = Field(
        None, description="C12. Average high school GPA, 4.0 scale"
    )
    percent_submitting_gpa: Optional[float] = None


class OnlineFeePolicy(str, Enum):
    same_fee = "same_fee"
    free = "free"
    reduced = "reduced"


class HousingDepositRefund(str, Enum):
    yes_in_full = "yes_in_full"
    yes_in_part = "yes_in_part"
    no = "no"


class C13to20Policies(CDSModel):
    """C13–C20. Application fee, dates, and reply policies."""

    has_application_fee: Optional[bool] = None
    application_fee: Optional[float] = None
    fee_waivable_for_need: Optional[bool] = None
    online_fee_policy: Optional[OnlineFeePolicy] = None
    online_fee_waivable_for_need: Optional[bool] = None
    has_closing_date: Optional[bool] = Field(None, description="C14")
    closing_date: Optional[str] = Field(
        None, description="MM/DD fall application closing date"
    )
    priority_date: Optional[str] = None
    nonfall_admission: Optional[bool] = Field(
        None, description="C15. First-time students accepted for terms other than fall"
    )
    notification_rolling_begin: Optional[str] = Field(
        None, description="C16. MM/DD rolling notification begins, if rolling"
    )
    notification_by_date: Optional[str] = Field(
        None, description="C16. MM/DD fixed notification date, if fixed"
    )
    notification_other: Optional[str] = None
    reply_by_date: Optional[str] = Field(
        None, description="C17. MM/DD admitted applicants must reply by"
    )
    reply_no_set_date: Optional[bool] = None
    reply_may1_or_weeks: Optional[int] = Field(
        None, description="C17. Reply by May 1 or within N weeks if notified after"
    )
    housing_deposit_deadline: Optional[str] = Field(None, description="MM/DD")
    housing_deposit_amount: Optional[float] = None
    housing_deposit_refundable: Optional[HousingDepositRefund] = None
    deferred_admission_allowed: Optional[bool] = Field(None, description="C18")
    deferred_admission_max_period: Optional[str] = Field(
        None, description="C18. e.g. '1 year'"
    )
    early_admission_of_hs_students: Optional[bool] = Field(
        None, description="C19. Full-time enrollment ≥1 year before HS graduation"
    )


class C21EarlyDecision(CDSModel):
    """C21. Binding early decision plan."""

    offered: Optional[bool] = None
    first_closing_date: Optional[str] = Field(None, description="MM/DD")
    first_notification_date: Optional[str] = None
    other_closing_date: Optional[str] = None
    other_notification_date: Optional[str] = None
    applications_received: Optional[int] = None
    admitted: Optional[int] = None
    details: Optional[str] = None


class C22EarlyAction(CDSModel):
    """C22. Non-binding early action plan."""

    offered: Optional[bool] = None
    closing_date: Optional[str] = Field(None, description="MM/DD")
    notification_date: Optional[str] = None
    is_restrictive: Optional[bool] = Field(
        None, description="Whether plan limits applying to other early plans"
    )


class SectionC(CDSModel):
    """Section C: First-time, first-year (freshman) admission."""

    applications: Optional[C1Applications] = None
    waitlist: Optional[C2Waitlist] = None
    hs_completion_requirement: Optional[HSCompletionRequirement] = Field(
        None, description="C3"
    )
    college_prep_program: Optional[CollegePrepPolicy] = Field(None, description="C4")
    hs_units: Optional[C5HSUnitDistribution] = None
    open_admission: Optional[C6OpenAdmission] = None
    admission_factors: Optional[C7AdmissionFactors] = None
    test_policies: Optional[C8TestPolicies] = None
    test_scores: Optional[C9TestScores] = None
    class_rank: Optional[C10ClassRank] = None
    gpa: Optional[C11GPA] = None
    policies: Optional[C13to20Policies] = None
    early_decision: Optional[C21EarlyDecision] = None
    early_action: Optional[C22EarlyAction] = None


# ------------------------------------------------------------- Section D ----


class D2TransferCounts(CDSModel):
    """D2. Degree-seeking transfer applicants for the fall term."""

    applied: Optional[SexBreakdown] = None
    admitted: Optional[SexBreakdown] = None
    enrolled: Optional[SexBreakdown] = None
    total_applied: Optional[int] = None
    total_admitted: Optional[int] = None
    total_enrolled: Optional[int] = None


class Term(str, Enum):
    fall = "fall"
    winter = "winter"
    spring = "spring"
    summer = "summer"


class D5TransferRequirements(CDSModel):
    """D5. Items required of transfer applicants."""

    high_school_transcript: Optional[RequirementLevel] = None
    college_transcripts: Optional[RequirementLevel] = None
    essay_personal_statement: Optional[RequirementLevel] = None
    interview: Optional[RequirementLevel] = None
    standardized_test_scores: Optional[RequirementLevel] = None
    statement_of_good_standing: Optional[RequirementLevel] = None


class TransferTermDates(CDSModel):
    """D9. Application dates for one entry term (MM/DD strings)."""

    term: Optional[Term] = None
    priority_date: Optional[str] = None
    closing_date: Optional[str] = None
    notification_date: Optional[str] = None
    reply_date: Optional[str] = None
    rolling_admission: Optional[bool] = None


class SectionD(CDSModel):
    """Section D: Transfer admission and credit policies."""

    enrolls_transfers: Optional[bool] = Field(None, description="D1")
    transfer_credit_accepted: Optional[bool] = Field(
        None, description="D1. Advanced standing credit for prior coursework"
    )
    fall_transfer_counts: Optional[D2TransferCounts] = None
    entry_terms: Optional[list[Term]] = Field(
        None, description="D3. Terms for which transfers may enroll"
    )
    minimum_credits_required_to_apply_as_transfer: Optional[bool] = Field(
        None,
        description="D4. Whether a minimum credit count is required, else applies as first-year",
    )
    minimum_credits_number: Optional[float] = None
    minimum_credits_unit: Optional[str] = Field(
        None, description="e.g. 'semester hours'"
    )
    application_requirements: Optional[D5TransferRequirements] = None
    min_hs_gpa: Optional[float] = Field(None, description="D6. 4.0 scale")
    min_college_gpa: Optional[float] = Field(None, description="D7. 4.0 scale")
    other_application_requirements: Optional[str] = Field(None, description="D8")
    term_dates: Optional[list[TransferTermDates]] = Field(None, description="D9")
    open_admission_applies_to_transfers: Optional[bool] = Field(None, description="D10")
    additional_requirements: Optional[str] = Field(None, description="D11")
    lowest_transferable_grade: Optional[str] = Field(None, description="D12. e.g. 'C'")
    max_credits_from_two_year: Optional[str] = Field(
        None, description="D13. Number and unit, e.g. '62 per credit'"
    )
    max_credits_from_four_year: Optional[str] = Field(None, description="D14")
    min_credits_for_associate: Optional[str] = Field(
        None, description="D15. Credits transfers must complete at the institution"
    )
    min_credits_for_bachelors: Optional[str] = Field(None, description="D16")
    other_transfer_credit_policies: Optional[str] = Field(None, description="D17")
    accepts_ace_credit: Optional[bool] = Field(
        None, description="D18. American Council on Education military credit"
    )
    accepts_clep: Optional[bool] = Field(None, description="D18")
    accepts_dsst: Optional[bool] = Field(
        None, description="D18. DANTES Subject Standardized Tests"
    )
    max_ace_credits: Optional[str] = Field(None, description="D19")
    max_clep_dsst_credits: Optional[str] = Field(None, description="D20")
    military_credit_policy_url: Optional[str] = Field(None, description="D21")
    other_military_credit_policies: Optional[str] = Field(None, description="D22")


# ------------------------------------------------------------- Section E ----


class SpecialStudyOption(str, Enum):
    accelerated_program = "accelerated_program"
    cooperative_education = "cooperative_education"
    comprehensive_transition_program = "comprehensive_transition_program"
    cross_registration = "cross_registration"
    distance_learning = "distance_learning"
    double_major = "double_major"
    dual_enrollment = "dual_enrollment"
    english_as_second_language = "english_as_second_language"
    exchange_student_domestic = "exchange_student_domestic"
    external_degree_program = "external_degree_program"
    honors_program = "honors_program"
    independent_study = "independent_study"
    internships = "internships"
    liberal_arts_career_combination = "liberal_arts_career_combination"
    student_designed_major = "student_designed_major"
    study_abroad = "study_abroad"
    teacher_certification = "teacher_certification"
    undergraduate_research = "undergraduate_research"
    weekend_college = "weekend_college"
    other = "other"


class RequiredCourseworkArea(str, Enum):
    arts_fine_arts = "arts_fine_arts"
    computer_literacy = "computer_literacy"
    english_composition = "english_composition"
    foreign_languages = "foreign_languages"
    history = "history"
    humanities = "humanities"
    mathematics = "mathematics"
    philosophy = "philosophy"
    sciences = "sciences"
    social_science = "social_science"
    other = "other"


class SectionE(CDSModel):
    """Section E: Academic offerings and policies."""

    special_study_options: Optional[list[SpecialStudyOption]] = Field(
        None, description="E1"
    )
    special_study_other: Optional[str] = None
    required_coursework_areas: Optional[list[RequiredCourseworkArea]] = Field(
        None, description="E3. Areas all/most students must complete before graduation"
    )
    required_coursework_other: Optional[str] = Field(
        None, description="E3. e.g. 'Physical Education; Intensive writing'"
    )


# ------------------------------------------------------------- Section F ----


class F1Column(CDSModel):
    """F1 percentages (0-100) and average ages for one cohort column."""

    percent_out_of_state: Optional[float] = Field(
        None, description="Excludes international/nonresident students"
    )
    percent_men_joining_fraternities: Optional[float] = None
    percent_women_joining_sororities: Optional[float] = None
    percent_in_college_housing: Optional[float] = Field(
        None, description="College-owned, -operated, or -affiliated housing"
    )
    percent_off_campus_or_commute: Optional[float] = None
    percent_age_25_and_older: Optional[float] = None
    average_age_full_time: Optional[float] = None
    average_age_all: Optional[float] = None


class Activity(str, Enum):
    campus_ministries = "campus_ministries"
    choral_groups = "choral_groups"
    concert_band = "concert_band"
    dance = "dance"
    drama_theater = "drama_theater"
    international_student_organization = "international_student_organization"
    jazz_band = "jazz_band"
    literary_magazine = "literary_magazine"
    marching_band = "marching_band"
    model_un = "model_un"
    music_ensembles = "music_ensembles"
    musical_theater = "musical_theater"
    opera = "opera"
    pep_band = "pep_band"
    radio_station = "radio_station"
    student_government = "student_government"
    student_newspaper = "student_newspaper"
    student_run_film_society = "student_run_film_society"
    symphony_orchestra = "symphony_orchestra"
    television_station = "television_station"
    yearbook = "yearbook"


class ROTCBranch(CDSModel):
    """F3. Availability of one ROTC branch."""

    offered_on_campus: Optional[bool] = None
    cooperating_institution: Optional[str] = Field(
        None, description="Name of cooperating institution, if offered there"
    )


class HousingType(str, Enum):
    coed_halls = "coed_halls"
    mens_halls = "mens_halls"
    womens_halls = "womens_halls"
    apartments_married = "apartments_married"
    apartments_single = "apartments_single"
    special_housing_disabled = "special_housing_disabled"
    special_housing_international = "special_housing_international"
    fraternity_sorority = "fraternity_sorority"
    cooperative = "cooperative"
    theme_housing = "theme_housing"
    wellness_housing = "wellness_housing"
    living_learning_communities = "living_learning_communities"
    other = "other"


class SectionF(CDSModel):
    """Section F: Student life."""

    first_time_first_year: Optional[F1Column] = Field(
        None, description="F1, first-time first-year column"
    )
    all_undergraduates: Optional[F1Column] = Field(
        None, description="F1, degree-seeking undergraduates column"
    )
    activities: Optional[list[Activity]] = Field(None, description="F2")
    army_rotc: Optional[ROTCBranch] = None
    naval_rotc: Optional[ROTCBranch] = None
    naval_rotc_marine_option: Optional[bool] = None
    air_force_rotc: Optional[ROTCBranch] = None
    housing_options: Optional[list[HousingType]] = Field(None, description="F4")
    housing_other: Optional[str] = None


# ------------------------------------------------------------- Section G ----


class G1Charges(CDSModel):
    """G1. Full-academic-year charges (USD) for full-time undergraduates."""

    private_tuition: Optional[float] = None
    public_in_district_tuition: Optional[float] = None
    public_in_state_tuition: Optional[float] = None
    public_out_of_state_tuition: Optional[float] = None
    nonresident_tuition: Optional[float] = None
    required_fees: Optional[float] = Field(
        None,
        description="Charges all full-time students must pay, excluded from tuition",
    )
    food_and_housing: Optional[float] = Field(
        None, description="On-campus, double occupancy, max/19-meals plan"
    )
    housing_only: Optional[float] = None
    food_only: Optional[float] = None
    comprehensive_tuition_food_housing: Optional[float] = Field(
        None, description="Only if tuition and food/housing cannot be separated"
    )
    other: Optional[float] = None


class G5ExpenseColumn(CDSModel):
    """G5. Estimated annual expenses (USD) for one residence status."""

    books_and_supplies: Optional[float] = None
    housing_only: Optional[float] = None
    food_only: Optional[float] = None
    food_and_housing_total: Optional[float] = None
    transportation: Optional[float] = None
    other_expenses: Optional[float] = None


class SectionG(CDSModel):
    """Section G: Annual expenses for the academic year."""

    net_price_calculator_url: Optional[str] = Field(None, description="G0")
    first_year_charges: Optional[G1Charges] = None
    all_undergraduate_charges: Optional[G1Charges] = None
    min_credits_full_time: Optional[float] = Field(
        None, description="G2. Min credits/term for stated full-time tuition"
    )
    max_credits_full_time: Optional[float] = None
    tuition_varies_by_year: Optional[bool] = Field(None, description="G3")
    tuition_varies_by_program: Optional[bool] = Field(None, description="G4")
    percent_paying_more_than_g1: Optional[float] = Field(
        None, description="G4. Percent of FT undergrads paying more than G1 rates"
    )
    expenses_residents: Optional[G5ExpenseColumn] = None
    expenses_commuters_at_home: Optional[G5ExpenseColumn] = None
    expenses_commuters_not_at_home: Optional[G5ExpenseColumn] = None
    per_credit_private: Optional[float] = Field(
        None, description="G6. Tuition-only per-credit-hour charge"
    )
    per_credit_in_district: Optional[float] = None
    per_credit_in_state: Optional[float] = None
    per_credit_out_of_state: Optional[float] = None
    per_credit_nonresident: Optional[float] = None


# ------------------------------------------------------------- Section H ----


class NeedNonNeed(CDSModel):
    """Dollars (USD) by aid basis. Non-need-based aid used to meet need counts as need-based."""

    need_based: Optional[float] = None
    non_need_based: Optional[float] = None


class NeedsMethodology(str, Enum):
    federal = "federal"
    institutional = "institutional"
    both = "both"


class H1AidDollars(CDSModel):
    """H1. Total aid dollars awarded to enrolled degree-seeking undergraduates (B1 cohort)."""

    academic_year: Optional[str] = Field(
        None,
        description="Year reported, e.g. '2024-2025 final' or '2025-2026 estimated'",
    )
    needs_methodology: Optional[NeedsMethodology] = None
    federal_grants: Optional[NeedNonNeed] = None
    state_grants: Optional[NeedNonNeed] = None
    institutional_grants: Optional[NeedNonNeed] = Field(
        None,
        description="Endowed/annual-gift/tuition-funded grants, excl. athletic aid and tuition waivers",
    )
    external_grants: Optional[NeedNonNeed] = Field(
        None, description="Outside scholarships, e.g. Kiwanis, National Merit"
    )
    total_scholarships_grants: Optional[NeedNonNeed] = None
    student_loans: Optional[NeedNonNeed] = Field(
        None, description="All sources, excluding parent loans"
    )
    federal_work_study: Optional[NeedNonNeed] = None
    state_other_work_study: Optional[NeedNonNeed] = None
    total_self_help: Optional[NeedNonNeed] = None
    parent_loans: Optional[NeedNonNeed] = None
    tuition_waivers: Optional[NeedNonNeed] = Field(
        None, description="Optional reporting"
    )
    athletic_awards: Optional[NeedNonNeed] = None


class H2Column(CDSModel):
    """H2 lines a–m for one cohort column. Students may appear in multiple lines."""

    degree_seeking_count: Optional[int] = Field(
        None, description="a. Degree-seeking undergrads (B1 cohort)"
    )
    applied_for_need_aid: Optional[int] = Field(
        None, description="b. Of line a, applied for need-based aid"
    )
    determined_to_have_need: Optional[int] = Field(
        None, description="c. Of line b, determined to have financial need"
    )
    awarded_any_aid: Optional[int] = Field(
        None, description="d. Of line c, awarded any financial aid"
    )
    awarded_need_grant: Optional[int] = Field(
        None, description="e. Of line d, awarded need-based scholarship/grant"
    )
    awarded_need_self_help: Optional[int] = Field(
        None, description="f. Of line d, awarded need-based self-help (loans/work)"
    )
    awarded_non_need_grant: Optional[int] = Field(
        None, description="g. Of line d, awarded non-need-based scholarship/grant"
    )
    need_fully_met: Optional[int] = Field(
        None,
        description="h. Of line d, need fully met excl. PLUS/unsubsidized/private loans",
    )
    avg_percent_need_met: Optional[float] = Field(
        None, description="i. Average percent of need met, 0-100"
    )
    avg_aid_package: Optional[float] = Field(
        None, description="j. Average package (USD) of line d"
    )
    avg_need_grant: Optional[float] = Field(
        None, description="k. Average need-based grant (USD) of line e"
    )
    avg_need_self_help: Optional[float] = Field(
        None, description="l. Average need-based self-help (USD) of line f"
    )
    avg_need_loan: Optional[float] = Field(
        None,
        description="m. Average need-based loan (USD) of those in line f with a need-based loan",
    )


class H2AColumn(CDSModel):
    """H2A lines n–q for one cohort column: non-need awards to students without need."""

    awarded_non_need_grant_no_need: Optional[int] = Field(
        None,
        description="n. No financial need, awarded institutional non-need grant (excl. athletic/tuition benefits)",
    )
    avg_non_need_grant: Optional[float] = Field(
        None, description="o. Average USD for line n"
    )
    awarded_athletic_award: Optional[int] = Field(
        None, description="p. Awarded institutional non-need athletic scholarship"
    )
    avg_athletic_award: Optional[float] = Field(
        None, description="q. Average USD for line p"
    )


class H2Cohorts(CDSModel):
    """The three H2/H2A reporting columns."""

    full_time_first_time: Optional[H2Column] = None
    full_time_undergrad: Optional[H2Column] = Field(
        None, description="All full-time undergrads, including first-time"
    )
    less_than_full_time: Optional[H2Column] = None


class H2ACohorts(CDSModel):
    full_time_first_time: Optional[H2AColumn] = None
    full_time_undergrad: Optional[H2AColumn] = None
    less_than_full_time: Optional[H2AColumn] = None


class LoanSourceRow(CDSModel):
    """H5. Borrowing by the H4 graduating class from one loan source."""

    number_borrowed: Optional[int] = None
    percent_borrowed: Optional[float] = Field(
        None, description="Percent of the H4 class, 0-100"
    )
    avg_cumulative_principal: Optional[float] = Field(
        None, description="Average per-borrower cumulative principal, USD"
    )


class H5Borrowing(CDSModel):
    """H5. Cumulative borrowing of bachelor's recipients who entered as first-time students (H4 class).
    Excludes transfers-in, parent loans, and money borrowed elsewhere; includes co-signed loans."""

    any_loans: Optional[LoanSourceRow] = None
    federal_loans: Optional[LoanSourceRow] = None
    institutional_loans: Optional[LoanSourceRow] = None
    state_loans: Optional[LoanSourceRow] = None
    private_loans: Optional[LoanSourceRow] = None


class FinancialAidForm(str, Enum):
    fafsa = "fafsa"
    institutional_form = "institutional_form"
    css_profile = "css_profile"
    state_aid_form = "state_aid_form"
    noncustodial_profile = "noncustodial_profile"
    business_farm_supplement = "business_farm_supplement"
    other = "other"


class AidCriterion(CDSModel):
    """H14. Whether a criterion is used for non-need and/or need-based institutional aid."""

    non_need_based: Optional[bool] = None
    need_based: Optional[bool] = None


class H14Criteria(CDSModel):
    """H14. Criteria used in awarding institutional aid."""

    academics: Optional[AidCriterion] = None
    alumni_affiliation: Optional[AidCriterion] = None
    art: Optional[AidCriterion] = None
    athletics: Optional[AidCriterion] = None
    job_skills: Optional[AidCriterion] = None
    rotc: Optional[AidCriterion] = None
    leadership: Optional[AidCriterion] = None
    music_drama: Optional[AidCriterion] = None
    religious_affiliation: Optional[AidCriterion] = None
    state_district_residency: Optional[AidCriterion] = None


class SectionH(CDSModel):
    """Section H: Financial aid."""

    aid_dollars: Optional[H1AidDollars] = None
    students_awarded_aid: Optional[H2Cohorts] = Field(None, description="H2")
    non_need_awards: Optional[H2ACohorts] = Field(None, description="H2A")
    bachelors_class_size: Optional[int] = Field(
        None,
        description="H4. First-time entrants receiving a bachelor's July 1–June 30; excludes transfers-in",
    )
    borrowing: Optional[H5Borrowing] = None
    nonresident_need_aid_available: Optional[bool] = Field(
        None,
        description="H6. Institutional need-based aid for degree-seeking nonresidents",
    )
    nonresident_non_need_aid_available: Optional[bool] = None
    nonresident_aid_not_available: Optional[bool] = None
    nonresidents_awarded_aid: Optional[int] = Field(None, description="H6")
    nonresident_avg_aid: Optional[float] = Field(None, description="H6. USD")
    nonresident_total_aid: Optional[float] = Field(None, description="H6. USD")
    nonresident_required_forms: Optional[list[FinancialAidForm]] = Field(
        None, description="H7"
    )
    nonresident_other_form: Optional[str] = None
    domestic_required_forms: Optional[list[FinancialAidForm]] = Field(
        None, description="H8"
    )
    domestic_other_form: Optional[str] = None
    filing_priority_date: Optional[str] = Field(None, description="H9. MM/DD")
    filing_deadline: Optional[str] = Field(
        None, description="H9. MM/DD; null if rolling/no deadline"
    )
    filing_no_deadline_rolling: Optional[bool] = None
    notification_on_or_about: Optional[str] = Field(None, description="H10. MM/DD")
    notification_rolling: Optional[bool] = None
    notification_rolling_start: Optional[str] = Field(None, description="H10. MM/DD")
    reply_by_date: Optional[str] = Field(None, description="H11. MM/DD")
    reply_within_weeks: Optional[int] = None
    loans_available: Optional[list[str]] = Field(
        None,
        description="H12. e.g. ['Federal Direct Subsidized', 'Federal Direct Unsubsidized', 'Federal Direct PLUS']",
    )
    need_based_grants_available: Optional[list[str]] = Field(
        None,
        description="H13. e.g. ['Federal Pell', 'SEOG', 'State scholarships/grants', 'Private', 'Institutional']",
    )
    award_criteria: Optional[H14Criteria] = None
    affordability_initiatives: Optional[str] = Field(
        None, description="H15. Recent major affordability policies/programs"
    )


# ------------------------------------------------------------- Section I ----


class FacultyCounts(CDSModel):
    """Headcounts of instructional faculty by employment status (AAUP definitions)."""

    full_time: Optional[int] = None
    part_time: Optional[int] = None
    total: Optional[int] = None


class I1Faculty(CDSModel):
    """I1. Instructional faculty as of the fall census. Lines f+g+h+i sum to line a."""

    total_instructional: Optional[FacultyCounts] = Field(None, description="a")
    minority: Optional[FacultyCounts] = Field(
        None,
        description="b. Black, American Indian/Alaska Native, Asian, NH/PI, or Hispanic",
    )
    women: Optional[FacultyCounts] = Field(None, description="c")
    men: Optional[FacultyCounts] = Field(None, description="d")
    nonresident_international: Optional[FacultyCounts] = Field(None, description="e")
    doctorate_or_terminal: Optional[FacultyCounts] = Field(None, description="f")
    masters_non_terminal: Optional[FacultyCounts] = Field(None, description="g")
    bachelors_highest: Optional[FacultyCounts] = Field(None, description="h")
    unknown_other: Optional[FacultyCounts] = Field(None, description="i")
    standalone_graduate_programs: Optional[FacultyCounts] = Field(
        None, description="j. Faculty teaching virtually only graduate students"
    )


class ClassSizeDistribution(CDSModel):
    """I3. Number of fall-term class sections (or subsections) per enrollment interval."""

    size_2_9: Optional[int] = None
    size_10_19: Optional[int] = None
    size_20_29: Optional[int] = None
    size_30_39: Optional[int] = None
    size_40_49: Optional[int] = None
    size_50_99: Optional[int] = None
    size_100_plus: Optional[int] = None
    total: Optional[int] = None


class SectionI(CDSModel):
    """Section I: Instructional faculty and class size."""

    faculty: Optional[I1Faculty] = None
    student_faculty_ratio: Optional[float] = Field(
        None,
        description="I2. FTE students per FTE instructional faculty, e.g. 8 for 8:1",
    )
    ratio_fte_students: Optional[float] = Field(
        None, description="I2. FTE student count used in the ratio"
    )
    ratio_fte_faculty: Optional[float] = Field(
        None, description="I2. FTE faculty count used in the ratio"
    )
    class_sections: Optional[ClassSizeDistribution] = Field(
        None,
        description="I3. Organized credit course sections (excl. subsections, distance, one-on-one)",
    )
    class_subsections: Optional[ClassSizeDistribution] = Field(
        None,
        description="I3. Labs, recitations, discussions meeting separately from lecture",
    )


# ------------------------------------------------------------- Section J ----


class DegreePercents(CDSModel):
    """Percent (0-100) of awards in a discipline, by majors not headcount (double majors counted twice)."""

    diplomas_certificates: Optional[float] = None
    associate: Optional[float] = None
    bachelors: Optional[float] = None


class SectionJ(CDSModel):
    """Section J: Disciplinary areas of degrees conferred (CIP 2020 categories);
    each award-level column should sum to 100."""

    agriculture: Optional[DegreePercents] = Field(None, description="CIP 01")
    natural_resources_conservation: Optional[DegreePercents] = Field(
        None, description="CIP 03"
    )
    architecture: Optional[DegreePercents] = Field(None, description="CIP 04")
    area_ethnic_gender_studies: Optional[DegreePercents] = Field(
        None, description="CIP 05"
    )
    communication_journalism: Optional[DegreePercents] = Field(
        None, description="CIP 09"
    )
    communication_technologies: Optional[DegreePercents] = Field(
        None, description="CIP 10"
    )
    computer_information_sciences: Optional[DegreePercents] = Field(
        None, description="CIP 11"
    )
    personal_culinary_services: Optional[DegreePercents] = Field(
        None, description="CIP 12"
    )
    education: Optional[DegreePercents] = Field(None, description="CIP 13")
    engineering: Optional[DegreePercents] = Field(None, description="CIP 14")
    engineering_technologies: Optional[DegreePercents] = Field(
        None, description="CIP 15"
    )
    foreign_languages_linguistics: Optional[DegreePercents] = Field(
        None, description="CIP 16"
    )
    family_consumer_sciences: Optional[DegreePercents] = Field(
        None, description="CIP 19"
    )
    law_legal_studies: Optional[DegreePercents] = Field(None, description="CIP 22")
    english: Optional[DegreePercents] = Field(None, description="CIP 23")
    liberal_arts_general_studies: Optional[DegreePercents] = Field(
        None, description="CIP 24"
    )
    library_science: Optional[DegreePercents] = Field(None, description="CIP 25")
    biological_life_sciences: Optional[DegreePercents] = Field(
        None, description="CIP 26"
    )
    mathematics_statistics: Optional[DegreePercents] = Field(None, description="CIP 27")
    military_science_technologies: Optional[DegreePercents] = Field(
        None, description="CIP 28/29"
    )
    interdisciplinary_studies: Optional[DegreePercents] = Field(
        None, description="CIP 30"
    )
    parks_recreation: Optional[DegreePercents] = Field(None, description="CIP 31")
    philosophy_religious_studies: Optional[DegreePercents] = Field(
        None, description="CIP 38"
    )
    theology_religious_vocations: Optional[DegreePercents] = Field(
        None, description="CIP 39"
    )
    physical_sciences: Optional[DegreePercents] = Field(None, description="CIP 40")
    science_technologies: Optional[DegreePercents] = Field(None, description="CIP 41")
    psychology: Optional[DegreePercents] = Field(None, description="CIP 42")
    homeland_security_protective_services: Optional[DegreePercents] = Field(
        None, description="CIP 43"
    )
    public_administration_social_services: Optional[DegreePercents] = Field(
        None, description="CIP 44"
    )
    social_sciences: Optional[DegreePercents] = Field(None, description="CIP 45")
    construction_trades: Optional[DegreePercents] = Field(None, description="CIP 46")
    mechanic_repair_technologies: Optional[DegreePercents] = Field(
        None, description="CIP 47"
    )
    precision_production: Optional[DegreePercents] = Field(None, description="CIP 48")
    transportation_materials_moving: Optional[DegreePercents] = Field(
        None, description="CIP 49"
    )
    visual_performing_arts: Optional[DegreePercents] = Field(None, description="CIP 50")
    health_professions: Optional[DegreePercents] = Field(None, description="CIP 51")
    business_marketing: Optional[DegreePercents] = Field(None, description="CIP 52")
    history: Optional[DegreePercents] = Field(None, description="CIP 54")
    other: Optional[DegreePercents] = None


# ------------------------------------------------------------------ root ----


class CommonDataSet(CDSModel):
    """Complete Common Data Set 2025-2026 response."""

    general_information: SectionA
    enrollment_and_persistence: SectionB
    first_time_first_year_admission: SectionC
    transfer_admission: SectionD
    academic_offerings: SectionE
    student_life: SectionF
    annual_expenses: SectionG
    financial_aid: SectionH
    faculty_and_class_size: Optional[SectionI] = None
    degrees_conferred: Optional[SectionJ] = None
