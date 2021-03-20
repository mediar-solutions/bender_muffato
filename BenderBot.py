import sys
import json
# Slack bot API
from slack import WebClient
from slack import RTMClient
from slack.errors import SlackApiError


class BenderBot:
    """Our Bender Bot interface with the Slack API. We are currently using the WebClient instead of the RTMClient.

    Attributes:
        audit_channel_id (str): The id of the default channel the bot posts a message to when no channel is specified.
        client (slack.WebClient): The Slack bot API wrapper for Python, by Slack.

    Methods:
        parseChannelId: For internal class use only, figures out if it should post to the default channel or if the user specified one.
        postMessageToChannel: Posts a text message with no attachment to a channel.
        postTextFileToChannel: Posts a text message with a text file attachment to a channel.
        postFileToChannel: Posts a text message with an arbitrary file attachment to a channel.

    """

    def __init__(self):
        """Constructor. Expects a config.json at the root directory containing the string attributes token and audit_channel_id.
        """
        try:
            with open('config.json', mode='r') as file:
                config = json.load(file)

                self.audit_channel_id = config["audit_channel_id"]
                self.client = WebClient(token=config["token"])
        except SlackApiError as e:
            print(e.response["error"])
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def parseChannelId(self, channel_id):
        """For internal class use only, figures out if it should post to the default channel or if the user specified one.

        Args:
            channel_id (str): The target channel_id, if None, this function returns the default audit channel id.
        """
        if channel_id is None:
            return self.audit_channel_id
        return channel_id

    def postMessageToChannel(self, message: str, channel_id=None):
        """Posts a text message with no attachment to a channel.

        Args:
            message (str): The message text.
            channel_id (str): The target channel_id, if None, this function posts to the default audit channel.
        """
        return self.client.chat_postMessage(channel=self.parseChannelId(channel_id),
                                            text=message)

    def postTextFileToChannel(self, message: str, file_text: str, file_name: str, channel_id=None):
        """Posts a text message with a text file attachment to a channel.

        Args:
            message (str): The message text.
            file_text (str): The text file content.
            file_name (str): The name to be given to the text file.
            channel_id (str): The target channel_id, if None, this function posts to the default audit channel.
        """
        return self.client.files_upload(channels=self.parseChannelId(channel_id),
                                        initial_comment=message,
                                        content=file_text,
                                        filename=file_name)

    def postFileToChannel(self, message: str, file_addr: str, channel_id=None):
        """Posts a text message with an arbitrary file attachment to a channel.

        Args:
            message (str): The message text.
            file_addr (str): The address of the file to be attached.
            channel_id (str): The target channel_id, if None, this function posts to the default audit channel.
        """
        return self.client.files_upload(channels=self.parseChannelId(channel_id),
                                        initial_comment=message,
                                        file=file_addr)
