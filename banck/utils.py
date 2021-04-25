def create_error(message, status):
  return {
    'error': True,
    'message': message,
    'status': status
  }