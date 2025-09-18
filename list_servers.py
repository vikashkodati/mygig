import discord
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ServerListBot:
    def __init__(self, token):
        """
        Think of this as creating a digital assistant that can visit 
        all the Discord communities you've invited it to
        """
        # Set up intents (what the bot is allowed to see/do)
        intents = discord.Intents.default()
        intents.guilds = True  # Can see server info
        intents.members = True  # Can see member counts (if privileged intent enabled)
        
        self.client = discord.Client(intents=intents)
        self.token = token
        self.servers = []
        
        # Set up event handlers
        self.setup_events()
    
    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'🤖 Bot logged in as {self.client.user}')
            print(f'📡 Connected to {len(self.client.guilds)} servers\n')
            
            # Collect server information
            for guild in self.client.guilds:
                server_info = {
                    'name': guild.name,
                    'id': guild.id,
                    'member_count': guild.member_count,
                    'owner_id': guild.owner_id,
                    'created_at': guild.created_at.strftime('%Y-%m-%d'),
                    'region': str(guild.region) if hasattr(guild, 'region') else 'Unknown',
                    'boost_level': guild.premium_tier
                }
                self.servers.append(server_info)
                
                # Pretty print each server
                print(f"🏠 {guild.name}")
                print(f"   └─ Members: {guild.member_count:,}")
                print(f"   └─ Created: {server_info['created_at']}")
                print(f"   └─ Boost Level: {guild.premium_tier}")
                print()
            
            # Close connection after getting data
            await self.client.close()
    
    async def get_servers(self):
        """Main method to fetch server list"""
        try:
            await self.client.start(self.token)
        except discord.LoginFailure:
            print("❌ Invalid bot token!")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return self.servers

# Main execution
async def main():
    # Your bot token from Discord Developer Portal
    # At the top of your script
    load_dotenv()
    BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    # BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual token
    
    # Or load from environment variable (recommended)
    # BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("❌ No bot token provided!")
        return
    
    # Create and run the bot
    bot = ServerListBot(BOT_TOKEN)
    servers = await bot.get_servers()
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"Total servers: {len(servers)}")
    
    if servers:
        total_members = sum(s['member_count'] for s in servers if s['member_count'])
        print(f"Total members across all servers: {total_members:,}")
        
        # Save to file
        import json
        with open('discord_servers.json', 'w') as f:
            json.dump(servers, f, indent=2, default=str)
        print("✅ Server data saved to discord_servers.json")

if __name__ == "__main__":
    asyncio.run(main())