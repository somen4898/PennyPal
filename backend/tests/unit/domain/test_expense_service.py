from decimal import Decimal

import pytest

from src.domain.entities.expense import SplitType
from src.domain.exceptions import ValidationError
from src.domain.services.expense_service import calculate_splits


class TestCalculateEqualSplits:
    def test_equal_split_two_users(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("100.00"),
            split_type=SplitType.EQUAL,
            user_ids=[1, 2],
            split_amounts=None,
            split_percentages=None,
        )
        assert len(result) == 2
        assert result[0] == {"user_id": 1, "amount": Decimal("50.00"), "percentage": None}
        assert result[1] == {"user_id": 2, "amount": Decimal("50.00"), "percentage": None}

    def test_equal_split_three_users(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("100.00"),
            split_type=SplitType.EQUAL,
            user_ids=[1, 2, 3],
            split_amounts=None,
            split_percentages=None,
        )
        assert len(result) == 3
        for split in result:
            assert split["amount"] == Decimal("100.00") / 3

    def test_equal_split_empty_users_raises(self) -> None:
        with pytest.raises(ValidationError, match="At least one user"):
            calculate_splits(
                total_amount=Decimal("100.00"),
                split_type=SplitType.EQUAL,
                user_ids=[],
                split_amounts=None,
                split_percentages=None,
            )


class TestCalculateExactSplits:
    def test_exact_split_valid(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("100.00"),
            split_type=SplitType.EXACT,
            user_ids=[1, 2],
            split_amounts=[Decimal("60.00"), Decimal("40.00")],
            split_percentages=None,
        )
        assert result[0] == {"user_id": 1, "amount": Decimal("60.00"), "percentage": None}
        assert result[1] == {"user_id": 2, "amount": Decimal("40.00"), "percentage": None}

    def test_exact_split_sum_mismatch_raises(self) -> None:
        with pytest.raises(ValidationError, match="must equal total"):
            calculate_splits(
                total_amount=Decimal("100.00"),
                split_type=SplitType.EXACT,
                user_ids=[1, 2],
                split_amounts=[Decimal("60.00"), Decimal("30.00")],
                split_percentages=None,
            )

    def test_exact_split_missing_amounts_raises(self) -> None:
        with pytest.raises(ValidationError, match="Amount must be specified"):
            calculate_splits(
                total_amount=Decimal("100.00"),
                split_type=SplitType.EXACT,
                user_ids=[1, 2],
                split_amounts=None,
                split_percentages=None,
            )


class TestCalculatePercentageSplits:
    def test_percentage_split_valid(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("200.00"),
            split_type=SplitType.PERCENTAGE,
            user_ids=[1, 2],
            split_amounts=None,
            split_percentages=[Decimal("60"), Decimal("40")],
        )
        assert result[0] == {"user_id": 1, "amount": Decimal("120.00"), "percentage": Decimal("60")}
        assert result[1] == {"user_id": 2, "amount": Decimal("80.00"), "percentage": Decimal("40")}

    def test_percentage_split_not_100_raises(self) -> None:
        with pytest.raises(ValidationError, match="must sum to 100"):
            calculate_splits(
                total_amount=Decimal("200.00"),
                split_type=SplitType.PERCENTAGE,
                user_ids=[1, 2],
                split_amounts=None,
                split_percentages=[Decimal("60"), Decimal("30")],
            )

    def test_percentage_split_missing_raises(self) -> None:
        with pytest.raises(ValidationError, match="Percentage must be specified"):
            calculate_splits(
                total_amount=Decimal("200.00"),
                split_type=SplitType.PERCENTAGE,
                user_ids=[1, 2],
                split_amounts=None,
                split_percentages=None,
            )


class TestEdgeCases:
    def test_single_user_equal_split(self) -> None:
        result = calculate_splits(Decimal("100.00"), SplitType.EQUAL, [1], None, None)
        assert len(result) == 1
        assert result[0]["amount"] == Decimal("100.00")

    def test_zero_amount_equal_split(self) -> None:
        result = calculate_splits(Decimal("0"), SplitType.EQUAL, [1, 2], None, None)
        assert all(s["amount"] == Decimal("0") for s in result)

    def test_large_group_equal_split(self) -> None:
        user_ids = list(range(1, 11))  # 10 users
        result = calculate_splits(Decimal("1000.00"), SplitType.EQUAL, user_ids, None, None)
        assert len(result) == 10
        assert all(s["amount"] == Decimal("100.00") for s in result)

    def test_exact_split_count_mismatch_raises(self) -> None:
        with pytest.raises(ValidationError, match="Amount must be specified"):
            calculate_splits(Decimal("100"), SplitType.EXACT, [1, 2], [Decimal("100")], None)

    def test_percentage_count_mismatch_raises(self) -> None:
        with pytest.raises(ValidationError, match="Percentage must be specified"):
            calculate_splits(Decimal("100"), SplitType.PERCENTAGE, [1, 2], None, [Decimal("100")])
