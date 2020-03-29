from config import TELEGRAM_TOKEN, CHAT_ID
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time 
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app import data
from app import helper
from noti import send
import os

updater = Updater(TELEGRAM_TOKEN)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def build_button(text_list, callback_header = "") : # make button list
    button_list = []
    text_header = callback_header
    if callback_header != "" :
        text_header += ","

    for text in text_list :
        button_list.append(InlineKeyboardButton(text, callback_data=text_header + text))

    return button_list

main_menu = ["국내현황", "병원찾기", "생존일기"]
main_menu.append("취소")

def main_command(bot, update):
    button_list = build_button(main_menu) # make button list
    show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1)) # make markup
    update.message.reply_text("원하시는 메뉴를 선택해주세요.", reply_markup=show_markup) # reply text with markup

gall = "판데믹 갤러리입니다.\n\n"+f'https://gall.dcinside.com/mgallery/board/lists?id=thepandemic'
    
def gall_command(bot, update):
    send(gall)

def local_command(bot, update):
    print("local")
    send(data)

hospital="국내 응급실 찾기\nhttps://www.e-gen.or.kr/egen/main.do"

def hospital_command(bot, update):
    print("hospital")
    send(hospital)

diary_writter = ["부산 판붕이"]
diary_writter.append("취소")

head = 80;
diary = "생존일기 목록입니다.\n\n"+f'https://gall.dcinside.com/mgallery/board/lists/?id=thepandemic&sort_type=N&search_head={head}'

def diary_command(bot, update):
    print("diary")
    #button_list = build_button(diary_writter) # make button list
    #show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1)) # make markup
    #update.message.reply_text("생존일기 목록입니다.\n\n"+f'https://m.dcinside.com/board/thepandemic?headid={head}', reply_markup=show_markup) # reply text with markup
    send(diary)

def callback_get(bot, update):
    data_selected = update.callback_query.data
    print("callback : " + data_selected)

    for i in main_menu:
        if "취소" in data_selected:
            print("취소" == data_selected)
            bot.edit_message_text(text="취소하였습니다.",
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

        if "국내현황" in data_selected:
            bot.edit_message_text(text=data,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

        if "병원찾기" in data_selected:
            print("병원찾기" == data_selected)
            bot.edit_message_text(text=hospital,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

        if "생존일기" in data_selected:
            print("생존일기" == data_selected)
            #button_list = build_button(diary_writter)
            #show_markup = InlineKeyboardMarkup(build_menu(button_list, len(button_list) - 1))
            bot.edit_message_text(text=diary,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)

    #for j in diary_writter:
    #    if j == data_selected:
    #        if j == "부산 판붕이":
    #            writter = "생존일기"
    #        bot.edit_message_text(text=j+"의 생존일기입니다.\n\n"+f'https://gall.dcinside.com/mgallery/board/lists/?id=thepandemic&sort_type=N&search_head={head}&s_type=search_name&s_keyword={writter}&page=1'.format(update.callback_query.data),
    #                          chat_id=update.callback_query.message.chat_id,
    #                          message_id=update.callback_query.message.message_id)
    #        return

main_handler = CommandHandler('start', main_command)
updater.dispatcher.add_handler(main_handler)

gall_handler = CommandHandler('gall', gall_command)
updater.dispatcher.add_handler(gall_handler)

gallery_handler = CommandHandler('gallery', gall_command)
updater.dispatcher.add_handler(gallery_handler)

hospital_handler = CommandHandler('hospital', hospital_command)
updater.dispatcher.add_handler(hospital_handler)

local_handler = CommandHandler('local', local_command)
updater.dispatcher.add_handler(local_handler)

diary_handler = CommandHandler('diary', diary_command)
updater.dispatcher.add_handler(diary_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))

updater.start_polling(timeout=0, clean=True)
updater.idle()
