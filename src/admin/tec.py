from admin import admin_blue
from flask import request, jsonify
import models
from util import login_required
from app import db
import datetime


@admin_blue.route('/SearchCard', methods=['POST','GET'])
@login_required
def SearchCard():
    username = request.values.get('id')
    if username == '':
        cards = models.Card.query.all()
    else:
        cards = models.Card.query.filter_by(id=username).all()
    CardList = []
    for card in cards:
        CardList.append(card.as_dict())
    return jsonify({'errno': 0, 'errmsg': 'ok', 'CardList': CardList})


@admin_blue.route('/SaveCard', methods=['POST'])
@login_required
def SaveCard():
    username = request.json.get('id')
    CardOn = request.json.get('CardOn')
    EmailOn = request.json.get('EmailOn')

    card_exist = models.Card.query.filter_by(id=username).first()
    if card_exist == None:
        return jsonify({'errno': 121, 'errmsg': 'invalid_user'}), '400 ERR'
    elif CardOn == False and EmailOn == True:
        return jsonify({'errno': 127, 'errmsg': 'logic_error'})
    else:
        card_exist.CardOn = CardOn
        card_exist.EmailOn = EmailOn
        db.session.add(card_exist)
        db.session.commit()
        return jsonify({'errno': 0, 'errmsg': 'ok'}) 

# 自动打卡定时任务
def card():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    cards = models.Card.query.all()
    for card in cards:
        if card.CardOn == 1:
            doCard(id=card.id, email=card.email)

def doCard(id, email):
    print(id)
    print(email)
