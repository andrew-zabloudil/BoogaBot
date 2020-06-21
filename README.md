This is a Discord bot made as a personal project.

Commands can be invoked either with the ! prefix or by mentioning BoogaBot with @BoogaBot

Regular Commands:

    !covid {country}
        Displays the current COVID-19 case data for the specified country using data from Worldometers.
        If no country is specified, it will give global values by default.

    !covid-news {source}
        Displays news articles from a Coronavirus live update feed of the specified source.
        Currently supported sources are BBC, Reuters, NPR, The Hill and a mixed feed of all sources.
        If no source is specified, it will give the mixed feed by default.

    !gunpla-news
        Displays news articles from the Gundam.Info Gunpla news page.

    !anime-news
        Displays news articles from the MyAnimeList news page.

    !roll-dice {number of dice} {number of sides}
        Generates random numbers to simulate dice rolls using the specified parameters.

    !wikirandom
        Posts a link to a random Wikipedia article.

    !cryle-busch
        Sends a gif of Kyle Busch fake crying.

    !dad-joke "input seed"
        Uses machine learning to generate a dad joke from the input seed.

Admin Commands:

    !create-channel {channel-name}
        Creates a new text channel on the server with the specified channel name.
        If no channel name is given, the new channel will be named "new-channel."

    !kick {user_name} {reason}
        Kicks the specified user from the current server.
        Reason is not a required field.
        Sends a DM to the kicked user telling them they were kicked, including the reason if specified.

    !ban {user_name} {reason} {days}
        Bans the specified user from the current server.
        Reason is required if you wish to specify the number of days.
        Days will delete all messages by the user from up to the last 7 days. Defaults to 1.
        Sends a DM to the banned user telling them they were banned, including the reason if specified.

    !add-role {user_name} {role_name} {reason}
        Adds the specified role to the specified user. Reason is optional.

    !remove-role {user_name} {role_name} {reason}
        Removes the specified role from the specified user. Reason is optional.

Bot Listeners:

    on_message:
        Uses a dictionary of messages and replies to automatically respond to certain phrases with a given reply.
        (Only works if the message contains nothing but the key message, case insensitive.)
        {
            'ooga': 'Booga',
            'epic': 'WOW',
            'oof': 'Thanks for contributing nothing to the conversation.',
            'wow': 'EPIC',
            'animewasamistake': send a random anime gif,
            '🐡': 'https://tenor.com/view/pufferfish-carrot-meme-stfu-funny-gif-15837792',
            '🐇': 'https://tenor.com/view/bunny-rabbit-eating-food-munchies-gif-17294792',
            '🐰': 'https://tenor.com/view/bunny-rabbit-eating-food-munchies-gif-17294792',
            '🧀': 'https://cdn.discordapp.com/emojis/716293527054843914.gif',
            '🧅': 'https://tenor.com/view/shrek-surprise-bathroom-ogre-gif-11492547',
            'f': f'{message.author.display_name} has paid respects.'
        }

        Responds to the phrase "Anime was a mistake" with a random anime gif.
        (Case insensitive, works regardless of a period at the end or spacing in the middle.))