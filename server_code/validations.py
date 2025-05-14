import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import re

@anvil.server.callable
def is_valid_email(email):
  # Simple and reasonably safe email validation
  pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
  print (f"Email: {re.match(pattern, email) is not None}")
  return re.match(pattern, email) is not None

# @anvil.server.callable
# def is_valid_phone(phone):
#   # Allow optional leading plus sign, followed by at least 6 digits, no spaces
#   return re.fullmatch(r"\+?\d{6,}", phone) is not None

@anvil.server.callable
def is_valid_phone(phone):
  # Remove common formatting characters
  digits_only = re.sub(r"[^\d]", "", phone)

  # Validate that we have at least 7 digits
  return len(digits_only) == 10 