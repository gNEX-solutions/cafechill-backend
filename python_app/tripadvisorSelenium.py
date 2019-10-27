# import csv
import time
from selenium import webdriver
from textblob import TextBlob
from selenium.common.exceptions import NoSuchElementException
# ****** creating the firbase auth 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore   
from google.cloud import exceptions     


#   ************************** import the webdriver and featuring the web url ****************************
driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://www.tripadvisor.com/Restaurant_Review-g616035-d2051648-Reviews-Cafe_Chill-Ella_Uva_Province.html")


# **************** getting the firestore database and initialising it  ******************************
cred = credentials.Certificate('./fireapp-58e6e-firebase-adminsdk-9zyak-1c7a34bb01.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# **************** counts regard to the reviews ***************************
reviewCount = 0 # review id 
pagesCount = 0  # no of pages to be scraped 
lastPageReviewsCount = 0 # no of reviews scraped in last page 



# *********** function to get the number of reviws to be added *********************************
def getReviewDifference():
    global reviewCount , pagesCount , lastPageReviewsCount
    countsWords = driver.find_element_by_class_name('pagination-details').text.split() 
    webReviewCount = int(countsWords[4].replace(',','')) # number of reviews in the web
    firebaseReviewCount = 0 # numberof engreviews on the firbase 
    reviewCounRef = db.collection(u'ReviewCount').document(u'English')
    try:
        doc = reviewCounRef.get()
        data = doc.to_dict()
        firebaseReviewCount = data['amount']
        
        pagesCount = int( (webReviewCount - firebaseReviewCount)/10 ) +1
        lastPageReviewsCount = (webReviewCount - firebaseReviewCount)%10
        reviewCount = firebaseReviewCount + 1
    except exceptions.NotFound:
        pagesCount = 0
        lastPageReviewsCount = 0
        print(u'error occured in getting data')

    print('dj')


# ************************ function to check if the button is on the page ***********************
        
def check_exists_by_classname(classname):
    try:
        driver.find_element_by_class_name(classname)
    except NoSuchElementException:
        return False
    return True

# open the file to save the review
# csvFile = open('../reviews2.csv', 'a', encoding='utf-8')
# csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

def sentiment_analyser(feedbackString ):
    blob = TextBlob(feedbackString)
    return blob.polarity, blob.subjectivity
    
    # if(blob.subjectivity > 0.5): # if the subjectivity is less than 0.5 it is ignored and hence return -2
    #     return blob.polarity
    # else:
    #     return -2


getReviewDifference()

# ***************** extracting the data with the use of selennium *******************

for i in range(0,pagesCount):
    #  arrays to store the eading info and element info 
    headingElements = []
    headings= []

    contentElements = []
    contents = []

    ratingElements = []
    ratings = []

    userInfoElements = []
    userNames = []
    userLocations = []

    reviewDateElements = []
    reviewDates = []


    visitedDateElements = []
    visitedDates = []


    if(check_exists_by_classname('ulBlueLinks')):
        moreLink = driver.find_element_by_class_name('ulBlueLinks')
        moreLink.click()
        time.sleep(1)

    # check elemens exists with the classnames 
    
    if(check_exists_by_classname('noQuotes')):
        headingElements = driver.find_elements_by_class_name('noQuotes')
    
    if(check_exists_by_classname('partial_entry')):
        contentElements = driver.find_elements_by_class_name('partial_entry')
    
    if(check_exists_by_classname('ui_bubble_rating')):
        ratingElements = driver.find_elements_by_xpath(".//div[contains(@class, 'rev_wrap ui_columns')]//div[contains(@class, 'is-9')]//span[contains(@class, 'ui_bubble_rating bubble_')]")

    if(check_exists_by_classname('info_text')):
        # userInfoElements = driver.find_elements_by_xpath(".//div[contains(@class, 'info_text')//div][1]")
        userInfoElements = driver.find_elements_by_class_name('info_text')

    if(check_exists_by_classname('ratingDate')):
        reviewDateElements = driver.find_elements_by_class_name('ratingDate')

    if(check_exists_by_classname('prw_reviews_stay_date_hsx')):
        visitedDateElements = driver.find_elements_by_class_name('prw_reviews_stay_date_hsx')

    
 # ************* add the contents to the headings  contents and ratings *****************
    for element in headingElements:
        headings.append(element.text)
    for element in contentElements:
        contents.append(element.text)
    for element in ratingElements:
        className = element.get_attribute("class").split("_")
        ratings.append(className[3])

    for element in userInfoElements:
        info = element.text.split('\n')
        if(len(info) > 0 ):
            userNames.append(info[0])
        else: 
            userNames.append('Anonymous')
        
        if(len(info) > 1):
            userLocations.append(info[1])
        else :
            userLocations.append(' ')
        

    for element in reviewDateElements:
        reviewDates.append(element.get_attribute("title"))
    
    for element in visitedDateElements:
        dateString = element.text
        visitedDates.append(dateString[15:len(dateString)])

    if( i < pagesCount - 1):
    
        for j in range(0,len(headings)):
            sentimentVal , subjectivity = sentiment_analyser(contents[j])  # getting the sentiment value 
            currentTime = time.ctime()[4:]
        
            rating = float(ratings[j])/10
            doc_ref = db.collection(u'Reviews').document(str(reviewCount))

            # doc_ref.set({
            #     u'feedback': contents[j],
            #     u'rating': rating,
            #     u'reviewDate': reviewDates[j],
            #     u'visitedDate': visitedDates[j],
            #     u'sentimentValue': sentimentVal,
            #     u'title': headings[j],
            #     u'userId': userNames[j],
            #     u'userLocation': userLocations[j],
            #     u'subjectivity': subjectivity,
            #     u'addedTimeAudit': currentTime
            # })
            reviewCount += 1
    else :
        for j in range(0,lastPageReviewsCount):
            sentimentVal , subjectivity = sentiment_analyser(contents[j])  # getting the sentiment value 
            currentTime = time.ctime()[4:]
        
            rating = float(ratings[j])/10
            doc_ref = db.collection(u'Reviews').document(str(reviewCount))

            # doc_ref.set({
            #     u'feedback': contents[j],
            #     u'rating': rating,
            #     u'reviewDate': reviewDates[j],
            #     u'visitedDate': visitedDates[j],
            #     u'sentimentValue': sentimentVal,
            #     u'title': headings[j],
            #     u'userId': userNames[j],
            #     u'userLocation': userLocations[j],
            #     u'subjectivity': subjectivity,
            #     u'addedTimeAudit': currentTime
            # })
            reviewCount += 1
        

    print('page ' + str(i+1) +' completed')
    print('headings ' +str(len(headings)) )
    print('ratings ' + str(len(ratings)))
    print('contents ' + str(len(contents)))
    print('review date ' + str(len(reviewDates)))
    # else:
        # print('error in page ' + str(i+1))

    # to change the page
    driver.find_element_by_xpath('//a[@class="nav next taLnk ui_button primary"]').click()
    time.sleep(2)
    

# *********************** finally update the total count on the db ***************
reviewCount -= 1
docRefCount = db.collection(u'ReviewCount').document('English')
currentTime = time.ctime()[4:]
docRefCount.set({
                u'amount': reviewCount,
                u'editedTime': currentTime,
                u'language': 'English'
            })
driver.close()
# csvFile.close()
