# Approach

I created a class called edgarUser to hold all relevant information for a particular IP making a request, such as IP address, first request datetime, latest request datetime, and number of requests in the current session.

I created a dictionary of edgarUsers with their IPs as keys to be able to quickly update a specific user's session details.

I created a list to store IPs in order of which were going to finish their sessions soonest (latest request), and replaced the position of some IPs in the list if their sessions were extended by a new request.

I created another list to store IPs with active sessions in order of the time of their current session's first request.

For every line read, I checked to see if the IP of the request was already in the dictionary, and if it was I checked if that user had an active session. If so, I incremented the number of requests and updated the latest request and datetime. If not, I set the number of requests to 1 and updated the first and latest request and datetime.

I checked if the IP of the latest request was in the list sorted by latest request, and if it was there I moved it to the back of the list, as it "refreshed" that IP's current session. If not, I appended it to both lists.

I looped through the list holding IPs sorted by first request and checked if their sessions had ended by comparing their latest datetimes to the current request's datetime, and wrote their session information to the output file if they had ended, then removed those IPs from the list.

After the file was finished reading, I looped through the list sorted by first request to output the remaining active sessions in order of their first request.
