This is a Discord bot made as a personal project.

Regular Commands:
    
    !covid {country}
        Displays the current COVID-19 case data for the specified country using data from Worldometers.
        If no country is specified, it will give global values by default.
    
    !covid-news {source}
        Displays news articles from a Coronavirus live update feed of the specified source. 
        Currently supported sources are BBC, Reuters, and a mixed feed of the two. 
        If no source is specified, it will give the mixed feed by default.

    !gunpla-news
        Displays news articles from the Gundam.Info Gunpla news page.

    !anime-news
        Displays news articles from the MyAnimeList news page.

    !roll-dice {number of dice} {number of sides}
        Generates random numbers to simulate dice rolls using the specified parameters.

    !wikirandom
        Posts a link to a random Wikipedia article.

Admin Commands:

    !create-channel {channel-name}
        Creates a new text channel on the server with the specified channel name. 
        If no channel name is given, the new channel will be named "new-channel."

Bot Listeners:

    on_message:
        Uses a dictionary of messages and replies to automatically respond to certain phrases with a given reply.
        (Only works if the message contains nothing but the key message, case insensitive.)
        {
            'ooga': 'Booga',
            'epic': 'WOW',
            'oof': 'Thanks for contributing nothing to the conversation.',
            'wow': 'EPIC'
        }
        
        Responds to the phrase "Anime was a mistake" with a random anime gif. 
        (Case insensitive, works regardless of a period at the end or spacing in the middle.))