import sqlite3 as db
import os
import datetime


def addSampleTextandResponseToDatabase(sampleTexts,semantics):
    databaseName = 'ReqRespData.db'
    #dataBase = os.path.join(os.getcwd(), 'sid', databaseName)
    dataBase = os.path.join(os.getcwd(), databaseName)
    con = None
    try:
        # Connect to database, or create if it doesn't exist and connect
        con = db.connect(dataBase)
        cur = con.cursor()

        # Create table if it doesn't exist in current workig directory
        cur.execute("CREATE TABLE IF NOT EXISTS SampleTexts ( clientRequest TEXT, serverResponse TEXT )" )
    
        # Add sample text and its predicted semantics label to database
        i=0
        for text in sampleTexts:
            try:
                data = [text, str(semantics[i])]
                cur.execute("INSERT INTO SampleTexts VALUES( ? , ? )",data)
                i+=1
            except db.Error as e:
                raise e

        # commit changes to database
        con.commit()
    
        # Display all rows from SampleTexts table
        #cur.execute("SELECT * FROM SampleTexts")
        #rows = cur.fetchall()
        #for row in rows:
        #    print(row)

        # Print all tables in the database
        #res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #for name in res:
        #    print( name[0])
    
    # Create and/or update log file in case of database error and backup current
    # sample text in a backup file
    except db.Error as e:

        # Files will be created in current working directory
        backupFile = open('BackupSamples.txt', 'a+')
        logFile = open('DatabaseErrorLog.log', 'a+')

        # Sample Text is in quotes then label separated by single tab
        backupText = '"'+ sampleTexts[i].rstrip('\n\t').lstrip('\n\t') + '"' + '\t' + str(semantics[i]) +'\n'
        # Error message along with time when error occured
        errorMessage = 'Time Of Database Error : '+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) +\
                       '\tError : ' + str(e)+'\n'

        logFile.write(errorMessage)
        backupFile.write(backupText)

        logFile.close()
        backupFile.close()

    except Exception as e:
        # Files will be created in current working directory
        backupFile = open('BackupSamples.txt', 'a+')
        logFile = open('DatabaseErrorLog.log', 'a+')

        # Sample Text is in quotes then label separated by single tab
        backupText = '"'+ sampleTexts[i].rstrip('\n\t').lstrip('\n\t') + '"' + '\t' + str(semantics[i]) +'\n'
        # Error message along with time when error occured
        errorMessage = 'Time Of Exception : '+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) +\
                        '\tError : ' + str(e)+'\n'

        logFile.write(errorMessage)
        backupFile.write(backupText)

        logFile.close()
        backupFile.close()
    finally:
        if con:
            con.close()
    return

if __name__=='__main__':
    addSampleTextandResponseToDatabase(['apple launches iPhone54'],['10000 $'])