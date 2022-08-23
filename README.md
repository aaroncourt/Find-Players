# Individual-Capstone-Project aka Find Players
This was my individual capstone project at Coding Dojo. I used Python, Flask, and MySQL to make a website for board game players. The website allows users to search for each other and search for board games. The player search results are provided by a ZIP Code radius search using a ZIP Code API and the results are then queried against the database to select users with those ZIP Codes and then display them. The boardgame results are retreived from a different API provided by Board Game Atlas. The website also allows users to favorite other users, favorite games, and mark games that you own. The site features user registration and login. There are future developments planned. 

A walkthru of the site which demonstrates the site's functionality can be found here: https://youtu.be/8fFeOaJaIyk.  
If you prefer only a demonstration with no guided walkthru, you can find that video here: https://youtu.be/_20WnQkOuMc.  


### Backlog Items:
1. Ability for users to change their passwords
2. Ability for users to send messages to other users
3. Ability for users to block other users
4. Login as a popup instead of seperate page
5. Show all games user has favorited on search results
6. Be able to favorite a user/game from the results page using JS
    * Eventually code all favorite/own buttons for users and games to use JS to increase server efficency by reducing # of API calls
7. ~~Require being logged in to search for players~~
8. Add avatars for players to choose from
9. Add a no search results page
10. Create repository and api call class 
11. Register a domain or subdomain name for the site.

