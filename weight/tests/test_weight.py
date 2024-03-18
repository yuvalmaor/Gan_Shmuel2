from src.models import Transaction, Container


def test(app):
    response = 1 + 1
    
    with app.app_context():
        containers_count = Container.query.count()
        print(containers_count)
        
        containers_count = Transaction.query.count()
        print(containers_count)

    assert response == 2