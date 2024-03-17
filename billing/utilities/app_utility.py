from app import db,logger
from app.models import Rate, Provider
import os


def add_rates_to_rates_db(updates):
        for update in updates:
            product_id = update['product_id']
            rate = update['rate']
            scope = update['scope']
            provider_id = scope
            if scope == 'All':
                provider = Provider.query.filter_by(name='ALL').first()
                if provider is None:
                    # Create a new provider with name 'ALL'
                    new_provider = Provider(name='ALL')
                    db.session.add(new_provider)
                    db.session.flush()  # Flush to get the ID of the newly created provider
                    provider_id = new_provider.id
                else:
                    provider_id = provider.id

            # Update or create rate in the database
            existing_rate = Rate.query.filter_by(product_id=product_id, scope=provider_id)
            if existing_rate:
                existing_rate.rate = rate
            elif existing_rate and (not scope == "ALL"):
                 existing_rate.scope = provider_id
            elif not existing_rate:
                new_rate = Rate(product_id=product_id, rate=rate, scope=provider_id)
                db.session.add(new_rate)

        # Commit changes to the database
        db.session.commit()



def delete_prev_rates_file(in_directory):

    existing_files = os.listdir(in_directory)

        # Delete existing file if it exists
    for existing_file in existing_files:
        if existing_file.endswith('.xlsx'):
            os.remove(os.path.join(in_directory, existing_file))