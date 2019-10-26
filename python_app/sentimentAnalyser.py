from textblob import TextBlob
import csv

class UserReview:
   userId = ''
   userLocation = ''
   title = ''
   reviewDate = ''
   rating = ''
   feedback = ''
   sentimentValue = -1


UserReviews = [] # store the userReviews data


#  opening the csv file 
csvfile = open('./reviews2.csv' ,encoding="utf8" )
readCSV = csv.reader(csvfile, delimiter=',')

# reading the values through csv
for row in readCSV:
    if(row and row[0] != ''):    # if row is null retrun                      
        feedbackString = row[5]
        blob = TextBlob(feedbackString) # adding phrase to the blob element 
        if(blob.subjectivity > 0.5): # if subjectivity is more than 0.5 review is accepted
            comment = UserReview()
            comment.userId = row[0]
            comment.userLocation = row[1]
            comment.reviewDate = row[2]
            comment.rating = int(row[3])/10 # ratings are multiples of 10 , scalng down to a range of 1 to 5
            comment.title = row[4]
            comment.feedback = row[5]
            comment.sentimentValue = blob.polarity
            UserReviews.append(comment)
csvfile.close()


# witing the new dataset to a new csv file 
with open('./ReviewAnalysis.csv', 'w', newline='',encoding='utf-8') as outfile:
    # for i in range(0,10):
    csvWriter = csv.writer(outfile)
    csvWriter.writerow(['User_Id','User_Location','Review_Date','Rating','Title','Feedback','Sentiment_Value'])
    for review in UserReviews:
        # review = UserReviews[i]
        
        csvWriter.writerow([review.userId , review.userLocation , review.reviewDate , review.rating , review.title , review.feedback , review.sentimentValue])
outfile.close()         