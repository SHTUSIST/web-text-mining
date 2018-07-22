from bs4 import BeautifulSoup
import requests
import re
import csv
import sys

def text_process(sources, session, writer):
    page = 1
    for source in sources:
        try:
            sys.stdout.write("\rprocessing %d/%d\n" % (page, len(sources)))
            sys.stdout.flush()
            page += 1
            soup = BeautifulSoup(source,'lxml')
            questions = []
            #followers
            follower = soup.find('span', {'class':'icon_action_bar-count'}).get_text().lstrip(' · ')
            #question
            question = soup.find('span', class_='rendered_qtext').get_text()
            print(question)

            topic = soup.find_all('span', class_ = "name_text")
            topic_list = []
            for each in topic:
                topic_list.append(each.text)
            while len(topic_list) <= 5:
                topic_list.append('1!')


            questions.append(follower)
            questions.append(question)
            questions.append(topic_list)
            #answers(text,viewer,upvote, )
            answers = []
            blocks = soup.find_all('div', {'class':'pagedlist_item'})
            for block in blocks:
                try:
                    text = block.find('div', {'class':'ui_qtext_expanded'}).get_text()


                    viewer = block.find('span', {'class':'meta_num'}).get_text()

                    upvote = block.find('span',{'class':'icon_action_bar-count'}).get_text().lstrip(' · ')

                    user_block = block.find('a', {'class':'user'})
                    user_href = re.search(r'href="(.*?")', str(user_block)).group()
                    user_link = user_href.lstrip('href=').replace('"','')

                    user_pagesource = session.get('https://www.quora.com'+user_link, allow_redirects = False).text
                    user_soup = BeautifulSoup(user_pagesource, 'lxml')

                    user_follower_block = user_soup.find('span', {'class':'icon_action_bar-count'})
                    user_follower = user_follower_block.get_text().lstrip(' · ')

                    user_answers_block = user_soup.find('div',{'class':'nav_item_selected'})
                    user_answers = user_answers_block.find('span', {'class':'list_count'}).get_text()


                    img_list = block.find_all('img')
                    zoomable_img = []
                    for each in img_list:
                        if 'zoomable' in str(each):
                            zoomable_img.append(each)
                    img_num = len(zoomable_img)

                    external_link = block.find_all('a', class_="external_link")
                    link_num = len(external_link)
                except:
                    continue


                answers.append(text)
                answers.append(viewer)
                answers.append(upvote)
                answers.append(user_follower)
                answers.append(user_answers)
                answers.append(img_num)
                answers.append(link_num)

                questions.append(answers)
                answers = []

            '''
            输出格式：列表
            第0位为followers
            第1位为question
            第2位为topic列表（默认含6个topic，不足用 字符串"1!"占位）
            第3位及以后为answer列表（默认含6个元素，第0位为 文本，第1位为 浏览量，第2位为 赞同数，第3位为 该作者被关注数，第4位为 图片数，第5位为 外链数）
                后续answer列表形式与第三位相同
            '''

            #print(all_)
            while True:
                try:
                    #print(questions)
                    follower = questions[0]
                    question = questions[1]
                    topic_1 = questions[2][0]
                    topic_2 = questions[2][1]
                    topic_3 = questions[2][2]
                    topic_4 = questions[2][3]
                    topic_5 = questions[2][4]
                    topic_6 = questions[2][5]
                    answerr = questions.pop(3)
                    answer_text = answerr[0]
                    viewer = answerr[1]
                    upvote = answerr[2]
                    user_follower = answerr[3]
                    user_answers = answerr[4]
                    img = answerr[5]
                    link = answerr[6]
                    writer.writerow([follower, question, topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, answer_text, viewer, upvote, user_follower, user_answers, str(img), str(link)])
                
                except IndexError:
                    print('Index Finished')
                    break
                '''
                except:
                    print('Error when saving Question: ' + str(question))
                    pass
                '''
            questions = []
        except ConnectionError:
            print('ConnectionError when Crawling Page:' + str(page))
            pass
