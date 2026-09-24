# Test Analysis

## 4. Equivalence Partitioning

### 4(a) Equivalence classes

**can_register(current_credits, course_credits, prerequisite_met)**

| Input | Class | Range | Valid? | Expected result |
|---|---|---|---|---|
| current_credits | C1 | 0 to 15 | Valid | can register (if other rules pass) |
| current_credits | C2 | below 0 | Invalid | False |
| current_credits | C3 | above 15 | Invalid | False |
| course_credits | K1 | 1 to 4 | Valid | can register (if other rules pass) |
| course_credits | K2 | below 1 | Invalid | False |
| course_credits | K3 | above 4 | Invalid | False |
| prerequisite_met | P1 | True | Valid | can register (if other rules pass) |
| prerequisite_met | P2 | False | Invalid | False |
| current + course | R1 | 18 or less | Valid | can register (if other rules pass) |
| current + course | R2 | more than 18 | Invalid | False |

**calculate_registration_fee(total_credits)**

| Input | Class | Range | Valid? | Expected result |
|---|---|---|---|---|
| total_credits | F1 | 0 to 12 | Valid | $100 per credit |
| total_credits | F2 | 13 to 18 | Valid | $1200 + $75 per credit above 12 |
| total_credits | F3 | below 0 | Invalid | ValueError |
| total_credits | F4 | above 18 | Invalid | ValueError |

The fee has two valid classes because the price changes after 12 credits.

### 4(b) Representative values

| Class | Value used | Test |
|---|---|---|
| C1, K1, P1, R1 | 12 current, 3 course, True | test_valid_student_can_register |
| C1, K1, R1 | (0,1), (6,2), (12,3), (14,4) | test_registration_allowed_for_valid_scenarios |
| C2 | -3 | test_registration_rejected_for_out_of_range_credits |
| C3 | 20 | test_registration_rejected_for_out_of_range_credits |
| K2 | 0 | test_registration_rejected_for_out_of_range_credits |
| K3 | 6 | test_registration_rejected_for_out_of_range_credits |
| P2 | False | test_registration_rejected_when_prerequisite_not_met |
| R2 | 15 + 4 = 19 | test_registration_rejected_when_total_credits_exceed_18 |
| F1 | 6 | test_fee_below_at_and_above_12_credits |
| F2 | 15 | test_fee_below_at_and_above_12_credits |
| F3 | -5 | test_fee_raises_error_for_invalid_credits |
| F4 | 25 | test_fee_raises_error_for_invalid_credits |

Every value inside a class should behave the same way. If the code works for one
value in a class, it very likely works for all of them. So one value per class
checks every kind of behavior without testing every possible number. Each invalid
test changes only one input and keeps the others valid, so we know which rule
caused the rejection.

## 5. Boundary-Value Analysis

### 5(a) and 5(b) Boundaries, neighbors, and expected behavior

**current_credits** (course_credits = 1, prerequisite met)

| Boundary | Value | Expected |
|---|---|---|
| 0 (lower) | -1 | False |
| | 0 | True |
| | 1 | True |
| 15 (upper) | 14 | True |
| | 15 | True |
| | 16 | False |

**course_credits** (current_credits = 10, prerequisite met)

| Boundary | Value | Expected |
|---|---|---|
| 1 (lower) | 0 | False |
| | 1 | True |
| | 2 | True |
| 4 (upper) | 3 | True |
| | 4 | True |
| | 5 | False |

**Resulting credit load** (current + course, prerequisite met)

| Boundary | Values | Total | Expected |
|---|---|---|---|
| 18 | 13 + 4 | 17 | True |
| | 14 + 4 | 18 | True |
| | 15 + 3 | 18 | True |
| | 15 + 4 | 19 | False |

**total_credits for the fee**

| Boundary | Value | Expected |
|---|---|---|
| 0 (lower) | -1 | ValueError |
| | 0 | 0.0 |
| | 1 | 100.0 |
| 12 (price change) | 11 | 1100.0 |
| | 12 | 1200.0 |
| | 13 | 1275.0 |
| 18 (upper) | 17 | 1575.0 |
| | 18 | 1650.0 |
| | 19 | ValueError |

### 5(c) How a wrong comparison causes a defect

Programmers often make mistakes at the edges of a range. For example:

- If the code used `current_credits < 15` instead of `current_credits <= 15`,
  a student with exactly 15 credits would be wrongly rejected. The test with 15
  catches this.
- If the code used `total > 19` instead of `total > 18`, a load of 19 would be
  wrongly allowed. The test with 15 + 4 = 19 catches this.
- If the fee code used `total_credits <= 13` instead of `total_credits <= 12`,
  13 credits would cost 1300 instead of 1275. The test with 13 catches this.
- If the fee code used `total_credits < 18` instead of `total_credits <= 18`,
  18 credits would raise an error. The test with 18 catches this.
- If the code used `total_credits > 0` instead of `total_credits >= 0`, 0 credits
  would raise an error. The test with 0 catches this.

A value in the middle of a range (like 6) passes even with these mistakes. Only
values right at and next to the edge reveal them.
