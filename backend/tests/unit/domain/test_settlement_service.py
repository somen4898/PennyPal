from decimal import Decimal

from src.domain.services.settlement_service import (
    calculate_balances_from_splits,
    generate_settlement_suggestions,
)


class TestCalculateBalances:
    def test_single_expense_two_users(self) -> None:
        # User 1 paid 100, split equally with user 2
        splits = [
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances[1] == Decimal("50")   # user 1 is owed 50
        assert balances[2] == Decimal("-50")  # user 2 owes 50

    def test_two_expenses_cancel_out(self) -> None:
        splits = [
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 2, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 2, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances.get(1, Decimal("0")) == Decimal("0")
        assert balances.get(2, Decimal("0")) == Decimal("0")

    def test_empty_splits(self) -> None:
        balances = calculate_balances_from_splits([])
        assert balances == {}


class TestGenerateSettlementSuggestions:
    def test_simple_two_user_settlement(self) -> None:
        balances = {1: Decimal("50"), 2: Decimal("-50")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        assert len(suggestions) == 1
        assert suggestions[0]["payer_id"] == 2
        assert suggestions[0]["payee_id"] == 1
        assert suggestions[0]["amount"] == Decimal("50")

    def test_three_users_minimized(self) -> None:
        # User 1 is owed 100, user 2 owes 60, user 3 owes 40
        balances = {1: Decimal("100"), 2: Decimal("-60"), 3: Decimal("-40")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        assert len(suggestions) == 2
        total_settled = sum(s["amount"] for s in suggestions)
        assert total_settled == Decimal("100")

    def test_all_balanced(self) -> None:
        balances = {1: Decimal("0"), 2: Decimal("0")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        assert suggestions == []


class TestCalculateBalancesAdvanced:
    def test_three_way_expense(self) -> None:
        # User 1 paid 300, split among 3
        splits = [
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("100"), "total_amount": Decimal("300")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("100"), "total_amount": Decimal("300")},
            {"expense_creator_id": 1, "user_id": 3, "amount": Decimal("100"), "total_amount": Decimal("300")},
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances[1] == Decimal("200")   # owed 200
        assert balances[2] == Decimal("-100")  # owes 100
        assert balances[3] == Decimal("-100")  # owes 100

    def test_multiple_expenses_same_creator(self) -> None:
        splits = [
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("25"), "total_amount": Decimal("50")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("25"), "total_amount": Decimal("50")},
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances[1] == Decimal("75")
        assert balances[2] == Decimal("-75")

    def test_large_group_balances(self) -> None:
        # User 1 paid 500, split equally among 5
        splits = [
            {"expense_creator_id": 1, "user_id": uid, "amount": Decimal("100"), "total_amount": Decimal("500")}
            for uid in range(1, 6)
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances[1] == Decimal("400")
        for uid in range(2, 6):
            assert balances[uid] == Decimal("-100")


class TestGenerateSettlementSuggestionsAdvanced:
    def test_four_users_complex(self) -> None:
        balances = {1: Decimal("70"), 2: Decimal("30"), 3: Decimal("-60"), 4: Decimal("-40")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        total = sum(s["amount"] for s in suggestions)
        assert total == Decimal("100")
        # All payers should be debtors (3, 4), all payees should be creditors (1, 2)
        for s in suggestions:
            assert s["payer_id"] in [3, 4]
            assert s["payee_id"] in [1, 2]

    def test_single_debtor_single_creditor(self) -> None:
        balances = {1: Decimal("200"), 2: Decimal("-200")}
        suggestions = generate_settlement_suggestions(balances, group_id=5)
        assert len(suggestions) == 1
        assert suggestions[0]["payer_id"] == 2
        assert suggestions[0]["payee_id"] == 1
        assert suggestions[0]["amount"] == Decimal("200")
        assert suggestions[0]["group_id"] == 5
