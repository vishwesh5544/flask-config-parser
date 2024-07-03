from flask import Flask, jsonify
from config_loader import ConfigLoader
from config_service import ConfigService

app = Flask(__name__)

# Load configuration
config_loader = ConfigLoader(config_dir='./config')
app_config = config_loader.load_config()

# Initialize configuration service
config_service = ConfigService(config_dir='./config')

# Define a simple route to verify the configuration
@app.route('/')
def index():
    config_dict = config_service.get_configs_as_dict()
    return jsonify(config_dict)

if __name__ == '__main__':
    app.run(host=app.config['SERVER_ADDRESS'], port=app.config['SERVER_PORT'])