This is a Discord Bot made for a small personal server. All of the bot commands are detailed below.

Commands can be invoked either with the "!" prefix or by mentioning BoogaBot with @BoogaBot

Regular Commands:

    !covid "country"
        Displays the current COVID-19 case data for the specified country using data from Worldometers.
        If no country is specified, it will give global values by default.

    !covid-news "source"
        Displays the latest news articles about the coronavirus from whichever source is specified.
        Currently supported sources are BBC, Reuters, NPR, The Hill and a mixed feed of all sources.
        If no source is specified, it will give the mixed feed by default.

    !gunpla-news
        Displays the latest news articles from the Gundam.Info Gunpla news page.
        Gunpla are plastic models based on the anime series Gundam. (GUNdam PLAstic model => GUNPLA)

    !anime-news
        Displays the latest news articles from the MyAnimeList news page.

    !roll-dice "number of dice" "number of sides"
        Generates random numbers to simulate dice rolls using the specified parameters.

    !wikirandom
        BoogaBot responds to this command with a link to a random Wikipedia article.

    !cryle-busch
        Sends a gif of NASCAR driver Kyle Busch pretending to cry in a mocking manner.

    !dad-joke "input seed"
        Uses machine learning to generate a dad joke from the input seed.
    NOTE: This command is currently only available in the dad_bot_complete branch due to hosting limitations.

Admin Commands:

    !create-channel "channel-name"
        Creates a new text channel on the current server with the specified channel name.
        If no channel name is given, the new channel will be named "new-channel."

    !kick "user name" "reason"
        Kicks the specified user from the current server.
        Providing a reason is not required, and the command will function without it.
        BoogaBot sends a DM to the kicked user telling them they were kicked, including the reason if specified.

    !ban "user_name" "reason" "days"
        Bans the specified user from the current server.
        Providing a reason and number of days is not required, and the command will function without it.
        However, a reason is required if you wish to specify the number of days.
        If a number of days is provided, BoogaBot will delete all previous messages by the user from up to the last 7 days. "days" defaults to 1.
        BoogaBot sends a DM to the banned user telling them they were banned, including the reason if specified.

    !add-role "user_name" "role_name" "reason"
        Adds the specified role to the specified user. Providing a reason is optional.

    !remove-role "user_name" "role_name" "reason"
        Removes the specified role from the specified user. Providing a reason is optional.

Bot Listeners:

    on_message:
        Uses a dictionary containing certain messages and replies that BoogaBot will use to automatically respond to the messages with.
        (Only works if the message contains nothing but the key message and the characters [ .?!¡¿], case insensitive.)
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
