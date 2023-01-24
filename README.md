# Audio Loader has moved!!
Please use https://deckthemes.com/ for Audio Loader submissions.

<h1 align="center">
  <img src="./docs/images/logo.png#gh-light-mode-only" alt="Audio Loader logo" width="200"><img src="./docs/images/logo_white.png#gh-dark-mode-only" alt="Audio Loader logo" width="200">
  <br>
  Audio Loader - Pack Database
</h1>
<p align="center">
  <a href="https://github.com/EMERALD0874/AudioLoader-PackDB/stargazers"><img src="https://img.shields.io/github/stars/EMERALD0874/AudioLoader-PackDB" /></a>
  <a href="https://github.com/EMERALD0874/AudioLoader-PackDB/commits/main"><img src="https://img.shields.io/github/last-commit/EMERALD0874/AudioLoader-PackDB.svg" /></a>
  <a href="https://github.com/EMERALD0874/AudioLoader-PackDB/blob/main/LICENSE"><img src="https://img.shields.io/github/license/EMERALD0874/AudioLoader-PackDB" /></a>
  <a href="https://discord.gg/ZU74G2NJzk"><img src="https://img.shields.io/discord/960281551428522045?color=%235865F2&label=discord" /></a>
  <br>
  <br>
  <img src="https://media.discordapp.net/attachments/814629062806601778/1029928716152864809/unknown.png" alt="Audio Loader Pack Browser screenshot" width="80%">
</p>

## 📦 Creating a Pack

Development for the Audio Loader is intended to be as simple as possible. That being said, we understand not everyone understands how to edit audio and JSON files. If you have any suggestions for how we can make this guide easier to understand, please feel free to create an issue.

### 📋 Prerequisites

- Audio Loader installed on a Steam Deck (or a compatible device running the Steam Deck UI)
- Basic audio editing and JSON knowledge
- Audio files to use in a pack
- (Optional) SSH enabled on your Steam Deck
- (Optional) An FTP or SSH client on another computer

### ⌨️ Setting Up SSH (optional)

This is an optional step that will allow you to easily manage your pack's files remotely. Please follow one of the guides below to learn how to use SSH with your Steam Deck.

- [Enabling SSH Server on a Steam Deck](https://shendrick.net/Gaming/2022/05/30/sshonsteamdeck.html), Seth Hendrick

### 📁 Creating a Pack Template

To start, create a GitHub repository with a folder inside named after your pack. You can do this by clicking the + at the top-right of GitHub and selecting "New repository". Next, create a file titled `pack.json` inside of the folder with the following contents.

```json
{
  "name": "Pack Name",
  "description": "Use this field to describe the pack.",
  "author": "GitHubUsername",
  "version": "v1.0",
  "manifest_version": 2,
  "music": false,
  "ignore": [],
  "mappings": {}
}
```

### ✍️ Editing pack.json

Please follow these guidelines when changing variables inside your manifest.

- `name` - This is a permanent name that should describe your pack or allude to how it sounds like. For example, calling a science-fiction pack and calling it "Medieval" will likely get denied.
- `description` - This should describe your pack at a basic level. Try to include where you obtained your audio from or the feeling it conveys.
- `author` - This can be any name. We recommend using your GitHub username so users can easily report an issue if needed.
- `version` - This should follow the format of `v{MAJOR}.{MINOR}`. Major updates are usually new inclusions to the pack that help complete it. Minor updates are usually updates to poor or unintentionally missing audio or adding support for a new version of SteamOS.
- `manifest_version` - This should always reflect the latest manifest version available in this guide. Newer manifest versions provide additional features only available on newer installations. Make sure to check this README for a guide on updating versions.
- `music` - This determines whether your pack displays as music or Steam UI sound replacements.
- `ignore` - This controls which Steam UI sound files will not be customized if creating a sound pack. This is necessary if not replacing all sounds.
- `mappings` - This determines what sound files correspond to each Steam UI sound. This is not needed if you name your sound files the same as the Steam UI sounds. This feature requires manifest version 2 or higher.

### 🎵 Adding Audio Files

This is where the guide will split in two. If you are looking to add background music to the Steam UI, please read the **Music packs** section. If you are looking to replace existing Steam UI sounds, please read the **Sound packs** section.

#### 🎶 Music Packs

Music packs are background tracks for the Steam UI. Whenever a user does not have an application running, the active music pack will play indefinitely until an application is launched.

When creating a music pack, the first thing you should always have in mind is that this is a background track, not a general music player. Consider using ambiance and instrumental music rather than heavy-hitting music or anything with lyrics. Exceptions can be made but they shouldn't be expected.

Once you have found a music track that you want to use for your pack, make the following changes to your `pack.json`.

- Change `name` to the exact music track name. Don't use descriptions like "Beethoven Music" unless necessary.
- Use `description` to credit the source. You can also list where it appears in media if applicable (ex. Appears in the menu of...).
- Make sure `music` is set to true.

Next, find an audio file for the music you would like to use. Using an audio editing program (ex. Audacity), do the following.

- Make the music loop as seamlessly as possible. If you can't do this, please merge any pull requests doing so in your repo.
- Decrease the volume of the music by 10dB. In Audacity, select Effect and Amplify. Enter -10 as the New Peak Amplitude.
  - Keep in mind that your music pack will be denied if sound packs cannot be heard over it.
- Save your music as `menu_music.mp3` in your pack directory. In Audacity, select File, Export, and Export as MP3.

When uploading your music pack, please try to use the cover art for the album you retrieved the music from (more info about this is below). For a video game, this should be the cover of the original soundtrack and not the box art for the game itself.

#### 🔊 Sound Packs

To start, you will need to find the folder containing the Steam UI sounds. This can be found at `/home/deck/.local/share/Steam/steamui/sounds` on your Steam Deck. [If you have run the Steam Deck UI on another device](https://www.youtube.com/watch?v=1IAbZte8e7E), you can find the sounds at `{STEAM_INSTALLATION}/steamui/sounds`. **DO NOT MODIFY THESE FILES UNDER ANY CIRCUMSTANCE.** Modifying your Steam files is destructive and could lead to problems in the future. Using Audio Loader to manage your sound replacements is the safest way to avoid any potential issues.

Create a list of these file names as you will need to create a replacement or add an entry to your ignore array for all of them. For your convenience, an array of all file names is available below if you prefer to work from the bottom up.

```json
"ignore": [
  "bumper_end.wav",
  "confirmation_negative.wav",
  "confirmation_positive.wav",
  "deck_ui_achievement_toast.wav",
  "deck_ui_bumper_end_02.wav",
  "deck_ui_default_activation.wav",
  "deck_ui_hide_modal.wav",
  "deck_ui_into_game_detail.wav",
  "deck_ui_launch_game.wav",
  "deck_ui_message_toast.wav",
  "deck_ui_misc_01.wav",
  "deck_ui_misc_08.wav",
  "deck_ui_misc_10.wav",
  "deck_ui_navigation.wav",
  "deck_ui_out_of_game_detail.wav",
  "deck_ui_show_modal.wav",
  "deck_ui_side_menu_fly_in.wav",
  "deck_ui_side_menu_fly_out.wav",
  "deck_ui_slider_down.wav",
  "deck_ui_slider_up.wav",
  "deck_ui_switch_toggle_off.wav",
  "deck_ui_switch_toggle_on.wav",
  "deck_ui_tab_transition_01.wav",
  "deck_ui_tile_scroll.wav",
  "deck_ui_toast.wav",
  "deck_ui_typing.wav",
  "deck_ui_volume.wav",
  "pop_sound.wav",
  "steam_at_mention.m4a",
  "steam_chatroom_notification.m4a",
  "ui_steam_message_old_smooth.m4a",
  "ui_steam_smoother_friend_join.m4a",
  "ui_steam_smoother_friend_online.m4a"
]
```

To replace a sound file, remove its entry from the above array and place a sound file with the exact file name (including file type) inside of your pack folder. If you wish to use sound files that have different names or file extensions than the Steam UI sounds, see [🎲 Mappings and Randomization](#-mappings-and-randomization).

Below is a list of what each sound file is believed to mean.

- `bumper_end.wav` - Unknown or unused.
- `confirmation_negative.wav` - Unknown or unused.
- `confirmation_positive.wav` - Unknown or unused.
- `deck_ui_achievement_toast.wav` - Played when a user unlocks an achievement in a Steam game.
- `deck_ui_bumper_end_02.wav` - Played when attempting to navigate and being unable to move further.
- `deck_ui_default_activation.wav` - Played when selecting most interactable objects.
- `deck_ui_hide_modal.wav` - Played when exiting most pop-ups.
- `deck_ui_into_game_detail.wav` - Played when opening a game's details page.
- `deck_ui_launch_game.wav` - Played when launching a game.
- `deck_ui_message_toast.wav` - Unknown or unused.
- `deck_ui_misc_01.wav` - Unknown or unused.
- `deck_ui_misc_08.wav` - Unknown or unused.
- `deck_ui_misc_10.wav` - Played when navigating through most areas.
- `deck_ui_navigation.wav` - Played when navigating through specific areas (ex. Settings).
- `deck_ui_out_of_game_detail.wav` - Played when exiting a game's details page.
- `deck_ui_show_modal.wav` - Played when a pop-up appears.
- `deck_ui_side_menu_fly_in.wav` - Played when opening the Steam or Quick Access menus.
- `deck_ui_side_menu_fly_out.wav` - Played when exiting the Steam or Quick Access menus.
- `deck_ui_slider_down.wav` - Played when decreasing a slider.
- `deck_ui_slider_up.wav` - Played when increasing a slider.
- `deck_ui_switch_toggle_off.wav` - Played when toggling off a toggle.
- `deck_ui_switch_toggle_on.wav` - Played when toggling on a toggle.
- `deck_ui_tab_transition_01.wav` - Played when switching between tabs (ex. Library views).
- `deck_ui_tile_scroll.wav` - Unknown or unused.
- `deck_ui_toast.wav` - Played when a toast appears at the bottom-right corner of the UI.
- `deck_ui_typing.wav` - Played when typing on the keyboard.
- `deck_ui_volume.wav` - Played when confirming the volume setting in Settings.
- `pop_sound.wav` - Unknown or unused.
- `steam_at_mention.m4a` - Played when mentioned in a group chat.
- `steam_chatroom_notification.m4a` - Played when receiving a group chat message.
- `ui_steam_message_old_smooth.m4a` - Played when receiving a private chat message.
- `ui_steam_smoother_friend_join.m4a` - Played when a friend runs a game or software.
- `ui_steam_smoother_friend_online.m4a` - Played when a friend goes online on Steam.

### 🎲 Mappings and Randomization

Mapping is a feature that allows you to map a Steam UI sound to one or more sound files. This allows for custom file names, subfolders, multiple sounds sharing a file, and multiple files per sound that are picked at random. If you wish to use mapping, your sound pack must use manifest version 2 or higher.

```json
"mappings": {
    "deck_ui_toast.wav": ["folder1/my cool sound.mp3"],
    "deck_ui_achievement_toast.wav": ["achievement1.mp3", "achievement2.wav", "achievement3.mp3"]
}
```

For each entry in mappings, the object key is the file name (including the file extension) of the Steam UI sound that you wish to map and the value is an array of strings for the names of your sound files. If you wish to map a sound to more than one file, include them as entries in your array, and Audio Loader will randomly pick one each time the sound is played.

### 🧪 Testing

Once you have completed creating your pack, upload the folder containing it to the `/home/deck/homebrew/sounds` folder. If the sounds folder does not exist, you may not have the Audio Loader plugin properly installed. Depending on the type of pack you created, you should be able to find it in the music or sounds dropdowns. Select your pack and test it by either testing the functionality of each sound or using the [Decky Playground Plugin](https://github.com/SteamDeckHomebrew/decky-playground).

## 📨 Uploading a Pack

Uploading your pack requires some basic Git knowledge. If you have trouble understanding the instructions below, feel free to reach out to us or another developer familiar with Git for support.

### ☑️ Requirements

These requirements must be followed for all packs.

- You are the original author of the pack or have permission from the original author to make a pull request
- All copyright of the pack's contents belong to the listed author or are cited in the description and repository linked in the pull request
- The pack works properly on the latest versions of SteamOS for Steam Deck, [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader), and [Audio Loader](https://github.com/EMERALD0874/SDH-AudioLoader)
- The pack is under 10MB in size and uses the least disk space possible
- The pack is safe for work and does not contain any sexual, drug-related, or profane content
- The pack does not contain loud, distorted, or otherwise bad-faith sound files
- The pack is only for either music or sounds and only adds or modifies the intended sound files

#### 🎼 Music Requirements

All music packs with copyrighted content that do not meet one of the following criteria will most likely be denied. If you are unsure whether your music pack meets one of these criteria, [please reach out to us](#-support).

- Original compositions and performances
- Copyright-free and public-domain performances
- Music with explicit permission from the original author
- Music from other console firmware menus\*
- Other exceptions made by the development team

\*_Console firmware music must still be approved by repository maintainers. Music that is unlikely to be used by anyone but the author and music from first-party applications (ex. Wii Shop, Nintendo eShop) may be denied._

### 📝 Creating a Pull Request

1. Create a fork of this repository. You can do this using the Fork button at the top-right corner.
1. (Optional) Create and upload a square JPG preview image in `/images/{AUTHOR}`.
1. Create and upload a JSON file in `/packs` titled `{AUTHOR}-{PACK_NAME}.json` that follows this template.
   ```json
   {
     "repo_url": "https://github.com/AuthorGoesHere/RepoNameGoesHere",
     "repo_subpath": "FolderWherePackIsGoesHere",
     "repo_commit": "a1b2c3",
     "preview_image_path": "images/{AUTHOR}/{IMAGE_NAME}.jpg"
   }
   ```
1. (Optional) Test your pack submission by running `py main.py` in the repository folder.
   - Python and the Git CLI need to be installed.
   - If you are missing Python libraries, run `pip install -r requirements.txt`.
   - If the script throws no exceptions, you are ready to commit.
1. Commit your changes and repeat for as many packs as you plan to upload.
1. Create a pull request from your fork to the main repository.

## 🙏 Support

If you need any help creating or submitting a pack, please use [the Steam Deck Homebrew Discord server](https://discord.gg/ZU74G2NJzk). Please use the Audio Loader support thread in the #support-plugins channel.
