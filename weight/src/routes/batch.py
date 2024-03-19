import os
from flask import Flask, Blueprint, jsonify, request
from ..models import Container
from ..database import db
import csv
import json
from ..config import logger

batch_blueprint = Blueprint('batch_blueprint', __name__)

IN_FOLDER = './in'

@batch_blueprint.route('/batch', methods=['POST'])
def process_batch():
    if 'file' not in request.json: 
        return jsonify({'error': 'No file specified in the request body'}), 400

    filename = request.json['file']
    if not filename:
        return jsonify({'error': 'The File specified is empty'}), 400

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
            for row in csv_reader:
                container_id = row.get('id')
                if not container_id: 
                    continue
                weight = row.get('kg') or row.get('lbs') or None
                unit = 'kg' if 'kg' in row else 'lbs'
                
                existing_container = Container.query.filter_by(container_id=container_id).first()
                if existing_container:
                    existing_container.weight = weight
                    existing_container.unit = unit
                else:
                    new_container = Container(container_id=container_id, weight=weight, unit=unit)
                    db.session.add(new_container)
                    
            db.session.commit()
            logger.info(f"CSV file processed successfully: {file_path}")
            return jsonify({'message': 'CSV file processed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing CSV file {file_path}: {str(e)}")
        return jsonify({'error': f'Error processing CSV file: {str(e)}'}), 500


def process_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            print("JSON Data:", json_data) 
            for item in json_data:
                print(f"Processing item: {item}")
                container_id = item.get('id', None)
                print(container_id)
                if not container_id: 
                    continue 

                weight = item.get('weight')
                unit = item.get('unit')

                existing_container = Container.query.filter_by(container_id=container_id).first()
                if existing_container:
                    existing_container.weight = weight
                    existing_container.unit = unit
                else:
                    new_container = Container(container_id=container_id, weight=weight, unit=unit)
                    db.session.add(new_container)

            db.session.commit()
            logger.info(f"JSON file processed successfully: {file_path}")
            return jsonify({'message': 'JSON file processed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error processing JSON file {file_path}: {str(e)}")
        return jsonify({'error': f'Error processing JSON file: {str(e)}'}), 500




