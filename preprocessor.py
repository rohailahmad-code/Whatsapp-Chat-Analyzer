# import pandas as pd
# import re
# def preprocess(data):
#     # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#     # pattern = r'\[\d{2}/\d{2}/\d{4},\s\d{2}:\d{2}:\d{2}\]'

#     # Define regex patterns for dates and messages
#     date_pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\]'
#     message_pattern = r'\] ([^:]+): (.*)'

#     # Find all matches
#     dates = re.findall(date_pattern,data)
#     messages = re.findall(message_pattern,data)


#     df = pd.DataFrame({'User_message' : messages , 'message_date': dates})

#     # df['message_date'] = pd.to_datetime(df['message_date'], format = '%d/%m/%y, %H:%M - ')
#     df.rename(columns = {'message_date': 'date'}, inplace = True)

#     users = []
#     messages = []
#     for message in df['User_message']:
#         entry = re.split('([\w\W]+?):\s', message, 1)  # Add maxsplit argument
#         if entry[1:]:
#             users.append(entry[1])
#             messages.append(entry[2])
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns = ['User_message'], inplace = True)

#     df['year'] = df['date'].dt.year
#     df['month'] = df['date'].dt.month_name()
#     df['hour']= df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute
#     df['month_num'] = df['date'].dt.month
#     df['only_date'] = df['date'].dt.date
#     df['day_name'] =df['date'].dt.day_name()
#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour+1))
#         else: 
#             period.append(str(hour) + "-" + str(hour+1))

#     df['period'] = period
    
#     return df


import pandas as pd
import re

def preprocess(data):
    # Define regex patterns for dates and messages
    date_pattern = r'\[(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2})\]'
    message_pattern = r'\] ([^:]+): (.*)'

    # Find all matches
    dates = re.findall(date_pattern, data)
    messages = re.findall(message_pattern, data)
    
    # Reconstruct full messages
    full_messages = [f"{user}: {message}" for user, message in messages]

    df = pd.DataFrame({'User_message': full_messages, 'message_date': dates})

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M:%S')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Split user and message content
    users = []
    message_texts = []
    for user_message in df['User_message']:
        entry = re.split(r'([^:]+):\s', user_message, maxsplit=1)
        if len(entry) > 1:
            users.append(entry[1].strip())
            message_texts.append(entry[2].strip())
        else:
            users.append('group_notification')
            message_texts.append(entry[0].strip())

    df['user'] = users
    df['message'] = message_texts
    df.drop(columns=['User_message'], inplace=True)

    # Extract additional datetime features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    # Create period feature
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour:02d}-00")
        else:
            period.append(f"{hour:02d}-{(hour + 1) % 24:02d}")

    df['period'] = period
    
    return df