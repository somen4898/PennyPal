from src.domain.entities.user import User
from src.domain.ports.ai_client import AiClient
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.services.settlement_service import calculate_balances_from_splits

SYSTEM_PROMPT = """You are PennyPal, a helpful expense-splitting assistant.
You help users manage shared expenses, check balances, and settle debts.

When the user wants to add an expense, extract: title, amount, and suggest equal split.
When the user asks about balances, summarize who owes whom.
When the user wants to settle, confirm the amount and recipient.

Respond in a friendly, concise manner. Use currency symbol as per context (default INR ₹).

Current user context:
{user_context}

Group balances:
{balance_context}
"""


class SendChatMessageCommand:
    def __init__(
        self,
        ai_client: AiClient,
        group_repo: GroupRepository,
        expense_repo: ExpenseRepository,
    ) -> None:
        self._ai_client = ai_client
        self._group_repo = group_repo
        self._expense_repo = expense_repo

    async def execute(self, message: str, user: User, group_id: int | None = None) -> dict:
        user_context = f"Name: {user.full_name}, Username: {user.username}"

        balance_context = "No group selected."
        if group_id:
            splits = await self._expense_repo.get_group_splits(group_id)
            balances = calculate_balances_from_splits(splits)
            group = await self._group_repo.get_by_id(group_id)
            group_name = group.name if group else f"Group {group_id}"
            balance_lines = []
            for uid, bal in balances.items():
                if bal > 0:
                    balance_lines.append(f"User {uid} is owed ₹{bal:.2f}")
                elif bal < 0:
                    balance_lines.append(f"User {uid} owes ₹{abs(bal):.2f}")
            balance_context = (
                f"Group: {group_name}\n" + "\n".join(balance_lines)
                if balance_lines
                else f"Group: {group_name} — all settled"
            )

        system = SYSTEM_PROMPT.format(user_context=user_context, balance_context=balance_context)

        response = await self._ai_client.send_message(message=message, system_prompt=system)

        return {
            "response": response,
            "actions_taken": [],
            "suggested_actions": [],
        }
