''' This is carecrew api for customer '''
from api.app import create_app
#entry point in the app
if __name__ == '__main__':
  app = create_app(rest='True')

  # run app
  app.run(debug=True)
