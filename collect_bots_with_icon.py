import os
from telethon import TelegramClient
from telethon.tl.types import User

# Your API credentials
api_id = '24570614'  # Replace with your API ID
api_hash = '8097f662af777645b092df8b2657e057'  # Replace with your API Hash

# Initialize the client
client = TelegramClient('elaxairdrop', api_id, api_hash)

# Create a directory for bot icons
if not os.path.exists("bot_icons"):
    os.makedirs("bot_icons")

async def collect_and_write_to_html_with_icons():
    # Start the client session
    await client.start()

    bots = []
    # Iterate through all dialogs (chats, groups, channels, and bots)
    async for dialog in client.iter_dialogs():
        # Check if the dialog is a bot by checking the 'bot' attribute
        if isinstance(dialog.entity, User) and dialog.entity.bot:
            # Save bot profile picture, if available
            photo_path = f"bot_icons/{dialog.entity.username or dialog.id}.jpg"
            if dialog.entity.photo:
                await client.download_profile_photo(dialog.entity, file=photo_path)
            else:
                # Use a default placeholder if no profile picture exists
                photo_path = "https://via.placeholder.com/200?text=No+Photo"

            bot_info = {
                'name': dialog.name,  # Bot's display name
                'username': dialog.entity.username,  # Bot's username
                'id': dialog.id,  # Bot's unique ID
                'photo': photo_path,  # Path to bot's profile picture
            }
            bots.append(bot_info)  # Collect bot information

    # Generate the HTML content
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telegram Bots List</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { text-align: center; color: #4CAF50; }
            .bot-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
            .bot-card { border: 1px solid #ddd; border-radius: 10px; padding: 20px; width: 200px; text-align: center; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); }
            .bot-card img { border-radius: 50%; width: 100px; height: 100px; margin-bottom: 10px; }
            .bot-card h2 { color: #333; font-size: 18px; margin: 10px 0; }
            .bot-card p { color: #777; font-size: 14px; }
            .bot-card a { color: #007BFF; text-decoration: none; }
            .bot-card a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Your Tracked Telegram Bots</h1>
        <div class="bot-container">
    '''

    for bot in bots:
        # Use the photo path, or a placeholder if the photo doesn't exist
        html_content += f'''
        <div class="bot-card">
            <img src="{bot['photo']}" alt="Bot Photo">
            <h2>{bot['name']}</h2>
            <p>Username: <a href="https://t.me/{bot['username']}">@{bot['username']}</a></p>
            <p>ID: {bot['id']}</p>
        </div>
        '''

    # Closing tags for the HTML document
    html_content += '''
        </div>
    </body>
    </html>
    '''

    # Write the HTML content to a file
    with open("bot_list_mini_app.html", "w") as f:
        f.write(html_content)

    print("HTML file with icons generated successfully!")

# Run the Telethon client to fetch bots and write to HTML
client.loop.run_until_complete(collect_and_write_to_html_with_icons())
