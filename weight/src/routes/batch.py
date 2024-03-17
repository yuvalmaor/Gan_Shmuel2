import os
from flask import Flask, Blueprint, jsonify, request
from ..models import Container
from ..database import db
import csv
import json
from ..config import logger

batch_blueprint = Blueprint('batch_blueprint', __name__)

IN_FOLDER = 'in'

@batch_blueprint.route('/batch', methods=['POST'])
def process_batch():
    if 'file' not in request.json: # checking if the 'file' key is present in the JSON data
        return jsonify({'error': 'No file specified in the request body'}), 400

    filename = request.json['file']
    if not filename: # checking if the retrieved filename is empty
        return jsonify({'error': 'No file specified in the request body'}), 400

    file_path = os.path.join(IN_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({'error': f'File {filename} not found in the {IN_FOLDER} folder'}), 404

    if filename.endswith('.csv'):
        process_csv(file_path)
    elif filename.endswith('.json'):
        process_json(file_path)
    else:
        return jsonify({'error': 'Unsupported file format'}), 400

    return jsonify({'message': 'Batch processing completed'}), 200

def process_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            containers = []
            for row in csv_reader:
                container_id = row['id']
                weight = None
                unit = None

                try:
                    if 'kg' in row:
                        weight = int(row['kg']) if row['kg'] else None
                        unit = 'kg'
                    elif 'lbs' in row:
                        weight = int(row['lbs']) if row['lbs'] else None
                        unit = 'lbs'

                    if weight is None or unit is None:
                        logger.info(f"Skipping container {container_id} due to missing weight or unit information.")
                        continue

                    container = Container(container_id=container_id, weight=weight, unit=unit)
                    containers.append(container)
                except ValueError as e:
                    logger.error(f"Error processing container {container_id}: {e}")
                    continue

            if not containers:
                logger.info("No valid containers found in the CSV file. Adding placeholder container.")
                # Add a placeholder container with null values
                placeholder_container = Container(container_id='N/A', weight=None, unit=None)
                containers.append(placeholder_container)

            db.session.add_all(containers)
            db.session.commit()
            return jsonify({'message': 'CSV processing completed successfully'}), 200
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return jsonify({'error': f'File not found: {file_path}'}), 404
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return jsonify({'error': f'Error processing CSV file: {e}'}), 500


def process_csv(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            containers = []
            for row in csv_reader:
                container_id = row['id']
                if not container_id:  # Check if container_id is empty
                    container_id = None
                weight = row.get('kg') or row.get('lbs')
                if weight == '':
                    weight = None
                unit = 'kg' if 'kg' in row else 'lbs'

                container = Container(container_id=container_id, weight=weight, unit=unit)
                containers.append(container)

            db.session.add_all(containers)
            db.session.commit()

            logger.info(f"CSV file processed successfully: {file_path}")
            return jsonify({'message': 'CSV file processed successfully'}), 200

    except Exception as e:
        logger.error(f"Error processing CSV file {file_path}: {str(e)}")
        return jsonify({'error': f'Error processing CSV file: {str(e)}'}), 500

def process_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            containers = []
            for item in json_data:
                container_id = item['id']
            # Get weight and unit from the JSON item
            weight = item.get('weight')
            unit = item.get('unit')
            
            # Check if the unit is valid (either 'kg' or 'lbs')
            if unit not in ['kg', 'lbs']:
                logger.info(f"Invalid unit '{unit}' for container {container_id}. Setting unit to None.")
                unit = None
            
            # Convert empty string weight to None
            if not weight:
                weight = None

                container = Container(container_id=container_id, weight=weight, unit=unit)
                containers.append(container)

            db.session.add_all(containers)
            db.session.commit()

            logger.info(f"JSON file processed successfully: {file_path}")
            return jsonify({'message': 'JSON file processed successfully'}), 200

    except Exception as e:
        logger.error(f"Error processing JSON file {file_path}: {str(e)}")
        return jsonify({'error': f'Error processing JSON file: {str(e)}'}), 500



