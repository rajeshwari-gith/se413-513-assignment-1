import pytest

from registration import calculate_registration_fee, can_register

pytestmark = pytest.mark.unit


@pytest.mark.positive
@pytest.mark.parametrize(
    "current_credits, course_credits",
    [(0, 1), (6, 2), (12, 3), (14, 4)],
)
def test_registration_allowed_for_valid_scenarios(current_credits, course_credits):
    assert can_register(current_credits, course_credits, True) is True


@pytest.mark.positive
def test_valid_student_can_register(valid_student):
    assert can_register(**valid_student) is True


@pytest.mark.negative
def test_registration_rejected_when_prerequisite_not_met(valid_student):
    valid_student["prerequisite_met"] = False
    assert can_register(**valid_student) is False


@pytest.mark.negative
def test_registration_rejected_when_total_credits_exceed_18():
    assert can_register(15, 4, True) is False


@pytest.mark.negative
@pytest.mark.parametrize(
    "current_credits, course_credits",
    [(-3, 3), (20, 3), (10, 0), (10, 6)],
)
def test_registration_rejected_for_out_of_range_credits(current_credits, course_credits):
    assert can_register(current_credits, course_credits, True) is False


@pytest.mark.boundary
@pytest.mark.parametrize(
    "current_credits, expected",
    [(-1, False), (0, True), (1, True), (14, True), (15, True), (16, False)],
)
def test_current_credits_boundaries(current_credits, expected):
    assert can_register(current_credits, 1, True) is expected


@pytest.mark.boundary
@pytest.mark.parametrize(
    "course_credits, expected",
    [(0, False), (1, True), (2, True), (3, True), (4, True), (5, False)],
)
def test_course_credits_boundaries(course_credits, expected):
    assert can_register(10, course_credits, True) is expected


@pytest.mark.boundary
@pytest.mark.parametrize(
    "current_credits, course_credits, expected",
    [(13, 4, True), (14, 4, True), (15, 3, True), (15, 4, False)],
)
def test_resulting_credit_load_boundaries(current_credits, course_credits, expected):
    assert can_register(current_credits, course_credits, True) is expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "total_credits, expected_fee",
    [(6, 600.0), (12, 1200.0), (15, 1425.0)],
)
def test_fee_below_at_and_above_12_credits(total_credits, expected_fee):
    assert calculate_registration_fee(total_credits) == expected_fee


@pytest.mark.positive
def test_fee_for_valid_student_after_registration(valid_student):
    total = valid_student["current_credits"] + valid_student["course_credits"]
    assert calculate_registration_fee(total) == 1425.0


@pytest.mark.boundary
@pytest.mark.parametrize(
    "total_credits, expected_fee",
    [(0, 0.0), (1, 100.0), (11, 1100.0), (12, 1200.0), (13, 1275.0), (17, 1575.0), (18, 1650.0)],
)
def test_fee_boundaries(total_credits, expected_fee):
    assert calculate_registration_fee(total_credits) == expected_fee


@pytest.mark.negative
@pytest.mark.parametrize("total_credits", [-5, 25])
def test_fee_raises_error_for_invalid_credits(total_credits):
    with pytest.raises(ValueError):
        calculate_registration_fee(total_credits)


@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.parametrize("total_credits", [-1, 19])
def test_fee_raises_error_just_outside_valid_range(total_credits):
    with pytest.raises(ValueError):
        calculate_registration_fee(total_credits)


@pytest.mark.positive
def test_registration_result_is_saved_to_log(registration_log):
    fee = calculate_registration_fee(15)
    with open(registration_log, "w") as log:
        log.write(f"registered,{fee}")
    with open(registration_log) as log:
        assert log.read() == "registered,1425.0"
