import logging

import discord

from src.bot.strings import Checkout
from src.exceptions.custom_exceptions import BadRequest, InternalServerError
from src.utils.config import settings

intents = discord.Intents.default()
client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

logger = logging.getLogger(__name__)


@client.event
async def on_ready():
    await tree.sync()
    logger.info(f"Successfully logged in as {client.user}!")


# TODO: tie this file together better and rename class
class BotStuff:
    @staticmethod
    async def give_role(*, role_id: int, user_id: int, server_id: int):
        logger.info(
            f"attempting to give user {user_id} the role {role_id} in server {server_id}"
        )
        guild = client.get_guild(server_id)
        if guild is None:
            raise BadRequest(f"Bot is not connected to server {server_id}")

        role = guild.get_role(role_id)
        if role is None:
            raise BadRequest(f"Role {role_id} was not found in server {server_id}")

        try:
            member = await guild.fetch_member(user_id)
        except discord.NotFound as e:
            raise BadRequest(f"User {user_id} was not found in server {server_id}")

        if role not in member.roles:
            try:
                await member.add_roles(role)
            except Exception as e:
                logger.exception(
                    f"Something went wrong when grating user {user_id} the role {role_id} in server {server_id}\n {e}"
                )
                raise InternalServerError(
                    f"Failed to give user {user_id} the role {role_id} in server {server_id}\n {e}"
                )

        logger.info(f"user {user_id} now has the role {role_id} in server {server_id}")


# NOTE: Workaround: Set high level permission to prevent everyone from seeing the command
# then override on discord client to allow mentors
@discord.app_commands.default_permissions(administrator=True)
@tree.command(name="checkout", description="removes mentor role")
async def remove_mentor(interaction: discord.Interaction):
    logger.info("Attemping to checkout mentor")
    member = interaction.user
    if not isinstance(member, discord.Member):
        await interaction.response.send_message(Checkout.NOT_USER, ephemeral=True)
        return

    role_id = settings.MENTOR_ROLE_ID
    role = interaction.guild.get_role(role_id) if interaction.guild else None

    if role is None:
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        raise BadRequest(
            f"Role {role_id} was not found in server {interaction.guild_id}"
        )

    if role not in member.roles:
        await interaction.response.send_message(Checkout.NOT_MENTOR, ephemeral=True)
        return

    try:
        await member.remove_roles(role)
        await interaction.response.send_message(Checkout.SUCCESS, ephemeral=True)
        logger.info(f"Succesffuly checked out mentor {member.id}")
    except Exception as e:
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        raise InternalServerError(
            f"Failed to remove the role {role_id} from user {member.id} in server {interaction.guild_id}\n {e}"
        )
