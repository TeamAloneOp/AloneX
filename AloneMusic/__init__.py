from AloneMusic.core.bot import Alone
from AloneMusic.core.dir import dirr
from AloneMusic.core.git import git
from AloneMusic.core.userbot import Userbot
from AloneMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Alone()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
