import json
import re
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.group import Group, GroupMember
from app.models.expense import Expense, ExpenseSplit, SplitType
from app.models.settlement import Settlement, SettlementStatus
from app.schemas.expense import ExpenseCreate, ExpenseSplitCreate
from app.schemas.settlement import SettlementCreate
from app.services.settlement_service import calculate_group_balances

class ChatbotService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user
    
    def process_message(self, message: str, group_id: Optional[int] = None) -> Dict:
        """Process user message and determine intent"""
        message_lower = message.lower()
        
        # Expense creation patterns
        if any(keyword in message_lower for keyword in ['spent', 'paid for', 'expense', 'cost', 'bought']):
            return self._handle_expense_intent(message, group_id)
        
        # Settlement patterns
        elif any(keyword in message_lower for keyword in ['owe', 'owes', 'pay back', 'settle', 'debt']):
            return self._handle_settlement_intent(message, group_id)
        
        # Balance inquiry patterns
        elif any(keyword in message_lower for keyword in ['balance', 'owe me', 'i owe', 'who owes']):
            return self._handle_balance_inquiry(message, group_id)
        
        # Group information patterns
        elif any(keyword in message_lower for keyword in ['group', 'members', 'expenses in']):
            return self._handle_group_inquiry(message, group_id)
        
        # General help
        else:
            return self._handle_general_response(message)
    
    def _handle_expense_intent(self, message: str, group_id: Optional[int]) -> Dict:
        """Handle expense-related messages"""
        try:
            # Extract amount using regex
            amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', message)
            if not amount_match:
                return {
                    "response": "I couldn't find an amount in your message. Please specify how much was spent.",
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            amount = float(amount_match.group(1))
            
            # Extract title/description
            title_patterns = [
                r'(?:spent|paid for|bought|expense for)\s+(.+?)(?:\s+for|\s+\$|\s+costing|$)',
                r'(.+?)\s+(?:cost|was|costing)\s+\$?\d+',
                r'(.+?)\s+for\s+\$?\d+'
            ]
            
            title = "Expense"
            for pattern in title_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    break
            
            # If no group specified, suggest available groups
            if not group_id:
                user_groups = self.db.query(Group).join(GroupMember).filter(
                    GroupMember.user_id == self.current_user.id
                ).all()
                
                if not user_groups:
                    return {
                        "response": "You need to be part of a group to add expenses. Would you like to create a group first?",
                        "actions_taken": [],
                        "suggested_actions": [{"action": "create_group", "description": "Create a new group"}]
                    }
                
                group_suggestions = [
                    {"action": "add_expense", "group_id": g.id, "group_name": g.name, 
                     "amount": amount, "title": title}
                    for g in user_groups
                ]
                
                return {
                    "response": f"I found an expense for '{title}' costing ${amount}. Which group should I add this to?",
                    "actions_taken": [],
                    "suggested_actions": group_suggestions
                }
            
            # Get group members for equal split
            group_members = self.db.query(GroupMember).filter(
                GroupMember.group_id == group_id
            ).all()
            
            if not group_members:
                return {
                    "response": "Group not found or you're not a member.",
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            return {
                "response": f"I can add an expense for '{title}' costing ${amount} split equally among {len(group_members)} members. Should I proceed?",
                "actions_taken": [],
                "suggested_actions": [{
                    "action": "confirm_expense",
                    "title": title,
                    "amount": amount,
                    "group_id": group_id,
                    "split_type": "equal",
                    "member_count": len(group_members)
                }]
            }
            
        except Exception as e:
            return {
                "response": "I had trouble understanding your expense. Could you try rephrasing?",
                "actions_taken": [],
                "suggested_actions": []
            }
    
    def _handle_settlement_intent(self, message: str, group_id: Optional[int]) -> Dict:
        """Handle settlement-related messages"""
        try:
            # Extract amount
            amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', message)
            if not amount_match:
                return {
                    "response": "Please specify the amount for the settlement.",
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            amount = float(amount_match.group(1))
            
            # Extract username patterns
            username_patterns = [
                r'(?:owe|owes|pay back|settle with)\s+(\w+)',
                r'(\w+)\s+owes',
                r'pay\s+(\w+)'
            ]
            
            username = None
            for pattern in username_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    username = match.group(1)
                    break
            
            if not username:
                return {
                    "response": "I couldn't identify who the settlement is with. Please specify the username.",
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            # Find user
            payee = self.db.query(User).filter(User.username == username).first()
            if not payee:
                return {
                    "response": f"I couldn't find a user with username '{username}'.",
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            return {
                "response": f"I can create a settlement of ${amount} to {payee.full_name} ({username}). Should I proceed?",
                "actions_taken": [],
                "suggested_actions": [{
                    "action": "confirm_settlement",
                    "payee_id": payee.id,
                    "payee_name": payee.full_name,
                    "amount": amount,
                    "group_id": group_id
                }]
            }
            
        except Exception as e:
            return {
                "response": "I had trouble understanding your settlement request. Could you try rephrasing?",
                "actions_taken": [],
                "suggested_actions": []
            }
    
    def _handle_balance_inquiry(self, message: str, group_id: Optional[int]) -> Dict:
        """Handle balance inquiries"""
        try:
            if group_id:
                balances = calculate_group_balances(group_id, self.db)
                user_balance = balances.get(self.current_user.id, Decimal('0'))
                
                group = self.db.query(Group).filter(Group.id == group_id).first()
                group_name = group.name if group else f"Group {group_id}"
                
                if user_balance > 0:
                    response = f"In {group_name}, you are owed ${user_balance:.2f}."
                elif user_balance < 0:
                    response = f"In {group_name}, you owe ${abs(user_balance):.2f}."
                else:
                    response = f"In {group_name}, you're all settled up!"
                
                # Add details about who owes what
                other_balances = []
                for user_id, balance in balances.items():
                    if user_id != self.current_user.id and balance != 0:
                        user = self.db.query(User).filter(User.id == user_id).first()
                        if user:
                            if balance > 0:
                                other_balances.append(f"{user.username} is owed ${balance:.2f}")
                            else:
                                other_balances.append(f"{user.username} owes ${abs(balance):.2f}")
                
                if other_balances:
                    response += " Other balances: " + ", ".join(other_balances)
                
                return {
                    "response": response,
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            else:
                # Show balances across all groups
                groups = self.db.query(GroupMember).filter(
                    GroupMember.user_id == self.current_user.id
                ).all()
                
                total_balance = Decimal('0')
                group_details = []
                
                for membership in groups:
                    group_balances = calculate_group_balances(membership.group_id, self.db)
                    user_balance = group_balances.get(self.current_user.id, Decimal('0'))
                    
                    if user_balance != 0:
                        group = self.db.query(Group).filter(Group.id == membership.group_id).first()
                        group_name = group.name if group else f"Group {membership.group_id}"
                        
                        total_balance += user_balance
                        if user_balance > 0:
                            group_details.append(f"{group_name}: owed ${user_balance:.2f}")
                        else:
                            group_details.append(f"{group_name}: owe ${abs(user_balance):.2f}")
                
                if total_balance == 0 and not group_details:
                    response = "You're all settled up across all groups!"
                else:
                    response = f"Overall balance: "
                    if total_balance > 0:
                        response += f"you are owed ${total_balance:.2f}"
                    elif total_balance < 0:
                        response += f"you owe ${abs(total_balance):.2f}"
                    else:
                        response += "you're balanced"
                    
                    if group_details:
                        response += "\n\nBreakdown:\n" + "\n".join(group_details)
                
                return {
                    "response": response,
                    "actions_taken": [],
                    "suggested_actions": []
                }
                
        except Exception as e:
            return {
                "response": "I had trouble calculating your balance. Please try again.",
                "actions_taken": [],
                "suggested_actions": []
            }
    
    def _handle_group_inquiry(self, message: str, group_id: Optional[int]) -> Dict:
        """Handle group-related inquiries"""
        try:
            if group_id:
                group = self.db.query(Group).filter(Group.id == group_id).first()
                if not group:
                    return {
                        "response": "Group not found.",
                        "actions_taken": [],
                        "suggested_actions": []
                    }
                
                members = self.db.query(GroupMember).filter(
                    GroupMember.group_id == group_id
                ).all()
                
                member_names = []
                for member in members:
                    user = self.db.query(User).filter(User.id == member.user_id).first()
                    if user:
                        member_names.append(user.full_name)
                
                recent_expenses = self.db.query(Expense).filter(
                    Expense.group_id == group_id
                ).order_by(Expense.created_at.desc()).limit(5).all()
                
                response = f"Group: {group.name}\n"
                response += f"Members: {', '.join(member_names)}\n"
                response += f"Recent expenses: {len(recent_expenses)} expenses"
                
                if recent_expenses:
                    expense_list = []
                    for exp in recent_expenses:
                        creator = self.db.query(User).filter(User.id == exp.created_by_id).first()
                        creator_name = creator.username if creator else "Unknown"
                        expense_list.append(f"${exp.amount:.2f} for {exp.title} by {creator_name}")
                    response += "\n" + "\n".join(expense_list)
                
                return {
                    "response": response,
                    "actions_taken": [],
                    "suggested_actions": []
                }
            
            else:
                # List all user's groups
                groups = self.db.query(Group).join(GroupMember).filter(
                    GroupMember.user_id == self.current_user.id
                ).all()
                
                if not groups:
                    response = "You're not a member of any groups yet. Would you like to create one?"
                    suggested_actions = [{"action": "create_group", "description": "Create a new group"}]
                else:
                    group_list = []
                    for group in groups:
                        member_count = self.db.query(GroupMember).filter(
                            GroupMember.group_id == group.id
                        ).count()
                        group_list.append(f"{group.name} ({member_count} members)")
                    
                    response = f"Your groups:\n" + "\n".join(group_list)
                    suggested_actions = []
                
                return {
                    "response": response,
                    "actions_taken": [],
                    "suggested_actions": suggested_actions
                }
                
        except Exception as e:
            return {
                "response": "I had trouble getting group information. Please try again.",
                "actions_taken": [],
                "suggested_actions": []
            }
    
    def _handle_general_response(self, message: str) -> Dict:
        """Handle general queries and provide help"""
        help_text = """I can help you with:
        
• Adding expenses: "I spent $20 on lunch" or "Paid $50 for groceries"
• Checking balances: "What do I owe?" or "Who owes me money?"
• Settlement tracking: "I owe John $10" or "Mark paid me back $25"
• Group information: "Show my groups" or "Who's in this group?"

Just tell me what you'd like to do in plain English!"""
        
        return {
            "response": help_text,
            "actions_taken": [],
            "suggested_actions": [
                {"action": "show_groups", "description": "View your groups"},
                {"action": "show_balance", "description": "Check your overall balance"}
            ]
        }